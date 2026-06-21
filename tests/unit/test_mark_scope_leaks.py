from unittest.mock import MagicMock, patch


def test_audit_scope_leaks_marks_future_scope_questions():
    from certcoach.jobs import mark_scope_leaks as job

    questions_col = MagicMock()
    questions_col.find.return_value = [
        {
            "_id": "q1",
            "question_text": "Which query uses $elemMatch correctly?",
            "metadata": {
                "topic_id": 1,
                "topic": "General",
                "syllabus_topic": "General",
                "concept": "BSON Data Types",
                "content_contract_version": 2,
                "content_contract_status": "generated",
                "content_contract_issues": [],
            },
            "options": [{"code_snippet": "$elemMatch"}],
        }
    ]

    syllabus = [
        {"id": 1, "topic": "MongoDB Overview & The Document Model", "subtopics": ["BSON Data Types"]},
        {"id": 2, "topic": "CRUD Operations - Create", "subtopics": ["insertOne()"]},
        {"id": 3, "topic": "Query Operators & MQL", "subtopics": ["$elemMatch"]},
    ]

    with patch.object(job.database, "check_connection", return_value=None), \
         patch.object(job.database, "questions_col", questions_col), \
         patch.object(job.planner, "load_syllabus", return_value=syllabus):
        result = job.audit_scope_leaks(topic_filter="1", concept_filter="BSON Data Types", apply=True)

    assert result["topic_leaks"] == 1
    assert result["normalized"] == 1
    questions_col.update_one.assert_called_once()
    update_doc = questions_col.update_one.call_args.args[1]["$set"]
    assert update_doc["metadata.content_contract_status"] == "quarantined"
    assert "scope leak" in update_doc["metadata.content_contract_issues"][0]
