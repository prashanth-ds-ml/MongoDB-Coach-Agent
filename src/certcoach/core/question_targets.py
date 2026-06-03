from __future__ import annotations

import math
from dataclasses import dataclass


DEFAULT_TOTAL_BANK_TARGET = 540


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


def _largest_remainder_counts(total: int, weights: dict[str, float]) -> dict[str, int]:
    if total <= 0:
        return {k: 0 for k in weights}
    raw = {k: total * v for k, v in weights.items()}
    counts = {k: int(math.floor(v)) for k, v in raw.items()}
    remaining = total - sum(counts.values())
    for key, _ in sorted(raw.items(), key=lambda item: item[1] - math.floor(item[1]), reverse=True)[:remaining]:
        counts[key] += 1
    return counts


def build_weighted_targets(syllabus: list[dict], total_bank_target: int = DEFAULT_TOTAL_BANK_TARGET) -> list[QuestionTarget]:
    weighted_topics = [(item, parse_exam_weight(item.get("exam_weight"))) for item in syllabus]
    total_weight = sum(weight for _, weight in weighted_topics) or 1.0

    topic_counts = {}
    raw_topic_weights = {str(item["id"]): weight / total_weight for item, weight in weighted_topics}
    allocated = _largest_remainder_counts(total_bank_target, raw_topic_weights)

    for item, weight in weighted_topics:
        # Keep a useful minimum for low-weight topics while respecting overall allocation.
        topic_counts[item["id"]] = max(len(item.get("subtopics") or [item["topic"]]) * 3, allocated[str(item["id"])])

    targets: list[QuestionTarget] = []
    for item, weight in weighted_topics:
        subtopics = item.get("subtopics") or [item["topic"]]
        bank_topic = (item.get("bank_topic_keys") or [item["topic"]])[0]
        concept_counts = _largest_remainder_counts(topic_counts[item["id"]], concept_weight_map(item))

        for concept, concept_total in concept_counts.items():
            diff_counts = _largest_remainder_counts(concept_total, difficulty_distribution(weight))
            concept_weight = concept_counts[concept] / max(1, topic_counts[item["id"]])
            for difficulty, target_count in diff_counts.items():
                if target_count <= 0:
                    continue
                targets.append(QuestionTarget(
                    topic_id=item["id"],
                    topic=item["topic"],
                    bank_topic=bank_topic,
                    concept=concept,
                    difficulty=difficulty,
                    target_count=target_count,
                    exam_weight=weight,
                    concept_weight=concept_weight,
                ))
    return targets
