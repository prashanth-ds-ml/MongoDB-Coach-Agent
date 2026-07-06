from certcoach.jobs import map_questions_to_docs as mod


def _topics_by_id():
    return {
        1: {
            "id": 1,
            "topic": "MongoDB Overview & The Document Model",
            "subtopics": ["BSON Data Types", "Document structure"],
            "md_files": [
                "topic_01_docs_manual_core_document__a8bd5970ef.md",
                "topic_01_docs_manual_reference_bson_types__cf63661090.md",
            ],
            "bank_topic_keys": ["BSON Data Types", "General"],
        }
    }


def _topics_by_bank_key(topics_by_id):
    by_key = {}
    for item in topics_by_id.values():
        for key in item.get("bank_topic_keys", []):
            by_key[key.lower()] = item
    return by_key


def test_resolve_topic_and_concept_prefers_stored_metadata():
    topics_by_id = _topics_by_id()
    question = {"metadata": {"topic_id": 1, "concept": "BSON Data Types"}}

    result = mod.resolve_topic_and_concept(question, topics_by_id, _topics_by_bank_key(topics_by_id))

    assert result == {
        "topic_id": 1,
        "topic_name": "MongoDB Overview & The Document Model",
        "concept": "BSON Data Types",
        "source": "stored",
    }


def test_resolve_topic_and_concept_infers_when_topic_id_missing():
    topics_by_id = _topics_by_id()
    question = {
        "metadata": {"topic_id": None, "topic": "BSON Data Types"},
        "question_text": "Which BSON data type represents a document field?",
        "options": [],
    }

    result = mod.resolve_topic_and_concept(question, topics_by_id, _topics_by_bank_key(topics_by_id))

    assert result["source"] == "inferred"
    assert result["topic_id"] == 1
    assert result["concept"] in {"BSON Data Types", "Document structure"}


def test_resolve_topic_and_concept_unresolved_when_no_candidate_topic():
    topics_by_id = _topics_by_id()
    question = {"metadata": {"topic_id": None, "topic": "Some Unrelated Legacy Label"}}

    result = mod.resolve_topic_and_concept(question, topics_by_id, _topics_by_bank_key(topics_by_id))

    assert result == {"topic_id": None, "topic_name": None, "concept": None, "source": "unresolved"}


def test_resolve_official_docs_returns_concept_exact_match():
    topics_by_id = _topics_by_id()

    docs, is_exact = mod.resolve_official_docs(1, "BSON Data Types", topics_by_id)

    assert is_exact is True
    assert "topic_01_docs_manual_reference_bson_types__cf63661090.md" in docs


def test_resolve_official_docs_falls_back_when_no_concept_scores():
    topics_by_id = _topics_by_id()

    docs, is_exact = mod.resolve_official_docs(1, "Some concept with no filename overlap", topics_by_id)

    assert is_exact is False
    assert docs == topics_by_id[1]["md_files"][:2]


def test_resolve_official_docs_empty_for_unknown_topic():
    docs, is_exact = mod.resolve_official_docs(None, "BSON Data Types", {})

    assert docs == []
    assert is_exact is False


def test_current_citation_doc_prefers_provenance_over_legacy_field():
    question = {
        "provenance": {"citation": {"doc_file": "real_doc.md"}},
        "metadata": {"citation_source": "Some Human Title"},
    }

    assert mod.current_citation_doc(question) == "real_doc.md"


def test_current_citation_doc_falls_back_to_legacy_citation_source():
    question = {"metadata": {"citation_source": "Some Human Title"}}

    assert mod.current_citation_doc(question) == "Some Human Title"
