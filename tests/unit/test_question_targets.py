from certcoach.core.question_targets import build_weighted_targets, parse_exam_weight


def test_parse_exam_weight_handles_percent_and_semantic():
    assert parse_exam_weight("18%") == 0.18
    assert parse_exam_weight("High") == 0.10
    assert parse_exam_weight("Medium") == 0.06
    assert parse_exam_weight("Low") == 0.03


def test_build_weighted_targets_uses_study_ready_threshold():
    syllabus = [
        {
            "id": 1,
            "topic": "Low Topic",
            "subtopics": ["A", "B"],
            "exam_weight": "2%",
            "bank_topic_keys": ["Low Bank"],
        },
        {
            "id": 2,
            "topic": "High Topic",
            "subtopics": ["C", "D"],
            "exam_weight": "18%",
            "bank_topic_keys": ["High Bank"],
        },
    ]

    targets = build_weighted_targets(syllabus, total_bank_target=100)
    assert len(targets) == 8
    assert {(t.difficulty, t.target_count) for t in targets} == {("Easy", 3), ("Medium", 2)}
    assert not any(t.difficulty == "Hard" for t in targets)
    assert sum(t.target_count for t in targets if t.topic == "High Topic") == 10
    assert sum(t.target_count for t in targets if t.topic == "Low Topic") == 10


def test_build_weighted_targets_adds_only_explicit_extras():
    syllabus = [{
        "id": 1,
        "topic": "Topic",
        "subtopics": ["Concept"],
        "bank_topic_keys": ["Bank"],
    }]

    targets = build_weighted_targets(syllabus, extra_easy=5, extra_medium=4)

    assert {(t.difficulty, t.target_count) for t in targets} == {("Easy", 8), ("Medium", 6)}
