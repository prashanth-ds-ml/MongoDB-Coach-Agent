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
