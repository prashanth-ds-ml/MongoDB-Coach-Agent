"""Ingest a directly-authored MCQ (written by Claude or a human, not a local
Ollama generation call) through the exact same trust pipeline every other
question goes through: duplicate check, quality gate, deterministic citation
verification, and the self-consistency check.

This exists because the generation step (turning a doc into question text)
and the trust pipeline (deciding whether that question is safe to show a
learner) are separate concerns. `nightly_seed_questions.py` and
`generate_from_doc.py` both call a local Ollama model for the first part and
already reuse the same primitives for the second part; this module skips the
Ollama call and reuses the identical second-part primitives, so an
authored question is held to precisely the same bar. No question is ever
inserted as `confirmed` here -- it always lands at `draft` or `sourced`,
same as everywhere else, and still needs a human confirm (`certcoach-review-questions`).
"""
from __future__ import annotations

import time

from certcoach.core import database, planner
from certcoach.jobs.nightly_seed_questions import (
    LETTERS,
    StyleTarget,
    _load_env,
    _next_question_number,
    _question_needs_syntax_example,
    is_duplicate_question,
    make_question_id,
    question_fingerprint,
    run_generation_pipeline_checks,
    validate_question_quality,
)
from certcoach.core.content_contract import contract_metadata

VALID_STYLE_TYPES = {"Type A", "Type B", "Type C", "Type D"}
VALID_DIFFICULTIES = {"Easy", "Medium"}


def _assemble_explanation(sections: dict, needs_syntax_example: bool) -> str:
    """Assembles the seven-part explanation markdown from authored section
    text, in the exact heading format `repair_explanations.py` already uses,
    so `validate_question_quality`'s heading/length checks apply unchanged."""
    recs = sections.get("practice_recommendations") or []
    rec_bullets = "\n".join(f"- {rec.strip()}" for rec in recs)
    # The quality gate requires this section to explicitly say "not required"
    # (one of a fixed set of markers) whenever the style type doesn't need a
    # syntax example -- any other text there, even a real code example, fails
    # validation. So this is forced, not just a fallback for an empty value.
    if needs_syntax_example:
        syntax_example = sections.get("syntax_example", "").strip()
    else:
        syntax_example = "Not required for this concept."

    return f"""### 1. Correct Answer
{sections.get('correct_answer', '').strip()}

### 2. Why Correct
{sections.get('why_correct', '').strip()}

### 3. Why Other Options Are Wrong
{sections.get('why_wrong', '').strip()}

### 4. Exam Trap
{sections.get('exam_trap', '').strip()}

### 5. Memory Hook
{sections.get('memory_hook', '').strip()}

### 6. Follow-Up Practice Recommendation
{rec_bullets}

### 7. Syntax Example
{syntax_example}"""


def build_authored_question(authored: dict) -> dict:
    """Assembles a full question document from an authored-content dict (see
    module docstring for the expected shape) -- the same document shape
    `generate_weighted_question` builds, minus the LLM call. Does not touch
    the database."""
    topic_id = authored["topic_id"]
    concept = authored["concept"]
    difficulty = authored["difficulty"]
    style_type = authored.get("style_type")
    options_in = authored["options"]
    response_type = authored.get("response_type", "single")

    if difficulty not in VALID_DIFFICULTIES:
        raise ValueError(f"difficulty must be one of {VALID_DIFFICULTIES}, got {difficulty!r}")
    if style_type is not None and style_type not in VALID_STYLE_TYPES:
        raise ValueError(f"style_type must be one of {VALID_STYLE_TYPES}, got {style_type!r}")
    if len(options_in) != 4:
        raise ValueError(f"exactly 4 options are required, got {len(options_in)}")

    topic_item = next((item for item in planner.load_syllabus() if item["id"] == topic_id), None)
    if topic_item is None:
        raise ValueError(f"no syllabus topic with id {topic_id}")
    bank_topic = (topic_item.get("bank_topic_keys") or [topic_item["topic"]])[0]

    target = StyleTarget(
        topic_id=topic_id, topic=topic_item["topic"], bank_topic=bank_topic, concept=concept,
        difficulty=difficulty, style_type=style_type, target_count=1, exam_weight=0.0, concept_weight=0.0,
    )

    correct_indices = {idx for idx, opt in enumerate(options_in) if opt.get("is_correct")}
    if not correct_indices:
        raise ValueError("at least one option must be marked is_correct")
    if response_type == "single" and len(correct_indices) != 1:
        raise ValueError("response_type='single' requires exactly one is_correct option")
    if response_type == "multi" and len(correct_indices) < 2:
        raise ValueError("response_type='multi' requires at least two is_correct options")
    trap_idx = next((idx for idx in range(len(options_in)) if idx not in correct_indices), 0)

    question_text = authored["question_text"]
    fingerprint = question_fingerprint(bank_topic, concept, question_text)
    question_number = _next_question_number(target)
    q_id = make_question_id(target, question_number, fingerprint)

    question = {
        "_id": q_id,
        "citation_quote": authored.get("citation_quote", "").strip(),
        "generation_model": None,
        "metadata": {
            "topic": bank_topic,
            "syllabus_topic": topic_item["topic"],
            "topic_id": topic_id,
            "concept": concept,
            "difficulty": difficulty,
            "question_style": style_type or "",
            "question_style_type": style_type,
            "question_number": question_number,
            "question_fingerprint": fingerprint,
            "exam_weight": 0.0,
            "concept_weight": 0.0,
            "generation_source": "claude_authored",
            "citation_source": authored.get("citation_doc_file", ""),
            "response_type": response_type,
            "num_correct": len(correct_indices),
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            **contract_metadata("claude_authored"),
        },
        "context": {
            "scenario_description": authored.get("scenario_description", ""),
            "database_info": "",
        },
        "question_text": question_text,
        "options": [
            {
                "option_letter": LETTERS[idx],
                "code_snippet": opt["code_snippet"],
                "is_correct": idx in correct_indices,
                "is_trap": idx == trap_idx,
                "feedback": opt.get("feedback", ""),
            }
            for idx, opt in enumerate(options_in)
        ],
        "trap_analysis": authored.get("trap_analysis", ""),
        "citation_source": authored.get("citation_doc_file", ""),
        "global_metrics": {
            "times_seen": 0,
            "times_correct": 0,
            "times_incorrect": 0,
            "average_time_seconds": 0.0,
        },
    }
    question["explanation"] = _assemble_explanation(
        authored.get("explanation_sections", {}),
        _question_needs_syntax_example(question),
    )
    return question, target


def ingest_authored_question(authored: dict) -> dict:
    """Full pipeline for one authored question: build -> duplicate check ->
    quality gate -> insert -> citation verify -> self-consistency -> store
    provenance. Returns a summary dict; never raises for a question that
    simply fails a gate (that's an expected, reportable outcome), only for a
    malformed `authored` dict (see build_authored_question)."""
    question, target = build_authored_question(authored)

    is_dup, dup_reason = is_duplicate_question(question, target)
    if is_dup:
        return {"question_id": question["_id"], "status": "skipped", "reason": f"duplicate: {dup_reason}"}

    is_valid, quality_issues = validate_question_quality(question)
    if not is_valid:
        return {"question_id": question["_id"], "status": "skipped", "reason": f"quality gate failed: {quality_issues}"}

    database.questions_col.insert_one(question)

    _, local_llm_url = _load_env()
    provenance = run_generation_pipeline_checks(
        question,
        citation_doc_file=authored.get("citation_doc_file", ""),
        citation_quote=authored.get("citation_quote", ""),
        local_llm_url=local_llm_url,
        generation_model=None,
    )
    database.questions_col.update_one({"_id": question["_id"]}, {"$set": {"provenance": provenance}})

    return {
        "question_id": question["_id"],
        "status": "inserted",
        "provenance_state": provenance["state"],
        "pipeline_note": provenance["pipeline_note"],
    }


def main(argv: list[str] | None = None) -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Ingest a batch of authored MCQs through the standard trust pipeline (no LLM generation call).")
    parser.add_argument("authored_file", help="Path to a JSON file containing one authored question dict, or a list of them.")
    args = parser.parse_args(argv)

    database.check_connection()

    with open(args.authored_file, encoding="utf-8") as f:
        data = json.load(f)
    batch = data if isinstance(data, list) else [data]

    inserted = sourced = skipped = 0
    for authored in batch:
        result = ingest_authored_question(authored)
        if result["status"] == "skipped":
            skipped += 1
            print(f"  [skip] {result['question_id']}: {result['reason']}")
        else:
            inserted += 1
            if result["provenance_state"] == "sourced":
                sourced += 1
            print(f"  [{result['provenance_state']}] {result['question_id']}: {result['pipeline_note']}")

    print(f"\n{inserted} inserted ({sourced} reached 'sourced'), {skipped} skipped. Nothing is ever auto-confirmed -- review via certcoach-review-questions.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
