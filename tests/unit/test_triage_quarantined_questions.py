from unittest.mock import MagicMock, patch

from certcoach.jobs.triage_quarantined_questions import classify_question, run_triage


SYLLABUS = [
    {
        "id": 2,
        "topic": "CRUD Operations - Create",
        "subtopics": ["insertOne()", "insertMany()", "_id and ObjectId"],
    },
    {
        "id": 3,
        "topic": "CRUD Operations - Read",
        "subtopics": ["find()", "Projections", "countDocuments()"],
    },
]


def _question(stem, correct, distractors=()):
    return {
        "_id": "q1",
        "question_text": stem,
        "options": [
            {"code_snippet": correct, "is_correct": True},
            *({"code_snippet": text, "is_correct": False} for text in distractors),
        ],
        "metadata": {"content_contract_status": "quarantined"},
    }


def test_classifier_weights_stem_and_correct_answer_over_distractors():
    result = classify_question(
        _question(
            "Which method inserts multiple documents?",
            "db.books.insertMany([{title: 'A'}, {title: 'B'}])",
            ("db.books.insertOne({title: 'A'})",),
        ),
        SYLLABUS,
    )

    assert result.status == "mapped"
    assert result.topic_id == 2
    assert result.concept == "insertMany()"


def test_classifier_remaps_projection_question_from_unrelated_metadata():
    question = _question(
        "Which projection document excludes the password field?",
        '{"password": 0}',
    )
    question["metadata"].update({"topic_id": 2, "concept": "_id and ObjectId"})

    result = classify_question(question, SYLLABUS)

    assert result.status == "mapped"
    assert result.topic_id == 3
    assert result.concept == "Projections"


def test_classifier_keeps_contentless_record_as_misc():
    result = classify_question(_question("", ""), SYLLABUS)

    assert result.status == "misc"
    assert result.topic_id is None


def test_exact_replace_method_outweighs_incidental_id_reference():
    result = classify_question(
        _question(
            "Which call completely replaces the document while preserving its _id?",
            "collection.replace_one({'_id': 1}, {'name': 'new'})",
        ),
        [
            *SYLLABUS,
            {
                "id": 4,
                "topic": "CRUD Operations - Update",
                "subtopics": ["replaceOne()", "updateOne()"],
            },
        ],
    )

    assert result.status == "mapped"
    assert result.topic_id == 4
    assert result.concept == "replaceOne()"


@patch("certcoach.jobs.triage_quarantined_questions.planner")
@patch("certcoach.jobs.triage_quarantined_questions.database")
def test_apply_updates_mapping_but_keeps_record_quarantined(mock_database, mock_planner):
    mock_planner.load_syllabus.return_value = SYLLABUS
    mock_database.questions_col.find.return_value = [
        _question("Which method inserts multiple documents?", "db.c.insertMany([{a: 1}, {a: 2}])")
    ]
    mock_database.questions_col.update_one = MagicMock()

    result = run_triage(apply=True)

    assert result["mapped"] == 1
    update = mock_database.questions_col.update_one.call_args.args[1]["$set"]
    assert update["metadata.topic_id"] == 2
    assert update["metadata.concept"] == "insertMany()"
    assert update["metadata.quarantine_repair_disposition"] == "pending_repair"
    assert "metadata.content_contract_status" not in update


@patch("certcoach.jobs.triage_quarantined_questions.planner")
@patch("certcoach.jobs.triage_quarantined_questions.database")
def test_apply_respects_topic_and_concept_filters(mock_database, mock_planner):
    mock_planner.load_syllabus.return_value = SYLLABUS
    topic_match = _question("Which method inserts multiple documents?", "db.c.insertMany([{a: 1}, {a: 2}])")
    topic_match["metadata"].update({"topic_id": 2, "topic": "CRUD Operations - Create", "concept": "insertMany()"})
    other_topic = _question("Which projection document excludes the password field?", '{"password": 0}')
    other_topic["metadata"].update({"topic_id": 3, "topic": "CRUD Operations - Read", "concept": "Projections"})
    mock_database.questions_col.find.return_value = [topic_match, other_topic]
    mock_database.questions_col.update_one = MagicMock()

    result = run_triage(apply=True, topic_filter="CRUD Operations - Create", concept_filter="insertMany()")

    assert result["mapped"] == 1
    assert mock_database.questions_col.update_one.call_count == 1
    update = mock_database.questions_col.update_one.call_args.args[1]["$set"]
    assert update["metadata.topic"] == "CRUD Operations - Create"
