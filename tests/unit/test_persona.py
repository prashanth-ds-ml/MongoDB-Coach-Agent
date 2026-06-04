import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))


def test_build_lesson_prompt_adds_exam_recall_sections():
    from certcoach.core.persona import build_lesson_prompt

    prompt = build_lesson_prompt("CRUD Operations - Read", "findOne()", "Official doc content")

    assert "### 4. Exam Radar" in prompt
    assert "### 5. Micro-Challenge" in prompt
    assert "### 6. 30-Second Recall" in prompt
    assert "Type your answer, ask a question, or type practice when ready." in prompt


def test_build_followup_prompt_requires_gap_correction():
    from certcoach.core.persona import build_followup_prompt

    prompt = build_followup_prompt(
        "Querying Arrays & Embedded Documents",
        "I think I need {tags: ['mongodb']}",
        [{"role": "assistant", "content": "Answer the challenge."}],
    )

    assert "state what is correct" in prompt
    assert "exact code-smell or casing trap" in prompt
    assert "practice" in prompt


def test_build_free_chat_prompt_anchors_study_advice():
    from certcoach.core.persona import build_free_chat_prompt

    prompt = build_free_chat_prompt(
        "How should I study this week?",
        [{"role": "user", "content": "I keep missing projection questions."}],
        student_context="- Weakest Topics: Projections",
    )

    assert "**Today**" in prompt
    assert "**This Week**" in prompt
    assert "**Avoid**" in prompt
    assert "Option 1 (Today's Agenda)" in prompt
