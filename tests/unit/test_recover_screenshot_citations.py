from unittest.mock import MagicMock, patch


def _screenshot_question(qid: str, topic_id: int = 1) -> dict:
    return {
        "_id": qid,
        "question_text": "Which method inserts a single document?",
        "metadata": {"topic_id": topic_id, "citation_source": "pics_qa/Screenshot 2025-12-14 090435.png"},
        "options": [
            {"option_letter": "A", "code_snippet": "insert_one()", "is_correct": True},
            {"option_letter": "B", "code_snippet": "insert_many()", "is_correct": False},
            {"option_letter": "C", "code_snippet": "update_one()", "is_correct": False},
            {"option_letter": "D", "code_snippet": "delete_one()", "is_correct": False},
        ],
        "explanation": "insert_one() inserts a single document into a collection.",
        "provenance": {"state": "suspect"},
    }


def test_find_supporting_quote_returns_none_for_none_response():
    from certcoach.jobs import recover_screenshot_citations as job

    with patch.object(job, "_ollama_json_request", return_value={"response": "NONE"}):
        quote = job.find_supporting_quote(_screenshot_question("q1"), "some transcript text", "http://localhost:11434", "gemma4:12b")

    assert quote is None


def test_find_supporting_quote_returns_the_quote_text():
    from certcoach.jobs import recover_screenshot_citations as job

    with patch.object(job, "_ollama_json_request", return_value={"response": '"insert_one() inserts a single document"'}):
        quote = job.find_supporting_quote(_screenshot_question("q1"), "transcript", "http://localhost:11434", "gemma4:12b")

    assert quote == "insert_one() inserts a single document"


def test_find_supporting_quote_fails_closed_on_error():
    from certcoach.jobs import recover_screenshot_citations as job

    with patch.object(job, "_ollama_json_request", side_effect=RuntimeError("boom")):
        quote = job.find_supporting_quote(_screenshot_question("q1"), "transcript", "http://localhost:11434", "gemma4:12b")

    assert quote is None


def test_run_recovery_only_targets_screenshot_sourced_suspect_questions():
    from certcoach.jobs import recover_screenshot_citations as job

    screenshot_q = _screenshot_question("shot-1")
    doc_sourced_q = {
        "_id": "doc-1",
        "metadata": {"topic_id": 2, "citation_source": "topic_02_docs.md"},
        "provenance": {"state": "suspect"},
        "options": [],
    }

    questions_col = MagicMock()
    questions_col.find.return_value = [screenshot_q, doc_sourced_q]

    with patch.object(job.database, "questions_col", questions_col):
        with patch.object(job, "load_transcript_text", return_value=None) as mock_load:
            result = job.run_recovery()

    mock_load.assert_called_once_with("Screenshot 2025-12-14 090435.png")
    assert result["no_transcript"] == 1


def test_run_recovery_promotes_to_sourced_only_on_full_pass():
    from certcoach.jobs import recover_screenshot_citations as job

    screenshot_q = _screenshot_question("shot-1")
    questions_col = MagicMock()
    questions_col.find.return_value = [screenshot_q]

    fake_provenance = {"state": "sourced", "pipeline_note": "citation: citation verified; self-consistency: self-consistency check passed"}

    with patch.object(job.database, "questions_col", questions_col):
        with patch.object(job, "load_transcript_text", return_value="insert_one() inserts a single document into the collection."):
            with patch.object(job, "find_supporting_quote", return_value="insert_one() inserts a single document"):
                with patch.object(job, "run_generation_pipeline_checks", return_value=fake_provenance):
                    result = job.run_recovery()

    questions_col.update_one.assert_called_once_with({"_id": "shot-1"}, {"$set": {"provenance": fake_provenance}})
    assert result["sourced"] == 1


def test_run_recovery_leaves_record_untouched_when_checks_fail():
    from certcoach.jobs import recover_screenshot_citations as job

    screenshot_q = _screenshot_question("shot-1")
    questions_col = MagicMock()
    questions_col.find.return_value = [screenshot_q]

    fake_provenance = {"state": "draft", "pipeline_note": "citation: quote does not appear verbatim in the cited source file"}

    with patch.object(job.database, "questions_col", questions_col):
        with patch.object(job, "load_transcript_text", return_value="unrelated transcript text"):
            with patch.object(job, "find_supporting_quote", return_value="a fabricated-sounding quote"):
                with patch.object(job, "run_generation_pipeline_checks", return_value=fake_provenance):
                    result = job.run_recovery()

    questions_col.update_one.assert_not_called()
    assert result["still_suspect"] == 1
