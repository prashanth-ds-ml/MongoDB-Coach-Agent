from unittest.mock import MagicMock, patch


def test_get_random_questions_skips_legacy_and_quarantined_records():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.find.return_value = [
        {
            "_id": "legacy",
            "question_text": "Legacy question",
            "metadata": {"topic": "MongoDB", "difficulty": "Easy"},
        },
        {
            "_id": "quarantined",
            "question_text": "Quarantined question",
            "metadata": {
                "topic": "MongoDB",
                "difficulty": "Easy",
                "content_contract_version": 2,
                "content_contract_status": "quarantined",
            },
        },
        {
            "_id": "active",
            "question_text": "Active question",
            "metadata": {
                "topic": "MongoDB",
                "difficulty": "Easy",
                "content_contract_version": 2,
                "content_contract_status": "generated",
            },
        },
    ]

    with patch.object(database, "questions_col", questions_col):
        questions = database.get_random_questions(topic="MongoDB", limit=10)

    assert [q["_id"] for q in questions] == ["active"]


def test_migrate_question_repairs_topic1_invented_types():
    from certcoach.jobs import migrate_legacy_question_bank as job

    question = {
        "_id": "q1",
        "question_text": "Which BSON type can store an array of documents within a single document?",
        "metadata": {
            "topic_id": 1,
            "topic": "MongoDB Overview & The Document Model",
            "concept": "BSON Data Types",
            "difficulty": "Easy",
            "content_contract_version": 1,
        },
        "options": [
            {"option_letter": "A", "code_snippet": "array", "is_correct": True, "feedback": "Correct."},
            {"option_letter": "B", "code_snippet": "embeddedDocument", "is_correct": False, "feedback": "Wrong."},
            {"option_letter": "C", "code_snippet": "subdocumentArray", "is_correct": False, "feedback": "Wrong."},
            {"option_letter": "D", "code_snippet": "documentArray", "is_correct": False, "feedback": "Wrong."},
        ],
        "explanation": "\n".join([
            "### 1. Correct Answer",
            "Array is correct.",
            "### 2. Why Correct",
            "Array stores ordered values.",
            "### 3. Why Other Options Are Wrong",
            "They are not official BSON types.",
            "### 4. Exam Trap",
            "Fake BSON type names.",
            "### 5. Memory Hook",
            "Use official BSON vocabulary.",
            "### 6. Follow-Up Practice Recommendation",
            "- Review BSON types.",
            "- Practice arrays.",
            "- Compare arrays and embedded documents.",
            "### 7. Syntax Example",
            "Not required for this concept.",
        ]),
        "trap_analysis": "",
    }

    with patch.object(job, "validate_question_quality", return_value=(True, [])):
        action, updated, issues = job.migrate_question(question)

    assert action == "repair"
    assert updated["question_text"] == "Which BSON type should you use to store multiple values under one field?"
    assert updated["metadata"]["content_contract_version"] == 2
    assert updated["metadata"]["content_contract_status"] == "migrated"
    assert "repaired topic 1 question text" in issues


def test_migrate_question_routes_explanation_only_failures_to_repair():
    from certcoach.jobs import migrate_legacy_question_bank as job

    question = {
        "_id": "q2",
        "question_text": "Which method inserts one document?",
        "metadata": {"topic_id": 2, "topic": "CRUD Operations - Create", "concept": "insertOne()", "difficulty": "Easy"},
        "options": [
            {"option_letter": "A", "code_snippet": "insertOne()", "is_correct": True},
            {"option_letter": "B", "code_snippet": "insertMany()", "is_correct": False},
            {"option_letter": "C", "code_snippet": "updateOne()", "is_correct": False},
            {"option_letter": "D", "code_snippet": "replaceOne()", "is_correct": False},
        ],
        "explanation": "too short",
    }
    issues = ["seven-part explanation is too short"]

    with patch.object(job, "validate_question_quality", return_value=(False, issues)):
        action, updated, returned_issues = job.migrate_question(question)

    assert action == "repair"
    assert updated["metadata"]["content_contract_status"] == "needs_explanation_repair"
    assert returned_issues == issues


def test_migrate_question_quarantines_structural_failures():
    from certcoach.jobs import migrate_legacy_question_bank as job

    question = {
        "_id": "q3",
        "question_text": "Broken question",
        "metadata": {"topic_id": 2, "topic": "CRUD Operations - Create", "concept": "insertOne()", "difficulty": "Easy"},
        "options": [],
    }
    issues = ["does not have exactly four options"]

    with patch.object(job, "validate_question_quality", return_value=(False, issues)):
        action, updated, returned_issues = job.migrate_question(question)

    assert action == "quarantine"
    assert updated["metadata"]["content_contract_status"] == "quarantined"
    assert returned_issues == issues


def test_migrate_question_keeps_existing_quarantine_inactive():
    from certcoach.jobs import migrate_legacy_question_bank as job

    question = {
        "_id": "q4",
        "metadata": {
            "content_contract_version": 2,
            "content_contract_status": "quarantined",
            "content_contract_issues": ["manual review required"],
        },
    }

    action, updated, issues = job.migrate_question(question)

    assert action == "quarantine"
    assert updated is question
    assert issues == ["manual review required"]


def test_migrate_topic1_explanation_only_failure_routes_to_repair():
    from certcoach.jobs import migrate_legacy_question_bank as job

    question = {
        "_id": "q5",
        "question_text": "Which BSON type stores multiple values?",
        "metadata": {"topic_id": 1, "concept": "BSON Data Types", "difficulty": "Easy"},
        "options": [
            {"option_letter": "A", "code_snippet": "array", "is_correct": True},
            {"option_letter": "B", "code_snippet": "string", "is_correct": False},
            {"option_letter": "C", "code_snippet": "date", "is_correct": False},
            {"option_letter": "D", "code_snippet": "boolean", "is_correct": False},
        ],
        "explanation": "too short",
    }
    issues = ["seven-part explanation is too short"]

    with patch.object(job, "validate_question_quality", return_value=(False, issues)):
        action, updated, returned_issues = job.migrate_question(question)

    assert action == "repair"
    assert updated["metadata"]["content_contract_status"] == "needs_explanation_repair"
    assert returned_issues == issues
