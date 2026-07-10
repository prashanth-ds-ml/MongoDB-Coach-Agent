from __future__ import annotations

import re

CONTENT_CONTRACT_VERSION = 2
ACTIVE_CONTRACT_STATUSES = {"generated", "migrated"}

TOPIC1_MARKERS = (
    "bson data types",
    "document structure",
    "collections vs tables",
    "document model",
    "overview & the document model",
)

TOPIC1_INVENTED_TYPE_PATTERNS = (
    r"\bembeddedDocument\b",
    r"\bsubdocumentArray\b",
    r"\bdocumentArray\b",
    r"\bembeddedDocumentArray\b",
)

TOPIC1_OPTION_REPAIR_MAP = (
    ("embeddedDocumentArray", "array"),
    ("subdocumentArray", "array"),
    ("documentArray", "array"),
    ("embeddedDocument", "embedded document"),
    ("subdocument", "embedded document"),
)

TOPIC1_QUESTION_TEMPLATES = {
    "array": "Which BSON type should you use to store multiple values under one field?",
    "embedded document": "Which BSON type is best for storing related fields together inside a parent document?",
    "ObjectId": "Which BSON type is typically used as a unique identifier for documents?",
    "Date": "Which BSON type should you use to store a timestamp?",
    "string": "Which BSON type should you use to store text?",
    "boolean": "Which BSON type should you use for true/false values?",
    "null": "Which BSON value represents the absence of a value?",
}


def normalize_contract_text(text: str) -> str:
    return (text or "").strip().lower()


def is_topic1_concept_only(metadata: dict | None = None, text: str = "") -> bool:
    metadata = metadata or {}
    topic_id = metadata.get("topic_id")
    if topic_id == 1:
        return True

    haystack = " ".join(
        str(part or "")
        for part in (
            metadata.get("topic"),
            metadata.get("syllabus_topic"),
            metadata.get("concept"),
            text,
        )
    )
    lowered = normalize_contract_text(haystack)
    return any(marker in lowered for marker in TOPIC1_MARKERS)


def has_invented_topic1_type(text: str) -> bool:
    value = text or ""
    return any(re.search(pattern, value) for pattern in TOPIC1_INVENTED_TYPE_PATTERNS)


def normalize_topic1_option_text(text: str) -> str:
    result = str(text or "").strip()
    for source, target in TOPIC1_OPTION_REPAIR_MAP:
        result = re.sub(rf"\b{re.escape(source)}\b", target, result)
    return re.sub(r"\s+", " ", result).strip()


def suggest_topic1_question_text(correct_option_text: str) -> str | None:
    key = normalize_topic1_option_text(correct_option_text)
    return TOPIC1_QUESTION_TEMPLATES.get(key)


def is_contract_active(record: dict | None) -> bool:
    record = record or {}
    metadata = record.get("metadata", {}) or {}
    version = metadata.get("content_contract_version")
    status = str(metadata.get("content_contract_status", "") or "").strip().lower()
    if not version or int(version) < CONTENT_CONTRACT_VERSION:
        return False
    return status in ACTIVE_CONTRACT_STATUSES or status == ""


def contract_metadata(source: str) -> dict[str, object]:
    return {
        "content_contract_version": CONTENT_CONTRACT_VERSION,
        "content_contract_status": "generated",
        "content_contract_source": source,
    }


# ---------------------------------------------------------------------------
# Provenance: a separate trust axis from the content contract above.
#
# `is_contract_active` only answers "is this structurally well-formed" (right
# schema shape, right version) -- it says nothing about whether the content is
# actually true. That conflation is exactly what let factually wrong content
# ship as "active" throughout the bank. Provenance tracks the orthogonal
# question: has a human verified this specific item against its cited source?
#
# States:
#   draft     - exists, unverified. Never eligible for practice or a mock.
#   sourced   - carries a citation whose quote is deterministically verified
#               to occur in the named source file. Still not human-reviewed.
#   confirmed - a human read it against the citation and approved it. The
#               only state eligible to be served to a learner.
#   suspect   - previously sourced/confirmed, later flagged wrong. Quarantined
#               the same way draft is.
# ---------------------------------------------------------------------------
PROVENANCE_STATES = {"draft", "sourced", "confirmed", "suspect"}
DEFAULT_PROVENANCE_STATE = "draft"


def provenance_metadata(
    state: str = DEFAULT_PROVENANCE_STATE,
    citation_doc_file: str = "",
    citation_quote: str = "",
    model: str | None = None,
) -> dict[str, object]:
    if state not in PROVENANCE_STATES:
        raise ValueError(f"Unknown provenance state: {state!r}")
    return {
        "state": state,
        "citation": {"doc_file": citation_doc_file, "quote": citation_quote},
        "model": model,
        "confirmed_by": None,
        "confirmed_at": None,
    }


def is_confirmed(record: dict | None) -> bool:
    record = record or {}
    provenance = record.get("provenance", {}) or {}
    return str(provenance.get("state", "")).strip().lower() == "confirmed"
