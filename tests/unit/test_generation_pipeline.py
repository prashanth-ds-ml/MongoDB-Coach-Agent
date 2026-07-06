from unittest.mock import patch

from certcoach.jobs import nightly_seed_questions as job


def _question(explanation="Explanation text.") -> dict:
    return {
        "_id": "q1",
        "question_text": "Which method inserts a single document?",
        "options": [
            {"option_letter": "A", "code_snippet": "insert_one()", "is_correct": True},
            {"option_letter": "B", "code_snippet": "insert_many()", "is_correct": False},
            {"option_letter": "C", "code_snippet": "update_one()", "is_correct": False},
            {"option_letter": "D", "code_snippet": "delete_one()", "is_correct": False},
        ],
        "explanation": explanation,
    }


def test_strip_think_block_removes_reasoning():
    text = "<think>internal reasoning here</think>FINAL: CONSISTENT"
    assert job._strip_think_block(text) == "FINAL: CONSISTENT"


def test_run_self_consistency_check_passes_on_consistent_verdict():
    with patch.object(job, "_ollama_json_request", return_value={"response": "Looks fine.\nFINAL: CONSISTENT"}):
        ok, msg = job.run_self_consistency_check(_question(), "http://localhost:11434")

    assert ok is True
    assert "passed" in msg


def test_run_self_consistency_check_fails_on_inconsistent_verdict():
    with patch.object(job, "_ollama_json_request", return_value={"response": "FINAL: INCONSISTENT: option C also looks correct"}):
        ok, msg = job.run_self_consistency_check(_question(), "http://localhost:11434")

    assert ok is False
    assert "option C also looks correct" in msg


def test_run_self_consistency_check_fails_closed_on_unparseable_response():
    with patch.object(job, "_ollama_json_request", return_value={"response": "I am not sure."}):
        ok, msg = job.run_self_consistency_check(_question(), "http://localhost:11434")

    assert ok is False
    assert "no parseable verdict" in msg


def test_run_self_consistency_check_fails_closed_on_request_error():
    with patch.object(job, "_ollama_json_request", side_effect=RuntimeError("connection refused")):
        ok, msg = job.run_self_consistency_check(_question(), "http://localhost:11434")

    assert ok is False
    assert "errored" in msg


def test_pipeline_checks_reach_sourced_only_when_both_checks_pass():
    with patch.object(job.database, "verify_citation", return_value=(True, "citation verified")):
        with patch.object(job, "run_self_consistency_check", return_value=(True, "self-consistency check passed")):
            provenance = job.run_generation_pipeline_checks(
                _question(), "topic_02.md", "insert_one() inserts a single document", "http://localhost:11434"
            )

    assert provenance["state"] == "sourced"
    assert "citation verified" in provenance["pipeline_note"]
    assert "self-consistency check passed" in provenance["pipeline_note"]


def test_pipeline_checks_stay_draft_when_citation_fails():
    with patch.object(job.database, "verify_citation", return_value=(False, "quote does not appear verbatim in the cited source file")):
        with patch.object(job, "run_self_consistency_check") as mock_consistency:
            provenance = job.run_generation_pipeline_checks(
                _question(), "topic_02.md", "a fabricated quote", "http://localhost:11434"
            )

    assert provenance["state"] == "draft"
    mock_consistency.assert_not_called()  # short-circuits -- no point checking consistency if the citation is fake
    assert "skipped" in provenance["pipeline_note"]


def test_pipeline_checks_stay_draft_when_self_consistency_fails():
    with patch.object(job.database, "verify_citation", return_value=(True, "citation verified")):
        with patch.object(job, "run_self_consistency_check", return_value=(False, "self-consistency check failed: option C also correct")):
            provenance = job.run_generation_pipeline_checks(
                _question(), "topic_02.md", "insert_one() inserts a single document", "http://localhost:11434"
            )

    assert provenance["state"] == "draft"
    assert "option C also correct" in provenance["pipeline_note"]
