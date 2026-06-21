from __future__ import annotations

import argparse
import sys
from collections import Counter

from rich.console import Console
from rich.table import Table

from certcoach.core import database, planner
from certcoach.core.bank_state import canonical_status, question_scope_key
from certcoach.core.question_targets import build_weighted_targets

console = Console()


def _target_key(target: dict | object) -> tuple:
    return (
        getattr(target, "topic_id", None),
        getattr(target, "concept", ""),
        getattr(target, "difficulty", ""),
    )


def _question_key(question: dict) -> tuple:
    return (
        *question_scope_key(question),
    )


def build_inventory_report(topic_filter: str | None = None, limit: int | None = None) -> dict:
    database.check_connection()
    questions = list(database.questions_col.find({}))

    if topic_filter:
        filt = topic_filter.strip().lower()
        questions = [
            q for q in questions
            if filt in " ".join(str(part or "") for part in (
                q.get("metadata", {}).get("topic", ""),
                q.get("metadata", {}).get("syllabus_topic", ""),
                q.get("metadata", {}).get("concept", ""),
                q.get("question_text", ""),
            )).lower()
        ]

    if limit is not None:
        questions = questions[:limit]

    syllabus = planner.load_syllabus()
    targets = build_weighted_targets(syllabus)
    target_lookup = {_target_key(target): target for target in targets}
    target_counts = Counter()
    legacy_counts = Counter()
    repair_counts = Counter()
    regeneration_counts = Counter()
    quarantine_counts = Counter()

    target_rows = []
    needs_explanation_repair = 0
    needs_question_regeneration = 0
    quarantined = 0
    legacy_pending = 0
    active_records = 0

    for question in questions:
        status = canonical_status(question)
        stored_status = str(question.get("metadata", {}).get("content_contract_status", "")).strip().lower()
        key = _question_key(question)
        if status == "active":
            active_records += 1
            target_counts[key] += 1
            continue

        if stored_status == "needs_explanation_repair":
            needs_explanation_repair += 1
            repair_counts[key] += 1
            continue
        if stored_status == "needs_question_regeneration":
            needs_question_regeneration += 1
            regeneration_counts[key] += 1
            continue
        if stored_status == "quarantined":
            quarantined += 1
            quarantine_counts[key] += 1
            continue
        legacy_pending += 1
        legacy_counts[key] += 1

    for key, target in target_lookup.items():
        active_count = target_counts.get(key, 0)
        legacy = legacy_counts.get(key, 0)
        target_rows.append({
            "topic_id": target.topic_id,
            "topic": target.topic,
            "concept": target.concept,
            "difficulty": target.difficulty,
            "readiness_threshold": target.target_count,
            "active_count": active_count,
            "legacy_count": legacy,
            "readiness_deficit": max(0, target.target_count - active_count),
            "study_ready": active_count >= target.target_count,
        })

    concept_rows = []
    concepts = {}
    concepts_by_scope = {}
    for row in target_rows:
        key = (row["topic_id"], row["topic"], row["concept"])
        summary = concepts.setdefault(key, {
            "topic_id": row["topic_id"],
            "topic": row["topic"],
            "concept": row["concept"],
            "easy_active": 0,
            "medium_active": 0,
            "easy_readiness_deficit": 3,
            "medium_readiness_deficit": 2,
            "repair_pending": 0,
            "regeneration_pending": 0,
            "legacy_pending": 0,
            "quarantine_pending": 0,
        })
        concepts_by_scope[(row["topic_id"], row["concept"])] = summary
        if row["difficulty"] == "Easy":
            summary["easy_active"] = row["active_count"]
            summary["easy_readiness_deficit"] = row["readiness_deficit"]
        elif row["difficulty"] == "Medium":
            summary["medium_active"] = row["active_count"]
            summary["medium_readiness_deficit"] = row["readiness_deficit"]

    # Status backlog should count the whole concept, including non-target difficulties
    # such as legacy Hard records that still require repair or quarantine.
    for question in questions:
        stored_status = str(question.get("metadata", {}).get("content_contract_status", "")).strip().lower()
        if stored_status not in {
            "needs_explanation_repair",
            "needs_question_regeneration",
            "legacy",
            "quarantined",
        }:
            continue
        metadata = question.get("metadata", {}) or {}
        scope_key = (
            metadata.get("topic_id"),
            str(metadata.get("concept", "")).strip(),
        )
        summary = concepts_by_scope.get(scope_key)
        if not summary:
            continue
        if stored_status == "needs_explanation_repair":
            summary["repair_pending"] += 1
        elif stored_status == "needs_question_regeneration":
            summary["regeneration_pending"] += 1
        elif stored_status == "legacy":
            summary["legacy_pending"] += 1
        elif stored_status == "quarantined":
            summary["quarantine_pending"] += 1

    for summary in concepts.values():
        summary["study_ready"] = summary["easy_active"] >= 3 and summary["medium_active"] >= 2
        concept_rows.append(summary)

    return {
        "total": len(questions),
        "active": active_records,
        "inactive": len(questions) - active_records,
        "needs_explanation_repair": needs_explanation_repair,
        "needs_question_regeneration": needs_question_regeneration,
        "legacy_pending": legacy_pending,
        "quarantined": quarantined,
        "targets": target_rows,
        "concepts": concept_rows,
    }


def render_report(report: dict, topic_filter: str | None = None) -> None:
    console.print("\n[bold cyan]CertCoach Question Bank Comparison Report[/bold cyan]")
    if topic_filter:
        console.print(f"Topic filter: [bold]{topic_filter}[/bold]")
    console.print(f"Loaded questions: [bold]{report['total']}[/bold]")
    console.print(f"Active records: [bold green]{report['active']}[/bold green]")
    console.print(f"Inactive records: [bold yellow]{report['inactive']}[/bold yellow]")
    console.print(f"Needs explanation repair: [bold cyan]{report['needs_explanation_repair']}[/bold cyan]")
    console.print(f"Needs question regeneration: [bold magenta]{report['needs_question_regeneration']}[/bold magenta]")
    console.print(f"Legacy pending: [bold green]{report['legacy_pending']}[/bold green]")
    console.print(f"Quarantine candidates: [bold red]{report['quarantined']}[/bold red]")
    console.print()

    summary = Table(title="Bank Status Comparison")
    for col in ("Metric", "Count"):
        summary.add_column(col)
    summary.add_row("Active", str(report["active"]))
    summary.add_row("Inactive", str(report["inactive"]))
    summary.add_row("Needs Explanation Repair", str(report["needs_explanation_repair"]))
    summary.add_row("Needs Question Regeneration", str(report["needs_question_regeneration"]))
    summary.add_row("Legacy Pending", str(report["legacy_pending"]))
    summary.add_row("Quarantine", str(report["quarantined"]))
    console.print(summary)

    concept_table = Table(title="Concept Study Readiness")
    for col in ("Topic", "Concept", "Easy Active", "Medium Active", "Study Ready", "Easy Deficit", "Medium Deficit"):
        concept_table.add_column(col)
    for row in sorted(report["concepts"], key=lambda item: (item["topic_id"], item["concept"])):
        concept_table.add_row(
            str(row["topic"]),
            str(row["concept"]),
            str(row["easy_active"]),
            str(row["medium_active"]),
            "yes" if row["study_ready"] else "no",
            str(row["easy_readiness_deficit"]),
            str(row["medium_readiness_deficit"]),
        )
    console.print(concept_table)

    target_table = Table(title="Readiness Threshold vs Active Bank")
    for col in ("Topic", "Concept", "Difficulty", "Threshold", "Active", "Inactive", "Deficit", "Study Ready"):
        target_table.add_column(col)
    for row in sorted(report["targets"], key=lambda item: (item["topic_id"], item["concept"], item["difficulty"])):
        target_table.add_row(
            str(row["topic"]),
            str(row["concept"]),
            str(row["difficulty"]),
            str(row["readiness_threshold"]),
            str(row["active_count"]),
            str(row["legacy_count"]),
            str(row["readiness_deficit"]),
            "yes" if row["study_ready"] else "no",
        )
    console.print(target_table)


def run_report(topic_filter: str | None = None, limit: int | None = None) -> dict:
    report = build_inventory_report(topic_filter=topic_filter, limit=limit)
    render_report(report, topic_filter=topic_filter)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare the current question bank against the active contract and syllabus targets.")
    parser.add_argument("--topic", default=None, help="Optional topic/concept filter.")
    parser.add_argument("--limit", type=int, default=None, help="Cap the number of records processed.")
    args = parser.parse_args(argv)
    run_report(topic_filter=args.topic, limit=args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
