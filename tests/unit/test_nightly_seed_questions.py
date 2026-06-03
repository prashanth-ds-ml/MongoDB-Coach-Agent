from unittest.mock import patch


def test_audit_weighted_deficits_filters_by_topic_id():
    from certcoach.jobs import nightly_seed_questions as job

    syllabus = [
        {
            "id": 1,
            "topic": "Topic One",
            "subtopics": ["A"],
            "exam_weight": "10%",
            "bank_topic_keys": ["Bank One"],
        },
        {
            "id": 2,
            "topic": "Topic Two",
            "subtopics": ["B"],
            "exam_weight": "10%",
            "bank_topic_keys": ["Bank Two"],
        },
    ]

    with patch.object(job.planner, "load_syllabus", return_value=syllabus), \
         patch.object(job, "_question_count", return_value=0):
        deficits = job.audit_weighted_deficits(total_bank_target=20, topic_filter="2")

    assert deficits
    assert all(target.topic_id == 2 for target, _ in deficits)


def test_topic_matches_bank_topic_substring():
    from certcoach.core.question_targets import QuestionTarget
    from certcoach.jobs.nightly_seed_questions import _topic_matches

    target = QuestionTarget(
        topic_id=11,
        topic="MongoDB Drivers & PyMongo",
        bank_topic="PyMongo Basics",
        concept="MongoClient",
        difficulty="Medium",
        target_count=5,
        exam_weight=0.18,
        concept_weight=0.20,
    )

    assert _topic_matches(target, "pymongo")
    assert _topic_matches(target, "11")
    assert not _topic_matches(target, "aggregation")
