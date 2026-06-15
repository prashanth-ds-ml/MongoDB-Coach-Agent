from __future__ import annotations

import argparse
import sys
from collections import Counter

from rich.console import Console
from rich.table import Table

from certcoach.core import database, planner
from certcoach.core.content_contract import is_contract_active
from certcoach.core.question_targets import build_weighted_targets
from certcoach.jobs.migrate_legacy_question_bank import migrate_question

console = Console()


def _target_key(target: dict | object) -> tuple:
    return (
        getattr(target, "topic_id", None),
        getattr(target, "concept", ""),
        getattr(target, "difficulty", ""),
    )


def _question_key(question: dict) -> tuple:
    metadata = question.get("metadata", {}) or {}
    return (
        metadata.get("topic_id"),
        str(metadata.get("concept") or ""),
        str(metadata.get("difficulty") or ""),
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
    target_counts = Counter(_question_key(q) for q in questions if is_contract_active(q))
    legacy_counts = Counter(_question_key(q) for q in questions if not is_contract_active(q))
    repair_counts = Counter()

    target_rows = []
    needs_explanation_repair = 0
    quarantined = 0
    migratable = 0
    active_records = 0

    for question in questions:
        if is_contract_active(question):
            active_records += 1
            continue
        action, classified, _ = migrate_question(question)
        classified_status = str(classified.get("metadata", {}).get("content_contract_status", "")).strip().lower()
        if classified_status == "needs_explanation_repair":
            needs_explanation_repair += 1
            repair_counts[_question_key(classified)] += 1
        elif action == "quarantine":
            quarantined += 1
        elif action in {"promote", "repair"}:
            migratable += 1

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
        })
        summary["repair_pending"] += repair_counts.get((row["topic_id"], row["concept"], row["difficulty"]), 0)
        if row["difficulty"] == "Easy":
            summary["easy_active"] = row["active_count"]
            summary["easy_readiness_deficit"] = row["readiness_deficit"]
        elif row["difficulty"] == "Medium":
            summary["medium_active"] = row["active_count"]
            summary["medium_readiness_deficit"] = row["readiness_deficit"]

    for summary in concepts.values():
        summary["study_ready"] = summary["easy_active"] >= 3 and summary["medium_active"] >= 2
        concept_rows.append(summary)

    return {
        "total": len(questions),
        "active": active_records,
        "inactive": len(questions) - active_records,
        "needs_explanation_repair": needs_explanation_repair,
        "migratable": migratable,
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
    console.print(f"Migratable without LLM repair: [bold green]{report['migratable']}[/bold green]")
    console.print(f"Quarantine candidates: [bold red]{report['quarantined']}[/bold red]")
    console.print()

    summary = Table(title="Bank Status Comparison")
    for col in ("Metric", "Count"):
        summary.add_column(col)
    summary.add_row("Active", str(report["active"]))
    summary.add_row("Inactive", str(report["inactive"]))
    summary.add_row("Needs Explanation Repair", str(report["needs_explanation_repair"]))
    summary.add_row("Migratable", str(report["migratable"]))
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
