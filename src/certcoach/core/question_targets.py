from __future__ import annotations

from dataclasses import dataclass


# Absolute floor per concept. This mirrors the fixed five-question practice-session
# composition in cli.py (exactly 3 Easy + 2 Medium, hardcoded there as a live product/UX
# decision, not a population-planning artifact) -- every concept must reach this floor
# before practice unlocks at all, regardless of exam weight. Weight only changes how far
# *above* this floor a concept's deeper population target reaches (see build_weighted_targets).
MIN_CONCEPT_TARGETS = {"Easy": 3, "Medium": 2}

# Backward-compatible alias for the former name.
STUDY_READY_TARGETS = MIN_CONCEPT_TARGETS

# The official MongoDB Associate Python Developer exam blueprint (percentages, sum to
# 100), cross-checked against the real exam guide PDF -- see memory/MongoDB_Exam_Blueprint.md.
# This used to live only in database.py, used exclusively for mock-exam draws; population
# targets never consulted it and instead used the coarse per-topic High/Medium/Low label.
# Moved here so both consumers share one source of truth; database.py re-exports it.
EXAM_DOMAIN_WEIGHTS: dict[str, float] = {
    "CRUD Operations": 51,
    "Drivers & PyMongo": 18,
    "Indexes": 17,
    "Overview & Document Model": 8,
    "Data Modeling": 4,
    "Tools & Tooling": 2,
}

# Which syllabus topic_id belongs to which exam domain above.
DOMAIN_MAP: dict[int, str] = {
    1: "Overview & Document Model",
    2: "CRUD Operations",
    3: "CRUD Operations",
    4: "CRUD Operations",
    5: "CRUD Operations",
    6: "CRUD Operations",
    7: "CRUD Operations",
    8: "CRUD Operations",
    9: "Indexes",
    10: "Data Modeling",
    11: "Drivers & PyMongo",
    12: "Tools & Tooling",
}

# Previous flat per-concept population inventory baseline (5 Easy + 5 Medium). Used only
# as the default total pool size to redistribute by weight when a caller doesn't pass an
# explicit total_bank_target -- keeps overall bank scale in the same ballpark as before,
# just no longer split identically across all 58 concepts regardless of exam weight.
_DEFAULT_POOL_PER_CONCEPT = 10

_TOPIC_LABEL_MULTIPLIERS = {"high": 1.0, "medium": 0.6, "low": 0.3}


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


def easy_medium_split(exam_weight: float) -> tuple[float, float]:
    """difficulty_distribution's Easy:Medium ratio, renormalized without Hard.

    Population/practice generation only ever targets Easy and Medium today --
    Hard question generation is out of scope for the seeding loop -- so this
    is the piece of difficulty_distribution build_weighted_targets actually
    consumes: a weight-driven Easy/Medium split instead of a flat 3:2 ratio
    for every concept regardless of how heavily it's tested.
    """
    dist = difficulty_distribution(exam_weight)
    total = dist["Easy"] + dist["Medium"]
    if total <= 0:
        return 0.5, 0.5
    return dist["Easy"] / total, dist["Medium"] / total


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


def _topic_label_multiplier(exam_weight_field) -> float:
    text = str(exam_weight_field or "").strip().lower()
    return _TOPIC_LABEL_MULTIPLIERS.get(text, 1.0)


def topic_exam_weight_map(syllabus: list[dict]) -> dict[int, float]:
    """Real per-topic exam weight (fraction of the whole exam), cascaded from the
    official domain percentages in EXAM_DOMAIN_WEIGHTS/DOMAIN_MAP instead of the
    coarse High/Medium/Low -> 10%/6%/3% approximation parse_exam_weight uses alone.

    Domains that map to exactly one topic (every domain today except CRUD) hand
    that topic the full domain percentage. CRUD's 51% spans 7 topics with no
    official sub-split in the exam guide, so each topic's existing High/Medium/Low
    label is used as a relative multiplier, normalized within the domain -- the
    closest exam-relevant signal already present in the syllabus data.
    """
    topics_by_domain: dict[str | None, list[dict]] = {}
    for item in syllabus:
        domain = DOMAIN_MAP.get(item["id"])
        topics_by_domain.setdefault(domain, []).append(item)

    weights: dict[int, float] = {}
    for domain, items in topics_by_domain.items():
        domain_pct = EXAM_DOMAIN_WEIGHTS.get(domain) if domain else None
        if domain_pct is None:
            for item in items:
                weights[item["id"]] = parse_exam_weight(item.get("exam_weight"))
            continue
        multipliers = {item["id"]: _topic_label_multiplier(item.get("exam_weight")) for item in items}
        multiplier_total = sum(multipliers.values()) or 1.0
        for item in items:
            weights[item["id"]] = (domain_pct / 100.0) * (multipliers[item["id"]] / multiplier_total)
    return weights


def build_weighted_targets(
    syllabus: list[dict],
    total_bank_target: int | None = None,
    *,
    extra_easy: int = 0,
    extra_medium: int = 0,
) -> list[QuestionTarget]:
    """Build per-concept Easy/Medium population targets, plus explicitly requested extras.

    Every concept is floored at MIN_CONCEPT_TARGETS (3 Easy + 2 Medium) -- that floor
    mirrors the fixed five-question practice-session composition in cli.py and does not
    change with weight. Above that floor, the target scales with the concept's real
    exam-blueprint weight (topic_exam_weight_map cascaded through concept_weight_map):
    `total_bank_target` (default: the previous flat 10-per-concept average, times the
    concept count) is redistributed proportional to each concept's share of the whole
    exam, instead of split identically across all 58 concepts regardless of weight.
    """
    topic_weights = topic_exam_weight_map(syllabus)
    num_concepts = sum(len(item.get("subtopics") or [item["topic"]]) for item in syllabus) or 1
    pool_total = total_bank_target if total_bank_target is not None else _DEFAULT_POOL_PER_CONCEPT * num_concepts

    targets: list[QuestionTarget] = []
    for item in syllabus:
        subtopics = item.get("subtopics") or [item["topic"]]
        bank_topic = (item.get("bank_topic_keys") or [item["topic"]])[0]
        topic_weight = topic_weights.get(item["id"], parse_exam_weight(item.get("exam_weight")))
        concept_weights = concept_weight_map(item)
        easy_share, medium_share = easy_medium_split(topic_weight)

        for concept in subtopics:
            concept_weight = concept_weights[concept]
            concept_pool = topic_weight * concept_weight * pool_total
            weighted_target = {
                "Easy": round(concept_pool * easy_share),
                "Medium": round(concept_pool * medium_share),
            }
            for difficulty in ("Easy", "Medium"):
                extra = max(0, extra_easy if difficulty == "Easy" else extra_medium)
                target_count = max(MIN_CONCEPT_TARGETS[difficulty], weighted_target[difficulty]) + extra
                targets.append(QuestionTarget(
                    topic_id=item["id"],
                    topic=item["topic"],
                    bank_topic=bank_topic,
                    concept=concept,
                    difficulty=difficulty,
                    target_count=target_count,
                    exam_weight=topic_weight,
                    concept_weight=concept_weight,
                ))
    return targets
