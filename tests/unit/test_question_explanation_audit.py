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


def test_audit_question_explanations_accepts_seven_part_template():
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
    ### 7. Syntax Example
    Syntax Example: db.collection.insertOne({name: 'test'})
    """ * 3

    questions_col = MagicMock()
    questions_col.find.return_value = [
        {
            "_id": "q1",
            "question_text": "What is insertOne?",
            "metadata": {
                "topic": "CRUD",
                "concept": "insertOne()",
                "difficulty": "Easy",
                "content_contract_version": 2,
            },
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


def test_audit_question_explanations_flags_legacy_contract_versions():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.find.return_value = [
        {
            "_id": "q1",
            "question_text": "What is insertOne?",
            "metadata": {
                "topic": "CRUD",
                "concept": "insertOne()",
                "difficulty": "Easy",
                "generation_source": "nightly_weighted_seed",
            },
            "options": [
                {"option_letter": "A", "feedback": "Correct."},
                {"option_letter": "B", "feedback": "Wrong."},
                {"option_letter": "C", "feedback": "Wrong."},
                {"option_letter": "D", "feedback": "Wrong."},
            ],
            "explanation": "### 1. Correct Answer\n### 2. Why Correct\n### 3. Why Other Options Are Wrong\n### 4. Exam Trap\n### 5. Memory Hook\n### 6. Follow-Up Practice Recommendation",
        }
    ]

    with patch.object(database, "questions_col", questions_col):
        audit = database.audit_question_explanations()

    assert audit["non_compliant_questions"] == 1
    assert any("legacy content contract version" in issue for issue in audit["issues"][0]["issues"])
