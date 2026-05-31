"""
Map MongoDB docs markdown files into syllabus-specific folders.

The curated resolver output is the primary source for exam-aligned docs. A broad
full-docs scraper manifest is optional and only used when present.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SYLLABUS = PROJECT_ROOT / "data" / "syllabus.json"
DEFAULT_DOCS_MANIFEST = PROJECT_ROOT / "data" / "mongodb_docs" / "manifests" / "mongodb_docs_manifest.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "mongodb_docs" / "syllabus_mapped" / "associate_python_developer"
DEFAULT_EXISTING_RAW_DIR = PROJECT_ROOT / "data" / "raw_markdowns"
DEFAULT_RESOLVED_SOURCE_DIR = PROJECT_ROOT / "data" / "mongodb_docs" / "syllabus_sources" / "associate_python_developer"


CURATED_PATH_HINTS = {
    1: [
        "/docs/manual/introduction/",
        "/docs/manual/core/document/",
        "/docs/manual/reference/bson-types/",
        "/docs/manual/core/databases-and-collections/",
        "/docs/manual/reference/method/objectid/",
    ],
    2: [
        "/docs/manual/tutorial/insert-documents/",
        "/docs/manual/reference/method/db.collection.insertone/",
        "/docs/manual/reference/method/db.collection.insertmany/",
        "/docs/languages/python/pymongo-driver/current/crud/insert/",
    ],
    3: [
        "/docs/manual/tutorial/query-documents/",
        "/docs/manual/tutorial/project-fields-from-query-results/",
        "/docs/manual/reference/method/cursor.sort/",
        "/docs/manual/reference/method/cursor.limit/",
        "/docs/manual/reference/method/cursor.skip/",
        "/docs/languages/python/pymongo-driver/current/crud/query/",
    ],
    4: [
        "/docs/manual/tutorial/update-documents/",
        "/docs/manual/reference/operator/update/set/",
        "/docs/manual/reference/operator/update/push/",
        "/docs/manual/reference/operator/update/inc/",
        "/docs/languages/python/pymongo-driver/current/crud/update/",
    ],
    5: [
        "/docs/manual/tutorial/remove-documents/",
        "/docs/manual/reference/method/db.collection.deleteone/",
        "/docs/manual/reference/method/db.collection.deletemany/",
        "/docs/languages/python/pymongo-driver/current/crud/delete/",
    ],
    6: [
        "/docs/manual/reference/operator/query/",
        "/docs/manual/reference/operator/query-comparison/",
        "/docs/manual/reference/operator/query-logical/",
        "/docs/manual/reference/operator/query-element/",
        "/docs/manual/tutorial/query-documents/",
    ],
    7: [
        "/docs/manual/tutorial/query-arrays/",
        "/docs/manual/tutorial/query-array-of-documents/",
        "/docs/manual/tutorial/query-embedded-documents/",
        "/docs/manual/reference/operator/query/elemmatch/",
        "/docs/manual/reference/operator/query/size/",
        "/docs/manual/core/field-paths/",
    ],
    8: [
        "/docs/manual/aggregation/",
        "/docs/manual/core/aggregation-pipeline/",
        "/docs/manual/reference/operator/aggregation/",
        "/docs/manual/tutorial/aggregation",
        "/docs/languages/python/pymongo-driver/current/aggregation/",
    ],
    9: [
        "/docs/manual/indexes/",
        "/docs/manual/core/indexes/",
        "/docs/manual/core/index-single/",
        "/docs/manual/core/index-compound/",
        "/docs/manual/core/index-multikey/",
        "/docs/manual/core/index-unique/",
        "/docs/manual/reference/explain-results/",
        "/docs/languages/python/pymongo-driver/current/indexes/",
    ],
    10: [
        "/docs/manual/data-modeling/",
        "/docs/manual/core/data-modeling-introduction/",
        "/docs/manual/data-modeling/concepts/embedding-vs-references/",
        "/docs/manual/tutorial/model-embedded-one-to-many-relationships-between-documents/",
        "/docs/manual/tutorial/model-referenced-one-to-many-relationships-between-documents/",
        "/docs/manual/tutorial/model-data-for-atomic-operations/",
    ],
    11: [
        "/docs/languages/python/",
        "/docs/languages/python/pymongo-driver/current/",
        "/docs/languages/python/pymongo-driver/current/connect/",
        "/docs/languages/python/pymongo-driver/current/crud/",
        "/docs/languages/python/pymongo-driver/current/connection/",
    ],
    12: [
        "/docs/atlas/",
        "/docs/atlas/tutorial/deploy-free-tier-cluster/",
        "/docs/atlas/tutorial/create-new-cluster/",
        "/docs/atlas/manage-clusters/",
        "/docs/atlas/atlas-search/",
        "/docs/atlas/review-all-cluster-metrics/",
        "/docs/atlas/monitoring-alerts/",
    ],
}


@dataclass
class MappedDoc:
    topic_id: int
    topic: str
    score: int
    rank: int
    source_url: str
    markdown_url: str
    source_path: str
    mapped_path: str
    matched_terms: list[str]


def slugify(value: str, max_length: int = 90) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return (slug[:max_length].strip("_") or "untitled")


def normalize_term(value: str) -> str:
    term = value.lower().strip()
    term = re.sub(r"[()]", "", term)
    return term


def terms_for_topic(topic_item: dict) -> list[str]:
    raw_terms = [
        topic_item.get("topic", ""),
        *topic_item.get("subtopics", []),
        *topic_item.get("question_keywords", []),
        *topic_item.get("bank_topic_keys", []),
    ]
    terms = []
    seen = set()
    for raw in raw_terms:
        for part in re.split(r"\s+&\s+|\s+-\s+|,|\band\b|/|\|", raw):
            term = normalize_term(part)
            if len(term) < 2 or term in seen:
                continue
            seen.add(term)
            terms.append(term)
    return terms


def read_saved_docs(manifest_path: Path) -> list[dict]:
    if not manifest_path.exists():
        return []

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return [entry for entry in manifest if entry.get("status") == "saved"]


def score_doc(topic_item: dict, entry: dict, content: str) -> tuple[int, list[str]]:
    source_url = entry["source_url"].lower()
    path = urlparse(source_url).path.lower()
    haystack = f"{source_url}\n{content[:20000].lower()}"
    score = 0
    matched_terms = []
    is_atlas_topic = topic_item["id"] == 12
    is_pymongo_topic = topic_item["id"] == 11
    is_core_exam_topic = topic_item["id"] in set(range(1, 11))

    if is_core_exam_topic and not (
        "/docs/manual/" in source_url or "/docs/languages/python/pymongo-driver/current/" in source_url
    ):
        return -999, []
    if is_pymongo_topic and "/docs/languages/python/pymongo-driver/" not in source_url:
        return -999, []
    if is_atlas_topic and "/docs/atlas/" not in source_url:
        return -999, []

    for hint in CURATED_PATH_HINTS.get(topic_item["id"], []):
        normalized_hint = hint.lower()
        if path == normalized_hint:
            score += 160
            matched_terms.append(f"path:{hint}")
        elif normalized_hint in path:
            score += 100
            matched_terms.append(f"path:{hint}")

    for term in terms_for_topic(topic_item):
        if term in source_url:
            score += 24
            matched_terms.append(term)
        elif term in haystack:
            score += 6
            matched_terms.append(term)

    has_topic_signal = bool(matched_terms)

    if has_topic_signal and "/docs/manual/" in source_url:
        score += 20 if is_core_exam_topic else 8
    if "/docs/languages/python/pymongo-driver/current/" in source_url:
        score += 120 if is_pymongo_topic else 30
    if is_atlas_topic and "/docs/atlas/cli/" in source_url:
        score -= 25
    if has_topic_signal and is_atlas_topic and "/docs/atlas/" in source_url:
        score += 40

    return score, sorted(set(matched_terms))


def copy_existing_syllabus_docs(topic_item: dict, output_dir: Path, existing_raw_dir: Path) -> list[MappedDoc]:
    topic_dir = output_dir / f"{topic_item['id']:02d}_{slugify(topic_item['topic'])}"
    topic_dir.mkdir(parents=True, exist_ok=True)

    mapped_docs = []
    for rank, filename in enumerate(topic_item.get("md_files", []), start=1):
        source_path = existing_raw_dir / filename
        if not source_path.exists():
            continue

        target_path = topic_dir / f"00_existing_{filename}"
        shutil.copy2(source_path, target_path)
        mapped_docs.append(
            MappedDoc(
                topic_id=topic_item["id"],
                topic=topic_item["topic"],
                score=10_000 - rank,
                rank=rank,
                source_url=f"local://data/raw_markdowns/{filename}",
                markdown_url=f"local://data/raw_markdowns/{filename}",
                source_path=source_path.relative_to(PROJECT_ROOT).as_posix(),
                mapped_path=target_path.relative_to(PROJECT_ROOT).as_posix(),
                matched_terms=["existing_syllabus_md_file"],
            )
        )

    return mapped_docs


def copy_resolved_source_docs(topic_item: dict, output_dir: Path, resolved_source_dir: Path) -> list[MappedDoc]:
    source_topic_dir = resolved_source_dir / f"{topic_item['id']:02d}_{slugify(topic_item['topic'])}"
    if not source_topic_dir.exists():
        return []

    target_topic_dir = output_dir / f"{topic_item['id']:02d}_{slugify(topic_item['topic'])}"
    target_topic_dir.mkdir(parents=True, exist_ok=True)
    mapped_docs = []

    for rank, source_path in enumerate(sorted(source_topic_dir.glob("*.md")), start=1):
        target_path = target_topic_dir / f"00_resolved_{source_path.name}"
        shutil.copy2(source_path, target_path)
        mapped_docs.append(
            MappedDoc(
                topic_id=topic_item["id"],
                topic=topic_item["topic"],
                score=9_000 - rank,
                rank=rank,
                source_url=f"resolved://{source_path.relative_to(PROJECT_ROOT).as_posix()}",
                markdown_url=f"resolved://{source_path.relative_to(PROJECT_ROOT).as_posix()}",
                source_path=source_path.relative_to(PROJECT_ROOT).as_posix(),
                mapped_path=target_path.relative_to(PROJECT_ROOT).as_posix(),
                matched_terms=["resolved_associate_python_developer_source"],
            )
        )

    return mapped_docs


def prepare_topic_dir(topic_item: dict, output_dir: Path) -> Path:
    topic_dir = output_dir / f"{topic_item['id']:02d}_{slugify(topic_item['topic'])}"
    topic_dir.mkdir(parents=True, exist_ok=True)
    for markdown_file in topic_dir.glob("*.md"):
        markdown_file.unlink()
    return topic_dir


def clean_stale_topic_dirs(syllabus: list[dict], output_dir: Path) -> None:
    expected = {f"{item['id']:02d}_{slugify(item['topic'])}" for item in syllabus}
    for child in output_dir.iterdir():
        if child.is_dir() and re.match(r"^\d{2}_", child.name) and child.name not in expected:
            shutil.rmtree(child)


def copy_topic_docs(topic_item: dict, scored_docs: list[tuple[int, list[str], dict]], output_dir: Path, top_k: int) -> list[MappedDoc]:
    topic_dir = output_dir / f"{topic_item['id']:02d}_{slugify(topic_item['topic'])}"
    topic_dir.mkdir(parents=True, exist_ok=True)

    mapped_docs = []
    for rank, (score, matched_terms, entry) in enumerate(scored_docs[:top_k], start=1):
        source_path = PROJECT_ROOT / entry["local_path"]
        target_name = f"{rank:02d}_{Path(entry['local_path']).name}"
        target_path = topic_dir / target_name
        shutil.copy2(source_path, target_path)

        mapped_docs.append(
            MappedDoc(
                topic_id=topic_item["id"],
                topic=topic_item["topic"],
                score=score,
                rank=rank,
                source_url=entry["source_url"],
                markdown_url=entry["markdown_url"],
                source_path=entry["local_path"],
                mapped_path=target_path.relative_to(PROJECT_ROOT).as_posix(),
                matched_terms=matched_terms,
            )
        )

    return mapped_docs


def map_docs_to_syllabus(
    syllabus_path: Path,
    manifest_path: Path,
    output_dir: Path,
    existing_raw_dir: Path,
    resolved_source_dir: Path,
    top_k: int,
    min_score: int,
) -> list[MappedDoc]:
    syllabus = json.loads(syllabus_path.read_text(encoding="utf-8"))
    docs = read_saved_docs(manifest_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    clean_stale_topic_dirs(syllabus, output_dir)

    content_cache = {}
    all_mapped = []
    summary = []

    for topic_item in syllabus:
        prepare_topic_dir(topic_item, output_dir)
        existing_mapped = copy_existing_syllabus_docs(topic_item, output_dir, existing_raw_dir)
        resolved_mapped = copy_resolved_source_docs(topic_item, output_dir, resolved_source_dir)
        all_mapped.extend(resolved_mapped)
        all_mapped.extend(existing_mapped)

        scored_docs = []
        for entry in docs:
            local_path = PROJECT_ROOT / entry["local_path"]
            if local_path not in content_cache:
                content_cache[local_path] = local_path.read_text(encoding="utf-8", errors="replace")

            score, matched_terms = score_doc(topic_item, entry, content_cache[local_path])
            if score >= min_score:
                scored_docs.append((score, matched_terms, entry))

        scored_docs.sort(key=lambda item: (-item[0], item[2]["source_url"]))
        mapped = copy_topic_docs(topic_item, scored_docs, output_dir, top_k)
        all_mapped.extend(mapped)
        summary.append(
            {
                "topic_id": topic_item["id"],
                "topic": topic_item["topic"],
                "folder": (output_dir / f"{topic_item['id']:02d}_{slugify(topic_item['topic'])}").relative_to(PROJECT_ROOT).as_posix(),
                "existing_docs": len(existing_mapped),
                "resolved_docs": len(resolved_mapped),
                "mapped_docs": len(existing_mapped) + len(resolved_mapped) + len(mapped),
                "candidate_docs": len(scored_docs),
                "top_score": scored_docs[0][0] if scored_docs else 0,
            }
        )

    (output_dir / "topic_mapping_manifest.json").write_text(
        json.dumps([asdict(item) for item in all_mapped], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "mapping_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return all_mapped


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Map cached MongoDB docs to syllabus topic folders.")
    parser.add_argument("--syllabus", default=str(DEFAULT_SYLLABUS), help="Syllabus JSON path.")
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_DOCS_MANIFEST),
        help="Optional broad MongoDB docs scraper manifest path.",
    )
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory for topic folders.")
    parser.add_argument("--existing-raw-dir", default=str(DEFAULT_EXISTING_RAW_DIR), help="Existing syllabus raw markdown directory.")
    parser.add_argument("--resolved-source-dir", default=str(DEFAULT_RESOLVED_SOURCE_DIR), help="Curated resolved syllabus source directory.")
    parser.add_argument("--top-k", type=int, default=12, help="Maximum docs to copy per topic.")
    parser.add_argument("--min-score", type=int, default=40, help="Minimum relevance score to include a doc.")
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    mapped = map_docs_to_syllabus(
        syllabus_path=Path(args.syllabus).resolve(),
        manifest_path=Path(args.manifest).resolve(),
        output_dir=Path(args.output_dir).resolve(),
        existing_raw_dir=Path(args.existing_raw_dir).resolve(),
        resolved_source_dir=Path(args.resolved_source_dir).resolve(),
        top_k=args.top_k,
        min_score=args.min_score,
    )
    print(f"Mapped {len(mapped)} docs into {Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()
