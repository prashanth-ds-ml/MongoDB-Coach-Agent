"""
Resolve official docs for the MongoDB Associate Python Developer syllabus.

This fills the gap left by direct .md scraping: many high-value manual and
PyMongo pages are listed in llms.txt but return 403 from their .md endpoint.
For this exam-specific source set, we try direct markdown first and then use a
selective HTML-to-Markdown fallback for only curated syllabus pages.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import requests

from src.scripts.utils.mongodb_docs_md_scraper import url_to_markdown_url


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "mongodb_docs" / "syllabus_sources" / "associate_python_developer"
USER_AGENT = "CertCoach Associate Python Developer syllabus resolver/0.1"


ASSOCIATE_PYTHON_DEVELOPER_TARGETS = [
    {
        "topic_id": 1,
        "topic": "MongoDB Overview & The Document Model",
        "urls": [
            "https://www.mongodb.com/docs/manual/introduction/",
            "https://www.mongodb.com/docs/manual/core/document/",
            "https://www.mongodb.com/docs/manual/reference/bson-types/",
            "https://www.mongodb.com/docs/manual/core/databases-and-collections/",
            "https://www.mongodb.com/docs/manual/core/data-modeling-introduction/",
        ],
    },
    {
        "topic_id": 2,
        "topic": "CRUD Operations - Create",
        "urls": [
            "https://www.mongodb.com/docs/manual/tutorial/insert-documents/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/insert/",
        ],
    },
    {
        "topic_id": 3,
        "topic": "CRUD Operations - Read",
        "urls": [
            "https://www.mongodb.com/docs/manual/tutorial/query-documents/",
            "https://www.mongodb.com/docs/manual/tutorial/project-fields-from-query-results/",
            "https://www.mongodb.com/docs/manual/reference/method/cursor.sort/",
            "https://www.mongodb.com/docs/manual/reference/method/cursor.limit/",
            "https://www.mongodb.com/docs/manual/reference/method/cursor.skip/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/count/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/project/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/specify-query/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/cursors/",
        ],
    },
    {
        "topic_id": 4,
        "topic": "CRUD Operations - Update",
        "urls": [
            "https://www.mongodb.com/docs/manual/tutorial/update-documents/",
            "https://www.mongodb.com/docs/manual/reference/operator/update/set/",
            "https://www.mongodb.com/docs/manual/reference/operator/update/push/",
            "https://www.mongodb.com/docs/manual/reference/operator/update/inc/",
            "https://www.mongodb.com/docs/manual/reference/operator/update/unset/",
            "https://www.mongodb.com/docs/manual/reference/method/db.collection.findAndModify/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/update/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/replace/",
        ],
    },
    {
        "topic_id": 5,
        "topic": "CRUD Operations - Delete",
        "urls": [
            "https://www.mongodb.com/docs/manual/tutorial/remove-documents/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/delete/",
        ],
    },
    {
        "topic_id": 6,
        "topic": "Query Operators & MQL",
        "urls": [
            "https://www.mongodb.com/docs/manual/reference/operator/query/",
            "https://www.mongodb.com/docs/manual/reference/operator/query-comparison/",
            "https://www.mongodb.com/docs/manual/reference/operator/query-logical/",
            "https://www.mongodb.com/docs/manual/reference/operator/query-element/",
            "https://www.mongodb.com/docs/manual/reference/operator/query/in/",
            "https://www.mongodb.com/docs/manual/reference/operator/query/exists/",
            "https://www.mongodb.com/docs/manual/reference/operator/query/type/",
        ],
    },
    {
        "topic_id": 7,
        "topic": "Querying Arrays & Embedded Documents",
        "urls": [
            "https://www.mongodb.com/docs/manual/tutorial/query-arrays/",
            "https://www.mongodb.com/docs/manual/tutorial/query-array-of-documents/",
            "https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/",
            "https://www.mongodb.com/docs/manual/reference/operator/query/elemMatch/",
            "https://www.mongodb.com/docs/manual/reference/operator/query/size/",
            "https://www.mongodb.com/docs/manual/core/field-paths/",
        ],
    },
    {
        "topic_id": 8,
        "topic": "Aggregation Framework",
        "urls": [
            "https://www.mongodb.com/docs/manual/aggregation/",
            "https://www.mongodb.com/docs/manual/core/aggregation-pipeline/",
            "https://www.mongodb.com/docs/manual/reference/operator/aggregation/",
            "https://www.mongodb.com/docs/manual/reference/operator/aggregation/match/",
            "https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/",
            "https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/",
            "https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/",
            "https://www.mongodb.com/docs/manual/reference/operator/aggregation/out/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/aggregation/",
        ],
    },
    {
        "topic_id": 9,
        "topic": "Indexes & Performance",
        "urls": [
            "https://www.mongodb.com/docs/manual/indexes/",
            "https://www.mongodb.com/docs/manual/core/index-single/",
            "https://www.mongodb.com/docs/manual/core/index-compound/",
            "https://www.mongodb.com/docs/manual/core/index-multikey/",
            "https://www.mongodb.com/docs/manual/core/index-unique/",
            "https://www.mongodb.com/docs/manual/reference/explain-results/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/indexes/",
        ],
    },
    {
        "topic_id": 10,
        "topic": "Data Modeling",
        "urls": [
            "https://www.mongodb.com/docs/manual/data-modeling/",
            "https://www.mongodb.com/docs/manual/core/data-modeling-introduction/",
            "https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/",
            "https://www.mongodb.com/docs/manual/tutorial/model-embedded-one-to-many-relationships-between-documents/",
            "https://www.mongodb.com/docs/manual/tutorial/model-referenced-one-to-many-relationships-between-documents/",
            "https://www.mongodb.com/docs/manual/tutorial/model-data-for-atomic-operations/",
        ],
    },
    {
        "topic_id": 11,
        "topic": "MongoDB Drivers & PyMongo",
        "urls": [
            "https://www.mongodb.com/docs/languages/python/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/mongoclient/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/connection-targets/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/connection-options/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/connection-options/connection-pools/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/atlas-search/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/issues-and-help/",
        ],
    },
    {
        "topic_id": 12,
        "topic": "Tools, Tooling & Atlas Search",
        "urls": [
            "https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/",
            "https://www.mongodb.com/docs/atlas/tutorial/create-new-cluster/",
            "https://www.mongodb.com/docs/atlas/manage-clusters/",
            "https://www.mongodb.com/docs/atlas/atlas-search/",
            "https://www.mongodb.com/docs/atlas/atlas-search/index-definitions/",
            "https://www.mongodb.com/docs/atlas/atlas-search/query-syntax/",
            "https://www.mongodb.com/docs/atlas/atlas-search/aggregation-stages/search/",
            "https://www.mongodb.com/docs/atlas/sample-data/",
            "https://www.mongodb.com/docs/atlas/atlas-ui/documents/",
            "https://www.mongodb.com/docs/atlas/atlas-ui/query/filter/",
            "https://www.mongodb.com/docs/atlas/review-all-cluster-metrics/",
            "https://www.mongodb.com/docs/atlas/monitoring-alerts/",
            "https://www.mongodb.com/docs/atlas/atlas-ui/",
        ],
    },
]


@dataclass
class ResolvedDoc:
    topic_id: int
    topic: str
    source_url: str
    markdown_url: str
    local_path: str
    status: str
    fetch_method: str | None
    status_code: int | None
    bytes: int
    content_sha256: str | None
    fetched_at: str
    error: str | None = None


def slugify(value: str, max_length: int = 90) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return slug[:max_length].strip("_") or "untitled"


def filename_for_url(url: str) -> str:
    parsed = urlparse(url)
    slug = slugify(parsed.path.strip("/").replace("/", "_"), max_length=150)
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
    return f"{slug}__{digest}.md"


def topic_dir(output_dir: Path, topic_id: int, topic: str) -> Path:
    return output_dir / f"{topic_id:02d}_{slugify(topic)}"


def fetch_url(url: str, timeout: int) -> tuple[int, str]:
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    return response.status_code, response.text


class SimpleMarkdownParser(HTMLParser):
    BLOCK_TAGS = {"p", "div", "section", "article", "main", "br", "tr", "table"}
    SKIP_TAGS = {"script", "style", "nav", "footer", "header", "aside", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0
        self.link_href: str | None = None
        self.in_pre = False
        self.title_parts: list[str] = []
        self.in_title = False
        self.in_h1 = False

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        attrs_dict = dict(attrs)
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.in_h1 = True
            self.parts.append("\n# ")
        elif tag in {"h2", "h3", "h4"}:
            level = {"h2": "##", "h3": "###", "h4": "####"}[tag]
            self.parts.append(f"\n\n{level} ")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "pre":
            self.in_pre = True
            self.parts.append("\n\n```\n")
        elif tag == "code" and not self.in_pre:
            self.parts.append("`")
        elif tag == "a":
            self.link_href = attrs_dict.get("href")
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
            self.parts.append("\n")
        elif tag in {"h2", "h3", "h4", "p", "li"}:
            self.parts.append("\n")
        elif tag == "pre":
            self.in_pre = False
            self.parts.append("\n```\n")
        elif tag == "code" and not self.in_pre:
            self.parts.append("`")
        elif tag == "a":
            self.link_href = None

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = unescape(data)
        if not self.in_pre:
            text = re.sub(r"\s+", " ", text)
        if not text.strip():
            return
        if self.in_title or self.in_h1:
            self.title_parts.append(text.strip())
        if self.link_href:
            self.parts.append(f"[{text.strip()}]({self.link_href})")
        else:
            self.parts.append(text if self.in_pre else text.strip() + " ")

    def markdown(self) -> str:
        content = "".join(self.parts)
        content = re.sub(r"[ \t]+\n", "\n", content)
        content = re.sub(r"\n{3,}", "\n\n", content)
        return content.strip()

    def title(self, fallback: str) -> str:
        title = " ".join(part for part in self.title_parts if part).strip()
        title = re.sub(r"\s+", " ", title)
        return title or fallback


def html_to_markdown(html: str, source_url: str) -> str:
    parser = SimpleMarkdownParser()
    parser.feed(html)
    title = parser.title(source_url.rstrip("/").split("/")[-1])
    content = parser.markdown()
    if not content.startswith("#"):
        content = f"# {title}\n\n{content}"
    return f"> Source: {source_url}\n> Fetch method: html_fallback\n\n{content.strip()}\n"


def markdown_with_header(markdown: str, source_url: str) -> str:
    if markdown.lstrip().startswith("#"):
        return f"> Source: {source_url}\n> Fetch method: direct_markdown\n\n{markdown.strip()}\n"
    title = source_url.rstrip("/").split("/")[-1]
    return f"# {title}\n\n> Source: {source_url}\n> Fetch method: direct_markdown\n\n{markdown.strip()}\n"


def resolve_one(topic_id: int, topic: str, source_url: str, output_dir: Path, timeout: int, min_chars: int) -> ResolvedDoc:
    folder = topic_dir(output_dir, topic_id, topic)
    folder.mkdir(parents=True, exist_ok=True)
    local_path = folder / filename_for_url(source_url)
    markdown_url = url_to_markdown_url(source_url)
    fetched_at = datetime.now(timezone.utc).isoformat()

    try:
        status_code, text = fetch_url(markdown_url, timeout)
        if status_code == 200 and len(text.strip()) >= min_chars:
            content = markdown_with_header(text, source_url)
            local_path.write_text(content, encoding="utf-8", errors="replace")
            return build_entry(topic_id, topic, source_url, markdown_url, local_path, "saved", "direct_markdown", status_code, content, fetched_at)

        html_status, html = fetch_url(source_url, timeout)
        if html_status == 200 and len(html.strip()) >= min_chars:
            content = html_to_markdown(html, source_url)
            if len(content.strip()) >= min_chars:
                local_path.write_text(content, encoding="utf-8", errors="replace")
                return build_entry(topic_id, topic, source_url, markdown_url, local_path, "saved", "html_fallback", html_status, content, fetched_at)

        return ResolvedDoc(
            topic_id=topic_id,
            topic=topic,
            source_url=source_url,
            markdown_url=markdown_url,
            local_path=local_path.relative_to(PROJECT_ROOT).as_posix(),
            status="failed",
            fetch_method=None,
            status_code=html_status,
            bytes=0,
            content_sha256=None,
            fetched_at=fetched_at,
            error=f"direct_md_status={status_code}; html_status={html_status}",
        )
    except Exception as exc:
        return ResolvedDoc(
            topic_id=topic_id,
            topic=topic,
            source_url=source_url,
            markdown_url=markdown_url,
            local_path=local_path.relative_to(PROJECT_ROOT).as_posix(),
            status="failed",
            fetch_method=None,
            status_code=None,
            bytes=0,
            content_sha256=None,
            fetched_at=fetched_at,
            error=str(exc),
        )


def build_entry(
    topic_id: int,
    topic: str,
    source_url: str,
    markdown_url: str,
    local_path: Path,
    status: str,
    fetch_method: str,
    status_code: int,
    content: str,
    fetched_at: str,
) -> ResolvedDoc:
    encoded = content.encode("utf-8")
    return ResolvedDoc(
        topic_id=topic_id,
        topic=topic,
        source_url=source_url,
        markdown_url=markdown_url,
        local_path=local_path.relative_to(PROJECT_ROOT).as_posix(),
        status=status,
        fetch_method=fetch_method,
        status_code=status_code,
        bytes=len(encoded),
        content_sha256=hashlib.sha256(encoded).hexdigest(),
        fetched_at=fetched_at,
    )


def resolve_targets(output_dir: Path, timeout: int, delay: float, min_chars: int, force: bool) -> list[ResolvedDoc]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "associate_python_developer_sources_manifest.json"
    results = []

    for target in ASSOCIATE_PYTHON_DEVELOPER_TARGETS:
        folder = topic_dir(output_dir, target["topic_id"], target["topic"])
        folder.mkdir(parents=True, exist_ok=True)
        if force:
            for file_path in folder.glob("*.md"):
                file_path.unlink()

        for source_url in target["urls"]:
            local_path = folder / filename_for_url(source_url)
            if local_path.exists() and not force:
                content = local_path.read_text(encoding="utf-8", errors="replace")
                results.append(
                    build_entry(
                        target["topic_id"],
                        target["topic"],
                        source_url,
                        url_to_markdown_url(source_url),
                        local_path,
                        "saved",
                        "existing_file",
                        200,
                        content,
                        datetime.now(timezone.utc).isoformat(),
                    )
                )
                continue

            entry = resolve_one(target["topic_id"], target["topic"], source_url, output_dir, timeout, min_chars)
            results.append(entry)
            print(f"{entry.status}: topic={entry.topic_id} method={entry.fetch_method} url={source_url}")
            manifest_path.write_text(json.dumps([asdict(item) for item in results], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            if delay > 0:
                time.sleep(delay)

    manifest_path.write_text(json.dumps([asdict(item) for item in results], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return results


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resolve curated official docs for the Associate Python Developer syllabus.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory.")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout.")
    parser.add_argument("--delay", type=float, default=0.15, help="Delay between requests.")
    parser.add_argument("--min-chars", type=int, default=100, help="Minimum page body length.")
    parser.add_argument("--force", action="store_true", help="Re-resolve existing files.")
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    results = resolve_targets(Path(args.output_dir).resolve(), args.timeout, args.delay, args.min_chars, args.force)
    saved = sum(1 for item in results if item.status == "saved")
    failed = sum(1 for item in results if item.status != "saved")
    print(f"Resolved Associate Python Developer docs: saved={saved} failed={failed}")


if __name__ == "__main__":
    main()
