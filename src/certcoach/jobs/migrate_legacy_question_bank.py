from __future__ import annotations

import argparse
import copy
import sys
from datetime import datetime

from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn

from certcoach.core import database
from certcoach.core.content_contract import (
    CONTENT_CONTRACT_VERSION,
    has_invented_topic1_type,
    is_contract_active,
    is_topic1_concept_only,
    normalize_topic1_option_text,
    suggest_topic1_question_text,
)
from certcoach.jobs.nightly_seed_questions import validate_question_quality

console = Console()

EXPLANATION_ISSUE_MARKERS = (
    "missing seven-part headings or content",
    "seven-part explanation sections are too short",
    "seven-part explanation sections need more bullets",
    "missing syntax example code block",
    "syntax example needs a fenced code block",
    "syntax example is too short",
    "syntax example should explicitly say",
    "seven-part explanation is too short",
)

STRUCTURAL_ISSUE_MARKERS = (
    "missing question text",
    "does not have exactly four options",
    "contains blank option text",
    "does not have exactly one correct option",
    "contains placeholder option text",
    "duplicate option text",
    "correct answer does not match any option",
    "contains invented BSON type names",
    "question text contains invented BSON type names",
)


def _clone_question(question: dict) -> dict:
    return copy.deepcopy(question)


def _safe_contract_metadata(source: str, status: str) -> dict[str, object]:
    return {
        "content_contract_version": CONTENT_CONTRACT_VERSION,
        "content_contract_status": status,
        "content_contract_source": source,
    }


def _current_question_text(correct_option_text: str) -> str | None:
    return suggest_topic1_question_text(correct_option_text)


def _repair_topic1_question(question: dict) -> tuple[dict | None, list[str]]:
    candidate = _clone_question(question)
    metadata = dict(candidate.get("metadata", {}) or {})
    issues: list[str] = []
    repair_issues: list[str] = []
    original_question_text = str(candidate.get("question_text", ""))
    original_options = candidate.get("options", []) or []
    has_legacy_vocab = has_invented_topic1_type(original_question_text) or any(
        has_invented_topic1_type(str(opt.get("code_snippet", ""))) for opt in original_options
    )
    options = []

    for opt in original_options:
        updated = dict(opt)
        updated["code_snippet"] = normalize_topic1_option_text(updated.get("code_snippet", ""))
        options.append(updated)
    candidate["options"] = options

    correct_option = next((opt for opt in options if opt.get("is_correct")), None)
    correct_text = str(correct_option.get("code_snippet", "")).strip() if correct_option else ""
    if has_legacy_vocab and correct_text:
        replacement = _current_question_text(correct_text)
        if replacement:
            candidate["question_text"] = replacement
            repair_issues.append("repaired topic 1 question text")

    if has_invented_topic1_type(str(candidate.get("question_text", ""))):
        issues.append("question text still contains invented type names")
        return None, issues
    if any(has_invented_topic1_type(str(opt.get("code_snippet", ""))) for opt in options):
        issues.append("option text still contains invented type names")
        return None, issues

    metadata.update(_safe_contract_metadata("migrate_legacy_question_bank", "migrated"))
    metadata["content_contract_migrated_at"] = datetime.utcnow().isoformat()
    previous_metadata = question.get("metadata", {}) or {}
    metadata["content_contract_previous_status"] = str(previous_metadata.get("content_contract_status", "") or "legacy")
    metadata["content_contract_previous_version"] = previous_metadata.get("content_contract_version")
    candidate["metadata"] = metadata

    ok, quality_issues = validate_question_quality(candidate)
    if not ok:
        issues.extend(quality_issues)
        return None, issues
    return candidate, repair_issues


def _promote_existing_question(question: dict) -> dict:
    updated = _clone_question(question)
    metadata = dict(updated.get("metadata", {}) or {})
    previous_metadata = question.get("metadata", {}) or {}
    previous_status = str(previous_metadata.get("content_contract_status", "") or "legacy")
    previous_version = previous_metadata.get("content_contract_version")
    metadata.update(_safe_contract_metadata("migrate_legacy_question_bank", "migrated"))
    metadata["content_contract_migrated_at"] = datetime.utcnow().isoformat()
    metadata["content_contract_previous_status"] = previous_status
    metadata["content_contract_previous_version"] = previous_version
    updated["metadata"] = metadata
    return updated


def _quarantine_question(question: dict, issues: list[str]) -> dict:
    updated = _clone_question(question)
    metadata = dict(updated.get("metadata", {}) or {})
    previous_metadata = question.get("metadata", {}) or {}
    previous_status = str(previous_metadata.get("content_contract_status", "") or "legacy")
    previous_version = previous_metadata.get("content_contract_version")
    metadata.update(_safe_contract_metadata("migrate_legacy_question_bank", "quarantined"))
    metadata["content_contract_quarantined_at"] = datetime.utcnow().isoformat()
    metadata["content_contract_issues"] = issues
    metadata["content_contract_previous_status"] = previous_status
    metadata["content_contract_previous_version"] = previous_version
    updated["metadata"] = metadata
    return updated


def _mark_needs_question_regeneration(question: dict, issues: list[str]) -> dict:
    updated = _clone_question(question)
    metadata = dict(updated.get("metadata", {}) or {})
    previous_metadata = question.get("metadata", {}) or {}
    previous_status = str(previous_metadata.get("content_contract_status", "") or "legacy")
    previous_version = previous_metadata.get("content_contract_version")
    metadata.update(_safe_contract_metadata("migrate_legacy_question_bank", "needs_question_regeneration"))
    metadata["content_contract_issues"] = issues
    metadata["content_contract_previous_status"] = previous_status
    metadata["content_contract_previous_version"] = previous_version
    updated["metadata"] = metadata
    return updated


def _needs_explanation_repair(quality_issues: list[str]) -> bool:
    return bool(quality_issues) and all(
        any(issue.startswith(marker) for marker in EXPLANATION_ISSUE_MARKERS)
        for issue in quality_issues
    )


def _needs_regeneration(quality_issues: list[str]) -> bool:
    return bool(quality_issues) and any(
        any(issue.startswith(marker) for marker in STRUCTURAL_ISSUE_MARKERS)
        for issue in quality_issues
    )


def _mark_needs_explanation_repair(question: dict, issues: list[str]) -> dict:
    updated = _clone_question(question)
    metadata = dict(updated.get("metadata", {}) or {})
    metadata.update(_safe_contract_metadata("migrate_legacy_question_bank", "needs_explanation_repair"))
    metadata["content_contract_issues"] = issues
    updated["metadata"] = metadata
    return updated


def migrate_question(question: dict) -> tuple[str, dict, list[str]]:
    metadata = question.get("metadata", {}) or {}
    if is_contract_active(question):
        return "skip", question, []
    if str(metadata.get("content_contract_status", "")).strip().lower() == "quarantined":
        return "quarantine", question, list(metadata.get("content_contract_issues", []) or [])

    topic1 = is_topic1_concept_only(metadata, str(question.get("question_text", "")))
    ok, quality_issues = validate_question_quality(question)

    if ok and not topic1:
        return "promote", _promote_existing_question(question), []

    if topic1:
        repaired, repair_issues = _repair_topic1_question(question)
        if repaired:
            return "regenerate", repaired, repair_issues
        combined_issues = list(dict.fromkeys(quality_issues + repair_issues))
        if _needs_explanation_repair(combined_issues):
            return "repair", _mark_needs_explanation_repair(question, combined_issues), combined_issues
        if _needs_regeneration(combined_issues):
            return "regenerate", _mark_needs_question_regeneration(question, combined_issues), combined_issues
        return "quarantine", _quarantine_question(question, combined_issues), combined_issues

    if ok:
        return "promote", _promote_existing_question(question), []
    if _needs_explanation_repair(quality_issues):
        return "repair", _mark_needs_explanation_repair(question, quality_issues), quality_issues
    if _needs_regeneration(quality_issues):
        return "regenerate", _mark_needs_question_regeneration(question, quality_issues), quality_issues
    return "quarantine", _quarantine_question(question, quality_issues), quality_issues


def run_migration(*, dry_run: bool = False, topic_filter: str | None = None, limit: int | None = None) -> dict[str, int]:
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

    console.print("\n[bold cyan]CertCoach Legacy Question Bank Migration[/bold cyan]")
    console.print(f"Loaded questions: [bold]{len(questions)}[/bold]")
    console.print(f"Mode: {'dry-run' if dry_run else 'apply'}")
    if topic_filter:
        console.print(f"Topic filter: [bold]{topic_filter}[/bold]")
    if limit is not None:
        console.print(f"Batch cap: [bold]{limit}[/bold]")
    console.print()

    counts = {"skip": 0, "promote": 0, "repair": 0, "regenerate": 0, "quarantine": 0}

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=34),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
    )

    with progress:
        task_id = progress.add_task("Migrating legacy content", total=len(questions))
        for question in questions:
            action, updated, issues = migrate_question(question)
            counts[action] += 1
            progress.advance(task_id)
            if not dry_run and action in {"promote", "repair", "regenerate", "quarantine"}:
                database.questions_col.replace_one({"_id": question["_id"]}, updated)

    console.print()
    console.print(f"[green]Promoted:[/green] {counts['promote']}")
    console.print(f"[green]Repaired:[/green] {counts['repair']}")
    console.print(f"[green]Regenerated:[/green] {counts['regenerate']}")
    console.print(f"[yellow]Skipped:[/yellow] {counts['skip']}")
    console.print(f"[red]Quarantined:[/red] {counts['quarantine']}")

    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migrate legacy CertCoach question-bank records to the current content contract.")
    parser.add_argument("--topic", default=None, help="Optional topic/concept filter.")
    parser.add_argument("--limit", type=int, default=None, help="Cap the number of records processed.")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without writing to MongoDB.")
    args = parser.parse_args(argv)
    run_migration(dry_run=args.dry_run, topic_filter=args.topic, limit=args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
