from __future__ import annotations

import argparse
from datetime import datetime, timezone
from typing import Any

from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn
from rich.table import Table

from certcoach.core import database
from certcoach.jobs.nightly_seed_questions import question_fingerprint

console = Console()


def _dedupe_key(question: dict[str, Any]) -> str:
    metadata = question.get("metadata", {}) or {}
    stored = str(metadata.get("question_fingerprint", "") or "").strip()
    if stored:
        return stored
    topic = str(metadata.get("topic") or metadata.get("syllabus_topic") or "")
    concept = str(metadata.get("concept") or "")
    return question_fingerprint(topic, concept, str(question.get("question_text", "") or ""))


def _created_at_sort_value(question: dict[str, Any]) -> str:
    metadata = question.get("metadata", {}) or {}
    return str(metadata.get("created_at") or question.get("created_at") or "")


def _quality_score(question: dict[str, Any]) -> tuple[int, int, int, str]:
    explanation_parts = [
        str(question.get("explanation", "") or ""),
        str(question.get("trap_analysis", "") or ""),
        str(question.get("citation_source", "") or ""),
    ]
    for option in question.get("options", []) or []:
        explanation_parts.append(str(option.get("feedback", "") or ""))
    explanation_text = "\n".join(explanation_parts)
    lowered = explanation_text.lower()

    marker_count = sum(
        1 for marker in database.SEVEN_PART_EXPLANATION_MARKERS
        if marker in lowered
    )
    option_feedback_count = sum(
        1 for option in question.get("options", []) or []
        if str(option.get("feedback", "") or "").strip()
    )
    attempts = int((question.get("global_metrics", {}) or {}).get("total_attempts", 0) or 0)
    created_at = _created_at_sort_value(question)
    return marker_count, len(explanation_text), option_feedback_count + attempts, created_at


def _topic_matches(question: dict[str, Any], topic_filter: str | None) -> bool:
    if not topic_filter:
        return True

    wanted = topic_filter.strip().lower()
    metadata = question.get("metadata", {}) or {}
    values = [
        str(metadata.get("topic", "")),
        str(metadata.get("syllabus_topic", "")),
        str(metadata.get("topic_id", "")),
        str(metadata.get("topic_number", "")),
    ]
    return any(value.strip().lower() == wanted for value in values if value)


def find_duplicate_groups(topic_filter: str | None = None) -> list[dict[str, Any]]:
    questions = list(database.questions_col.find({}))
    groups: dict[str, list[dict[str, Any]]] = {}

    progress = Progress(
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=34),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    )
    with progress:
        task_id = progress.add_task("Fingerprinting questions", total=len(questions))
        for question in questions:
            if _topic_matches(question, topic_filter):
                key = _dedupe_key(question)
                if key:
                    groups.setdefault(key, []).append(question)
            progress.advance(task_id)

    duplicate_groups = []
    for key, items in groups.items():
        if len(items) < 2:
            continue
        sorted_items = sorted(items, key=_quality_score, reverse=True)
        duplicate_groups.append({
            "key": key,
            "keep": sorted_items[0],
            "remove": sorted_items[1:],
        })

    return sorted(
        duplicate_groups,
        key=lambda group: len(group["remove"]),
        reverse=True,
    )


def run_dedupe(*, apply: bool = False, topic: str | None = None, limit: int | None = None) -> dict[str, int]:
    database.check_connection()
    duplicate_groups = find_duplicate_groups(topic)
    if limit is not None:
        duplicate_groups = duplicate_groups[:limit]

    duplicate_docs = sum(len(group["remove"]) for group in duplicate_groups)

    console.print("\n[bold cyan]CertCoach Question Bank Duplicate Check[/bold cyan]")
    console.print(f"Mode: {'apply/delete duplicates' if apply else 'dry-run/report only'}")
    if topic:
        console.print(f"Topic filter: {topic}")
    console.print(f"Duplicate groups: {len(duplicate_groups)}")
    console.print(f"Duplicate documents removable: {duplicate_docs}")

    if duplicate_groups:
        table = Table(title="Duplicate Groups")
        table.add_column("#", justify="right")
        table.add_column("Topic")
        table.add_column("Copies", justify="right")
        table.add_column("Question")
        for index, group in enumerate(duplicate_groups[:25], start=1):
            keep = group["keep"]
            metadata = keep.get("metadata", {}) or {}
            table.add_row(
                str(index),
                str(metadata.get("topic") or metadata.get("syllabus_topic") or "-"),
                str(len(group["remove"]) + 1),
                str(keep.get("question_text", ""))[:90],
            )
        console.print(table)

    deleted = 0
    if apply and duplicate_groups:
        ids_to_remove = [
            item["_id"]
            for group in duplicate_groups
            for item in group["remove"]
            if "_id" in item
        ]
        if ids_to_remove:
            result = database.questions_col.delete_many({"_id": {"$in": ids_to_remove}})
            deleted = int(result.deleted_count)
            database.questions_col.update_many(
                {"_id": {"$in": [group["keep"]["_id"] for group in duplicate_groups if "_id" in group["keep"]]}},
                {"$set": {"metadata.dedupe_checked_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()}},
            )
            console.print(f"\n[green]Deleted duplicate documents: {deleted}[/green]")

    if not apply:
        console.print("\n[yellow]Dry run only. Re-run with --apply to remove duplicates.[/yellow]")

    return {
        "duplicate_groups": len(duplicate_groups),
        "duplicate_documents": duplicate_docs,
        "deleted": deleted,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit and remove duplicate CertCoach question-bank items.")
    parser.add_argument("--apply", action="store_true", help="Delete duplicate question documents. Without this, only reports.")
    parser.add_argument("--topic", help="Optional exact topic id/name filter.")
    parser.add_argument("--limit", type=int, help="Only process the first N duplicate groups.")
    args = parser.parse_args()

    run_dedupe(apply=args.apply, topic=args.topic, limit=args.limit)


if __name__ == "__main__":
    main()
