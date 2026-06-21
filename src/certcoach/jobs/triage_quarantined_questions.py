from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone

from certcoach.core import database, planner
from certcoach.core.bank_state import matches_concept_filter, matches_topic_filter


EXTRA_ALIASES: dict[str, tuple[str, ...]] = {
    "BSON Data Types": ("bson type", "bson data type", "decimal128", "binary data"),
    "Document structure": ("document structure", "field value pair", "nested document", "embed a document"),
    "Collections vs Tables": ("collection vs table", "collections and tables", "relational table"),
    "insertOne()": ("insertone", "insert_one", "insert a single document", "inserting a single document"),
    "insertMany()": ("insertmany", "insert_many", "insert multiple documents", "inserting multiple documents"),
    "_id and ObjectId": ("objectid", "object id", "unique document identifier"),
    "find()": (".find(", " find method", "query documents"),
    "findOne()": ("findone", "find_one", "single matching document"),
    "Projections": ("projection document", "project fields", "include fields", "exclude fields"),
    "Cursors": ("cursor", "iterate query results"),
    "sort/limit/skip": (".sort(", ".limit(", ".skip(", "sort limit skip"),
    "countDocuments()": ("countdocuments", "count_documents"),
    "replaceOne()": (
        "replaceone",
        "replace_one",
        "replacement document",
        "completely replace",
        "entire document",
    ),
    "updateOne()": ("updateone", "update_one"),
    "updateMany()": ("updatemany", "update_many", "update multiple documents", "updates multiple documents"),
    "findAndModify": ("findandmodify", "find_and_modify"),
    "deleteOne()": ("deleteone", "delete_one"),
    "deleteMany()": ("deletemany", "delete_many"),
    "Comparison ($eq, $gt, $lt, $in, $nin)": ("$eq", "$gt", "$gte", "$lt", "$lte", "$in", "$nin"),
    "Logical ($and, $or, $not, $nor)": ("$and", "$or", "$not", "$nor"),
    "Element ($exists, $type)": ("$exists", "$type"),
    "Atlas Search query basics": ("$search", "atlas search query"),
    "$elemMatch": ("$elemmatch",),
    "dot notation": ("dot notation", "embedded field path"),
    "Array size queries": ("$size", "array size"),
    "$match": ("$match",),
    "$group": ("$group",),
    "$project": ("$project",),
    "$sort": ("$sort",),
    "$limit": ("$limit",),
    "$lookup": ("$lookup",),
    "$out": ("$out",),
    "$unwind": ("$unwind",),
    "$addFields": ("$addfields", "$set stage"),
    "Single field indexes": ("single field index", "createindex"),
    "Compound indexes": ("compound index", "compound key index"),
    "Multikey indexes": ("multikey index",),
    "Atlas Search indexes": ("atlas search index", "search indexes"),
    "explain()": ("explain(", "explain plan", "executionstats"),
    "COLLSCAN vs IXSCAN": ("collscan", "ixscan"),
    "Embedding vs Referencing": ("embedding vs referencing", "embed or reference", "embedded data"),
    "Anti-patterns": ("anti-pattern", "antipattern", "unbounded array"),
    "One-to-Many relationships": ("one-to-many", "one to many"),
    "PyMongo purpose": ("what is pymongo", "purpose of pymongo", "pymongo is the python driver"),
    "Connection strings and URI components": ("connection string", "mongodb uri", "mongodb+srv"),
    "MongoClient": ("mongoclient",),
    "Connection pooling": ("connection pool", "pool_size", "maxpoolsize"),
    "CRUD with PyMongo": ("pymongo crud",),
    "Aggregation with PyMongo": ("aggregate(", "pymongo aggregation"),
    "Load Atlas Sample Dataset": ("load sample dataset", "sample dataset"),
    "Data Explorer document lookup": ("data explorer", "find a document in atlas"),
    "Atlas Search queries": ("atlas search query", "$search"),
}

GENERIC_ALIASES = {
    "find",
    "sort",
    "limit",
    "skip",
    "match",
    "group",
    "project",
    "out",
    "type",
}

STRONG_ALIASES = {
    "insertone",
    "insert_one",
    "insertmany",
    "insert_many",
    "findone",
    "find_one",
    "countdocuments",
    "count_documents",
    "replaceone",
    "replace_one",
    "updateone",
    "update_one",
    "updatemany",
    "update_many",
    "findandmodify",
    "find_and_modify",
    "deleteone",
    "delete_one",
    "deletemany",
    "delete_many",
    "mongoclient",
}


@dataclass(frozen=True)
class Classification:
    status: str
    topic_id: int | None
    topic: str
    concept: str
    score: int
    margin: int
    evidence: tuple[str, ...]
    reason: str


def _normalize(value: object) -> str:
    text = str(value or "").casefold()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _correct_text(question: dict) -> str:
    return " ".join(
        str(option.get("code_snippet", ""))
        for option in (question.get("options", []) or [])
        if option.get("is_correct")
    )


def _incorrect_text(question: dict) -> str:
    return " ".join(
        str(option.get("code_snippet", ""))
        for option in (question.get("options", []) or [])
        if not option.get("is_correct")
    )


def _concept_aliases(concept: str) -> tuple[str, ...]:
    aliases = set(EXTRA_ALIASES.get(concept, ()))
    normalized = _normalize(concept)
    aliases.add(normalized)
    aliases.add(normalized.replace("()", ""))
    aliases.discard("")
    return tuple(sorted(aliases, key=len, reverse=True))


def _alias_present(alias: str, text: str) -> bool:
    alias = _normalize(alias)
    if not alias or alias in GENERIC_ALIASES:
        return False
    if alias.startswith("$") or any(char in alias for char in "._+("):
        return alias in text
    return re.search(rf"(?<![\w$]){re.escape(alias)}(?![\w])", text) is not None


def _evidence_weight(alias: str, source: str) -> int:
    normalized = _normalize(alias)
    base = {"stem": 12, "correct": 7, "distractor": 1, "explanation": 1}[source]
    compact = normalized.replace("()", "")
    if compact in STRONG_ALIASES:
        return base * 2
    if normalized in {"objectid", "object id", "unique document identifier"}:
        return max(1, base - 2)
    return base


def classify_question(question: dict, syllabus: list[dict] | None = None) -> Classification:
    syllabus = syllabus or planner.load_syllabus()
    stem = _normalize(question.get("question_text", ""))
    correct = _normalize(_correct_text(question))
    incorrect = _normalize(_incorrect_text(question))
    explanation = _normalize(question.get("explanation", ""))

    if not stem and not correct:
        return Classification(
            "misc",
            None,
            "",
            "",
            0,
            0,
            (),
            "insufficient question and correct-answer content",
        )

    candidates: list[tuple[int, int, str, str, tuple[str, ...]]] = []
    for topic in syllabus:
        for concept in topic.get("subtopics", []):
            score = 0
            evidence: list[str] = []
            for alias in _concept_aliases(concept):
                if _alias_present(alias, stem):
                    score += _evidence_weight(alias, "stem")
                    evidence.append(f"stem:{alias}")
                if _alias_present(alias, correct):
                    score += _evidence_weight(alias, "correct")
                    evidence.append(f"correct:{alias}")
                if _alias_present(alias, incorrect):
                    score += _evidence_weight(alias, "distractor")
                    evidence.append(f"distractor:{alias}")
                if _alias_present(alias, explanation):
                    score += _evidence_weight(alias, "explanation")
                    evidence.append(f"explanation:{alias}")
            if score:
                candidates.append(
                    (score, int(topic["id"]), str(topic["topic"]), str(concept), tuple(dict.fromkeys(evidence)))
                )

    candidates.sort(key=lambda item: (-item[0], item[1], item[3]))
    if not candidates:
        return Classification("misc", None, "", "", 0, 0, (), "no canonical syllabus evidence")

    best = candidates[0]
    runner_up_score = candidates[1][0] if len(candidates) > 1 else 0
    margin = best[0] - runner_up_score
    explicit_primary = any(item.startswith(("stem:", "correct:")) for item in best[4])
    if best[0] >= 7 and explicit_primary and margin >= 4:
        status = "mapped"
        reason = "high-confidence canonical match"
    else:
        status = "ambiguous"
        reason = "candidate scores are too weak or too close"
    return Classification(status, best[1], best[2], best[3], best[0], margin, best[4], reason)


def _syllabus_order(classification: Classification, syllabus: list[dict]) -> tuple[int, int]:
    if classification.topic_id is None:
        return (len(syllabus), 10_000)
    topic_pos = next(
        (index for index, topic in enumerate(syllabus) if int(topic["id"]) == classification.topic_id),
        len(syllabus),
    )
    topic = next((topic for topic in syllabus if int(topic["id"]) == classification.topic_id), {})
    concept_pos = next(
        (index for index, concept in enumerate(topic.get("subtopics", [])) if concept == classification.concept),
        10_000,
    )
    return topic_pos, concept_pos


def _topic_matches(question: dict, topic_filter: str | None) -> bool:
    return matches_topic_filter(question, topic_filter)


def _concept_matches(question: dict, concept_filter: str | None) -> bool:
    return matches_concept_filter(question, concept_filter)


def run_triage(
    *,
    apply: bool = False,
    limit: int | None = None,
    topic_filter: str | None = None,
    concept_filter: str | None = None,
) -> dict[str, int]:
    database.check_connection()
    syllabus = planner.load_syllabus()
    questions = list(database.questions_col.find({"metadata.content_contract_status": "quarantined"}))
    classified = [
        (question, classify_question(question, syllabus))
        for question in questions
        if _topic_matches(question, topic_filter) and _concept_matches(question, concept_filter)
    ]
    classified.sort(key=lambda item: (*_syllabus_order(item[1], syllabus), str(item[0].get("_id", ""))))
    if limit is not None:
        classified = classified[:limit]

    counts = Counter(classification.status for _, classification in classified)
    for question, classification in classified:
        current = question.get("metadata", {}) or {}
        target = (
            f"T{classification.topic_id} | {classification.concept}"
            if classification.topic_id is not None
            else "-"
        )
        print(
            f"{question.get('_id')} | {classification.status} | {target} | "
            f"score {classification.score} margin {classification.margin} | {classification.reason}"
        )
        if not apply:
            continue

        now = datetime.now(timezone.utc).isoformat()
        updates: dict[str, object] = {
            "metadata.quarantine_triage_status": classification.status,
            "metadata.quarantine_triage_reason": classification.reason,
            "metadata.quarantine_triage_score": classification.score,
            "metadata.quarantine_triage_margin": classification.margin,
            "metadata.quarantine_triage_evidence": list(classification.evidence),
            "metadata.quarantine_triaged_at": now,
        }
        if classification.status == "mapped":
            updates.update(
                {
                    "metadata.topic_id": classification.topic_id,
                    "metadata.topic": classification.topic,
                    "metadata.syllabus_topic": classification.topic,
                    "metadata.concept": classification.concept,
                    "metadata.quarantine_repair_disposition": "pending_repair",
                }
            )
        elif classification.status == "misc":
            updates["metadata.quarantine_repair_disposition"] = "keep_aside_misc"
        else:
            updates["metadata.quarantine_repair_disposition"] = "needs_manual_classification"
        database.questions_col.update_one({"_id": question["_id"]}, {"$set": updates})

    print(
        f"Summary | total {len(classified)} | mapped {counts['mapped']} | "
        f"ambiguous {counts['ambiguous']} | misc {counts['misc']} | mode {'apply' if apply else 'dry-run'}"
    )
    return {
        "total": len(classified),
        "mapped": counts["mapped"],
        "ambiguous": counts["ambiguous"],
        "misc": counts["misc"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Classify quarantined questions into canonical syllabus scopes without activating them."
    )
    parser.add_argument("--apply", action="store_true", help="Persist triage labels and high-confidence mappings.")
    parser.add_argument("--limit", type=int, default=None, help="Process at most this many records.")
    parser.add_argument("--topic", default=None, help="Filter quarantined questions to a topic id/name/bank topic.")
    parser.add_argument("--concept", default=None, help="Filter quarantined questions to an exact syllabus concept.")
    args = parser.parse_args(argv)
    run_triage(apply=args.apply, limit=args.limit, topic_filter=args.topic, concept_filter=args.concept)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
