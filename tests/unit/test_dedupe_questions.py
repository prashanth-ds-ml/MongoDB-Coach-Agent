from unittest.mock import MagicMock, patch


def _question(q_id, text, explanation="", topic="CRUD Operations"):
    return {
        "_id": q_id,
        "question_text": text,
        "metadata": {"topic": topic},
        "explanation": explanation,
        "trap_analysis": "",
        "options": [
            {"option_letter": "A", "feedback": explanation},
            {"option_letter": "B", "feedback": explanation},
            {"option_letter": "C", "feedback": explanation},
            {"option_letter": "D", "feedback": explanation},
        ],
        "global_metrics": {"total_attempts": 0},
    }


def test_find_duplicate_groups_keeps_higher_quality_question():
    from certcoach.jobs import dedupe_questions as job

    weak = _question("weak", "What is insertOne?", "short")
    strong = _question(
        "strong",
        "  What   is insertOne? ",
        "Correct answer. Why correct. Why other options are wrong. Exam trap. "
        "Memory hook. Follow-up practice recommendation. Detailed explanation.",
    )

    questions_col = MagicMock()
    questions_col.find.return_value = [weak, strong]

    with patch.object(job.database, "questions_col", questions_col):
        groups = job.find_duplicate_groups()

    assert len(groups) == 1
    assert groups[0]["keep"]["_id"] == "strong"
    assert groups[0]["remove"][0]["_id"] == "weak"


def test_run_dedupe_apply_deletes_only_duplicates():
    from certcoach.jobs import dedupe_questions as job

    keep = _question(
        "keep",
        "What is findOne?",
        "Correct answer. Why correct. Why other options are wrong. Exam trap. "
        "Memory hook. Follow-up practice recommendation. Detailed explanation.",
    )
    duplicate = _question("dup", "What is findOne?", "short")

    questions_col = MagicMock()
    questions_col.find.return_value = [keep, duplicate]
    questions_col.delete_many.return_value.deleted_count = 1

    with patch.object(job.database, "check_connection", return_value=None), \
         patch.object(job.database, "questions_col", questions_col):
        result = job.run_dedupe(apply=True)

    assert result["duplicate_groups"] == 1
    assert result["duplicate_documents"] == 1
    assert result["deleted"] == 1
    questions_col.delete_many.assert_called_once_with({"_id": {"$in": ["dup"]}})
