from unittest.mock import MagicMock, patch


def test_build_inventory_report_counts_active_legacy_and_targets():
    from certcoach.core.question_targets import QuestionTarget
    from certcoach.jobs import question_bank_comparison_report as report

    target = QuestionTarget(
        topic_id=1,
        topic="MongoDB Overview & The Document Model",
        bank_topic="MongoDB Overview & The Document Model",
        concept="BSON Data Types",
        difficulty="Easy",
        target_count=3,
        exam_weight=0.1,
        concept_weight=1.0,
    )

    questions_col = MagicMock()
    questions_col.find.return_value = [
        {
            "_id": "active",
            "question_text": "Active question",
            "metadata": {
                "topic_id": 1,
                "topic": "MongoDB Overview & The Document Model",
                "syllabus_topic": "MongoDB Overview & The Document Model",
                "concept": "BSON Data Types",
                "difficulty": "Easy",
                "content_contract_version": 2,
                "content_contract_status": "generated",
            },
        },
        {
            "_id": "legacy",
            "question_text": "Legacy question",
            "metadata": {
                "topic_id": 1,
                "topic": "MongoDB Overview & The Document Model",
                "syllabus_topic": "MongoDB Overview & The Document Model",
                "concept": "BSON Data Types",
                "difficulty": "Easy",
                "content_contract_status": "needs_explanation_repair",
            },
        },
        {
            "_id": "hard-repair",
            "question_text": "Hard repair question",
            "metadata": {
                "topic_id": 1,
                "topic": "BSON Data Types",
                "syllabus_topic": "MongoDB Overview & The Document Model",
                "concept": "BSON Data Types",
                "difficulty": "Hard",
                "content_contract_status": "needs_explanation_repair",
            },
        },
    ]

    with patch.object(report.database, "check_connection", return_value=None), \
         patch.object(report.database, "questions_col", questions_col), \
         patch.object(report.planner, "load_syllabus", return_value=[{"id": 1, "topic": target.topic, "subtopics": [target.concept]}]), \
         patch.object(report, "build_weighted_targets", return_value=[target]):
        inventory = report.build_inventory_report()

    assert inventory["total"] == 3
    assert inventory["active"] == 1
    assert inventory["inactive"] == 2
    assert inventory["needs_explanation_repair"] == 2
    assert inventory["needs_question_regeneration"] == 0
    assert inventory["legacy_pending"] == 0
    assert inventory["quarantined"] == 0
    assert inventory["targets"][0]["active_count"] == 1
    assert inventory["targets"][0]["legacy_count"] == 0
    assert inventory["targets"][0]["readiness_deficit"] == 2
    assert inventory["targets"][0]["study_ready"] is False
    assert inventory["concepts"][0]["easy_active"] == 1
    assert inventory["concepts"][0]["repair_pending"] == 2
    assert inventory["concepts"][0]["easy_readiness_deficit"] == 2
    assert inventory["concepts"][0]["study_ready"] is False
