from unittest.mock import MagicMock, patch


def test_style_weights_for_topic_syntax_heavy_gets_full_taxonomy():
    from certcoach.jobs.generate_from_doc import style_weights_for_topic

    weights = style_weights_for_topic(3)  # CRUD Read, syntax-heavy

    assert set(weights) == {"Type A", "Type B", "Type C", "Type D"}
    assert sum(weights.values()) == 1.0


def test_style_weights_for_topic_concept_only_gets_reduced_taxonomy():
    from certcoach.jobs.generate_from_doc import style_weights_for_topic

    weights = style_weights_for_topic(1)  # Overview & Document Model, concept-only

    assert set(weights) == {"Type B", "Type D"}
    assert weights["Type B"] == 0.70
    assert weights["Type D"] == 0.30


def test_select_generation_targets_picks_first_verified_fact_per_section():
    from certcoach.jobs.generate_from_doc import select_generation_targets

    chunks = [
        {
            "label": "ObjectId", "doc_file": "bson.md", "text": "objectid text",
            "verified": [
                {"quote": "first quote", "suggested_difficulty": "Easy", "suggested_style_type": "Type B"},
                {"quote": "second quote", "suggested_difficulty": "Medium"},
            ],
        },
        {"label": "Empty Section", "doc_file": "bson.md", "text": "empty", "verified": []},
        {
            "label": "Date", "doc_file": "bson.md", "text": "date text",
            "verified": [{"quote": "date quote", "suggested_difficulty": "Medium"}],
        },
    ]

    selected = select_generation_targets(chunks, max_questions=8)

    assert len(selected) == 2
    assert selected[0]["chunk_label"] == "ObjectId"
    assert selected[0]["difficulty"] == "Easy"
    assert selected[0]["suggested_style_type"] == "Type B"
    assert selected[1]["chunk_label"] == "Date"
    assert selected[1]["difficulty"] == "Medium"
    assert selected[1]["suggested_style_type"] is None


def test_select_generation_targets_caps_at_max_questions():
    from certcoach.jobs.generate_from_doc import select_generation_targets

    chunks = [
        {"label": f"Section {i}", "doc_file": "d.md", "text": "t", "verified": [{"quote": "q", "suggested_difficulty": "Easy"}]}
        for i in range(10)
    ]

    selected = select_generation_targets(chunks, max_questions=3)

    assert len(selected) == 3
    assert [s["chunk_label"] for s in selected] == ["Section 0", "Section 1", "Section 2"]


def test_select_generation_targets_defaults_missing_difficulty_to_medium():
    from certcoach.jobs.generate_from_doc import select_generation_targets

    chunks = [{"label": "S", "doc_file": "d.md", "text": "t", "verified": [{"quote": "q"}]}]

    selected = select_generation_targets(chunks, max_questions=8)

    assert selected[0]["difficulty"] == "Medium"


def test_assign_style_types_falls_back_to_weighted_random_when_no_suggestion():
    """No suggested_style_type on the target (inspection couldn't classify
    it, or it suggested something outside this topic's taxonomy and
    inspect_doc already cleared it) -- assign_style_types must fall back to
    the topic's weighted-random draw, same as before this feature existed."""
    from certcoach.jobs.generate_from_doc import assign_style_types

    selected = [{"chunk_label": "S0"}, {"chunk_label": "S1"}]

    with patch("certcoach.jobs.generate_from_doc.random.choices") as mock_choices:
        mock_choices.side_effect = [["Type B"], ["Type D"]]
        assign_style_types(selected, topic_id=1)  # concept-only -> Type B/D only

    assert selected[0]["style_type"] == "Type B"
    assert selected[0]["style_source"] == "fallback"
    assert selected[1]["style_type"] == "Type D"
    assert selected[1]["style_source"] == "fallback"
    for call in mock_choices.call_args_list:
        assert call.args[0] == ["Type B", "Type D"]
        assert call.kwargs["weights"] == [0.70, 0.30]


def test_assign_style_types_prefers_content_aware_suggestion_over_random():
    """A target with a valid suggested_style_type for its topic (i.e. what
    inspect_doc's fact-extraction actually said the chunk supports) must be
    used directly, without ever consulting the random weighted draw."""
    from certcoach.jobs.generate_from_doc import assign_style_types

    selected = [{"chunk_label": "S0", "suggested_style_type": "Type D"}]

    with patch("certcoach.jobs.generate_from_doc.random.choices") as mock_choices:
        assign_style_types(selected, topic_id=1)  # concept-only -> Type B/D only

    assert selected[0]["style_type"] == "Type D"
    assert selected[0]["style_source"] == "content"
    mock_choices.assert_not_called()


def test_assign_style_types_falls_back_when_suggestion_is_invalid_for_topic():
    """A suggested_style_type that isn't valid for this topic (e.g. "Type A"
    for a concept-only topic) must not be trusted -- falls back to weighted
    random, same as a missing suggestion."""
    from certcoach.jobs.generate_from_doc import assign_style_types

    selected = [{"chunk_label": "S0", "suggested_style_type": "Type A"}]

    with patch("certcoach.jobs.generate_from_doc.random.choices", return_value=["Type B"]) as mock_choices:
        assign_style_types(selected, topic_id=1)  # concept-only -> Type A not allowed

    assert selected[0]["style_type"] == "Type B"
    assert selected[0]["style_source"] == "fallback"
    mock_choices.assert_called_once()


def test_assign_style_types_all_results_are_valid_for_the_topic():
    from certcoach.jobs.generate_from_doc import assign_style_types, style_weights_for_topic

    selected = [{"chunk_label": f"S{i}"} for i in range(20)]
    assign_style_types(selected, topic_id=3)  # syntax-heavy -> full Type A-D taxonomy

    valid_styles = set(style_weights_for_topic(3))
    assert all(item["style_type"] in valid_styles for item in selected)


def test_generate_one_retries_on_low_quality_then_succeeds():
    from certcoach.jobs.generate_from_doc import generate_one

    good_question = {"_id": "q1", "question_text": "A real question"}
    bad_question = {"_id": "q0", "question_text": "A bad question"}

    with patch("certcoach.jobs.generate_from_doc.generate_weighted_question") as mock_generate, \
         patch("certcoach.jobs.generate_from_doc.validate_question_quality") as mock_validate, \
         patch("certcoach.jobs.generate_from_doc.is_duplicate_question") as mock_dup:
        mock_generate.side_effect = [bad_question, good_question]
        mock_validate.side_effect = [(False, ["too short"]), (True, [])]
        mock_dup.return_value = (False, "")

        question, reason = generate_one(
            target=MagicMock(), context_text="ctx", citation_source="doc.md",
            local_llm_url="http://x", avoid_questions=[], max_attempts=3,
        )

    assert question == good_question
    assert reason == ""
    assert mock_generate.call_count == 2


def test_generate_one_gives_up_after_max_attempts():
    from certcoach.jobs.generate_from_doc import generate_one

    with patch("certcoach.jobs.generate_from_doc.generate_weighted_question", return_value=None) as mock_generate:
        question, reason = generate_one(
            target=MagicMock(), context_text="ctx", citation_source="doc.md",
            local_llm_url="http://x", avoid_questions=[], max_attempts=2,
        )

    assert question is None
    assert "2 attempts" in reason
    assert mock_generate.call_count == 2


def test_generate_from_concept_orchestrates_selection_generation_and_persistence():
    from certcoach.jobs.generate_from_doc import generate_from_concept

    topic_item = {
        "id": 1, "topic": "MongoDB Overview & The Document Model",
        "bank_topic_keys": ["Topic 1"], "md_files": ["bson.md"],
    }
    dry_run_result = {
        "chunks": [
            {
                "label": "ObjectId", "doc_file": "bson.md", "text": "objectid text",
                "verified": [{"quote": "q1", "suggested_difficulty": "Easy"}],
                "dropped": [],
            },
            {"label": "Empty", "doc_file": "bson.md", "text": "t", "verified": [], "dropped": []},
        ],
    }
    generated_question = {
        "_id": "certcoach-t01-objectid-easy-001-abc",
        "question_text": "Q",
        "metadata": {},
    }

    with patch("certcoach.jobs.generate_from_doc.database") as mock_database, \
         patch("certcoach.jobs.generate_from_doc._load_env", return_value=("model", "http://localhost:11434")), \
         patch("certcoach.jobs.generate_from_doc.inspect_doc") as mock_inspect_doc, \
         patch("certcoach.jobs.generate_from_doc.generate_weighted_question", return_value=generated_question), \
         patch("certcoach.jobs.generate_from_doc.validate_question_quality", return_value=(True, [])), \
         patch("certcoach.jobs.generate_from_doc.is_duplicate_question", return_value=(False, "")), \
         patch("certcoach.jobs.generate_from_doc.run_generation_pipeline_checks") as mock_pipeline_checks, \
         patch("certcoach.jobs.repair_explanations.generate_repair", return_value=None):
        mock_inspect_doc.load_topic_item.return_value = topic_item
        mock_inspect_doc.inspect_concept.return_value = dry_run_result
        mock_database.questions_col.find_one.return_value = generated_question

        result = generate_from_concept(topic_id=1, concept="BSON Data Types", max_questions=8, max_attempts=1)

    assert result["sections_with_verified_facts"] == 1
    assert result["selected_count"] == 1
    # No suggested_style_type in the fixture fact -> style assignment fell back to weighted random.
    assert result["content_aware_style_count"] == 0
    assert result["fallback_style_count"] == 1
    assert len(result["inserted"]) == 1
    assert result["inserted"][0]["question_id"] == "certcoach-t01-objectid-easy-001-abc"
    # generate_repair returned None (no repair) -> provenance stays "draft", pipeline checks never run.
    assert result["inserted"][0]["provenance_state"] == "draft"
    assert result["sourced_count"] == 0
    mock_pipeline_checks.assert_not_called()
    mock_database.questions_col.insert_one.assert_called_once_with(generated_question)


def test_generate_from_concept_skips_target_that_never_generates_successfully():
    from certcoach.jobs.generate_from_doc import generate_from_concept

    topic_item = {"id": 1, "topic": "Topic 1", "bank_topic_keys": ["Topic 1"], "md_files": ["bson.md"]}
    dry_run_result = {
        "chunks": [
            {
                "label": "ObjectId", "doc_file": "bson.md", "text": "objectid text",
                "verified": [{"quote": "q1", "suggested_difficulty": "Easy"}],
                "dropped": [],
            },
        ],
    }

    with patch("certcoach.jobs.generate_from_doc.database") as mock_database, \
         patch("certcoach.jobs.generate_from_doc._load_env", return_value=("model", "http://localhost:11434")), \
         patch("certcoach.jobs.generate_from_doc.inspect_doc") as mock_inspect_doc, \
         patch("certcoach.jobs.generate_from_doc.generate_weighted_question", return_value=None):
        mock_inspect_doc.load_topic_item.return_value = topic_item
        mock_inspect_doc.inspect_concept.return_value = dry_run_result

        result = generate_from_concept(topic_id=1, concept="BSON Data Types", max_questions=8, max_attempts=2)

    assert result["inserted"] == []
    assert len(result["skipped"]) == 1
    assert result["skipped"][0]["chunk_label"] == "ObjectId"
    mock_database.questions_col.insert_one.assert_not_called()
