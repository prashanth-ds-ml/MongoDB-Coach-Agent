from unittest.mock import MagicMock, patch


def test_audit_question_explanations_flags_missing_template():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.find.return_value = [
        {
            "_id": "q1",
            "question_text": "What is insertOne?",
            "metadata": {"topic": "CRUD", "concept": "insertOne()", "difficulty": "Easy"},
            "options": [{"option_letter": "A", "feedback": "Correct."}],
            "explanation": "Short answer.",
        }
    ]

    with patch.object(database, "questions_col", questions_col):
        audit = database.audit_question_explanations()

    assert audit["total_questions"] == 1
    assert audit["non_compliant_questions"] == 1
    assert "missing sections" in audit["issues"][0]["issues"][0]


def test_audit_question_explanations_accepts_six_part_template():
    from certcoach.core import database

    detailed = """
    ### 1. Correct Answer
    Correct Answer: A. This is correct because the method matches the documented API.
    ### 2. Why Correct
    Why Correct: insertOne accepts one document and returns acknowledged plus insertedId.
    ### 3. Why Other Options Are Wrong
    Why Other Options Are Wrong: the distractors use update operators or wrong casing.
    ### 4. Exam Trap
    Exam Trap: confusing insertOne with updateOne.
    ### 5. Memory Hook
    Memory Hook: insert means hand the document to MongoDB as-is.
    ### 6. Follow-Up Practice Recommendation
    Follow-Up Practice Recommendation: review insertOne documentation.
    """ * 3

    questions_col = MagicMock()
    questions_col.find.return_value = [
        {
            "_id": "q1",
            "question_text": "What is insertOne?",
            "metadata": {"topic": "CRUD", "concept": "insertOne()", "difficulty": "Easy"},
            "options": [
                {"option_letter": "A", "feedback": detailed},
                {"option_letter": "B", "feedback": "Wrong because it uses update syntax."},
                {"option_letter": "C", "feedback": "Wrong because it uses PyMongo casing."},
                {"option_letter": "D", "feedback": "Wrong because it adds invalid options."},
            ],
            "explanation": detailed,
        }
    ]

    with patch.object(database, "questions_col", questions_col):
        audit = database.audit_question_explanations()

    assert audit["compliant_questions"] == 1
    assert audit["non_compliant_questions"] == 0
