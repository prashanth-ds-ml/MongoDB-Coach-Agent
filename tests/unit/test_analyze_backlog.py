import os
from unittest.mock import MagicMock, patch


def _suspect_question(qid: str, topic_id: int | None, doc_file: str = "") -> dict:
    return {
        "_id": qid,
        "metadata": {"topic_id": topic_id, "citation_source": ""},
        "provenance": {"state": "suspect", "citation": {"doc_file": doc_file, "quote": ""}},
    }


def test_has_real_doc_lead_true_for_existing_cleaned_markdown_file():
    from certcoach.jobs import analyze_backlog

    real_files = os.listdir(analyze_backlog.CLEANED_MARKDOWNS_DIR)
    assert real_files, "expected at least one real cleaned markdown file for this test to be meaningful"
    question = _suspect_question("q1", None, doc_file=real_files[0])

    assert analyze_backlog._has_real_doc_lead(question) is True


def test_has_real_doc_lead_true_for_topic_with_cleaned_markdowns_even_without_filename_match():
    """Legacy citation_source values are human-readable titles or URLs, never
    the corpus's real filenames -- a per-question filename match alone would
    miss almost every legacy record even though its topic has real docs on
    file. Topic-level coverage is the honest signal here."""
    from certcoach.jobs import analyze_backlog

    question = _suspect_question("q1", 1, doc_file="pics_qa/Screenshot 2025-12-14 095943.png")

    assert analyze_backlog._has_real_doc_lead(question) is True


def test_has_real_doc_lead_false_when_blank_and_no_topic():
    from certcoach.jobs import analyze_backlog

    question = _suspect_question("q1", None, doc_file="")

    assert analyze_backlog._has_real_doc_lead(question) is False


def test_analyze_suspect_backlog_buckets_duplicates_before_doc_lead_check():
    from certcoach.jobs import analyze_backlog

    real_files = os.listdir(analyze_backlog.CLEANED_MARKDOWNS_DIR)
    dup_source = _suspect_question("dup", None, doc_file=real_files[0])  # has a real lead, but is a flagged duplicate
    keep_source = _suspect_question("keep", None, doc_file=real_files[0])
    no_lead = _suspect_question("no-lead", None, doc_file="")

    questions_col = MagicMock()
    questions_col.find.return_value = [dup_source, keep_source, no_lead]

    fake_dup_groups = [{"key": "k", "keep": keep_source, "remove": [dup_source]}]

    with patch.object(analyze_backlog.database, "questions_col", questions_col):
        with patch.object(analyze_backlog, "find_duplicate_groups", return_value=fake_dup_groups):
            result = analyze_backlog.analyze_suspect_backlog()

    dup_ids = [q["_id"] for q in result["buckets"]["duplicate"]]
    lead_ids = [q["_id"] for q in result["buckets"]["has_doc_lead"]]
    no_lead_ids = [q["_id"] for q in result["buckets"]["no_doc_lead"]]

    assert dup_ids == ["dup"]
    assert lead_ids == ["keep"]
    assert no_lead_ids == ["no-lead"]
    assert result["suspect_total"] == 3


def test_analyze_suspect_backlog_counts_all_provenance_states():
    from certcoach.jobs import analyze_backlog

    confirmed = {"_id": "c1", "metadata": {"topic_id": 1}, "provenance": {"state": "confirmed"}}
    draft = {"_id": "d1", "metadata": {"topic_id": 1}, "provenance": {"state": "draft"}}
    no_prov = {"_id": "n1", "metadata": {"topic_id": 1}}

    questions_col = MagicMock()
    questions_col.find.return_value = [confirmed, draft, no_prov]

    with patch.object(analyze_backlog.database, "questions_col", questions_col):
        with patch.object(analyze_backlog, "find_duplicate_groups", return_value=[]):
            result = analyze_backlog.analyze_suspect_backlog()

    assert result["state_counts"]["confirmed"] == 1
    assert result["state_counts"]["draft"] == 1
    assert result["state_counts"]["no_provenance"] == 1
