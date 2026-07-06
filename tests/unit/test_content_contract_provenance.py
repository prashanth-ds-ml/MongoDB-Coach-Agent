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
