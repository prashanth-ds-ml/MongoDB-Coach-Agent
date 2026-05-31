import json

from src.scripts.utils.mongodb_docs_md_scraper import (
    ManifestEntry,
    PROJECT_ROOT,
    filter_urls,
    load_existing_manifest,
    normalize_docs_url,
    project_relative_path,
    parse_llms_txt,
    safe_filename,
    url_to_markdown_url,
    write_json,
)


def test_normalize_docs_url_accepts_only_mongodb_docs_pages():
    assert normalize_docs_url("https://www.mongodb.com/docs/build-with-ai/") == (
        "https://www.mongodb.com/docs/build-with-ai/"
    )
    assert normalize_docs_url("https://www.mongodb.com/docs/build-with-ai/?x=1#section") == (
        "https://www.mongodb.com/docs/build-with-ai/"
    )
    assert normalize_docs_url("https://www.mongodb.com/docs/build-with-ai.md") == (
        "https://www.mongodb.com/docs/build-with-ai/"
    )
    assert normalize_docs_url("https://example.com/docs/build-with-ai/") is None
    assert normalize_docs_url("https://www.mongodb.com/products/platform") is None


def test_url_to_markdown_url():
    assert url_to_markdown_url("https://www.mongodb.com/docs/build-with-ai/") == (
        "https://www.mongodb.com/docs/build-with-ai.md"
    )
    assert url_to_markdown_url("https://www.mongodb.com/docs/manual/crud/") == (
        "https://www.mongodb.com/docs/manual/crud.md"
    )


def test_parse_llms_txt_deduplicates_and_strips_markdown_punctuation():
    text = """
    - [Build with AI](https://www.mongodb.com/docs/build-with-ai/)
    - [Build with AI md](https://www.mongodb.com/docs/build-with-ai.md)
    - https://www.mongodb.com/docs/manual/crud/).
    - https://www.mongodb.com/products/platform
    """

    assert parse_llms_txt(text) == [
        "https://www.mongodb.com/docs/build-with-ai/",
        "https://www.mongodb.com/docs/manual/crud/",
    ]


def test_safe_filename_is_stable_readable_and_hashed():
    filename = safe_filename("https://www.mongodb.com/docs/manual/tutorial/query-documents/")

    assert filename.startswith("docs_manual_tutorial_query-documents__")
    assert filename.endswith(".md")
    assert filename == safe_filename("https://www.mongodb.com/docs/manual/tutorial/query-documents/")


def test_filter_urls_include_and_exclude():
    urls = [
        "https://www.mongodb.com/docs/manual/crud/",
        "https://www.mongodb.com/docs/manual/indexes/",
        "https://www.mongodb.com/docs/atlas/search/",
    ]

    assert filter_urls(urls, include=["/docs/manual/"], exclude=["indexes"]) == [
        "https://www.mongodb.com/docs/manual/crud/"
    ]


def test_manifest_json_round_trip(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    entry = ManifestEntry(
        source_url="https://www.mongodb.com/docs/manual/crud/",
        markdown_url="https://www.mongodb.com/docs/manual/crud.md",
        local_path="data/mongodb_docs/raw_markdown/docs_manual_crud.md",
        status="saved",
        status_code=200,
        bytes=123,
        content_sha256="abc",
        fetched_at="2026-05-31T00:00:00+00:00",
    )

    write_json(manifest_path, [entry.__dict__])

    assert json.loads(manifest_path.read_text(encoding="utf-8"))[0]["status"] == "saved"
    assert load_existing_manifest(manifest_path)[entry.source_url] == entry


def test_project_relative_path_uses_posix_separators():
    path = PROJECT_ROOT / "data" / "mongodb_docs" / "raw_markdown" / "example.md"

    assert project_relative_path(path) == "data/mongodb_docs/raw_markdown/example.md"
