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


def _excerpt(citation_quote: str, verified: bool, message: str) -> dict:
    return {
        "doc_file": "topic_05.md",
        "quote": citation_quote,
        "verified": verified,
        "message": message,
        "excerpt_before": "",
        "excerpt_match": citation_quote,
        "excerpt_after": "",
    }


def test_review_session_does_not_offer_confirm_when_citation_check_fails():
    from certcoach.jobs import review_questions

    question = _question("this quote is fabricated and will not verify")

    with patch.object(review_questions, "database") as mock_db:
        mock_db.get_questions_for_review.return_value = [question]
        mock_db.count_questions_for_review.return_value = 1
        mock_db.verify_citation.return_value = (False, "quote does not appear verbatim in the cited source file")
        mock_db.get_citation_excerpt.return_value = _excerpt(
            "this quote is fabricated and will not verify", False, "quote does not appear verbatim in the cited source file"
        )
        mock_db.get_legacy_reference_questions.return_value = []

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
        mock_db.get_citation_excerpt.return_value = _excerpt(
            "delete_one() removes the first match", True, "citation verified"
        )
        mock_db.get_legacy_reference_questions.return_value = []

        with patch.object(review_questions, "Prompt") as mock_prompt:
            mock_prompt.ask.return_value = "c"
            review_questions.run_review_session(limit=1)

        args, kwargs = mock_prompt.ask.call_args
        assert "c" in kwargs["choices"]
        mock_db.confirm_question.assert_called_once_with("q1", review_questions.USER_ID)


def test_run_review_session_forwards_concept_filter():
    from certcoach.jobs import review_questions

    question = _question("delete_one() removes the first match")

    with patch.object(review_questions, "database") as mock_db:
        mock_db.get_questions_for_review.return_value = [question]
        mock_db.count_questions_for_review.return_value = 1
        mock_db.verify_citation.return_value = (True, "citation verified")
        mock_db.get_citation_excerpt.return_value = _excerpt(
            "delete_one() removes the first match", True, "citation verified"
        )
        mock_db.get_legacy_reference_questions.return_value = []

        with patch.object(review_questions, "Prompt") as mock_prompt:
            mock_prompt.ask.return_value = "k"
            review_questions.run_review_session(topic_id=5, concept="deleteOne()", limit=1)

        mock_db.get_questions_for_review.assert_called_once_with(limit=1, topic_id=5, concept="deleteOne()")
        mock_db.count_questions_for_review.assert_called_once_with(topic_id=5, concept="deleteOne()")


def test_render_citation_panel_verified_style():
    from certcoach.jobs import review_questions

    question = _question("delete_one() removes the first match")

    with patch.object(review_questions, "database") as mock_db:
        mock_db.get_citation_excerpt.return_value = _excerpt(
            "delete_one() removes the first match", True, "citation verified"
        )

        panel = review_questions.render_citation_panel(question)

    assert panel.border_style == "green"
    rendered = str(panel.renderable)
    assert "citation verified" in rendered
    assert "topic_05.md" in rendered


def test_render_citation_panel_unverified_style():
    from certcoach.jobs import review_questions

    question = _question("fabricated quote")

    with patch.object(review_questions, "database") as mock_db:
        mock_db.get_citation_excerpt.return_value = _excerpt(
            "fabricated quote", False, "quote does not appear verbatim in the cited source file"
        )

        panel = review_questions.render_citation_panel(question)

    assert panel.border_style == "yellow"
    assert "quote does not appear verbatim" in str(panel.renderable)


def test_render_legacy_reference_prints_panel_when_legacy_questions_exist():
    from certcoach.jobs import review_questions

    legacy_question = {"question_text": "An older, unconfirmed variant of this question."}

    with patch.object(review_questions, "database") as mock_db, \
         patch.object(review_questions, "console") as mock_console:
        mock_db.get_legacy_reference_questions.return_value = [legacy_question]

        review_questions.render_legacy_reference(5, "deleteOne()")

    mock_db.get_legacy_reference_questions.assert_called_once_with(5, "deleteOne()")
    mock_console.print.assert_called_once()


def test_render_legacy_reference_prints_nothing_when_empty():
    from certcoach.jobs import review_questions

    with patch.object(review_questions, "database") as mock_db, \
         patch.object(review_questions, "console") as mock_console:
        mock_db.get_legacy_reference_questions.return_value = []

        review_questions.render_legacy_reference(5, "deleteOne()")

    mock_console.print.assert_not_called()
