from unittest.mock import MagicMock, patch


def test_suspect_uncited_drafts_dry_run_reports_count_without_writing():
    from certcoach.jobs import backfill_provenance

    questions_col = MagicMock()
    questions_col.find.return_value = [{"_id": "q1"}, {"_id": "q2"}]

    with patch.object(backfill_provenance.database, "questions_col", questions_col):
        with patch.object(backfill_provenance.database, "mark_question_suspect") as mock_suspect:
            result = backfill_provenance.suspect_uncited_drafts(dry_run=True)

    assert result == {"would_suspect": 2}
    mock_suspect.assert_not_called()

    args, kwargs = questions_col.find.call_args
    assert args[0] == {"provenance.state": "draft", "provenance.citation.quote": ""}


def test_suspect_uncited_drafts_marks_each_matching_question_suspect():
    from certcoach.jobs import backfill_provenance

    questions_col = MagicMock()
    questions_col.find.return_value = [{"_id": "q1"}, {"_id": "q2"}]

    with patch.object(backfill_provenance.database, "questions_col", questions_col):
        with patch.object(backfill_provenance.database, "mark_question_suspect") as mock_suspect:
            result = backfill_provenance.suspect_uncited_drafts(dry_run=False)

    assert result == {"suspected": 2}
    assert mock_suspect.call_count == 2
    called_ids = {call.args[0] for call in mock_suspect.call_args_list}
    assert called_ids == {"q1", "q2"}
    for call in mock_suspect.call_args_list:
        assert "legacy backlog" in call.kwargs["reason"]
