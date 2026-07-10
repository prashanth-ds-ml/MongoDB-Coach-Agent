from unittest.mock import MagicMock, patch


def _active_question(question_id: str, concept: str) -> dict:
    return {
        "_id": question_id,
        "question_text": question_id,
        "metadata": {
            "topic_id": 1,
            "concept": concept,
            "content_contract_version": 2,
            "content_contract_status": "generated",
        },
        # Practice-readiness now requires BOTH contract-active AND human-confirmed
        # provenance (see database.is_practice_ready) -- these fixtures represent
        # questions that have already been through the confirm review screen.
        "provenance": {"state": "confirmed"},
    }


def test_strict_concept_retrieval_does_not_fall_back_to_topic_pool():
    from certcoach.core import database

    direct = _active_question("direct", "Concept A")
    questions_col = MagicMock()
    questions_col.find.return_value = [direct]

    with patch.object(database, "questions_col", questions_col):
        result = database.get_random_questions(
            topic_id=1,
            concepts=["Concept A"],
            strict_keywords=True,
            limit=5,
        )

    assert result == [direct]
    questions_col.find.assert_called_once_with({
        "metadata.topic_id": 1,
        "metadata.concept": {"$in": ["Concept A"]},
    })


def test_active_question_count_excludes_legacy_and_quarantined_records():
    from certcoach.core import database

    active = _active_question("active", "Concept A")
    legacy = {
        "_id": "legacy",
        "metadata": {"topic_id": 1, "concept": "Concept A"},
    }
    quarantined = _active_question("quarantined", "Concept A")
    quarantined["metadata"]["content_contract_status"] = "quarantined"

    questions_col = MagicMock()
    questions_col.find.return_value = [active, legacy, quarantined]

    with patch.object(database, "questions_col", questions_col):
        count = database.get_active_question_count(topic_id=1, concepts=["Concept A"])

    assert count == 1


def test_active_question_counts_by_difficulty_normalizes_and_excludes_inactive():
    from certcoach.core import database

    easy = _active_question("easy", "Concept A")
    easy["metadata"]["difficulty"] = "easy"
    medium = _active_question("medium", "Concept A")
    medium["metadata"]["difficulty"] = "Medium"
    hard = _active_question("hard", "Concept A")
    hard["metadata"]["difficulty"] = "HARD"
    legacy = {"_id": "legacy", "metadata": {"topic_id": 1, "concept": "Concept A", "difficulty": "Easy"}}

    questions_col = MagicMock()
    questions_col.find.return_value = [easy, medium, hard, legacy]

    with patch.object(database, "questions_col", questions_col):
        counts = database.get_active_question_counts_by_difficulty(topic_id=1, concepts=["Concept A"])

    assert counts == {"Easy": 1, "Medium": 1, "Hard": 1, "Other": 0}


def test_concept_lesson_context_uses_only_relevant_files_when_available(tmp_path):
    from certcoach.core import planner

    original_data_dir = planner.DATA_DIR
    try:
        planner.DATA_DIR = str(tmp_path)
        cleaned_dir = tmp_path / "cleaned_markdowns"
        cleaned_dir.mkdir()
        (cleaned_dir / "insertone_reference.md").write_text("insertOne concept", encoding="utf-8")
        (cleaned_dir / "unrelated_indexes.md").write_text("unrelated index content", encoding="utf-8")

        context = planner.load_md_context(
            ["unrelated_indexes.md", "insertone_reference.md"],
            prioritize_concept="insertOne()",
        )

        assert "insertOne concept" in context
        assert "unrelated index content" not in context
    finally:
        planner.DATA_DIR = original_data_dir


def test_score_md_file_for_concept_matches_bare_dollar_operator_names():
    """A concept that is just a bare operator name (e.g. '$set') must still
    match its own dedicated reference doc, whose filename never contains the
    literal '$' character (e.g. ..._operator_update_set__....md). Regression
    for a real gap found while mapping the syllabus to official docs: every
    bare-operator concept in Topics 4/7/8 ($set, $push, $inc, $unset,
    $elemMatch, $match, $group, ...) was scoring 0 against its correct doc and
    silently falling back to a generic topic-level doc instead."""
    from certcoach.core import planner

    assert planner.score_md_file_for_concept(
        "topic_04_docs_manual_reference_operator_update_set__0d2334e3f5.md", "$set"
    ) > 0
    assert planner.score_md_file_for_concept(
        "topic_07_docs_manual_reference_operator_query_elemmatch__1986be12b6.md", "$elemMatch"
    ) > 0
    assert planner.score_md_file_for_concept(
        "topic_08_docs_manual_reference_operator_aggregation_match__f0bbcf2597.md", "$match"
    ) > 0


def test_resolve_concept_docs_drops_generic_token_false_positives():
    """Regression for a real bug found live: 'BSON Data Types' tokenizes to
    ['bson', 'data', 'types'], and the generic 'data' token alone was enough
    to score topic-level filler docs (core_data_modeling_introduction,
    core_databases_and_collections) above the score>0 threshold purely because
    'data' is a substring of their filenames -- both got concatenated into the
    lesson/generation context alongside the real BSON-types doc. Requiring a
    candidate to reach half the top score for the concept excludes these
    single-token coincidental matches (score 10) while keeping the real match
    (score 25, matching both 'bson' and 'types')."""
    from certcoach.core import planner

    md_files = [
        "topic_01_docs_manual_core_data_modeling_introduction__c1bfc595e5.md",
        "topic_01_docs_manual_core_databases_and_collections__6c0162b19c.md",
        "topic_01_docs_manual_core_document__a8bd5970ef.md",
        "topic_01_docs_manual_reference_bson_types__cf63661090.md",
    ]

    resolved = planner.resolve_concept_docs(md_files, "BSON Data Types")

    assert resolved == ["topic_01_docs_manual_reference_bson_types__cf63661090.md"]


def test_resolve_concept_docs_keeps_all_tied_top_scores():
    """A concept whose docs are genuinely tied for the top score (e.g. the
    three cursor docs for sort/limit/skip) must all survive the relative
    threshold, not just the first one -- otherwise a real multi-doc concept
    would be wrongly narrowed to a single file."""
    from certcoach.core import planner

    md_files = [
        "topic_03_docs_manual_reference_method_cursor_limit__fadfb5c4f7.md",
        "topic_03_docs_manual_reference_method_cursor_skip__b2de4f9998.md",
        "topic_03_docs_manual_reference_method_cursor_sort__fe46cee93b.md",
    ]

    resolved = planner.resolve_concept_docs(md_files, "sort/limit/skip")

    assert set(resolved) == set(md_files)


def test_resolve_concept_docs_falls_back_to_first_two_when_nothing_scores():
    from certcoach.core import planner

    resolved = planner.resolve_concept_docs(["a.md", "b.md", "c.md"], "totally unrelated concept")

    assert resolved == ["a.md", "b.md"]


def test_resolve_concept_docs_caps_at_max_files():
    from certcoach.core import planner

    md_files = [f"topic_09_docs_manual_core_index_{name}__abc123.md" for name in ("single", "compound", "multikey", "hashed")]

    resolved = planner.resolve_concept_docs(md_files, "index", max_files=3)

    assert len(resolved) <= 3


def test_topic_benchmark_context_loads_topic_record(tmp_path):
    from certcoach.core import planner

    original_memory_dir = planner.MEMORY_DIR
    try:
        planner.MEMORY_DIR = str(tmp_path)
        (tmp_path / "topic_01_benchmark.md").write_text("Topic 1 benchmark content", encoding="utf-8")

        benchmark = planner.load_topic_benchmark_context(1, "BSON Data Types")

        assert "Topic 1 benchmark content" in benchmark
        assert "BSON Data Types" in benchmark
        assert "Benchmark context for Topic 1" in benchmark
    finally:
        planner.MEMORY_DIR = original_memory_dir


def test_topic_benchmark_focus_loads_weak_focus_section(tmp_path):
    from certcoach.core import planner

    original_memory_dir = planner.MEMORY_DIR
    try:
        planner.MEMORY_DIR = str(tmp_path)
        (tmp_path / "topic_01_benchmark.md").write_text(
            "# Topic 1 Benchmark Record\n\n- `weak_focus`:\n  - BSON vs JSON\n  - collections vs tables\n\n- `generation_notes`:\n  - keep short\n",
            encoding="utf-8",
        )

        focus = planner.load_topic_benchmark_focus(1, "BSON Data Types")

        assert "Benchmark weak focus for Topic 1" in focus
        assert "BSON vs JSON" in focus
        assert "collections vs tables" in focus
        assert "generation_notes" not in focus
    finally:
        planner.MEMORY_DIR = original_memory_dir
