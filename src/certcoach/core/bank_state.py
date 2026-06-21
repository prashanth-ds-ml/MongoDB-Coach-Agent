from __future__ import annotations

from certcoach.core.content_contract import CONTENT_CONTRACT_VERSION, is_contract_active

KNOWN_BANK_STATUSES = {
    "legacy",
    "needs_explanation_repair",
    "needs_question_regeneration",
    "quarantined",
}


def _metadata(record: dict | None) -> dict:
    return (record or {}).get("metadata", {}) or {}


def normalize_text(value: object) -> str:
    return str(value or "").strip()


def normalize_casefold(value: object) -> str:
    return normalize_text(value).casefold()


def canonical_status(record: dict | None) -> str:
    record = record or {}
    metadata = _metadata(record)
    if is_contract_active(record):
        return "active"

    status = normalize_casefold(metadata.get("content_contract_status", ""))
    if status in KNOWN_BANK_STATUSES:
        return status

    version = metadata.get("content_contract_version")
    try:
        version_num = int(version)
    except (TypeError, ValueError):
        version_num = None
    if version_num is None or version_num < CONTENT_CONTRACT_VERSION:
        return "legacy"
    if not status:
        return "legacy"
    return status


def matches_topic_filter(record: dict | None, topic_filter: str | None) -> bool:
    if not topic_filter:
        return True
    filt = normalize_text(topic_filter)
    if not filt:
        return True

    metadata = _metadata(record)
    if filt.isdigit():
        try:
            return int(metadata.get("topic_id")) == int(filt)
        except (TypeError, ValueError):
            return False

    filt_cf = filt.casefold()
    topic_candidates = (
        metadata.get("topic"),
        metadata.get("syllabus_topic"),
    )
    return any(normalize_casefold(candidate) == filt_cf for candidate in topic_candidates if candidate)


def matches_concept_filter(record: dict | None, concept_filter: str | None) -> bool:
    if not concept_filter:
        return True
    metadata = _metadata(record)
    return normalize_casefold(metadata.get("concept")) == normalize_casefold(concept_filter)


def question_scope_key(record: dict | None) -> tuple[int | None, str, str]:
    metadata = _metadata(record)
    return (
        metadata.get("topic_id"),
        normalize_text(metadata.get("concept")),
        normalize_text(metadata.get("difficulty")),
    )
