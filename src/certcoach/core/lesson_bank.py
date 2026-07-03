"""Stored lesson artifacts and concept-scoped lesson prebuild helpers."""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone

from certcoach.core import database, planner
from certcoach.core.content_contract import CONTENT_CONTRACT_VERSION
from certcoach.core.persona import CoachPersona, clean_lesson_explanation

LESSON_CONTRACT_VERSION = 1
LESSON_HEADINGS = [
    "### 1. Core Concept",
    "### 2. Level-Based Breakdown",
    "### 3. Syntax & Code Examples",
    "### 4. Exam Radar",
    "### 5. Micro-Challenge",
    "### 6. 30-Second Recall",
]


@dataclass(frozen=True)
class LessonTarget:
    topic_id: int
    topic: str
    concept: str
    md_files: list[str]


def get_first_lesson_target() -> LessonTarget:
    syllabus = planner.load_syllabus()
    if not syllabus:
        raise ValueError("Syllabus is empty.")

    first_topic = syllabus[0]
    first_concept = first_topic.get("subtopics", [first_topic["topic"]])[0]
    return LessonTarget(
        topic_id=int(first_topic["id"]),
        topic=first_topic["topic"],
        concept=first_concept,
        md_files=list(first_topic.get("md_files", [])),
    )


def resolve_lesson_target(topic_id: int | None = None, concept: str | None = None) -> LessonTarget:
    syllabus = planner.load_syllabus()
    if topic_id is None:
        target = get_first_lesson_target()
        if concept and concept != target.concept:
            raise ValueError("Concept override requires an explicit topic_id.")
        return target

    topic_item = next((item for item in syllabus if int(item["id"]) == int(topic_id)), None)
    if not topic_item:
        raise ValueError(f"Unknown topic_id: {topic_id}")

    subtopics = topic_item.get("subtopics", [])
    resolved_concept = concept or (subtopics[0] if subtopics else topic_item["topic"])
    if subtopics and resolved_concept not in subtopics:
        raise ValueError(f"Concept '{resolved_concept}' is not part of Topic {topic_id}.")

    return LessonTarget(
        topic_id=int(topic_item["id"]),
        topic=topic_item["topic"],
        concept=resolved_concept,
        md_files=list(topic_item.get("md_files", [])),
    )


def build_lesson_source_bundle(target: LessonTarget) -> dict:
    prioritized_files = planner.prioritize_md_files(target.md_files, target.concept)
    source_files = [
        filename for filename in prioritized_files
        if planner.score_md_file_for_concept(filename, target.concept) > 0
    ]
    source_files = (source_files or prioritized_files[:2])[:3]

    md_context = planner.load_md_context(target.md_files, prioritize_concept=target.concept)
    weak_focus_context = planner.load_topic_benchmark_focus(target.topic_id, target.concept)
    benchmark_context = planner.load_topic_benchmark_context(target.topic_id, target.concept)
    combined_context = "\n\n---\n\n".join(
        part for part in (weak_focus_context, md_context, benchmark_context)
        if isinstance(part, str) and part.strip()
    )

    return {
        "topic_id": target.topic_id,
        "topic": target.topic,
        "concept": target.concept,
        "source_files": source_files,
        "md_context": combined_context or md_context,
        "benchmark_included": bool(weak_focus_context or benchmark_context),
    }


def _contains_forbidden_micro_content(micro_text: str) -> bool:
    lowered = micro_text.lower()
    forbidden_markers = (
        "correct answer",
        "answer:",
        "corrected answer",
        "hint:",
        "solution:",
        "worked solution",
        "example response",
        "explanation:",
    )
    return any(marker in lowered for marker in forbidden_markers)


def _validate_topic1_scope(cleaned_markdown: str, concept: str) -> list[str]:
    issues: list[str] = []
    lowered = cleaned_markdown.lower()

    banned_patterns = {
        r"\binsertone\s*\(": "CRUD write method leak: insertOne()",
        r"\binsertmany\s*\(": "CRUD write method leak: insertMany()",
        r"\bfindone\s*\(": "CRUD read method leak: findOne()",
        r"\bfind\s*\(": "CRUD read method leak: find()",
        r"\bupdateone\s*\(": "CRUD update method leak: updateOne()",
        r"\bupdatemany\s*\(": "CRUD update method leak: updateMany()",
        r"\breplaceone\s*\(": "CRUD update method leak: replaceOne()",
        r"\bdeletemany\s*\(": "CRUD delete method leak: deleteMany()",
        r"\bdeleteone\s*\(": "CRUD delete method leak: deleteOne()",
        r"\baggregate\s*\(": "Aggregation leak: aggregate()",
        r"\$project\b": "Aggregation/query operator leak: $project",
        r"\$addfields\b": "Aggregation operator leak: $addFields",
        r"\$\[\]": "Update positional operator leak: $[]",
        r"\$type\b": "Query operator leak: $type",
        r"\$set\b": "Update operator leak: $set",
        r"\$push\b": "Update operator leak: $push",
        r"\$inc\b": "Update operator leak: $inc",
        r"\$unset\b": "Update operator leak: $unset",
        r"\batlas\b": "Platform leak: Atlas",
        r"\bdata explorer\b": "Platform leak: Data Explorer",
        r"\bdot notation\b": "Future concept leak: dot notation",
    }

    for pattern, issue in banned_patterns.items():
        if re.search(pattern, lowered):
            issues.append(issue)

    if concept == "Document structure":
        extra_patterns = {
            r"\bquery\b": "Future workflow leak: query",
            r"\bqueries\b": "Future workflow leak: queries",
            r"\bprojection\b": "Future concept leak: projection",
            r"\bpositional operator\b": "Future concept leak: positional operator",
        }
        for pattern, issue in extra_patterns.items():
            if re.search(pattern, lowered):
                issues.append(issue)

    deduped: list[str] = []
    for issue in issues:
        if issue not in deduped:
            deduped.append(issue)
    return deduped


def _extract_section_body(lesson_markdown: str, heading: str) -> str:
    if not lesson_markdown.strip():
        return ""
    heading_pattern = re.escape(heading)
    later_headings = [re.escape(item) for item in LESSON_HEADINGS if item != heading]
    tail_pattern = "|".join(later_headings)
    match = re.search(
        rf"{heading_pattern}\s*(.*?)(?=(?:{tail_pattern})|\Z)",
        lesson_markdown,
        flags=re.DOTALL,
    )
    if not match:
        return ""
    return match.group(1).strip()


def _sanitize_document_structure_lesson(lesson_markdown: str) -> str:
    cleaned_lines: list[str] = []
    for line in lesson_markdown.splitlines():
        lowered = line.lower()
        if "dot notation" in lowered:
            continue
        if "query" in lowered:
            continue
        if "queries" in lowered:
            continue
        if "query execution" in lowered:
            continue
        if "queries may reorder fields" in lowered:
            continue
        if "inconsistent query results" in lowered:
            continue
        if "projection" in lowered:
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()


def _sanitize_bson_data_types_lesson(lesson_markdown: str) -> str:
    cleaned = lesson_markdown
    cleaned = cleaned.replace("db.myCollection.insertOne({", "{")
    cleaned = cleaned.replace("db.myCollection.insertOne( {", "{")
    cleaned = cleaned.replace("});", "}")
    cleaned = cleaned.replace("} );", "}")
    
    cleaned_lines = []
    for line in cleaned.splitlines():
        lowered = line.lower()
        if "insertone" in lowered:
            if "db." in lowered:
                continue
            line = line.replace("insertOne()", "document creation")
            line = line.replace("insertOne", "document insertion")
        cleaned_lines.append(line)
        
    return "\n".join(cleaned_lines).strip()


def _sanitize_collections_vs_tables_lesson(lesson_markdown: str) -> str:
    cleaned_lines: list[str] = []
    for line in lesson_markdown.splitlines():
        lowered = line.lower()
        if "insertone" in lowered:
            continue
        if "crud" in lowered:
            continue
        if "query syntax" in lowered:
            continue
        if "projection" in lowered:
            continue
        if "dot notation" in lowered:
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()


def _assemble_lesson(sections: dict[str, str]) -> str:
    parts = []
    for heading in LESSON_HEADINGS:
        body = sections.get(heading, "").strip()
        parts.append(f"{heading}\n{body}".rstrip())
    return "\n\n".join(parts).strip()


def _repair_lesson_by_sections(
    coach: CoachPersona,
    topic: str,
    concept: str,
    md_context: str,
    draft_markdown: str,
) -> str:
    sections: dict[str, str] = {
        heading: _extract_section_body(draft_markdown, heading)
        for heading in LESSON_HEADINGS
    }

    for heading in LESSON_HEADINGS:
        body = sections.get(heading, "").strip()
        if body:
            continue
        partial_lesson = _assemble_lesson(sections)
        generated_body = coach.generate_lesson_section(
            topic,
            concept,
            md_context,
            heading,
            partial_lesson=partial_lesson,
        )
        generated_body = clean_lesson_explanation(generated_body)
        for known_heading in LESSON_HEADINGS:
            generated_body = generated_body.replace(known_heading, "").strip()
        sections[heading] = generated_body.strip()

    return _assemble_lesson(sections)


def _section_has_topic1_scope_leak(section_body: str, concept: str) -> bool:
    section_text = (section_body or "").lower()
    issue_markers = [
        "insertone(",
        "insertmany(",
        "findone(",
        "find(",
        "updateone(",
        "updatemany(",
        "replaceone(",
        "deleteone(",
        "deletemany(",
        "$project",
        "$addfields",
        "$[]",
        "$type",
        "$set",
        "$push",
        "$inc",
        "$unset",
        "atlas",
        "data explorer",
        "dot notation",
    ]
    if any(marker in section_text for marker in issue_markers):
        return True
    if concept == "Document structure" and re.search(r"\bquery\b|\bqueries\b", section_text):
        return True
    return False


def _regenerate_leaky_topic1_sections(
    coach: CoachPersona,
    topic: str,
    concept: str,
    md_context: str,
    draft_markdown: str,
) -> str:
    sections: dict[str, str] = {
        heading: _extract_section_body(draft_markdown, heading)
        for heading in LESSON_HEADINGS
    }

    for heading in LESSON_HEADINGS:
        body = sections.get(heading, "").strip()
        if not _section_has_topic1_scope_leak(body, concept):
            continue
        sections[heading] = ""
        partial_lesson = _assemble_lesson(sections)
        regenerated_body = coach.generate_lesson_section(
            topic,
            concept,
            md_context,
            heading,
            partial_lesson=partial_lesson,
        )
        regenerated_body = clean_lesson_explanation(regenerated_body)
        for known_heading in LESSON_HEADINGS:
            regenerated_body = regenerated_body.replace(known_heading, "").strip()
        sections[heading] = regenerated_body.strip()

    return _assemble_lesson(sections)


def _repair_invalid_sections(
    coach: CoachPersona,
    topic: str,
    concept: str,
    md_context: str,
    draft_markdown: str,
    validation_issues: list[str],
) -> str:
    sections: dict[str, str] = {
        heading: _extract_section_body(draft_markdown, heading)
        for heading in LESSON_HEADINGS
    }

    headings_to_regenerate: list[str] = []
    if any("30-Second Recall must end with 3-5 recall bullets" in issue for issue in validation_issues):
        headings_to_regenerate.append("### 6. 30-Second Recall")
    if any("micro-challenge is empty" in issue for issue in validation_issues):
        headings_to_regenerate.append("### 5. Micro-Challenge")

    for heading in headings_to_regenerate:
        sections[heading] = ""
        partial_lesson = _assemble_lesson(sections)
        regenerated_body = coach.generate_lesson_section(
            topic,
            concept,
            md_context,
            heading,
            partial_lesson=partial_lesson,
        )
        regenerated_body = clean_lesson_explanation(regenerated_body)
        for known_heading in LESSON_HEADINGS:
            regenerated_body = regenerated_body.replace(known_heading, "").strip()
        sections[heading] = regenerated_body.strip()

    return _assemble_lesson(sections)


def _fallback_recall_body(topic: str, concept: str) -> str:
    concept_key = concept.strip().lower()
    fallbacks = {
        "bson data types": (
            "- BSON stores typed values, not plain JSON text.\n"
            "- ObjectId, Date, NumberLong, and Decimal128 are BSON types.\n"
            "- Arrays and embedded documents are valid BSON structures."
        ),
        "document structure": (
            "- A MongoDB document is a BSON object made of field-value pairs.\n"
            "- Documents can contain arrays and embedded documents.\n"
            "- `_id` uniquely identifies each document."
        ),
        "collections vs tables": (
            "- Collections store documents; tables store rows.\n"
            "- Collections allow flexible document shapes.\n"
            "- Tables usually enforce a fixed schema."
        ),
        "insertone()": (
            "- `insertOne()` inserts exactly one document.\n"
            "- MongoDB generates `_id` automatically if you omit it.\n"
            "- The result includes `acknowledged` and `insertedId`."
        ),
        "insertmany()": (
            "- `insertMany()` inserts multiple documents from one array.\n"
            "- The result includes `acknowledged` and `insertedIds`.\n"
            "- `ordered: false` lets later inserts continue after an earlier error."
        ),
        "_id and objectid": (
            "- `_id` uniquely identifies each document.\n"
            "- MongoDB generates an ObjectId automatically if `_id` is omitted.\n"
            "- A duplicate `_id` value causes the insert to fail."
        ),
        "projections": (
            "- Projections control which fields are returned in query results.\n"
            "- You can include fields or exclude fields, but not mix both except for `_id`.\n"
            "- `_id` is included by default unless you explicitly exclude it."
        ),
        "sort/limit/skip": (
            "- `sort()` orders the result set.\n"
            "- `limit()` caps how many documents are returned.\n"
            "- `skip()` moves past earlier documents before returning results."
        ),
    }
    return fallbacks.get(concept_key, "")


def _sanitize_out_of_scope_content(markdown: str) -> str:
    lines = markdown.splitlines()
    cleaned_lines = []
    for line in lines:
        lowered = line.lower()
        
        # 1. Option replacement for micro-challenges
        if "transaction" in lowered and ("a)" in lowered or "b)" in lowered or "c)" in lowered or "d)" in lowered):
            line = line.replace("inside distributed transactions", "for multiple collections")
            line = line.replace("inside transactions", "for bulk inserts")
            line = line.replace("transaction", "write operation")
            cleaned_lines.append(line)
            continue
            
        # 2. General transaction line removal
        if "transaction" in lowered:
            continue
            
        # 3. .forEach removal/replacement
        if ".foreach" in lowered:
            line = line.replace("db.collection.find().forEach(printjson)", "for doc in cursor: print(doc)")
            line = line.replace(".forEach()", "looping")
            if ".foreach" in line.lower():
                continue
                
        # 4. Sharding config line removal in modeling
        if "shard key" in lowered or "configure sharding" in lowered:
            continue
            
        cleaned_lines.append(line)
        
    return "\n".join(cleaned_lines)


def _validate_general_exam_scope(cleaned_markdown: str, topic_id: int, concept: str) -> list[str]:
    issues: list[str] = []
    lowered = cleaned_markdown.lower()
    
    # 1. Multi-document transaction check (Topic < 11 should not discuss transactions)
    if topic_id < 11 and "transaction" in lowered:
        issues.append("Out of scope topic: Multi-document Transactions (not in Associate syllabus)")
        
    # 2. JavaScript cursor iteration check (e.g. .forEach() is shell specific, Python developer exam uses PyMongo/cursors)
    if ".foreach" in lowered:
        issues.append("Cursor iteration leak: .forEach() is JavaScript shell specific and out of scope for Python developer exam")
        
    # 3. countDocuments return inaccuracy check (returns count directly, not a document)
    if "countdocuments" in lowered and ("{ 'n':" in lowered or '{"n":' in lowered or "{'n':" in lowered):
        issues.append("Technical inaccuracy: countDocuments() returns an integer, not a document like { 'n': <value> }")
        
    # 4. Aggregation Stage leak in basic CRUD / MQL topics
    if "$search" in lowered and topic_id not in (6, 12):
        issues.append("Aggregation leak: $search stage is out of scope outside of Atlas Search topics")
        
    # 5. Sharding/replica set config check (Topic 10 should not go into sharding configuration)
    if "sharding" in lowered and "anti-patterns" in lowered:
        if "shard key" in lowered or "configure sharding" in lowered:
            issues.append("Out of scope topic: Sharding (only cluster basics allowed, no configuration)")
            
    return issues


def validate_lesson_markdown(
    lesson_markdown: str,
    topic_id: int | None = None,
    concept: str = "",
) -> dict:
    issues: list[str] = []
    raw_text = (lesson_markdown or "").strip()
    raw_micro_match = re.search(
        r"### 5\. Micro-Challenge(.*?)(?:### 6\. 30-Second Recall|\Z)",
        raw_text,
        flags=re.DOTALL,
    )
    if raw_micro_match and _contains_forbidden_micro_content(raw_micro_match.group(1).strip()):
        issues.append("micro-challenge contains forbidden answer or hint content")

    cleaned = clean_lesson_explanation(raw_text).strip()
    cleaned = _sanitize_out_of_scope_content(cleaned)
    if not cleaned:
        return {"is_valid": False, "issues": ["lesson is empty"], "cleaned_markdown": ""}

    positions = []
    for heading in LESSON_HEADINGS:
        position = cleaned.find(heading)
        if position < 0:
            issues.append(f"missing heading: {heading}")
        positions.append(position)

    found_positions = [position for position in positions if position >= 0]
    if len(found_positions) == len(LESSON_HEADINGS) and found_positions != sorted(found_positions):
        issues.append("lesson headings are out of order")

    for heading in LESSON_HEADINGS:
        if cleaned.count(heading) != 1:
            issues.append(f"heading must appear exactly once: {heading}")

    micro_match = re.search(
        r"### 5\. Micro-Challenge(.*?)(?:### 6\. 30-Second Recall|\Z)",
        cleaned,
        flags=re.DOTALL,
    )
    if not micro_match:
        issues.append("missing micro-challenge body")
    else:
        micro_text = micro_match.group(1).strip()
        if not micro_text:
            issues.append("micro-challenge is empty")
        if _contains_forbidden_micro_content(micro_text) and "micro-challenge contains forbidden answer or hint content" not in issues:
            issues.append("micro-challenge contains forbidden answer or hint content")

    recall_match = re.search(r"### 6\. 30-Second Recall(.*)\Z", cleaned, flags=re.DOTALL)
    if recall_match:
        bullet_count = len(re.findall(r"^\s*[-*•]\s+", recall_match.group(1), flags=re.MULTILINE))
        if bullet_count < 3:
            issues.append("30-Second Recall must end with 3-5 recall bullets")
    else:
        issues.append("missing 30-Second Recall body")

    if topic_id == 1:
        issues.extend(_validate_topic1_scope(cleaned, concept))

    if topic_id is not None:
        issues.extend(_validate_general_exam_scope(cleaned, topic_id, concept))

    return {
        "is_valid": not issues,
        "issues": issues,
        "cleaned_markdown": cleaned,
    }


def get_validated_lesson(topic_id: int, concept: str) -> dict | None:
    return database.get_lesson_artifact(topic_id=topic_id, concept=concept, status="validated")


def prebuild_lesson(
    topic_id: int | None = None,
    concept: str | None = None,
    coach: CoachPersona | None = None,
) -> dict:
    target = resolve_lesson_target(topic_id=topic_id, concept=concept)
    source_bundle = build_lesson_source_bundle(target)
    coach = coach or CoachPersona()
    raw_markdown = coach.explain_topic(target.topic, target.concept, source_bundle["md_context"])
    cleaned_markdown = clean_lesson_explanation(raw_markdown)
    if target.concept == "Document structure":
        cleaned_markdown = _sanitize_document_structure_lesson(cleaned_markdown)
    elif target.concept == "Collections vs Tables":
        cleaned_markdown = _sanitize_collections_vs_tables_lesson(cleaned_markdown)
    elif target.concept == "BSON Data Types":
        cleaned_markdown = _sanitize_bson_data_types_lesson(cleaned_markdown)
    validation = validate_lesson_markdown(cleaned_markdown, topic_id=target.topic_id, concept=target.concept)
    if not validation["is_valid"]:
        first_pass_markdown = cleaned_markdown
        first_pass_validation = validation
        repaired_markdown = coach.repair_topic_lesson(
            target.topic,
            target.concept,
            source_bundle["md_context"],
            cleaned_markdown,
            validation["issues"],
        )
        cleaned_markdown = clean_lesson_explanation(repaired_markdown)
        if target.concept == "Document structure":
            cleaned_markdown = _sanitize_document_structure_lesson(cleaned_markdown)
        elif target.concept == "Collections vs Tables":
            cleaned_markdown = _sanitize_collections_vs_tables_lesson(cleaned_markdown)
        elif target.concept == "BSON Data Types":
            cleaned_markdown = _sanitize_bson_data_types_lesson(cleaned_markdown)
        validation = validate_lesson_markdown(cleaned_markdown, topic_id=target.topic_id, concept=target.concept)
        if len(validation["issues"]) > len(first_pass_validation["issues"]):
            cleaned_markdown = first_pass_markdown
            validation = first_pass_validation
    if not validation["is_valid"]:
        sectional_markdown = _repair_lesson_by_sections(
            coach,
            target.topic,
            target.concept,
            source_bundle["md_context"],
            cleaned_markdown,
        )
        if target.concept == "Document structure":
            sectional_markdown = _sanitize_document_structure_lesson(sectional_markdown)
        elif target.concept == "Collections vs Tables":
            sectional_markdown = _sanitize_collections_vs_tables_lesson(sectional_markdown)
        elif target.concept == "BSON Data Types":
            sectional_markdown = _sanitize_bson_data_types_lesson(sectional_markdown)
        sectional_validation = validate_lesson_markdown(sectional_markdown, topic_id=target.topic_id, concept=target.concept)
        if len(sectional_validation["issues"]) <= len(validation["issues"]):
            cleaned_markdown = sectional_markdown
            validation = sectional_validation
    if not validation["is_valid"] and target.topic_id == 1:
        leaky_section_markdown = _regenerate_leaky_topic1_sections(
            coach,
            target.topic,
            target.concept,
            source_bundle["md_context"],
            cleaned_markdown,
        )
        if target.concept == "Document structure":
            leaky_section_markdown = _sanitize_document_structure_lesson(leaky_section_markdown)
        elif target.concept == "Collections vs Tables":
            leaky_section_markdown = _sanitize_collections_vs_tables_lesson(leaky_section_markdown)
        elif target.concept == "BSON Data Types":
            leaky_section_markdown = _sanitize_bson_data_types_lesson(leaky_section_markdown)
        leaky_section_validation = validate_lesson_markdown(
            leaky_section_markdown,
            topic_id=target.topic_id,
            concept=target.concept,
        )
        if len(leaky_section_validation["issues"]) <= len(validation["issues"]):
            cleaned_markdown = leaky_section_markdown
            validation = leaky_section_validation
    if not validation["is_valid"]:
        invalid_section_markdown = _repair_invalid_sections(
            coach,
            target.topic,
            target.concept,
            source_bundle["md_context"],
            cleaned_markdown,
            validation["issues"],
        )
        invalid_section_validation = validate_lesson_markdown(
            invalid_section_markdown,
            topic_id=target.topic_id,
            concept=target.concept,
        )
        if len(invalid_section_validation["issues"]) <= len(validation["issues"]):
            cleaned_markdown = invalid_section_markdown
            validation = invalid_section_validation
    if not validation["is_valid"] and any(
        "30-Second Recall must end with 3-5 recall bullets" in issue
        for issue in validation["issues"]
    ):
        sections = {
            heading: _extract_section_body(cleaned_markdown, heading)
            for heading in LESSON_HEADINGS
        }
        fallback_recall = _fallback_recall_body(target.topic, target.concept)
        if fallback_recall:
            sections["### 6. 30-Second Recall"] = fallback_recall
            fallback_markdown = _assemble_lesson(sections)
            fallback_validation = validate_lesson_markdown(
                fallback_markdown,
                topic_id=target.topic_id,
                concept=target.concept,
            )
            if len(fallback_validation["issues"]) <= len(validation["issues"]):
                cleaned_markdown = fallback_markdown
                validation = fallback_validation
    timestamp = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    artifact = {
        "topic_id": target.topic_id,
        "topic": target.topic,
        "concept": target.concept,
        "lesson_markdown": validation["cleaned_markdown"],
        "source_files": source_bundle["source_files"],
        "status": "validated" if validation["is_valid"] else "needs_review",
        "validation_issues": validation["issues"],
        "lesson_contract_version": LESSON_CONTRACT_VERSION,
        "content_contract_version": CONTENT_CONTRACT_VERSION,
        "generated_at": timestamp,
        "validated_at": timestamp if validation["is_valid"] else None,
    }
    database.upsert_lesson_artifact(artifact)
    return artifact
