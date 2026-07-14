import os

import pytest
from unittest.mock import MagicMock, patch


def test_provenance_metadata_defaults_to_draft():
    from certcoach.core.content_contract import provenance_metadata

    provenance = provenance_metadata()

    assert provenance["state"] == "draft"
    assert provenance["citation"] == {"doc_file": "", "quote": ""}
    assert provenance["confirmed_by"] is None
    assert provenance["confirmed_at"] is None


def test_provenance_metadata_rejects_unknown_state():
    from certcoach.core.content_contract import provenance_metadata

    with pytest.raises(ValueError):
        provenance_metadata(state="verified")  # not one of the four real states


def test_is_confirmed_true_only_for_confirmed_state():
    from certcoach.core.content_contract import is_confirmed

    assert is_confirmed({"provenance": {"state": "confirmed"}}) is True
    assert is_confirmed({"provenance": {"state": "draft"}}) is False
    assert is_confirmed({"provenance": {"state": "sourced"}}) is False
    assert is_confirmed({"provenance": {"state": "suspect"}}) is False


def test_is_confirmed_false_when_provenance_missing():
    from certcoach.core.content_contract import is_confirmed

    # Pre-migration questions have no provenance field at all -- must not be
    # treated as confirmed just because the field is absent.
    assert is_confirmed({}) is False
    assert is_confirmed(None) is False


def test_is_practice_ready_requires_both_contract_active_and_confirmed():
    from certcoach.core import database

    contract_active_and_confirmed = {
        "metadata": {"content_contract_version": 2, "content_contract_status": "generated"},
        "provenance": {"state": "confirmed"},
    }
    contract_active_but_draft = {
        "metadata": {"content_contract_version": 2, "content_contract_status": "generated"},
        "provenance": {"state": "draft"},
    }
    confirmed_but_not_contract_active = {
        "metadata": {},  # no content_contract_version -> is_contract_active() is False
        "provenance": {"state": "confirmed"},
    }

    assert database.is_practice_ready(contract_active_and_confirmed) is True
    assert database.is_practice_ready(contract_active_but_draft) is False
    assert database.is_practice_ready(confirmed_but_not_contract_active) is False


# Uses a real, stable file already in the repo rather than monkeypatching
# filesystem lookups -- os.path.dirname is called too broadly elsewhere in
# the process to safely patch globally in a test.
REAL_SOURCE_FILE = "topic_05_docs_languages_python_pymongo_driver_current_crud_delete__8c58393d1b.md"


def test_verify_citation_true_when_quote_appears_verbatim_in_source():
    from certcoach.core import database

    question = {
        "provenance": {
            "citation": {
                "doc_file": REAL_SOURCE_FILE,
                "quote": "removes one or more documents from a MongoDB collection",
            }
        }
    }

    verified, message = database.verify_citation(question)

    assert verified is True
    assert "verified" in message


def test_verify_citation_true_when_quote_drops_source_markdown_backticks():
    """A model copying a quote verbatim naturally reproduces the words, not the
    source doc's markdown inline-code backticks around technical terms -- that
    must not count as a fabricated quote. Regression for a real generation run
    where a genuinely verbatim quote of the BSON types doc's `$type`/`number`
    sentence failed only because the doc wraps those terms in backticks."""
    from certcoach.core import database

    question = {
        "provenance": {
            "citation": {
                "doc_file": "topic_01_docs_manual_reference_bson_types__cf63661090.md",
                "quote": "$type also supports the number alias, which matches the integer, decimal, double, and long BSON types.",
            }
        }
    }

    verified, message = database.verify_citation(question)

    assert verified is True
    assert "verified" in message


def test_verify_citation_false_when_quote_is_fabricated():
    from certcoach.core import database

    question = {
        "provenance": {
            "citation": {
                "doc_file": REAL_SOURCE_FILE,
                "quote": "this exact sentence does not appear anywhere in the source",
            }
        }
    }

    verified, message = database.verify_citation(question)

    assert verified is False


def test_verify_citation_false_when_source_file_does_not_exist():
    from certcoach.core import database

    question = {
        "provenance": {
            "citation": {
                "doc_file": "does_not_exist_anywhere.md",
                "quote": "anything",
            }
        }
    }

    verified, message = database.verify_citation(question)

    assert verified is False
    assert "not found" in message


def test_verify_citation_false_when_citation_missing():
    from certcoach.core import database

    assert database.verify_citation({}) == (False, "missing citation doc_file or quote")


def test_verify_citation_checks_pics_qa_transcripts_as_a_fallback_source(tmp_path):
    from certcoach.core import database

    here = os.path.dirname(os.path.abspath(database.__file__))
    transcript_dir = os.path.join(here, "..", "data", "pics_qa_transcripts")
    os.makedirs(transcript_dir, exist_ok=True)
    transcript_path = os.path.join(transcript_dir, "__test_transcript__.md")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write("insert_one() inserts a single document into a collection.")

    try:
        question = {
            "provenance": {
                "citation": {
                    "doc_file": "__test_transcript__.md",
                    "quote": "insert_one() inserts a single document",
                }
            }
        }
        verified, message = database.verify_citation(question)
    finally:
        os.remove(transcript_path)

    assert verified is True
    assert "verified" in message


def test_get_citation_excerpt_locates_quote_in_its_source_paragraph():
    from certcoach.core import database

    question = {
        "provenance": {
            "citation": {
                "doc_file": "topic_01_docs_manual_reference_bson_types__cf63661090.md",
                "quote": "$type also supports the number alias, which matches the integer, decimal, double, and long BSON types.",
            }
        }
    }

    excerpt = database.get_citation_excerpt(question)

    assert excerpt["verified"] is True
    # The doc wraps `number` in backticks -- the excerpt must preserve that
    # original markdown formatting rather than silently normalizing it away,
    # since the frontend renders it as inline code.
    assert "`number` alias" in excerpt["excerpt_match"]
    # The source paragraph (one bulleted list item) also contains the
    # sentence before the quote, which must land in excerpt_before rather
    # than being swallowed by the match. The quote is the last sentence in
    # its bullet, so excerpt_after is empty -- the next bullet is a separate
    # paragraph and must not bleed in.
    assert "supports using these values to query fields" in excerpt["excerpt_before"]
    assert excerpt["excerpt_after"] == ""


def test_get_citation_excerpt_falls_back_when_quote_not_found():
    from certcoach.core import database

    question = {
        "provenance": {
            "citation": {
                "doc_file": REAL_SOURCE_FILE,
                "quote": "this exact sentence does not appear anywhere in the source",
            }
        }
    }

    excerpt = database.get_citation_excerpt(question)

    assert excerpt["verified"] is False
    assert excerpt["excerpt_match"] == question["provenance"]["citation"]["quote"]
    assert excerpt["excerpt_before"] == ""
    assert excerpt["excerpt_after"] == ""


def test_get_citation_excerpt_handles_missing_citation():
    from certcoach.core import database

    excerpt = database.get_citation_excerpt({})

    assert excerpt == {
        "doc_file": "",
        "quote": "",
        "verified": False,
        "message": "missing citation doc_file or quote",
        "excerpt_before": "",
        "excerpt_match": "",
        "excerpt_after": "",
    }


def test_confirm_question_sets_state_and_confirmed_by():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.update_one.return_value = MagicMock(matched_count=1)

    with patch.object(database, "questions_col", questions_col):
        result = database.confirm_question("q1", "local_user_1")

    assert result is True
    args, kwargs = questions_col.update_one.call_args
    assert args[0] == {"_id": "q1"}
    assert args[1]["$set"]["provenance.state"] == "confirmed"
    assert args[1]["$set"]["provenance.confirmed_by"] == "local_user_1"


def test_mark_question_suspect_sets_state_and_reason():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.update_one.return_value = MagicMock(matched_count=1)

    with patch.object(database, "questions_col", questions_col):
        result = database.mark_question_suspect("q1", "distractor B is also correct")

    assert result is True
    args, kwargs = questions_col.update_one.call_args
    assert args[1]["$set"]["provenance.state"] == "suspect"
    assert args[1]["$set"]["provenance.suspect_reason"] == "distractor B is also correct"


def test_add_question_review_note_pushes_note_with_decision():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.update_one.return_value = MagicMock(matched_count=1)

    with patch.object(database, "questions_col", questions_col):
        result = database.add_question_review_note("q1", "explanation could show an example", "confirmed")

    assert result is True
    args, kwargs = questions_col.update_one.call_args
    assert args[0] == {"_id": "q1"}
    pushed = args[1]["$push"]["review_notes"]
    assert pushed["note"] == "explanation could show an example"
    assert pushed["decision"] == "confirmed"
    assert pushed["actioned"] is False
    assert "reviewed_at" in pushed


def test_add_question_review_note_skips_blank_notes():
    from certcoach.core import database

    questions_col = MagicMock()

    with patch.object(database, "questions_col", questions_col):
        result = database.add_question_review_note("q1", "   ", "skipped")

    assert result is False
    questions_col.update_one.assert_not_called()


def test_get_open_review_notes_excludes_actioned_entries():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.find.return_value = [
        {
            "_id": "q1",
            "question_text": "What does find() return?",
            "metadata": {"topic_id": 3, "concept": "find()"},
            "review_notes": [
                {"note": "add a code example", "decision": "confirmed", "reviewed_at": "t1", "actioned": False},
                {"note": "already fixed this one", "decision": "confirmed", "reviewed_at": "t0", "actioned": True},
            ],
        }
    ]

    with patch.object(database, "questions_col", questions_col):
        open_notes = database.get_open_review_notes()

    assert len(open_notes) == 1
    assert open_notes[0]["question_id"] == "q1"
    assert open_notes[0]["note"] == "add a code example"
    assert open_notes[0]["concept"] == "find()"


def test_get_open_review_notes_scopes_by_topic_and_concept():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.find.return_value = []

    with patch.object(database, "questions_col", questions_col):
        database.get_open_review_notes(topic_id=3, concept="find()")

    query = questions_col.find.call_args[0][0]
    assert query["metadata.topic_id"] == 3
    assert query["metadata.concept"] == "find()"


def test_resolve_review_note_marks_matching_note_actioned():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.update_one.return_value = MagicMock(matched_count=1)

    with patch.object(database, "questions_col", questions_col):
        result = database.resolve_review_note("q1", "t1")

    assert result is True
    args, kwargs = questions_col.update_one.call_args
    assert args[0] == {"_id": "q1", "review_notes.reviewed_at": "t1"}
    assert args[1]["$set"]["review_notes.$.actioned"] is True


def test_get_questions_for_review_only_includes_draft_and_sourced():
    from certcoach.core import database

    questions_col = MagicMock()
    cursor = MagicMock()
    cursor.sort.return_value = cursor
    cursor.limit.return_value = ["placeholder"]
    questions_col.find.return_value = cursor

    with patch.object(database, "questions_col", questions_col):
        database.get_questions_for_review(limit=10)

    query = questions_col.find.call_args[0][0]
    assert query["provenance.state"] == {"$in": ["draft", "sourced"]}


def test_get_questions_for_review_can_scope_to_a_single_concept():
    from certcoach.core import database

    questions_col = MagicMock()
    cursor = MagicMock()
    cursor.sort.return_value = cursor
    cursor.limit.return_value = []
    questions_col.find.return_value = cursor

    with patch.object(database, "questions_col", questions_col):
        database.get_questions_for_review(limit=10, topic_id=1, concept="BSON Data Types")

    query = questions_col.find.call_args[0][0]
    assert query["metadata.topic_id"] == 1
    assert query["metadata.concept"] == "BSON Data Types"


def test_count_questions_for_review_can_scope_to_a_single_concept():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.count_documents.return_value = 2

    with patch.object(database, "questions_col", questions_col):
        result = database.count_questions_for_review(topic_id=1, concept="BSON Data Types")

    query = questions_col.count_documents.call_args[0][0]
    assert query["metadata.concept"] == "BSON Data Types"
    assert result == 2


def test_get_review_queue_summary_groups_by_topic_and_concept():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.aggregate.return_value = [
        {"_id": {"topic_id": 1, "concept": "BSON Data Types"}, "count": 14},
        {"_id": {"topic_id": 2, "concept": "insertOne()"}, "count": 11},
    ]

    with patch.object(database, "questions_col", questions_col):
        summary = database.get_review_queue_summary()

    assert summary == [
        {"topic_id": 1, "concept": "BSON Data Types", "count": 14},
        {"topic_id": 2, "concept": "insertOne()", "count": 11},
    ]
    pipeline = questions_col.aggregate.call_args[0][0]
    assert pipeline[0]["$match"]["provenance.state"] == {"$in": ["draft", "sourced"]}


def test_get_review_queue_summary_empty_when_nothing_pending():
    from certcoach.core import database

    questions_col = MagicMock()
    questions_col.aggregate.return_value = []

    with patch.object(database, "questions_col", questions_col):
        summary = database.get_review_queue_summary()

    assert summary == []


def test_add_quick_note_inserts_timestamped_note():
    from certcoach.core import database

    quick_notes_col = MagicMock()

    with patch.object(database, "quick_notes_col", quick_notes_col):
        result = database.add_quick_note("user1", "check() ignores partial indexes")

    assert result is True
    args, kwargs = quick_notes_col.insert_one.call_args
    doc = args[0]
    assert doc["user_id"] == "user1"
    assert doc["note"] == "check() ignores partial indexes"
    assert "created_at" in doc


def test_add_quick_note_skips_blank_notes():
    from certcoach.core import database

    quick_notes_col = MagicMock()

    with patch.object(database, "quick_notes_col", quick_notes_col):
        result = database.add_quick_note("user1", "   ")

    assert result is False
    quick_notes_col.insert_one.assert_not_called()


def test_get_quick_notes_returns_most_recent_first():
    from certcoach.core import database

    quick_notes_col = MagicMock()
    cursor = MagicMock()
    quick_notes_col.find.return_value = cursor
    cursor.sort.return_value = cursor
    cursor.limit.return_value = [{"note": "b"}, {"note": "a"}]

    with patch.object(database, "quick_notes_col", quick_notes_col):
        notes = database.get_quick_notes("user1")

    quick_notes_col.find.assert_called_once_with({"user_id": "user1"})
    cursor.sort.assert_called_once_with("created_at", -1)
    cursor.limit.assert_called_once_with(500)
    assert notes == [{"note": "b"}, {"note": "a"}]


def test_get_provenance_counts_tallies_each_state_scoped_to_concept():
    from certcoach.core import database

    questions_col = MagicMock()
    # One count_documents call per state (draft/sourced/confirmed/suspect), in that order.
    questions_col.count_documents.side_effect = [2, 1, 0, 29]

    with patch.object(database, "questions_col", questions_col):
        counts = database.get_provenance_counts(topic_id=1, concept="BSON Data Types")

    assert counts == {"draft": 2, "sourced": 1, "confirmed": 0, "suspect": 29}
    # Every call must be scoped to the requested topic/concept, not the whole bank.
    for call in questions_col.count_documents.call_args_list:
        query = call[0][0]
        assert query["metadata.topic_id"] == 1
        assert query["metadata.concept"] == "BSON Data Types"


def test_get_legacy_reference_questions_scopes_to_suspect_state_and_concept():
    from certcoach.core import database

    questions_col = MagicMock()
    cursor = MagicMock()
    cursor.limit.return_value = ["placeholder"]
    questions_col.find.return_value = cursor

    with patch.object(database, "questions_col", questions_col):
        result = database.get_legacy_reference_questions(topic_id=1, concept="BSON Data Types", limit=10)

    query = questions_col.find.call_args[0][0]
    assert query["provenance.state"] == "suspect"
    assert query["metadata.topic_id"] == 1
    assert query["metadata.concept"] == "BSON Data Types"
    cursor.limit.assert_called_once_with(10)
    assert result == ["placeholder"]


def test_get_legacy_reference_questions_returns_empty_without_full_scope():
    from certcoach.core import database

    questions_col = MagicMock()

    with patch.object(database, "questions_col", questions_col):
        assert database.get_legacy_reference_questions(topic_id=None, concept="BSON Data Types") == []
        assert database.get_legacy_reference_questions(topic_id=1, concept=None) == []

    questions_col.find.assert_not_called()
