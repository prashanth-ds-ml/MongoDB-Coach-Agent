import pytest

from certcoach.core.question_targets import (
    MIN_CONCEPT_TARGETS,
    build_weighted_targets,
    parse_exam_weight,
    topic_exam_weight_map,
)


def test_parse_exam_weight_handles_percent_and_semantic():
    assert parse_exam_weight("18%") == 0.18
    assert parse_exam_weight("High") == 0.10
    assert parse_exam_weight("Medium") == 0.06
    assert parse_exam_weight("Low") == 0.03


def test_topic_exam_weight_map_uses_official_domain_percentages_for_solo_domains():
    """Topic ids that map 1:1 to an exam domain (every domain except CRUD) get the
    real official percentage straight from EXAM_DOMAIN_WEIGHTS, ignoring whatever
    coarse High/Medium/Low label happens to sit on the syllabus entry."""
    syllabus = [
        {"id": 1, "topic": "Overview", "subtopics": ["A"], "exam_weight": "irrelevant-label"},
        {"id": 11, "topic": "Drivers", "subtopics": ["B"], "exam_weight": "irrelevant-label"},
    ]
    weights = topic_exam_weight_map(syllabus)
    assert weights[1] == pytest.approx(0.08)
    assert weights[11] == pytest.approx(0.18)


def test_topic_exam_weight_map_splits_crud_domain_by_high_medium_label():
    """CRUD's 51% has no official sub-split across its 7 topics, so topics sharing
    that domain split it proportional to their existing High/Medium/Low label."""
    syllabus = [
        {"id": 2, "topic": "Create", "subtopics": ["X"], "exam_weight": "High"},
        {"id": 5, "topic": "Delete", "subtopics": ["Y"], "exam_weight": "Medium"},
    ]
    weights = topic_exam_weight_map(syllabus)
    assert weights[2] + weights[5] == pytest.approx(0.51)
    assert weights[2] > weights[5]
    assert weights[2] == pytest.approx(0.51 * (1.0 / 1.6))
    assert weights[5] == pytest.approx(0.51 * (0.6 / 1.6))


def test_topic_exam_weight_map_falls_back_outside_domain_map():
    syllabus = [{"id": 999, "topic": "Unmapped", "subtopics": ["Z"], "exam_weight": "High"}]
    weights = topic_exam_weight_map(syllabus)
    assert weights[999] == pytest.approx(0.10)


def test_build_weighted_targets_scales_with_weight_above_the_floor():
    syllabus = [
        {"id": 12, "topic": "Low Topic", "subtopics": ["A", "B"], "bank_topic_keys": ["Low Bank"]},
        {"id": 11, "topic": "High Topic", "subtopics": ["C", "D"], "bank_topic_keys": ["High Bank"]},
    ]

    targets = build_weighted_targets(syllabus, total_bank_target=200)
    by_topic = {}
    for t in targets:
        by_topic.setdefault(t.topic_id, {})[t.difficulty] = t.target_count

    assert by_topic[12]["Easy"] >= MIN_CONCEPT_TARGETS["Easy"]
    assert by_topic[12]["Medium"] >= MIN_CONCEPT_TARGETS["Medium"]
    assert by_topic[11]["Easy"] > by_topic[12]["Easy"]
    assert by_topic[11]["Medium"] > by_topic[12]["Medium"]


def test_build_weighted_targets_never_drops_below_floor():
    syllabus = [{"id": 12, "topic": "Tiny", "subtopics": ["A"], "bank_topic_keys": ["Bank"]}]

    targets = build_weighted_targets(syllabus, total_bank_target=1)
    assert all(t.target_count >= MIN_CONCEPT_TARGETS[t.difficulty] for t in targets)


def test_build_weighted_targets_adds_only_explicit_extras():
    syllabus = [{
        "id": 1,
        "topic": "Topic",
        "subtopics": ["Concept"],
        "bank_topic_keys": ["Bank"],
    }]

    targets = build_weighted_targets(syllabus, extra_easy=5, extra_medium=4)

    assert {(t.difficulty, t.target_count) for t in targets} == {("Easy", 8), ("Medium", 6)}
