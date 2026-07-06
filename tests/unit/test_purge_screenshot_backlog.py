from unittest.mock import MagicMock, patch


def test_is_screenshot_sourced_suspect_true_for_pics_qa_suspect_question():
    from certcoach.jobs import purge_screenshot_backlog as job

    question = {
        "metadata": {"citation_source": "pics_qa/Screenshot 2025-12-14 090435.png"},
        "provenance": {"state": "suspect"},
    }

    assert job._is_screenshot_sourced_suspect(question) is True


def test_is_screenshot_sourced_suspect_false_for_non_suspect_state():
    from certcoach.jobs import purge_screenshot_backlog as job

    question = {
        "metadata": {"citation_source": "pics_qa/Screenshot 2025-12-14 090435.png"},
        "provenance": {"state": "sourced"},
    }

    assert job._is_screenshot_sourced_suspect(question) is False


def test_is_screenshot_sourced_suspect_false_when_no_citation_source():
    from certcoach.jobs import purge_screenshot_backlog as job

    question = {"metadata": {}, "provenance": {"state": "suspect"}}

    assert job._is_screenshot_sourced_suspect(question) is False


def test_run_purge_dry_run_does_not_delete():
    from certcoach.jobs import purge_screenshot_backlog as job

    screenshot_q = {"_id": "s1", "metadata": {"citation_source": "pics_qa/a.png"}, "provenance": {"state": "suspect"}}
    blank_q = {"_id": "b1", "metadata": {}, "provenance": {"state": "suspect"}}

    questions_col = MagicMock()
    questions_col.find.return_value = [screenshot_q, blank_q]

    with patch.object(job.database, "questions_col", questions_col):
        result = job.run_purge(dry_run=True)

    assert result == {"would_delete": 1}
    questions_col.delete_many.assert_not_called()


def test_run_purge_deletes_only_screenshot_sourced_and_leaves_blank_ones():
    from certcoach.jobs import purge_screenshot_backlog as job

    screenshot_q = {"_id": "s1", "metadata": {"citation_source": "pics_qa/a.png"}, "provenance": {"state": "suspect"}}
    blank_q = {"_id": "b1", "metadata": {}, "provenance": {"state": "suspect"}}

    questions_col = MagicMock()
    questions_col.find.return_value = [screenshot_q, blank_q]

    with patch.object(job.database, "questions_col", questions_col):
        with patch.object(job, "backup_questions") as mock_backup:
            result = job.run_purge(dry_run=False)

    mock_backup.assert_called_once()
    questions_col.delete_many.assert_called_once_with({"_id": {"$in": ["s1"]}})
    assert result == {"deleted": 1}


def test_run_purge_skip_backup_flag_skips_backup_call():
    from certcoach.jobs import purge_screenshot_backlog as job

    questions_col = MagicMock()
    questions_col.find.return_value = []

    with patch.object(job.database, "questions_col", questions_col):
        with patch.object(job, "backup_questions") as mock_backup:
            job.run_purge(dry_run=False, skip_backup=True)

    mock_backup.assert_not_called()
