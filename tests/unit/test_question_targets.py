from certcoach.core.question_targets import build_weighted_targets, parse_exam_weight


def test_parse_exam_weight_handles_percent_and_semantic():
    assert parse_exam_weight("18%") == 0.18
    assert parse_exam_weight("High") == 0.10
    assert parse_exam_weight("Medium") == 0.06
    assert parse_exam_weight("Low") == 0.03


def test_build_weighted_targets_prioritizes_high_weight_topics():
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
    high_total = sum(t.target_count for t in targets if t.topic == "High Topic")
    low_total = sum(t.target_count for t in targets if t.topic == "Low Topic")

    assert high_total > low_total
    assert any(t.concept == "C" and t.difficulty == "Hard" for t in targets)
