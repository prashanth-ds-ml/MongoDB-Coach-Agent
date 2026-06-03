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


def test_validate_question_quality_rejects_shallow_six_part_explanation():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "Which insert method should you use when adding one document?",
        "options": [
            {"code_snippet": "insertOne()", "is_correct": True},
            {"code_snippet": "insertMany()", "is_correct": False},
            {"code_snippet": "replaceOne()", "is_correct": False},
            {"code_snippet": "updateOne()", "is_correct": False},
        ],
        "explanation": "\n".join([
            "### 1. Correct Answer",
            "insertOne()",
            "### 2. Why Correct",
            "Because it inserts one document.",
            "### 3. Why Other Options Are Wrong",
            "insertMany() is for multiple documents.",
            "### 4. Exam Trap",
            "Confusing single-document and multi-document inserts.",
            "### 5. Memory Hook",
            "One = One.",
            "### 6. Follow-Up Practice Recommendation",
            "Review the MongoDB insert documents guide.",
        ]),
    }

    is_valid, issues = validate_question_quality(question)

    assert not is_valid
    assert any("sections are too short" in issue for issue in issues)
