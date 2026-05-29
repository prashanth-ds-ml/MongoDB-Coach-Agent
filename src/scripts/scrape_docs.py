"""
Scrapes MongoDB documentation pages and saves them as markdown files in data/.
"""

import re
import time
import html2text
import requests
from bs4 import BeautifulSoup
from pathlib import Path

BASE_URL = "https://www.mongodb.com"

URLS = [
    # --- Already scraped (batch 1) ---
    "/docs/manual/introduction/",
    "/docs/manual/core/document",
    "/docs/manual/reference/bson-types/",
    "/docs/manual/core/databases-and-collections/",
    "/docs/manual/core/data-modeling-introduction/",

    # --- CRUD ---
    "/docs/manual/crud/",
    "/docs/manual/tutorial/insert-documents/",
    "/docs/manual/tutorial/query-documents/",
    "/docs/manual/tutorial/update-documents/",
    "/docs/manual/tutorial/remove-documents/",

    # --- Query operators ---
    "/docs/manual/reference/operator/query/",
    "/docs/manual/reference/operator/query-comparison/",
    "/docs/manual/reference/operator/query-logical/",
    "/docs/manual/reference/operator/query-array/",
    "/docs/manual/reference/operator/query-element/",

    # --- Query tutorials ---
    "/docs/manual/tutorial/query-arrays/",
    "/docs/manual/tutorial/query-array-of-documents/",
    "/docs/manual/tutorial/query-embedded-documents/",
    "/docs/manual/tutorial/project-fields-from-query-results/",

    # --- Cursor methods ---
    "/docs/manual/reference/method/cursor.sort/",
    "/docs/manual/reference/method/cursor.limit/",
    "/docs/manual/reference/method/cursor.skip/",

    # --- Indexes ---
    "/docs/manual/indexes/",
    "/docs/manual/core/index-single/",
    "/docs/manual/core/index-compound/",
    "/docs/manual/core/index-multikey/",
    "/docs/manual/core/index-unique/",

    # --- Aggregation ---
    "/docs/manual/aggregation/",
    "/docs/manual/core/aggregation-pipeline/",
    "/docs/manual/reference/operator/aggregation/",

    # --- PyMongo driver ---
    "/docs/languages/python/pymongo-driver/current/",
    "/docs/languages/python/pymongo-driver/current/connect/",
    "/docs/languages/python/pymongo-driver/current/crud/",
    "/docs/languages/python/pymongo-driver/current/aggregation/",
    "/docs/languages/python/pymongo-driver/current/indexes/",
]

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data"
OUTPUT_DIR.mkdir(exist_ok=True)


def url_to_filename(path: str) -> str:
    """Convert a URL path to a snake_case .md filename."""
    slug = path.strip("/").replace("/", "_")
    slug = re.sub(r"[^a-z0-9_-]", "", slug.lower())
    return f"{slug}.md"


def extract_main_content(soup: BeautifulSoup) -> str:
    """Return the primary content element, stripping nav/footer noise."""
    # MongoDB docs use <main> or a div with role="main"
    for selector in ["main", "[role='main']", "article", ".main-column", "#main-content"]:
        content = soup.select_one(selector)
        if content:
            return content

    # Fallback: strip obvious chrome and return body
    for tag in soup.find_all(["nav", "footer", "header", "aside", "script", "style"]):
        tag.decompose()
    return soup.body or soup


def to_markdown(html_element) -> str:
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = True
    converter.body_width = 0          # no hard line wraps
    converter.protect_links = True
    converter.unicode_snob = True
    return converter.handle(str(html_element))


def scrape(path: str) -> None:
    url = BASE_URL + path
    print(f"Fetching {url} ...")

    headers = {"User-Agent": "Mozilla/5.0 (educational scraper)"}
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Page title for the markdown header
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else path.strip("/").split("/")[-1]

    content_el = extract_main_content(soup)
    md = to_markdown(content_el)

    # Prepend a clean top-level heading + source link
    header = f"# {title}\n\n> Source: {url}\n\n"
    output = header + md

    filename = url_to_filename(path)
    out_path = OUTPUT_DIR / filename
    if out_path.exists():
        print(f"  Skipping (already exists) -> {out_path.relative_to(OUTPUT_DIR.parent)}")
        return
    out_path.write_text(output, encoding="utf-8", errors="replace")
    print(f"  Saved -> {out_path.relative_to(OUTPUT_DIR.parent)}")


def main():
    for path in URLS:
        try:
            scrape(path)
        except Exception as exc:
            print(f"  ERROR scraping {path}: {exc}")
        time.sleep(1)   # be polite


if __name__ == "__main__":
    main()
