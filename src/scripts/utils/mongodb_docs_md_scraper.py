"""
Download MongoDB documentation markdown pages from llms.txt.

MongoDB documentation pages expose direct markdown variants by stripping a
trailing slash from the page URL and appending ".md". This utility treats that
markdown as the raw source cache for later exam-specific syllabus mapping.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, urlunparse
from urllib.request import Request, urlopen


LLMS_TXT_URL = "https://www.mongodb.com/docs/llms.txt"
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "mongodb_docs"
USER_AGENT = "CertCoach MongoDB docs markdown scraper/0.1"


@dataclass
class ManifestEntry:
    source_url: str
    markdown_url: str
    local_path: str
    status: str
    status_code: int | None
    bytes: int
    content_sha256: str | None
    fetched_at: str
    error: str | None = None


def normalize_docs_url(url: str) -> str | None:
    """Return a canonical MongoDB docs page URL, or None for non-doc URLs."""
    raw = url.strip().strip(").,;]")
    parsed = urlparse(raw)

    if parsed.scheme not in {"http", "https"}:
        return None
    if parsed.netloc.lower() != "www.mongodb.com":
        return None
    if not parsed.path.startswith("/docs/"):
        return None

    path = parsed.path
    if path.endswith(".md"):
        path = path[:-3]
    path = path.rstrip("/")
    if not path:
        return None

    return urlunparse(("https", parsed.netloc.lower(), path + "/", "", "", ""))


def url_to_markdown_url(source_url: str) -> str:
    """Convert a MongoDB docs page URL into its direct markdown URL."""
    parsed = urlparse(source_url)
    path = parsed.path.rstrip("/")
    if path.endswith(".md"):
        return urlunparse(("https", parsed.netloc.lower(), path, "", "", ""))
    return urlunparse(("https", parsed.netloc.lower(), path + ".md", "", "", ""))


def parse_llms_txt(text: str) -> list[str]:
    """Extract and deduplicate MongoDB docs URLs from llms.txt content."""
    candidates = re.findall(r"https://www\.mongodb\.com/docs/[^\s)\]]+", text)
    urls = []
    seen = set()

    for candidate in candidates:
        normalized = normalize_docs_url(candidate)
        if normalized and normalized not in seen:
            seen.add(normalized)
            urls.append(normalized)

    return urls


def safe_filename(source_url: str, max_slug_length: int = 160) -> str:
    """Build a stable, readable filename with a short URL hash suffix."""
    parsed = urlparse(source_url)
    slug = parsed.path.strip("/").replace("/", "_")
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "_", slug).strip("_").lower()
    slug = slug[:max_slug_length].strip("_") or "mongodb_docs"
    digest = hashlib.sha256(source_url.encode("utf-8")).hexdigest()[:10]
    return f"{slug}__{digest}.md"


def filter_urls(urls: Iterable[str], include: list[str], exclude: list[str]) -> list[str]:
    """Apply substring include/exclude filters to a URL list."""
    filtered = []
    for url in urls:
        if include and not any(pattern in url for pattern in include):
            continue
        if exclude and any(pattern in url for pattern in exclude):
            continue
        filtered.append(url)
    return filtered


def fetch_text(url: str, timeout: int) -> tuple[int, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        status_code = getattr(response, "status", response.getcode())
        body = response.read().decode("utf-8", errors="replace")
    return status_code, body


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def project_relative_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def load_existing_manifest(manifest_path: Path) -> dict[str, ManifestEntry]:
    if not manifest_path.exists():
        return {}

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = {}
    for item in data:
        try:
            entry = ManifestEntry(**item)
            entries[entry.source_url] = entry
        except TypeError:
            continue
    return entries


def build_failed_entry(
    source_url: str,
    markdown_url: str,
    local_path: Path,
    fetched_at: str,
    status_code: int | None,
    error: str,
    bytes_count: int = 0,
) -> ManifestEntry:
    return ManifestEntry(
        source_url=source_url,
        markdown_url=markdown_url,
        local_path=project_relative_path(local_path),
        status="failed",
        status_code=status_code,
        bytes=bytes_count,
        content_sha256=None,
        fetched_at=fetched_at,
        error=error,
    )


def fetch_markdown_page(
    source_url: str,
    raw_dir: Path,
    timeout: int,
    min_chars: int,
    retries: int,
    retry_backoff: float,
) -> ManifestEntry:
    filename = safe_filename(source_url)
    local_path = raw_dir / filename
    markdown_url = url_to_markdown_url(source_url)
    fetched_at = datetime.now(timezone.utc).isoformat()

    last_error = None
    for attempt in range(retries + 1):
        try:
            status_code, body = fetch_text(markdown_url, timeout)
            stripped = body.strip()
            if status_code == 200 and len(stripped) >= min_chars:
                local_path.write_text(body, encoding="utf-8", errors="replace")
                digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
                return ManifestEntry(
                    source_url=source_url,
                    markdown_url=markdown_url,
                    local_path=project_relative_path(local_path),
                    status="saved",
                    status_code=status_code,
                    bytes=len(body.encode("utf-8")),
                    content_sha256=digest,
                    fetched_at=fetched_at,
                )

            return build_failed_entry(
                source_url=source_url,
                markdown_url=markdown_url,
                local_path=local_path,
                fetched_at=fetched_at,
                status_code=status_code,
                error=f"Markdown response below minimum length {min_chars}",
                bytes_count=len(body.encode("utf-8")),
            )
        except HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504}:
                return build_failed_entry(
                    source_url=source_url,
                    markdown_url=markdown_url,
                    local_path=local_path,
                    fetched_at=fetched_at,
                    status_code=exc.code,
                    error=str(exc),
                )
            last_error = f"{exc}"
            last_status = exc.code
        except URLError as exc:
            last_error = str(exc.reason)
            last_status = None

        if attempt < retries:
            time.sleep(retry_backoff * (2**attempt))

    return build_failed_entry(
        source_url=source_url,
        markdown_url=markdown_url,
        local_path=local_path,
        fetched_at=fetched_at,
        status_code=last_status,
        error=last_error or "Request failed",
    )


def persist_manifest(manifest: dict[str, ManifestEntry], manifest_path: Path, error_path: Path) -> None:
    write_json(manifest_path, [asdict(item) for item in manifest.values()])
    errors = [asdict(item) for item in manifest.values() if item.status != "saved"]
    write_json(error_path, errors)


def download_markdown_pages(
    urls: list[str],
    output_dir: Path,
    timeout: int,
    delay: float,
    force: bool,
    min_chars: int,
    workers: int,
    retries: int,
    retry_backoff: float,
    progress_every: int,
    manifest_every: int,
) -> list[ManifestEntry]:
    raw_dir = output_dir / "raw_markdown"
    manifest_path = output_dir / "manifests" / "mongodb_docs_manifest.json"
    error_path = output_dir / "manifests" / "mongodb_docs_errors.json"

    raw_dir.mkdir(parents=True, exist_ok=True)
    existing = load_existing_manifest(manifest_path)
    manifest: dict[str, ManifestEntry] = dict(existing)

    pending = []
    skipped = 0
    for source_url in urls:
        filename = safe_filename(source_url)
        local_path = raw_dir / filename

        if not force and local_path.exists() and source_url in manifest and manifest[source_url].status == "saved":
            skipped += 1
            continue
        pending.append(source_url)

    if skipped:
        print(f"Skipped {skipped} pages already saved.")

    if not pending:
        persist_manifest(manifest, manifest_path, error_path)
        return list(manifest.values())

    workers = max(1, workers)
    print(f"Downloading {len(pending)} pages with workers={workers}.")

    completed = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for source_url in pending:
            futures.append(
                executor.submit(
                    fetch_markdown_page,
                    source_url,
                    raw_dir,
                    timeout,
                    min_chars,
                    retries,
                    retry_backoff,
                )
            )
            if delay > 0:
                time.sleep(delay)

        for future in as_completed(futures):
            entry = future.result()
            manifest[entry.source_url] = entry
            completed += 1

            should_report_progress = progress_every > 0 and completed % progress_every == 0
            if entry.status != "saved":
                print(f"[{completed}/{len(pending)}] failed {entry.markdown_url}: {entry.error}")
            elif should_report_progress or completed == len(pending):
                saved_total = sum(1 for item in manifest.values() if item.status == "saved")
                failed_total = sum(1 for item in manifest.values() if item.status != "saved")
                print(
                    f"[{completed}/{len(pending)}] progress "
                    f"saved_total={saved_total} failed_total={failed_total}"
                )

            if manifest_every > 0 and completed % manifest_every == 0:
                persist_manifest(manifest, manifest_path, error_path)

    persist_manifest(manifest, manifest_path, error_path)
    return list(manifest.values())


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download MongoDB docs direct markdown pages.")
    parser.add_argument("--llms-url", default=LLMS_TXT_URL, help="MongoDB llms.txt URL.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory.")
    parser.add_argument("--include", action="append", default=[], help="Only keep URLs containing this text. Repeatable.")
    parser.add_argument("--exclude", action="append", default=[], help="Skip URLs containing this text. Repeatable.")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of URLs after filtering.")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds.")
    parser.add_argument("--delay", type=float, default=0.05, help="Delay between scheduling markdown downloads.")
    parser.add_argument("--min-chars", type=int, default=100, help="Minimum markdown body length to accept.")
    parser.add_argument("--workers", type=int, default=4, help="Number of concurrent markdown downloads.")
    parser.add_argument("--retries", type=int, default=2, help="Retries for transient request failures.")
    parser.add_argument("--retry-backoff", type=float, default=1.0, help="Initial retry backoff in seconds.")
    parser.add_argument("--progress-every", type=int, default=25, help="Print progress every N completed downloads.")
    parser.add_argument("--manifest-every", type=int, default=25, help="Checkpoint manifest every N completed downloads.")
    parser.add_argument("--force", action="store_true", help="Re-download pages already saved.")
    parser.add_argument("--dry-run", action="store_true", help="Fetch llms.txt and print planned downloads only.")
    parser.add_argument("--count-only", action="store_true", help="Fetch llms.txt and print only the URL count.")
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    output_dir = Path(args.output_dir).resolve()

    print(f"Fetching URL index: {args.llms_url}")
    _, llms_text = fetch_text(args.llms_url, args.timeout)
    urls = parse_llms_txt(llms_text)
    urls = filter_urls(urls, args.include, args.exclude)
    if args.limit > 0:
        urls = urls[: args.limit]

    print(f"Discovered {len(urls)} MongoDB docs URLs after filtering.")

    if args.count_only:
        return

    if args.dry_run:
        for source_url in urls:
            print(f"{source_url} -> {url_to_markdown_url(source_url)}")
        return

    entries = download_markdown_pages(
        urls=urls,
        output_dir=output_dir,
        timeout=args.timeout,
        delay=args.delay,
        force=args.force,
        min_chars=args.min_chars,
        workers=args.workers,
        retries=args.retries,
        retry_backoff=args.retry_backoff,
        progress_every=args.progress_every,
        manifest_every=args.manifest_every,
    )
    saved = sum(1 for entry in entries if entry.status == "saved")
    failed = sum(1 for entry in entries if entry.status != "saved")
    print(f"Done. saved={saved} failed={failed} output={output_dir}")


if __name__ == "__main__":
    main()
