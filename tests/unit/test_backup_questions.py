from unittest.mock import MagicMock, patch


def test_backup_questions_writes_and_verifies_manifest(tmp_path):
    from certcoach.jobs import backup_questions as job

    questions_col = MagicMock()
    questions_col.find.return_value = [{"_id": "q1", "question_text": "Question"}]

    with patch.object(job.database, "check_connection", return_value=None), \
         patch.object(job.database, "questions_col", questions_col):
        backup_dir = job.backup_questions(tmp_path)
        manifest = job.verify_backup(backup_dir)

    assert manifest["record_count"] == 1
    assert len(manifest["sha256"]) == 64


def test_restore_requires_explicit_confirmation(tmp_path):
    from certcoach.jobs.backup_questions import restore_questions

    try:
        restore_questions(tmp_path)
    except ValueError as exc:
        assert "confirm_replace=True" in str(exc)
    else:
        raise AssertionError("restore should require explicit confirmation")
