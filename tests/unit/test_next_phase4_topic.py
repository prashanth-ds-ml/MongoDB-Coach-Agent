def test_select_next_topic_uses_syllabus_order_and_requires_all_concepts_ready():
    from certcoach.jobs.next_phase4_topic import select_next_topic

    report = {
        "concepts": [
            {"topic_id": 2, "topic": "Topic 2", "concept": "C", "study_ready": False, "easy_active": 2, "medium_active": 2, "easy_readiness_deficit": 1, "medium_readiness_deficit": 0},
            {"topic_id": 1, "topic": "Topic 1", "concept": "A", "study_ready": True, "easy_active": 3, "medium_active": 2, "easy_readiness_deficit": 0, "medium_readiness_deficit": 0},
            {"topic_id": 1, "topic": "Topic 1", "concept": "B", "study_ready": False, "easy_active": 3, "medium_active": 1, "easy_readiness_deficit": 0, "medium_readiness_deficit": 1},
        ]
    }

    selected = select_next_topic(report, easy_target=3, medium_target=2)

    assert selected["topic_id"] == 1
    assert selected["ready_concepts"] == 1
    assert selected["concept_count"] == 2
    assert selected["medium_readiness_deficit"] == 1


def test_select_next_topic_returns_none_when_all_topics_ready():
    from certcoach.jobs.next_phase4_topic import select_next_topic

    assert select_next_topic({
        "concepts": [
            {"topic_id": 1, "topic": "Topic 1", "concept": "A", "study_ready": True, "easy_active": 3, "medium_active": 2, "easy_readiness_deficit": 0, "medium_readiness_deficit": 0},
        ]
    }, easy_target=3, medium_target=2) is None


def test_select_next_topic_uses_canonical_concept_order():
    from certcoach.jobs.next_phase4_topic import select_next_topic

    report = {
        "concepts": [
            {"topic_id": 1, "topic": "Topic 1", "concept": "Second", "study_ready": False, "easy_active": 2, "medium_active": 2, "easy_readiness_deficit": 1, "medium_readiness_deficit": 0},
            {"topic_id": 1, "topic": "Topic 1", "concept": "First", "study_ready": False, "easy_active": 3, "medium_active": 1, "easy_readiness_deficit": 0, "medium_readiness_deficit": 1},
        ]
    }
    syllabus = [{"id": 1, "topic": "Topic 1", "subtopics": ["First", "Second"]}]

    selected = select_next_topic(report, syllabus, easy_target=3, medium_target=2)

    assert selected["concept"] == "First"
    assert selected["concept_medium_readiness_deficit"] == 1


def test_select_next_topic_continues_after_readiness_until_population_target():
    from certcoach.jobs.next_phase4_topic import select_next_topic

    report = {
        "concepts": [{
            "topic_id": 1,
            "topic": "Topic 1",
            "concept": "A",
            "study_ready": True,
            "easy_active": 3,
            "medium_active": 2,
            "easy_readiness_deficit": 0,
            "medium_readiness_deficit": 0,
            "repair_pending": 0,
        }]
    }

    selected = select_next_topic(report, easy_target=5, medium_target=5)

    assert selected["concept"] == "A"
    assert selected["concept_easy_population_deficit"] == 2
    assert selected["concept_medium_population_deficit"] == 3
