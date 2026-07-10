import json

from unittest.mock import MagicMock, patch


def _authored(**overrides):
    authored = {
        "topic_id": 1,
        "concept": "BSON Data Types",
        "difficulty": "Easy",
        "style_type": "Type B",
        "response_type": "single",
        "question_text": "Which BSON type alias matches any numeric value in a $type query?",
        "options": [
            {"option_letter": "A", "code_snippet": '"number"', "is_correct": True, "feedback": "Correct -- number matches int/long/double/decimal."},
            {"option_letter": "B", "code_snippet": '"int"', "is_correct": False, "feedback": "Only matches 32-bit integers."},
            {"option_letter": "C", "code_snippet": '"long"', "is_correct": False, "feedback": "Only matches 64-bit integers."},
            {"option_letter": "D", "code_snippet": '"decimal"', "is_correct": False, "feedback": "Only matches Decimal128."},
        ],
        "citation_doc_file": "topic_01_docs_manual_reference_bson_types__cf63661090.md",
        "citation_quote": '$type also supports the number alias, which matches the integer, decimal, double, and long BSON types.',
        "trap_analysis": "Learners often pick a single specific type instead of the umbrella alias.",
        "explanation_sections": {
            "correct_answer": "Option A (\"number\") is correct.",
            "why_correct": "The number alias is documented to match Int32, Int64, Double, and Decimal128 in one query.",
            "why_wrong": "B, C, and D each match only one specific numeric subtype, missing the others.",
            "exam_trap": "Assuming you need to enumerate every numeric BSON type separately.",
            "memory_hook": "\"number\" = umbrella for all numbers.",
            "practice_recommendations": ["Try $type: \"number\" against mixed numeric fields.", "Compare against $isNumber.", "Review the BSON type table."],
            "syntax_example": "```javascript\ndb.coll.find({ price: { $type: \"number\" } })\n```",
        },
    }
    authored.update(overrides)
    return authored


def _topic_item():
    return {
        "id": 1, "topic": "MongoDB Overview & The Document Model",
        "subtopics": ["BSON Data Types"], "bank_topic_keys": ["Topic 1"],
        "md_files": ["topic_01_docs_manual_reference_bson_types__cf63661090.md"],
    }


def test_build_authored_question_assembles_expected_shape():
    from certcoach.jobs.ingest_authored_content import build_authored_question

    with patch("certcoach.core.planner.load_syllabus", return_value=[_topic_item()]), \
         patch("certcoach.jobs.ingest_authored_content._next_question_number", return_value=1):
        question, target = build_authored_question(_authored())

    assert question["question_text"].startswith("Which BSON type alias")
    assert len(question["options"]) == 4
    assert question["options"][0]["is_correct"] is True
    assert question["options"][0]["option_letter"] == "A"
    assert question["metadata"]["topic_id"] == 1
    assert question["metadata"]["concept"] == "BSON Data Types"
    assert question["metadata"]["difficulty"] == "Easy"
    assert question["metadata"]["question_style_type"] == "Type B"
    assert question["metadata"]["generation_source"] == "claude_authored"
    assert question["metadata"]["content_contract_status"] == "generated"
    assert "### 1. Correct Answer" in question["explanation"]
    assert "### 7. Syntax Example" in question["explanation"]
    # Type B (theory/concept, no syntax needed) -- the gate requires the
    # explicit "not required" marker here, not a real code example.
    assert "Not required for this concept." in question["explanation"]
    assert target.topic_id == 1
    assert target.concept == "BSON Data Types"


def test_build_authored_question_forces_not_required_syntax_marker_for_type_b():
    """The real quality gate (validate_question_quality) requires the syntax
    section to explicitly say "not required" for non-syntax-heavy style
    types -- any other text, even a real code example, fails validation. See
    memory/decision_log.md for how this was caught by testing against the
    real gate rather than trusting the assembly logic blind."""
    from certcoach.jobs.ingest_authored_content import build_authored_question
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    authored = _authored(style_type="Type B")
    authored["explanation_sections"]["syntax_example"] = "```javascript\ndb.coll.find()\n```"

    with patch("certcoach.core.planner.load_syllabus", return_value=[_topic_item()]), \
         patch("certcoach.jobs.ingest_authored_content._next_question_number", return_value=1):
        question, _ = build_authored_question(authored)

    assert "Not required for this concept." in question["explanation"]
    assert "db.coll.find()" not in question["explanation"]
    is_valid, issues = validate_question_quality(question)
    assert is_valid, issues


def test_build_authored_question_rejects_wrong_option_count():
    from certcoach.jobs.ingest_authored_content import build_authored_question

    authored = _authored(options=_authored()["options"][:3])

    with patch("certcoach.core.planner.load_syllabus", return_value=[_topic_item()]):
        try:
            build_authored_question(authored)
            assert False, "expected ValueError"
        except ValueError as exc:
            assert "exactly 4 options" in str(exc)


def test_build_authored_question_rejects_no_correct_option():
    from certcoach.jobs.ingest_authored_content import build_authored_question

    options = [dict(o, is_correct=False) for o in _authored()["options"]]
    authored = _authored(options=options)

    with patch("certcoach.core.planner.load_syllabus", return_value=[_topic_item()]):
        try:
            build_authored_question(authored)
            assert False, "expected ValueError"
        except ValueError as exc:
            assert "is_correct" in str(exc)


def test_build_authored_question_rejects_unknown_topic():
    from certcoach.jobs.ingest_authored_content import build_authored_question

    with patch("certcoach.core.planner.load_syllabus", return_value=[]):
        try:
            build_authored_question(_authored())
            assert False, "expected ValueError"
        except ValueError as exc:
            assert "no syllabus topic" in str(exc)


def test_ingest_authored_question_skips_duplicates_without_inserting():
    from certcoach.jobs.ingest_authored_content import ingest_authored_question

    with patch("certcoach.core.planner.load_syllabus", return_value=[_topic_item()]), \
         patch("certcoach.jobs.ingest_authored_content._next_question_number", return_value=1), \
         patch("certcoach.jobs.ingest_authored_content.is_duplicate_question", return_value=(True, "exact question text already exists")), \
         patch("certcoach.jobs.ingest_authored_content.database") as mock_database:
        result = ingest_authored_question(_authored())

    assert result["status"] == "skipped"
    assert "duplicate" in result["reason"]
    mock_database.questions_col.insert_one.assert_not_called()


def test_ingest_authored_question_skips_on_quality_gate_failure():
    from certcoach.jobs.ingest_authored_content import ingest_authored_question

    with patch("certcoach.core.planner.load_syllabus", return_value=[_topic_item()]), \
         patch("certcoach.jobs.ingest_authored_content._next_question_number", return_value=1), \
         patch("certcoach.jobs.ingest_authored_content.is_duplicate_question", return_value=(False, "")), \
         patch("certcoach.jobs.ingest_authored_content.validate_question_quality", return_value=(False, ["explanation too short"])), \
         patch("certcoach.jobs.ingest_authored_content.database") as mock_database:
        result = ingest_authored_question(_authored())

    assert result["status"] == "skipped"
    assert "quality gate failed" in result["reason"]
    mock_database.questions_col.insert_one.assert_not_called()


def test_ingest_authored_question_inserts_and_stores_provenance():
    from certcoach.jobs.ingest_authored_content import ingest_authored_question

    fake_provenance = {"state": "sourced", "pipeline_note": "citation: ok; self-consistency: ok"}

    with patch("certcoach.core.planner.load_syllabus", return_value=[_topic_item()]), \
         patch("certcoach.jobs.ingest_authored_content._next_question_number", return_value=1), \
         patch("certcoach.jobs.ingest_authored_content.is_duplicate_question", return_value=(False, "")), \
         patch("certcoach.jobs.ingest_authored_content.validate_question_quality", return_value=(True, [])), \
         patch("certcoach.jobs.ingest_authored_content._load_env", return_value=("model", "http://localhost:11434")), \
         patch("certcoach.jobs.ingest_authored_content.run_generation_pipeline_checks", return_value=fake_provenance), \
         patch("certcoach.jobs.ingest_authored_content.database") as mock_database:
        result = ingest_authored_question(_authored())

    assert result["status"] == "inserted"
    assert result["provenance_state"] == "sourced"
    mock_database.questions_col.insert_one.assert_called_once()
    mock_database.questions_col.update_one.assert_called_once()
    update_call = mock_database.questions_col.update_one.call_args
    assert update_call.args[1] == {"$set": {"provenance": fake_provenance}}


def test_main_ingests_a_batch_and_reports_summary(tmp_path, capsys):
    from certcoach.jobs import ingest_authored_content as mod

    authored_file = tmp_path / "batch.json"
    authored_file.write_text(json.dumps([_authored(), _authored(question_text="A second question?")]), encoding="utf-8")

    with patch.object(mod, "database") as mock_database, \
         patch.object(mod, "ingest_authored_question") as mock_ingest:
        mock_ingest.side_effect = [
            {"question_id": "q1", "status": "inserted", "provenance_state": "sourced", "pipeline_note": "ok"},
            {"question_id": "q2", "status": "skipped", "reason": "duplicate: exact question text already exists"},
        ]
        exit_code = mod.main([str(authored_file)])

    assert exit_code == 0
    assert mock_ingest.call_count == 2
    mock_database.check_connection.assert_called_once()
    output = capsys.readouterr().out
    assert "1 inserted (1 reached 'sourced')" in output
    assert "1 skipped" in output


def test_main_accepts_a_single_authored_dict_not_just_a_list(tmp_path):
    from certcoach.jobs import ingest_authored_content as mod

    authored_file = tmp_path / "single.json"
    authored_file.write_text(json.dumps(_authored()), encoding="utf-8")

    with patch.object(mod, "database"), \
         patch.object(mod, "ingest_authored_question") as mock_ingest:
        mock_ingest.return_value = {"question_id": "q1", "status": "inserted", "provenance_state": "draft", "pipeline_note": "ok"}
        mod.main([str(authored_file)])

    assert mock_ingest.call_count == 1
