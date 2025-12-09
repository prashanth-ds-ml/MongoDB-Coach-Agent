"""Scraper Agent v1.2 – structured MongoDB docs scraper with seed support.

Capabilities:
- scrape_single_url(url): fetch & parse one MongoDB docs page
- scrape_all_seed_urls(): read seed config and scrape all seed URLs
- save_scrape_to_file(scraped): write JSON into data/raw/

Designed primarily for pages like:
https://www.mongodb.com/docs/manual/reference/method/db.collection.insertOne/
but works reasonably for other MongoDB docs pages too.
"""

import datetime as dt
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup  # type: ignore

from src.core.file_utils import write_json, read_json
from src.core.logging_utils import log
from src.config.settings import RAW_DATA_DIR

# Project root (mongo-coach/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SEED_CONFIG = PROJECT_ROOT / "config" / "sources_seed_associate_python.json"


class ScraperAgent:
    def __init__(self, user_agent: str = "MongoCoachScraper/0.1") -> None:
        self.user_agent = user_agent

    # -------------------- Public API -------------------- #

    def scrape_single_url(self, url: str) -> Dict[str, Any]:
        """Fetch + parse a single MongoDB docs page into a structured dict."""
        log(f"Scraping URL: {url}")
        html = self._fetch_html(url)
        soup = BeautifulSoup(html, "html.parser")

        main = self._find_main_container(soup)
        title = self._extract_title(main, soup)
        breadcrumbs = self._extract_breadcrumbs(soup)
        doc_type, method_name = self._infer_doc_type_and_method(url)
        version = self._infer_version_from_breadcrumbs(breadcrumbs)

        sections = self._extract_sections(main)

        scraped: Dict[str, Any] = {
            "url": url,
            "doc_type": doc_type,
            "method_name": method_name,
            "title": title,
            "version": version,
            "breadcrumbs": breadcrumbs,
            "sections": sections,
            "fetched_at": dt.datetime.utcnow().isoformat(),
        }
        return scraped

    def scrape_all_seed_urls(
        self,
        seed_config_path: Path = DEFAULT_SEED_CONFIG,
    ) -> List[Path]:
        """Scrape all seed URLs defined in the seed config.

        - Reads config/sources_seed_associate_python.json
        - Iterates domains[*].seed_urls[*]
        - Scrapes each URL
        - Enriches scraped docs with:
            exam_code, domain_id, domain_name, seed_id, source_type
        - Saves each as a JSON file in data/raw/

        Returns a list of file paths for the saved JSON files.
        """
        log(f"Loading seed config from: {seed_config_path}")
        config = read_json(seed_config_path)

        exam_code: str = config.get("exam_code", "unknown_exam")
        domains: List[Dict[str, Any]] = config.get("domains", [])

        saved_paths: List[Path] = []

        for domain in domains:
            domain_id = domain.get("id")
            domain_name = domain.get("name", f"domain-{domain_id}")
            seed_urls: List[Dict[str, Any]] = domain.get("seed_urls", [])

            log(
                f"Processing domain {domain_id} – {domain_name} "
                f"with {len(seed_urls)} seed URLs"
            )

            for seed in seed_urls:
                seed_id = seed.get("id")
                url = seed.get("url")
                source_type = seed.get("source_type", "manual")

                if not url:
                    log(f"Skipping seed with no URL (domain {domain_id}, seed {seed_id})")
                    continue

                try:
                    scraped = self.scrape_single_url(url)
                except Exception as e:
                    log(
                        f"ERROR scraping URL for seed '{seed_id}' in domain {domain_id}: "
                        f"{e}"
                    )
                    continue

                # Attach metadata from seed config
                scraped["exam_code"] = exam_code
                scraped["domain_id"] = domain_id
                scraped["domain_name"] = domain_name
                scraped["seed_id"] = seed_id
                scraped["source_type"] = source_type

                # Provide a file_stub so save_scrape_to_file makes unique filenames
                # Example: d2_insert-one, d6_pymongo-crud, etc.
                if seed_id:
                    scraped["file_stub"] = f"d{domain_id}_{seed_id}"

                path = self.save_scrape_to_file(scraped)
                saved_paths.append(path)

        log(f"Finished scraping all seeds. Total saved: {len(saved_paths)}")
        return saved_paths

    def save_scrape_to_file(self, scraped: Dict[str, Any]) -> Path:
        """Save the scraped document into data/raw/ and return the path.

        Filename priority:
        - If scraped['file_stub'] exists, use that.
        - Else if scraped['method_name'] exists, use that.
        - Else fall back to URL slug.
        """
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

        stub = scraped.get("file_stub")
        if not stub:
            method_name = scraped.get("method_name")
            if method_name:
                stub = method_name
            else:
                # Fallback: last part of the URL path
                url = scraped.get("url", "").split("?", 1)[0].rstrip("/")
                slug = url.split("/")[-1] if url else "article"
                stub = slug

        safe_name = (
            str(stub)
            .replace("/", "_")
            .replace(".", "_")
            .replace(" ", "_")
        )
        filename = f"docs_{safe_name}.json"

        path = RAW_DATA_DIR / filename
        write_json(path, scraped)
        log(f"Saved scraped doc to: {path}")
        return path

    # -------------------- Internal helpers -------------------- #

    def _fetch_html(self, url: str) -> str:
        headers = {"User-Agent": self.user_agent}
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.text

    def _find_main_container(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Locate the main article container or fall back to <body>."""
        main = (
            soup.find("main")
            or soup.find("article")
            or soup.find("div", attrs={"role": "main"})
            or soup.body
            or soup
        )
        return main

    def _extract_title(self, main: BeautifulSoup, soup: BeautifulSoup) -> str:
        h1 = main.find("h1") or soup.find("h1")
        if h1:
            return h1.get_text(strip=True)
        title_tag = soup.find("title")
        return title_tag.get_text(strip=True) if title_tag else "Untitled"

    def _extract_breadcrumbs(self, soup: BeautifulSoup) -> List[str]:
        """Extract breadcrumbs as a list of text items, if present."""
        nav = None
        for candidate in soup.find_all("nav"):
            label = candidate.get("aria-label", "") or candidate.get("aria-labelledby", "")
            classes = " ".join(candidate.get("class", []))
            if "breadcrumb" in label.lower() or "breadcrumb" in classes.lower():
                nav = candidate
                break

        if not nav:
            for ol in soup.find_all(["ol", "ul"]):
                classes = " ".join(ol.get("class", []))
                if "breadcrumb" in classes.lower():
                    nav = ol
                    break

        if not nav:
            return []

        items: List[str] = []
        for li in nav.find_all(["li", "span", "a"]):
            text = li.get_text(" ", strip=True)
            if text:
                items.append(text)
        seen = set()
        result: List[str] = []
        for t in items:
            if t not in seen:
                seen.add(t)
                result.append(t)
        return result

    def _infer_doc_type_and_method(self, url: str) -> Tuple[str, Optional[str]]:
        """Infer doc_type and method_name from the URL."""
        clean_url = url.split("?", 1)[0].rstrip("/")
        parts = clean_url.split("/")

        if "/reference/method/" in clean_url:
            method_name = parts[-1]
            return "mongodb_docs_method", method_name
        elif "/languages/python/" in clean_url:
            return "mongodb_docs_driver_python", None
        elif "/atlas/" in clean_url:
            return "mongodb_docs_atlas", None
        else:
            return "mongodb_docs_article", None

    def _infer_version_from_breadcrumbs(self, breadcrumbs: List[str]) -> Optional[str]:
        """Try to pull a version-like breadcrumb string."""
        for b in breadcrumbs:
            if "manual" in b.lower() and any(ch.isdigit() for ch in b):
                return b
        return None

    # ---------- Cleaning helpers (text & code) ---------- #

    def _clean_content_text(self, raw: str) -> str:
        """Remove nav noise, duplicate lines, and extra whitespace."""
        if not raw:
            return ""

        blacklist_exact = {
            "Back",
            "Next",
            "On this page",
            "Definition",
            "Compatibility",
            "Syntax",
            "Behaviors",
            "Examples",
        }

        blacklist_contains = [
            "On this page",
        ]

        lines = [ln.strip() for ln in raw.splitlines()]
        cleaned_lines: List[str] = []
        for ln in lines:
            if not ln:
                continue
            if ln in blacklist_exact:
                continue
            if any(token in ln for token in blacklist_contains):
                continue
            if cleaned_lines and cleaned_lines[-1] == ln:
                continue
            cleaned_lines.append(ln)

        return "\n".join(cleaned_lines)

    def _clean_code_block(self, raw: str) -> str:
        """Collapse wild whitespace inside code blocks to single spaces."""
        if not raw:
            return ""
        return " ".join(raw.split())

    # ---------- Section extraction ---------- #

    def _extract_sections(self, main: BeautifulSoup) -> List[Dict[str, Any]]:
        """Build a list of sections + subsections from h2/h3 headings."""
        sections: List[Dict[str, Any]] = []

        h1 = main.find("h1")
        start_node = h1 if h1 is not None else main

        current_section: Optional[Dict[str, Any]] = None
        current_subsection: Optional[Dict[str, Any]] = None

        def add_text(target: Dict[str, Any], text: str) -> None:
            text = text.strip()
            if not text:
                return
            if target["content"]:
                target["content"] += "\n" + text
            else:
                target["content"] = text

        for el in start_node.find_all_next():
            name = getattr(el, "name", None)
            if name is None:
                continue

            if el is main:
                continue
            if name in {"nav", "footer", "header"}:
                continue

            # Headings
            if name == "h2":
                heading = el.get_text(" ", strip=True)
                if not heading:
                    continue
                section_id = heading.lower().replace(" ", "-")
                current_section = {
                    "section_id": section_id,
                    "heading": heading,
                    "heading_level": 2,
                    "content": "",
                    "code_blocks": [],
                    "subsections": [],
                }
                sections.append(current_section)
                current_subsection = None
                continue

            if name == "h3":
                if current_section is None:
                    continue
                heading = el.get_text(" ", strip=True)
                if not heading:
                    continue
                subsection_id = heading.lower().replace(" ", "-")
                current_subsection = {
                    "subsection_id": subsection_id,
                    "heading": heading,
                    "heading_level": 3,
                    "content": "",
                    "code_blocks": [],
                }
                current_section["subsections"].append(current_subsection)
                continue

            target = current_subsection or current_section
            if target is None:
                continue

            # Text nodes
            if name in {"p", "li"}:
                text = el.get_text(" ", strip=True)
                add_text(target, text)

            elif name in {"ul", "ol"}:
                items = [li.get_text(" ", strip=True) for li in el.find_all("li")]
                items = [it for it in items if it]
                if items:
                    bullet_text = "\n".join(f"- {it}" for it in items)
                    add_text(target, bullet_text)

            # Code
            elif name == "pre":
                code_text = el.get_text("\n", strip=True)
                if code_text:
                    target["code_blocks"].append(code_text)

        # Post-clean contents and code blocks
        for sec in sections:
            sec["content"] = self._clean_content_text(sec.get("content", ""))
            sec["code_blocks"] = [
                self._clean_code_block(cb) for cb in sec.get("code_blocks", [])
            ]
            for sub in sec.get("subsections", []):
                sub["content"] = self._clean_content_text(sub.get("content", ""))
                sub["code_blocks"] = [
                    self._clean_code_block(cb) for cb in sub.get("code_blocks", [])
                ]

        return sections


# -------------------- Simple CLI for quick testing -------------------- #

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Scrape MongoDB docs into data/raw JSON."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["single", "seed"],
        default="single",
        help="Scrape a single URL or all seed URLs from config.",
    )
    parser.add_argument(
        "--url",
        type=str,
        required=False,
        default="https://www.mongodb.com/docs/manual/reference/method/db.collection.insertOne/",
        help="MongoDB docs URL to scrape in 'single' mode.",
    )
    parser.add_argument(
        "--seed-config",
        type=str,
        required=False,
        default=str(DEFAULT_SEED_CONFIG),
        help="Path to seed config JSON for 'seed' mode.",
    )
    args = parser.parse_args()

    agent = ScraperAgent()

    if args.mode == "single":
        scraped_doc = agent.scrape_single_url(args.url)
        path = agent.save_scrape_to_file(scraped_doc)
        log(f"Done. Single URL scraped JSON saved at: {path}")
    else:
        paths = agent.scrape_all_seed_urls(Path(args.seed_config))
        log("Done. Seed scrape complete.")
        for p in paths:
            log(f"  -> {p}")
