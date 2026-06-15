from unittest.mock import MagicMock, patch


def test_structural_repair_requires_four_options_and_one_correct():
    from certcoach.jobs.repair_explanations import is_structurally_repairable

    ok, reason = is_structurally_repairable({"question_text": "Q", "options": []})
    assert ok is False
    assert "exactly 4 options" in reason

    ok, reason = is_structurally_repairable({
        "question_text": "Q",
        "options": [{"is_correct": False}, {"is_correct": False}, {"is_correct": False}, {"is_correct": False}],
    })
    assert ok is False
    assert "exactly one correct" in reason


def test_repair_selection_requires_explicit_pending_status():
    from certcoach.jobs.repair_explanations import is_marked_for_explanation_repair

    assert is_marked_for_explanation_repair({
        "metadata": {"content_contract_status": "needs_explanation_repair"}
    })
    assert not is_marked_for_explanation_repair({
        "metadata": {"content_contract_status": "quarantined"}
    })
    assert not is_marked_for_explanation_repair({
        "metadata": {"content_contract_status": "migrated"}
    })


def test_numeric_topic_filter_matches_exact_topic_id_only():
    from certcoach.jobs.repair_explanations import _topic_matches

    assert _topic_matches({"metadata": {"topic_id": 1, "topic": "Topic 1"}}, "1")
    assert not _topic_matches({"metadata": {"topic_id": 10, "topic": "Topic 10"}}, "1")
    assert not _topic_matches({"metadata": {"topic_id": 11, "topic": "Topic 11"}}, "1")


def test_concept_filter_matches_exact_concept_only():
    from certcoach.jobs.repair_explanations import _concept_matches

    question = {"metadata": {"concept": "BSON Data Types"}}

    assert _concept_matches(question, "bson data types")
    assert not _concept_matches(question, "BSON")


def test_repair_order_key_uses_syllabus_topic_and_concept_order():
    from certcoach.jobs.repair_explanations import _syllabus_order_key

    syllabus = [
        {"id": 1, "subtopics": ["First", "Second"]},
        {"id": 2, "subtopics": ["Third"]},
    ]
    questions = [
        {"_id": "q3", "metadata": {"topic_id": 2, "concept": "Third"}},
        {"_id": "q2", "metadata": {"topic_id": 1, "concept": "Second"}},
        {"_id": "q1", "metadata": {"topic_id": 1, "concept": "First"}},
    ]

    ordered = sorted(questions, key=lambda question: _syllabus_order_key(question, syllabus))

    assert [question["_id"] for question in ordered] == ["q1", "q2", "q3"]


def test_apply_repair_updates_explanation_and_feedbacks():
    from certcoach.jobs import repair_explanations as repair

    q = {
        "_id": "q1",
        "options": [
            {"option_letter": "A", "feedback": ""},
            {"option_letter": "B", "feedback": ""},
            {"option_letter": "C", "feedback": ""},
            {"option_letter": "D", "feedback": ""},
        ],
    }
    repaired = repair.RepairedExplanation(
        explanation="### 1. Correct Answer\nA\n### 2. Why Correct\nBecause\n### 3. Why Other Options Are Wrong\nNo\n### 4. Exam Trap\nTrap\n### 5. Memory Hook\nHook\n### 6. Follow-Up Practice Recommendation\nPractice\n### 7. Syntax Example\nNot required for this concept.",
        feedbacks=["fa", "fb", "fc", "fd"],
        trap_analysis="trap",
    )

    questions_col = MagicMock()
    with patch.object(repair.database, "questions_col", questions_col):
        repair.apply_repair(q, repaired)

    update_doc = questions_col.update_one.call_args[0][1]["$set"]
    assert update_doc["explanation"].startswith("### 1. Correct Answer")
    assert update_doc["options"][2]["feedback"] == "fc"
    assert update_doc["metadata.explanation_repair_source"] == "certcoach_repair_explanations"


def test_repair_quality_helper_passes_candidate_to_validator():
    from certcoach.jobs import repair_explanations as repair

    q = {
        "metadata": {"topic_id": 2, "topic": "CRUD Operations - Create", "concept": "insertOne()", "difficulty": "Easy"},
        "options": [
            {"option_letter": "A", "is_correct": True},
            {"option_letter": "B", "is_correct": False},
            {"option_letter": "C", "is_correct": False},
            {"option_letter": "D", "is_correct": False},
        ],
    }
    repaired = repair.RepairedExplanation(
        explanation="### 1. Correct Answer\nA\n### 2. Why Correct\nBecause.\n### 3. Why Other Options Are Wrong\nNo.\n### 4. Exam Trap\nTrap.\n### 5. Memory Hook\nHook.\n### 6. Follow-Up Practice Recommendation\nPractice.\n### 7. Syntax Example\nNot required for this concept.",
        feedbacks=["fa", "fb", "fc", "fd"],
        trap_analysis="trap",
    )

    with patch.object(repair, "validate_question_quality", return_value=(True, [])) as validate:
        issues = repair._repair_quality_issues(q, repaired)

    assert issues == []
    candidate = validate.call_args[0][0]
    assert candidate["explanation"] == repaired.explanation
    assert candidate["options"][0]["feedback"] == "fa"
