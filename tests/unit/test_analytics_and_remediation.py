from unittest.mock import MagicMock, patch


def _attempt(topic_id: int, concept: str, is_correct: bool) -> dict:
    return {"user_id": "u1", "topic_id": topic_id, "concept": concept, "is_correct": is_correct}


def test_get_concept_accuracy_report_sorts_weakest_first():
    from certcoach.core import database

    attempts_col = MagicMock()
    attempts_col.find.return_value = [
        _attempt(2, "insertOne()", True),
        _attempt(2, "insertOne()", True),
        _attempt(2, "insertOne()", False),
        _attempt(2, "insertOne()", False),
        _attempt(9, "Compound Indexes", True),
    ]

    with patch.object(database, "attempts_col", attempts_col):
        report = database.get_concept_accuracy_report("u1")

    assert report[0]["concept"] == "insertOne()"
    assert report[0]["accuracy_pct"] == 50.0
    assert report[0]["domain"] == "CRUD Operations"
    assert report[1]["concept"] == "Compound Indexes"
    assert report[1]["accuracy_pct"] == 100.0
    assert report[1]["domain"] == "Indexes"


def test_get_concept_accuracy_report_handles_missing_concept_field():
    from certcoach.core import database

    attempts_col = MagicMock()
    attempts_col.find.return_value = [{"user_id": "u1", "topic_id": 1, "is_correct": True}]

    with patch.object(database, "attempts_col", attempts_col):
        report = database.get_concept_accuracy_report("u1")

    assert report[0]["concept"] == "Unclassified"


def test_get_domain_accuracy_report_orders_by_exam_weight_not_accuracy():
    from certcoach.core import database

    attempts_col = MagicMock()
    attempts_col.find.return_value = [
        _attempt(12, "Atlas Search", False),  # Tools & Tooling, 2%, 0% accuracy
        _attempt(2, "insertOne()", True),      # CRUD Operations, 51%, 100% accuracy
    ]

    with patch.object(database, "attempts_col", attempts_col):
        report = database.get_domain_accuracy_report("u1")

    domains_in_order = [r["domain"] for r in report]
    assert domains_in_order[0] == "CRUD Operations"  # heaviest weight first, regardless of accuracy
    assert domains_in_order[-1] == "Tools & Tooling"

    crud = next(r for r in report if r["domain"] == "CRUD Operations")
    tools = next(r for r in report if r["domain"] == "Tools & Tooling")
    assert crud["accuracy_pct"] == 100.0
    assert tools["accuracy_pct"] == 0.0


def test_get_domain_accuracy_report_reports_none_accuracy_for_untested_domains():
    from certcoach.core import database

    attempts_col = MagicMock()
    attempts_col.find.return_value = []

    with patch.object(database, "attempts_col", attempts_col):
        report = database.get_domain_accuracy_report("u1")

    assert all(r["accuracy_pct"] is None for r in report)
    assert all(r["attempts"] == 0 for r in report)


def test_get_remediation_uses_citation_and_domain_matched_flashcards():
    from certcoach.core import database

    question = {
        "_id": "q1",
        "metadata": {"topic_id": 2},
        "provenance": {"citation": {"doc_file": "topic_02.md", "quote": "insertOne() inserts a single document"}},
    }
    flashcards = [
        {"category": "CRUD Operations", "title": "insertOne() basics", "answer": "..."},
        {"category": "Indexes", "title": "unrelated", "answer": "..."},
    ]

    questions_col = MagicMock()
    questions_col.find_one.return_value = question

    with patch.object(database, "questions_col", questions_col):
        with patch.object(database, "load_flashcards", return_value=flashcards):
            result = database.get_remediation_for_wrong_attempt("q1")

    assert result["citation"]["quote"] == "insertOne() inserts a single document"
    assert result["domain"] == "CRUD Operations"
    assert len(result["flashcards"]) == 1
    assert result["flashcards"][0]["title"] == "insertOne() basics"


def test_get_remediation_caps_flashcards_to_limit():
    from certcoach.core import database

    question = {"_id": "q1", "metadata": {"topic_id": 2}, "provenance": {"citation": {}}}
    flashcards = [{"category": "CRUD Operations", "title": f"card {i}", "answer": ""} for i in range(10)]

    questions_col = MagicMock()
    questions_col.find_one.return_value = question

    with patch.object(database, "questions_col", questions_col):
        with patch.object(database, "load_flashcards", return_value=flashcards):
            result = database.get_remediation_for_wrong_attempt("q1", flashcard_limit=3)

    assert len(result["flashcards"]) == 3
    assert result["citation"] is None  # empty quote should not be surfaced as a citation


def test_get_remediation_returns_empty_when_question_not_found():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.find_one.return_value = None

    with patch.object(database, "questions_col", questions_col):
        result = database.get_remediation_for_wrong_attempt("missing")

    assert result == {"citation": None, "domain": None, "flashcards": []}
