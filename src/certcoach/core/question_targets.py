from __future__ import annotations

from dataclasses import dataclass


STUDY_READY_TARGETS = {"Easy": 3, "Medium": 2}


@dataclass(frozen=True)
class QuestionTarget:
    topic_id: int
    topic: str
    bank_topic: str
    concept: str
    difficulty: str
    target_count: int
    exam_weight: float
    concept_weight: float


def parse_exam_weight(weight: str | int | float | None) -> float:
    if isinstance(weight, (int, float)):
        return max(0.0, float(weight))
    if not weight:
        return 0.06

    text = str(weight).strip().lower()
    if text.endswith("%"):
        try:
            return max(0.0, float(text[:-1]) / 100.0)
        except ValueError:
            return 0.06

    semantic = {
        "high": 0.10,
        "medium": 0.06,
        "low": 0.03,
    }
    return semantic.get(text, 0.06)


def difficulty_distribution(exam_weight: float) -> dict[str, float]:
    if exam_weight >= 0.10:
        return {"Easy": 0.25, "Medium": 0.45, "Hard": 0.30}
    if exam_weight >= 0.06:
        return {"Easy": 0.35, "Medium": 0.45, "Hard": 0.20}
    return {"Easy": 0.45, "Medium": 0.40, "Hard": 0.15}


def concept_weight_map(topic_item: dict) -> dict[str, float]:
    subtopics = topic_item.get("subtopics") or [topic_item["topic"]]
    explicit = topic_item.get("concept_weights") or {}
    if explicit:
        total = sum(max(0.0, float(explicit.get(c, 0.0))) for c in subtopics)
        if total > 0:
            return {c: max(0.0, float(explicit.get(c, 0.0))) / total for c in subtopics}

    # Fallback: distribute by documentation keyword salience. Concepts with
    # multiple tokens tend to be broader and receive a small bump.
    raw_scores = {}
    for concept in subtopics:
        token_count = len([t for t in concept.replace("()", " ").replace("/", " ").split() if t])
        operator_bonus = 0.15 if "$" in concept or "index" in concept.lower() or "pymongo" in concept.lower() else 0.0
        raw_scores[concept] = 1.0 + min(0.5, token_count * 0.08) + operator_bonus
    total = sum(raw_scores.values()) or 1.0
    return {concept: score / total for concept, score in raw_scores.items()}


def build_weighted_targets(
    syllabus: list[dict],
    total_bank_target: int | None = None,
    *,
    extra_easy: int = 0,
    extra_medium: int = 0,
) -> list[QuestionTarget]:
    """Build per-concept readiness targets plus explicitly requested extras.

    `total_bank_target` remains accepted for compatibility but is intentionally
    ignored. CertCoach no longer uses a fixed global question-bank target.
    """
    requested_targets = {
        "Easy": STUDY_READY_TARGETS["Easy"] + max(0, extra_easy),
        "Medium": STUDY_READY_TARGETS["Medium"] + max(0, extra_medium),
    }
    targets: list[QuestionTarget] = []
    for item in syllabus:
        weight = parse_exam_weight(item.get("exam_weight"))
        subtopics = item.get("subtopics") or [item["topic"]]
        bank_topic = (item.get("bank_topic_keys") or [item["topic"]])[0]
        concept_weights = concept_weight_map(item)

        for concept in subtopics:
            for difficulty, target_count in requested_targets.items():
                targets.append(QuestionTarget(
                    topic_id=item["id"],
                    topic=item["topic"],
                    bank_topic=bank_topic,
                    concept=concept,
                    difficulty=difficulty,
                    target_count=target_count,
                    exam_weight=weight,
                    concept_weight=concept_weights[concept],
                ))
    return targets
