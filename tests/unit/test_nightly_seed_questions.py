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
            "### 7. Syntax Example",
            "```javascript\ninsertOne({ name: 'Ada' });\n```",
            "- This uses the single-document insert syntax.",
            "- The method returns insertion metadata for one document.",
        ]),
    }

    is_valid, issues = validate_question_quality(question)

    assert not is_valid
    assert any("sections are too short" in issue for issue in issues)


def test_validate_question_quality_rejects_section_six_without_bullets():
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
            "insertOne() is the correct choice because it inserts a single document.",
            "### 2. Why Correct",
            "It matches the single-document requirement and returns insertion metadata.",
            "### 3. Why Other Options Are Wrong",
            "insertMany() is for multiple documents.",
            "replaceOne() replaces an existing document.",
            "updateOne() modifies matching fields, it does not insert a new document.",
            "### 4. Exam Trap",
            "The trap is confusing insert semantics with update semantics.",
            "### 5. Memory Hook",
            "One document, one insert call, one clear outcome.",
            "### 6. Follow-Up Practice Recommendation",
            "Review the insert documents guide and practice with one-document and many-document inserts.",
            "### 7. Syntax Example",
            "```javascript\ninsertOne({ name: 'Ada' });\n```",
            "- This uses the single-document insert syntax.",
            "- The method returns insertion metadata for one document.",
        ]),
    }

    is_valid, issues = validate_question_quality(question)

    assert not is_valid
    assert any("need more bullets" in issue for issue in issues)


def test_validate_question_quality_allows_not_required_syntax_example_for_conceptual_topic():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "Which BSON type best fits a flexible nested structure?",
        "metadata": {"topic_id": 1, "concept": "BSON Data Types"},
        "options": [
            {"code_snippet": "embedded document", "is_correct": True},
            {"code_snippet": "string", "is_correct": False},
            {"code_snippet": "boolean", "is_correct": False},
            {"code_snippet": "date", "is_correct": False},
        ],
        "explanation": "\n".join([
            "### 1. Correct Answer",
            "Embedded document is the correct choice because it can hold a nested structure with related fields.",
            "### 2. Why Correct",
            "MongoDB lets you group related values inside a document so you can keep the nested data close to the parent record and read it back in one query.",
            "### 3. Why Other Options Are Wrong",
            "string only stores text, so it cannot represent nested fields. boolean stores true or false only, so it is far too limited. date stores time information, not structure, so it does not model nested data.",
            "### 4. Exam Trap",
            "The trap is confusing a data value type with a structural container type. Nested documents are used when the shape of the information matters more than a simple scalar value.",
            "### 5. Memory Hook",
            "Think of an embedded document as a folder inside a folder: the parent keeps the related details together instead of scattering them into separate records.",
            "### 6. Follow-Up Practice Recommendation",
            "- Review how embedded documents keep related data together in one parent document.",
            "- Compare nested documents against flat scalar fields in a simple sample collection.",
            "- Practice identifying when the shape of the data matters more than a single value.",
            "### 7. Syntax Example",
            "Not required for this concept.",
        ]),
    }

    is_valid, issues = validate_question_quality(question)

    assert is_valid
    assert not issues
