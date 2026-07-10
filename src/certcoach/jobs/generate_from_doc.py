"""Generate real, quality-gated questions from a single concept's official
doc(s), section by section, instead of chasing the exam-weighted quantity
target certcoach-seed-nightly works toward.

Journey: reuses inspect_doc.inspect_concept()'s chunked dry-run (per-section
fact extraction + citation verification, proven to lift verified yield ~22x
over flat-truncated context for BSON Data Types) to find verified candidate
facts, picks one per doc section so every part of the doc the learner just
read gets covered, distributes them across the same exam-style taxonomy
nightly_seed_questions.py already uses (Type A: Syntax Selection & Trap
Spotting, Type B: Theory/Constraints/Data Modeling, Type C: Predicting Query
Output, Type D: Troubleshooting/Errors/Performance) weighted the same way for
the topic, and runs each through the same generation + citation +
self-consistency + explanation-repair pipeline nightly_seed_questions.py
uses -- reused directly, not reimplemented, since that logic is
provenance-critical, not orchestration-specific. If this proves out,
nightly_seed_questions.py's quantity-target orchestration becomes
redundant; its generation/persistence primitives would then move to a
shared module rather than staying import-coupled to a file slated for
removal.
"""
from __future__ import annotations

import argparse
import random

from rich.console import Console
from rich.table import Table

from certcoach.core import database
from certcoach.core.config import get_population_source_chars
from certcoach.jobs import inspect_doc
from certcoach.jobs.nightly_seed_questions import (
    StyleTarget,
    _load_env,
    generate_weighted_question,
    is_duplicate_question,
    run_generation_pipeline_checks,
    style_weights_for_topic,
    validate_question_quality,
)

console = Console()

GENERATION_SOURCE = "doc_chunk_seed"


def select_generation_targets(chunks: list[dict], max_questions: int) -> list[dict]:
    """Picks the single strongest (first) verified fact per doc section, in
    doc reading order, capped at max_questions -- one question per section
    the learner actually read, not one question per verified fact (a doc
    like BSON Data Types can yield 60+ verified facts, far more than is
    useful to generate and review in one pass)."""
    selected: list[dict] = []
    for chunk in chunks:
        if not chunk["verified"]:
            continue
        fact = chunk["verified"][0]
        selected.append({
            "chunk_label": chunk["label"],
            "doc_file": chunk["doc_file"],
            "chunk_text": chunk["text"],
            "difficulty": str(fact.get("suggested_difficulty") or "Medium").strip().title(),
            "suggested_style_type": fact.get("suggested_style_type"),
        })
        if len(selected) >= max_questions:
            break
    return selected


def assign_style_types(selected: list[dict], topic_id: int) -> None:
    """Mutates each selected target in place with a style_type -- preferring
    the inspection step's own content-aware suggestion (inspect_doc.py
    already asked the model which Type A-D taxonomy each verified fact best
    supports, and cleared anything outside this topic's allowed set), and
    only falling back to a weighted-random draw from the topic's real
    exam-taxonomy weights when a target has no valid suggestion. Also tags
    each target with style_source ("content" vs "fallback") so callers can
    report how much of the generated set was content-driven vs. random."""
    weights = style_weights_for_topic(topic_id)
    styles = list(weights.keys())
    style_weights = list(weights.values())
    for target in selected:
        suggested = target.get("suggested_style_type")
        if suggested in styles:
            target["style_type"] = suggested
            target["style_source"] = "content"
        else:
            target["style_type"] = random.choices(styles, weights=style_weights, k=1)[0]
            target["style_source"] = "fallback"


def generate_one(
    target: StyleTarget,
    context_text: str,
    citation_source: str,
    local_llm_url: str,
    avoid_questions: list[str],
    max_attempts: int,
) -> tuple[dict | None, str]:
    """Retries generation for one target until it clears the quality/
    duplicate gates or max_attempts is exhausted, mirroring
    nightly_seed_questions.run_weighted_seed's per-slot retry loop."""
    for attempt in range(1, max_attempts + 1):
        question = generate_weighted_question(
            target, context_text, avoid_questions, citation_source,
            generation_source=GENERATION_SOURCE,
        )
        if not question:
            continue

        is_valid, quality_issues = validate_question_quality(question, require_explanation=False)
        if not is_valid:
            avoid_questions.append(question.get("question_text", ""))
            continue

        is_dup, reason = is_duplicate_question(question, target)
        if is_dup:
            avoid_questions.append(question.get("question_text", ""))
            continue

        return question, ""

    return None, f"no valid question after {max_attempts} attempts"


def generate_from_concept(
    topic_id: int,
    concept: str,
    max_questions: int = 8,
    max_attempts: int = 3,
    max_chars: int | None = None,
    progress_callback=None,
) -> dict:
    database.check_connection()
    _, local_llm_url = _load_env()
    max_chars = max_chars if max_chars is not None else get_population_source_chars()

    topic_item = inspect_doc.load_topic_item(topic_id)
    bank_topic = (topic_item.get("bank_topic_keys") or [topic_item["topic"]])[0]

    dry_run = inspect_doc.inspect_concept(topic_id, concept, max_chars)
    selected = select_generation_targets(dry_run["chunks"], max_questions)
    assign_style_types(selected, topic_id)

    inserted: list[dict] = []
    sourced_count = 0
    skipped: list[dict] = []
    avoid_questions: list[str] = []

    for index, item in enumerate(selected, start=1):
        target = StyleTarget(
            topic_id=topic_id,
            topic=topic_item["topic"],
            bank_topic=bank_topic,
            concept=concept,
            difficulty=item["difficulty"],
            style_type=item["style_type"],
            target_count=1,
            exam_weight=0.0,
            concept_weight=0.0,
        )

        question, failure_reason = generate_one(
            target, item["chunk_text"], item["doc_file"], local_llm_url, avoid_questions, max_attempts,
        )
        if not question:
            skipped.append({**item, "reason": failure_reason})
            if progress_callback:
                progress_callback(index, len(selected), item["chunk_label"], None)
            continue

        question["metadata"]["content_contract_status"] = "needs_explanation_repair"
        database.questions_col.insert_one(question)

        from certcoach.jobs.repair_explanations import apply_repair, generate_repair

        repair_candidate = database.questions_col.find_one({"_id": question["_id"]}) or question
        repair = generate_repair(repair_candidate)
        provenance_state = "draft"
        if repair:
            apply_repair(repair_candidate, repair)
            repaired_question = database.questions_col.find_one({"_id": question["_id"]}) or repair_candidate
            provenance = run_generation_pipeline_checks(
                repaired_question,
                citation_doc_file=item["doc_file"],
                citation_quote=repaired_question.get("citation_quote", ""),
                local_llm_url=local_llm_url,
                generation_model=repaired_question.get("generation_model"),
            )
            database.questions_col.update_one({"_id": repaired_question["_id"]}, {"$set": {"provenance": provenance}})
            provenance_state = provenance["state"]
            if provenance_state == "sourced":
                sourced_count += 1

        inserted.append({**item, "question_id": question["_id"], "provenance_state": provenance_state})
        if progress_callback:
            progress_callback(index, len(selected), item["chunk_label"], provenance_state)

    return {
        "topic_id": topic_id,
        "concept": concept,
        "sections_with_verified_facts": len([c for c in dry_run["chunks"] if c["verified"]]),
        "selected_count": len(selected),
        "content_aware_style_count": sum(1 for item in selected if item.get("style_source") == "content"),
        "fallback_style_count": sum(1 for item in selected if item.get("style_source") == "fallback"),
        "inserted": inserted,
        "skipped": skipped,
        "sourced_count": sourced_count,
    }


def print_summary(result: dict) -> None:
    table = Table(title=f"Doc-chunk generation: Topic {result['topic_id']} -> {result['concept']}")
    table.add_column("Metric")
    table.add_column("Count", justify="right")
    table.add_row("Doc sections with verified facts", str(result["sections_with_verified_facts"]))
    table.add_row("Sections selected for generation", str(result["selected_count"]))
    table.add_row("  -- style from inspection (content-aware)", str(result["content_aware_style_count"]))
    table.add_row("  -- style from weighted-random fallback", str(result["fallback_style_count"]))
    table.add_row("Inserted", str(len(result["inserted"])))
    table.add_row("Reached 'sourced' (citation + self-consistency both passed)", str(result["sourced_count"]))
    table.add_row("Skipped (no valid question after retries)", str(len(result["skipped"])))
    console.print(table)

    if result["inserted"]:
        breakdown = Table(title="Inserted by section / style / provenance state")
        breakdown.add_column("Section")
        breakdown.add_column("Style")
        breakdown.add_column("Difficulty")
        breakdown.add_column("Provenance")
        for item in result["inserted"]:
            breakdown.add_row(item["chunk_label"], item["style_type"], item["difficulty"], item["provenance_state"])
        console.print(breakdown)

    for item in result["skipped"]:
        console.print(f"[yellow]Skipped {item['chunk_label']}: {item['reason']}[/yellow]")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate real questions from one concept's official doc, section by section, "
                     "taxonomy-weighted -- not driven by the exam-weighted quantity target."
    )
    parser.add_argument("--topic", type=int, required=True, help="Syllabus topic id.")
    parser.add_argument("--concept", required=True, help="Exact syllabus concept name.")
    parser.add_argument("--max-questions", type=int, default=8, help="Cap on questions generated this run.")
    parser.add_argument("--max-attempts", type=int, default=3, help="Retry attempts per selected section.")
    args = parser.parse_args(argv)

    def report_progress(index: int, total: int, label: str, provenance_state: str | None) -> None:
        status = provenance_state or "skipped"
        console.print(f"  [dim]{index}/{total} {label}: {status}[/dim]")

    try:
        result = generate_from_concept(
            args.topic, args.concept, args.max_questions, args.max_attempts,
            progress_callback=report_progress,
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    print_summary(result)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
