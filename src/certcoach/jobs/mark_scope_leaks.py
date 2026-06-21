from __future__ import annotations

import argparse
from datetime import datetime

from certcoach.core import database, planner
from certcoach.core.bank_state import matches_concept_filter, matches_topic_filter
from certcoach.core.content_contract import CONTENT_CONTRACT_VERSION


def _normalize_scope_term(value: object) -> str:
    return "".join(ch for ch in str(value or "").strip().lower() if ch.isalnum() or ch in {"$", "_"})


def _normalize_question_text(question: dict) -> str:
    meta = question.get("metadata", {}) or {}
    parts = (
        question.get("question_text", ""),
        meta.get("topic", ""),
        meta.get("syllabus_topic", ""),
        meta.get("concept", ""),
        " ".join(str(opt.get("code_snippet", "")) for opt in (question.get("options", []) or [])),
    )
    return _normalize_scope_term(" ".join(str(part or "") for part in parts))


def _future_concepts_for_scope(topic_id: int, concept: str) -> list[str]:
    syllabus = planner.load_syllabus()
    topic_item = next((item for item in syllabus if int(item["id"]) == topic_id), None)
    if not topic_item:
        return []

    subtopics = list(topic_item.get("subtopics", []))
    future_same_topic: list[str] = []
    if concept in subtopics:
        future_same_topic = subtopics[subtopics.index(concept) + 1 :]

    future_later_topics = [
        subtopic
        for item in syllabus
        if int(item["id"]) > topic_id
        for subtopic in item.get("subtopics", [])
    ]
    return future_same_topic + future_later_topics


def _topic_label(topic_id: int) -> str:
    syllabus = planner.load_syllabus()
    topic_item = next((item for item in syllabus if int(item["id"]) == topic_id), None)
    return str(topic_item["topic"]) if topic_item else ""


def audit_scope_leaks(
    *,
    topic_filter: str | None = None,
    concept_filter: str | None = None,
    apply: bool = False,
) -> dict[str, int]:
    database.check_connection()

    query: dict[str, object] = {"metadata.content_contract_version": {"$gte": CONTENT_CONTRACT_VERSION}}
    if topic_filter:
        topic_norm = topic_filter.strip()
        if topic_norm.isdigit():
            query["metadata.topic_id"] = int(topic_norm)
        else:
            query["$or"] = [
                {"metadata.topic": topic_norm},
                {"metadata.syllabus_topic": topic_norm},
            ]

    questions = list(database.questions_col.find(query))
    topic_leaks = 0
    normalized = 0
    skipped = 0

    for question in questions:
        if not matches_topic_filter(question, topic_filter):
            continue
        if not matches_concept_filter(question, concept_filter):
            continue

        meta = dict(question.get("metadata", {}) or {})
        topic_id = meta.get("topic_id")
        concept = str(meta.get("concept", "")).strip()
        if not isinstance(topic_id, int) or not concept:
            skipped += 1
            continue

        future_concepts = [_normalize_scope_term(name) for name in _future_concepts_for_scope(topic_id, concept)]
        text = _normalize_question_text(question)
        hits = sorted({name for name in future_concepts if name and name in text})

        updates: dict[str, object] = {}
        canonical_topic = _topic_label(topic_id)
        if canonical_topic and meta.get("topic") != canonical_topic:
            updates["metadata.topic"] = canonical_topic
            updates["metadata.syllabus_topic"] = canonical_topic
            normalized += 1

        if hits:
            topic_leaks += 1
            updates["metadata.content_contract_version"] = CONTENT_CONTRACT_VERSION
            updates["metadata.content_contract_status"] = "quarantined"
            updates["metadata.content_contract_source"] = "mark_scope_leaks"
            updates["metadata.content_contract_quarantined_at"] = datetime.utcnow().isoformat()
            updates["metadata.content_contract_issues"] = list(
                dict.fromkeys(
                    list(meta.get("content_contract_issues", []) or [])
                    + [f"scope leak: references future scope ({', '.join(hits)})"]
                )
            )

        if apply and updates:
            database.questions_col.update_one({"_id": question["_id"]}, {"$set": updates})

    return {"topic_leaks": topic_leaks, "normalized": normalized, "skipped": skipped}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit and quarantine scope leaks for a topic/concept.")
    parser.add_argument("--topic", default=None, help="Exact topic id or topic label to audit.")
    parser.add_argument("--concept", default=None, help="Exact concept to audit.")
    parser.add_argument("--apply", action="store_true", help="Persist leak tagging / metadata normalization.")
    args = parser.parse_args(argv)

    result = audit_scope_leaks(topic_filter=args.topic, concept_filter=args.concept, apply=args.apply)
    mode = "applied" if args.apply else "dry-run"
    print(f"Mode: {mode}")
    print(f"Topic leaks: {result['topic_leaks']}")
    print(f"Normalized: {result['normalized']}")
    print(f"Skipped: {result['skipped']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
