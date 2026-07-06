"""Read-only report: for every question in the bank, resolve its syllabus
topic/concept and the official doc(s) that concept maps to (the same
resolution used to build memory/study_order_map.md), then compare that
against whatever citation doc the question currently carries. Writes
nothing to the database or filesystem outside the optional --out CSV.
"""
from __future__ import annotations

import argparse
import csv
import os

from rich.console import Console
from rich.table import Table

from certcoach.core import database, planner
from certcoach.jobs.map_questions import find_best_concept

console = Console()

CLEANED_MARKDOWNS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "cleaned_markdowns"
)


def build_syllabus_index() -> tuple[dict[int, dict], dict[str, dict]]:
    """Returns (topics_by_id, topics_by_bank_key) from syllabus.json."""
    syllabus = planner.load_syllabus()
    by_id = {item["id"]: item for item in syllabus}
    by_bank_key = {}
    for item in syllabus:
        for key in item.get("bank_topic_keys", []):
            by_bank_key.setdefault(key.lower(), item)
    return by_id, by_bank_key


def resolve_topic_and_concept(question: dict, topics_by_id: dict, topics_by_bank_key: dict) -> dict:
    """Prefers the question's own stored topic_id/concept; falls back to the
    same keyword-matching inference certcoach-map-questions would apply, so
    the 23 topic_id-less legacy records still get a best-effort placement
    instead of being reported as unmappable."""
    meta = question.get("metadata", {})
    topic_id = meta.get("topic_id")
    concept = meta.get("concept")

    if topic_id in topics_by_id and concept:
        return {"topic_id": topic_id, "topic_name": topics_by_id[topic_id]["topic"], "concept": concept, "source": "stored"}

    q_topic_key = str(meta.get("topic", "")).lower()
    candidate = topics_by_bank_key.get(q_topic_key)
    if candidate is None:
        for item in topics_by_id.values():
            if item["topic"].lower() == q_topic_key:
                candidate = item
                break

    if candidate is None:
        return {"topic_id": None, "topic_name": None, "concept": None, "source": "unresolved"}

    inferred_concept = concept or find_best_concept(
        question.get("question_text", ""), question.get("options", []), candidate.get("subtopics", [])
    )
    return {"topic_id": candidate["id"], "topic_name": candidate["topic"], "concept": inferred_concept, "source": "inferred"}


def resolve_official_docs(topic_id: int | None, concept: str | None, topics_by_id: dict) -> tuple[list[str], bool]:
    """Returns (doc_filenames, is_concept_exact). is_concept_exact is False
    when no doc scored a positive match and we fell back to the topic's
    first two docs -- mirrors the "shared/no dedicated doc" cases already
    documented in study_order_map.md."""
    topic = topics_by_id.get(topic_id)
    if topic is None:
        return [], False

    md_files = topic.get("md_files", [])
    if not concept:
        return md_files[:2], False

    matched = [f for f in planner.prioritize_md_files(md_files, concept) if planner.score_md_file_for_concept(f, concept) > 0]
    if matched:
        return matched, True
    return md_files[:2], False


def current_citation_doc(question: dict) -> str:
    provenance = question.get("provenance") or {}
    doc_file = (provenance.get("citation") or {}).get("doc_file", "")
    if doc_file:
        return doc_file
    return question.get("metadata", {}).get("citation_source", "") or question.get("citation_source", "") or ""


def build_report() -> list[dict]:
    topics_by_id, topics_by_bank_key = build_syllabus_index()
    rows = []
    for q in database.questions_col.find({}):
        placement = resolve_topic_and_concept(q, topics_by_id, topics_by_bank_key)
        resolved_docs, is_exact = resolve_official_docs(placement["topic_id"], placement["concept"], topics_by_id)
        current_doc = current_citation_doc(q)
        current_doc_is_real_file = bool(current_doc) and os.path.exists(os.path.join(CLEANED_MARKDOWNS_DIR, current_doc))

        rows.append(
            {
                "_id": q["_id"],
                "provenance_state": (q.get("provenance") or {}).get("state", "no_provenance"),
                "topic_id": placement["topic_id"],
                "topic_name": placement["topic_name"],
                "concept": placement["concept"],
                "concept_source": placement["source"],
                "resolved_docs": resolved_docs,
                "resolved_docs_exact": is_exact,
                "current_citation": current_doc,
                "current_citation_matches_resolved": current_doc_is_real_file and current_doc in resolved_docs,
            }
        )
    return rows


def print_summary(rows: list[dict]) -> None:
    console.print(f"\n[bold cyan]Mapped {len(rows)} questions to syllabus topic/concept + official docs[/bold cyan]")

    by_source = {}
    for r in rows:
        by_source[r["concept_source"]] = by_source.get(r["concept_source"], 0) + 1
    console.print("\n[bold]Concept resolution source[/bold]")
    for source, count in sorted(by_source.items(), key=lambda kv: -kv[1]):
        console.print(f"  {source:<12}: {count}")

    exact_count = sum(1 for r in rows if r["resolved_docs_exact"])
    fallback_count = sum(1 for r in rows if r["resolved_docs"] and not r["resolved_docs_exact"])
    no_doc_count = sum(1 for r in rows if not r["resolved_docs"])
    console.print("\n[bold]Official doc resolution[/bold]")
    console.print(f"  [green]concept-exact match[/green] : {exact_count}")
    console.print(f"  [yellow]topic-level fallback[/yellow]: {fallback_count}  (no doc scored an exact concept match)")
    console.print(f"  [red]unresolved (no topic)[/red] : {no_doc_count}")

    mismatch = [r for r in rows if r["current_citation"] and not r["current_citation_matches_resolved"]]
    console.print(f"\n[bold]Citation drift[/bold]: {len(mismatch)} questions have a recorded citation that is not one of the resolved official docs")

    table = Table(title="By topic")
    table.add_column("Topic ID")
    table.add_column("Topic")
    table.add_column("Questions", justify="right")
    table.add_column("Confirmed", justify="right")
    table.add_column("Sourced", justify="right")
    table.add_column("Suspect", justify="right")
    by_topic: dict = {}
    for r in rows:
        key = (r["topic_id"], r["topic_name"])
        entry = by_topic.setdefault(key, {"total": 0, "confirmed": 0, "sourced": 0, "suspect": 0})
        entry["total"] += 1
        if r["provenance_state"] in entry:
            entry[r["provenance_state"]] += 1
    for (topic_id, topic_name), counts in sorted(by_topic.items(), key=lambda kv: (kv[0][0] is None, kv[0][0] or 0)):
        table.add_row(str(topic_id), topic_name or "(unresolved)", str(counts["total"]), str(counts["confirmed"]), str(counts["sourced"]), str(counts["suspect"]))
    console.print(table)


def write_csv(rows: list[dict], path: str) -> None:
    fieldnames = [
        "_id", "provenance_state", "topic_id", "topic_name", "concept", "concept_source",
        "resolved_docs", "resolved_docs_exact", "current_citation", "current_citation_matches_resolved",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            row = dict(r)
            row["resolved_docs"] = "; ".join(row["resolved_docs"])
            writer.writerow(row)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only report mapping every question to its syllabus topic/concept and official doc(s).")
    parser.add_argument("--out", help="Optional path to write the full per-question detail as CSV.")
    args = parser.parse_args(argv)

    database.check_connection()
    rows = build_report()
    print_summary(rows)

    if args.out:
        write_csv(rows, args.out)
        console.print(f"\n[dim]Full per-question detail written to {args.out}[/dim]")

    console.print("\n[dim]This script wrote nothing to the database.[/dim]")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
