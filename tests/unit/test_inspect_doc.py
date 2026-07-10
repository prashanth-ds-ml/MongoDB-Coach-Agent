from unittest.mock import MagicMock, patch


def test_chunk_doc_text_splits_on_headers_and_tags_section_path():
    from certcoach.jobs.inspect_doc import chunk_doc_text

    text = (
        "# BSON Types\n\n"
        "Intro paragraph about BSON types that is long enough to survive the minimum chunk filter.\n\n"
        "## ObjectId\n\n"
        "ObjectIds are small, likely unique, fast to generate, and ordered across a distributed system.\n\n"
        "## Date\n\n"
        "BSON Date is a 64-bit integer representing milliseconds since the Unix epoch, useful for range queries.\n"
    )

    chunks = chunk_doc_text(text, max_chunk_chars=8000)

    labels = [c["label"] for c in chunks]
    assert "BSON Types" in labels
    assert "BSON Types > ObjectId" in labels
    assert "BSON Types > Date" in labels
    assert all("text" in c and c["text"].strip() for c in chunks)


def test_chunk_doc_text_drops_tiny_sections():
    from certcoach.jobs.inspect_doc import chunk_doc_text

    text = "# Heading\n\nx\n\n## Real Section\n\nThis section has enough real content to clear the minimum chunk filter easily.\n"

    chunks = chunk_doc_text(text, max_chunk_chars=8000)

    assert all(len(c["text"]) >= 40 for c in chunks)
    assert any(c["label"] == "Heading > Real Section" for c in chunks)


def test_chunk_doc_text_splits_oversized_section_into_parts():
    from certcoach.jobs.inspect_doc import chunk_doc_text

    long_paragraph = "This sentence repeats to build a long section. " * 60
    text = f"# Big Section\n\n{long_paragraph}\n"

    chunks = chunk_doc_text(text, max_chunk_chars=500)

    assert len(chunks) > 1
    assert all(c["label"].startswith("Big Section (part") for c in chunks)
    assert all(len(c["text"]) <= 700 for c in chunks)


def test_load_topic_item_raises_for_unknown_topic():
    from certcoach.jobs.inspect_doc import load_topic_item

    with patch("certcoach.jobs.inspect_doc.planner") as mock_planner:
        mock_planner.load_syllabus.return_value = [{"id": 1, "md_files": ["a.md"]}]
        try:
            load_topic_item(99)
            assert False, "expected ValueError"
        except ValueError as exc:
            assert "99" in str(exc)


def test_resolve_concept_docs_delegates_to_shared_planner_helper():
    from certcoach.jobs.inspect_doc import resolve_concept_docs

    topic_item = {"md_files": ["unrelated.md", "delete_one.md", "delete_many.md"]}
    with patch("certcoach.jobs.inspect_doc.planner") as mock_planner:
        mock_planner.resolve_concept_docs.return_value = ["delete_one.md", "delete_many.md"]

        resolved = resolve_concept_docs(topic_item, "deleteOne()")

    mock_planner.resolve_concept_docs.assert_called_once_with(topic_item["md_files"], "deleteOne()")
    assert resolved == ["delete_one.md", "delete_many.md"]


def test_verify_candidate_reuses_database_verify_citation_across_resolved_files():
    from certcoach.jobs.inspect_doc import verify_candidate

    with patch("certcoach.jobs.inspect_doc.database") as mock_database:
        mock_database.verify_citation.side_effect = [
            (False, "not found in first.md"),
            (True, "citation verified"),
        ]

        ok, matched_file = verify_candidate(["first.md", "second.md"], "some verbatim quote")

    assert ok is True
    assert matched_file == "second.md"
    assert mock_database.verify_citation.call_count == 2


def test_verify_candidate_returns_false_for_empty_quote():
    from certcoach.jobs.inspect_doc import verify_candidate

    with patch("certcoach.jobs.inspect_doc.database") as mock_database:
        ok, matched_file = verify_candidate(["first.md"], "")

    assert ok is False
    assert matched_file == ""
    mock_database.verify_citation.assert_not_called()


def test_extract_candidate_facts_parses_json_response():
    from certcoach.jobs.inspect_doc import extract_candidate_facts

    mock_runner = MagicMock()
    mock_runner._call_model.return_value = (
        '{"facts": [{"quote": "a verbatim quote", "suggested_difficulty": "Easy", '
        '"suggested_response_type": "single", "suggested_style_type": "Type B", '
        '"rationale": "tests a rule"}]}'
    )
    with patch("certcoach.jobs.inspect_doc.get_model_runner", return_value=mock_runner):
        facts = extract_candidate_facts("some doc context", "deleteOne()", max_chars=1600)

    assert len(facts) == 1
    assert facts[0]["quote"] == "a verbatim quote"
    assert facts[0]["suggested_style_type"] == "Type B"


def test_extract_candidate_facts_returns_empty_list_when_model_returns_nothing():
    from certcoach.jobs.inspect_doc import extract_candidate_facts

    mock_runner = MagicMock()
    mock_runner._call_model.return_value = None
    with patch("certcoach.jobs.inspect_doc.get_model_runner", return_value=mock_runner):
        facts = extract_candidate_facts("some doc context", "deleteOne()", max_chars=1600)

    assert facts == []


def test_extract_candidate_facts_returns_empty_list_for_blank_context():
    from certcoach.jobs.inspect_doc import extract_candidate_facts

    mock_runner = MagicMock()
    with patch("certcoach.jobs.inspect_doc.get_model_runner", return_value=mock_runner):
        facts = extract_candidate_facts("   ", "deleteOne()", max_chars=1600)

    assert facts == []
    mock_runner._call_model.assert_not_called()


def test_inspect_concept_drops_unverified_candidates_and_keeps_verified():
    from certcoach.jobs.inspect_doc import inspect_concept

    topic_item = {"id": 1, "md_files": ["delete_one.md"]}

    with patch("certcoach.jobs.inspect_doc.planner") as mock_planner, \
         patch("certcoach.jobs.inspect_doc.database") as mock_database, \
         patch("certcoach.jobs.inspect_doc.get_model_runner") as mock_get_runner, \
         patch("certcoach.jobs.inspect_doc.weighted_target_for_concept") as mock_weighted_target:
        mock_planner.load_syllabus.return_value = [topic_item]
        mock_planner.resolve_concept_docs.return_value = ["delete_one.md"]
        mock_planner.load_md_context.return_value = (
            "Official doc text about deleteOne(), describing exactly one matching document removal."
        )
        mock_weighted_target.return_value = {"Easy": 4, "Medium": 3}

        mock_runner = MagicMock()
        mock_runner._call_model.return_value = (
            '{"facts": ['
            '{"quote": "verified fact quote", "suggested_difficulty": "Easy", "suggested_response_type": "single", "suggested_style_type": "Type B", "rationale": "r1"},'
            '{"quote": "unverifiable fact quote", "suggested_difficulty": "Medium", "suggested_response_type": "single", "suggested_style_type": "Type B", "rationale": "r2"}'
            ']}'
        )
        mock_get_runner.return_value = mock_runner

        mock_database.verify_citation.side_effect = [
            (True, "citation verified"),
            (False, "quote does not appear verbatim in the cited source file"),
        ]

        result = inspect_concept(topic_id=1, concept="deleteOne()", max_chars=1600)

    assert result["resolved_files"] == ["delete_one.md"]
    assert len(result["verified"]) == 1
    assert result["verified"][0]["quote"] == "verified fact quote"
    assert result["verified"][0]["matched_doc_file"] == "delete_one.md"
    assert result["verified"][0]["suggested_style_type"] == "Type B"
    assert len(result["dropped"]) == 1
    assert result["dropped"][0]["quote"] == "unverifiable fact quote"
    assert result["weighted_target"] == {"Easy": 4, "Medium": 3}
    mock_weighted_target.assert_called_once_with([topic_item], 1, "deleteOne()")

    assert len(result["chunks"]) == 1
    assert result["chunks"][0]["doc_file"] == "delete_one.md"
    assert len(result["chunks"][0]["verified"]) == 1
    assert len(result["chunks"][0]["dropped"]) == 1


def test_inspect_concept_clears_style_type_outside_topics_allowed_taxonomy():
    """Topic 1 is not syntax-heavy, so only Type B/D are valid. A model
    suggestion of "Type A" for this topic must be cleared to None, not
    trusted verbatim -- inspection reports what's achievable, it doesn't
    guess a style outside the topic's real taxonomy."""
    from certcoach.jobs.inspect_doc import inspect_concept

    topic_item = {"id": 1, "md_files": ["delete_one.md"]}

    with patch("certcoach.jobs.inspect_doc.planner") as mock_planner, \
         patch("certcoach.jobs.inspect_doc.database") as mock_database, \
         patch("certcoach.jobs.inspect_doc.get_model_runner") as mock_get_runner, \
         patch("certcoach.jobs.inspect_doc.weighted_target_for_concept") as mock_weighted_target:
        mock_planner.load_syllabus.return_value = [topic_item]
        mock_planner.resolve_concept_docs.return_value = ["delete_one.md"]
        mock_planner.load_md_context.return_value = (
            "Official doc text about deleteOne(), describing exactly one matching document removal."
        )
        mock_weighted_target.return_value = {"Easy": 4, "Medium": 3}

        mock_runner = MagicMock()
        mock_runner._call_model.return_value = (
            '{"facts": ['
            '{"quote": "verified fact quote", "suggested_difficulty": "Easy", '
            '"suggested_response_type": "single", "suggested_style_type": "Type A", "rationale": "r1"}'
            ']}'
        )
        mock_get_runner.return_value = mock_runner
        mock_database.verify_citation.return_value = (True, "citation verified")

        result = inspect_concept(topic_id=1, concept="deleteOne()", max_chars=1600)

    assert len(result["verified"]) == 1
    assert result["verified"][0]["suggested_style_type"] is None


def test_print_taxonomy_yield_report_counts_verified_facts_by_style_type(capsys):
    from certcoach.jobs.inspect_doc import print_taxonomy_yield_report

    result = {
        "topic_id": 1,
        "concept": "deleteOne()",
        "verified": [
            {"suggested_style_type": "Type B"},
            {"suggested_style_type": "Type B"},
            {"suggested_style_type": "Type D"},
            {"suggested_style_type": None},
        ],
    }

    print_taxonomy_yield_report(result, topic_id=1)
    output = capsys.readouterr().out

    assert "Type B" in output
    assert "Type D" in output
    assert "unclassified" in output
    # Topic 1 is not syntax-heavy -- Type A/C must not appear as allowed rows.
    assert "Type A" not in output
    assert "Type C" not in output
