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
