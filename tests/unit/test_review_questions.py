from unittest.mock import MagicMock, patch


def _question(citation_quote: str) -> dict:
    return {
        "_id": "q1",
        "question_text": "Which method deletes exactly one document?",
        "metadata": {"topic_id": 5, "concept": "deleteOne()", "difficulty": "Easy"},
        "options": [{"option_letter": "A", "code_snippet": "delete_one()", "is_correct": True}],
        "explanation": "delete_one() removes the first match.",
        "provenance": {"citation": {"doc_file": "topic_05.md", "quote": citation_quote}},
    }


def test_review_session_does_not_offer_confirm_when_citation_check_fails():
    from certcoach.jobs import review_questions

    question = _question("this quote is fabricated and will not verify")

    with patch.object(review_questions, "database") as mock_db:
        mock_db.get_questions_for_review.return_value = [question]
        mock_db.count_questions_for_review.return_value = 1
        mock_db.verify_citation.return_value = (False, "quote does not appear verbatim in the cited source file")

        with patch.object(review_questions, "Prompt") as mock_prompt:
            mock_prompt.ask.return_value = "k"
            review_questions.run_review_session(limit=1)

        args, kwargs = mock_prompt.ask.call_args
        assert "c" not in kwargs["choices"]
        assert "s" in kwargs["choices"]
        mock_db.confirm_question.assert_not_called()


def test_review_session_offers_confirm_when_citation_check_passes():
    from certcoach.jobs import review_questions

    question = _question("delete_one() removes the first match")

    with patch.object(review_questions, "database") as mock_db:
        mock_db.get_questions_for_review.return_value = [question]
        mock_db.count_questions_for_review.return_value = 1
        mock_db.verify_citation.return_value = (True, "citation verified")

        with patch.object(review_questions, "Prompt") as mock_prompt:
            mock_prompt.ask.return_value = "c"
            review_questions.run_review_session(limit=1)

        args, kwargs = mock_prompt.ask.call_args
        assert "c" in kwargs["choices"]
        mock_db.confirm_question.assert_called_once_with("q1", review_questions.USER_ID)
