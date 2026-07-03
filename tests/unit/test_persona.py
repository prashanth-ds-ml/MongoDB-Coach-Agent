import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))


def test_build_lesson_prompt_adds_exam_recall_sections():
    from certcoach.core.persona import build_lesson_prompt

    prompt = build_lesson_prompt("CRUD Operations - Read", "findOne()", "Official doc content")

    assert "MODE: TEACH" in prompt
    assert "Stay strictly within the current syllabus topic and the current concept" in prompt
    assert "Assume the learner is seeing the concept for the first time" in prompt
    assert "Teach the syntax as if this is the learner's first time seeing it" in prompt
    assert "later-topic method such as CRUD writes" in prompt
    assert "query operators" in prompt
    assert "Do not answer your own Micro-Challenge inside the lesson" in prompt
    assert "The Micro-Challenge section must contain only the challenge prompt" in prompt
    assert "include 3-4 complete answer choices with full text, labeled A/B/C/D" in prompt
    assert "each option must be a full text choice, not just a letter" in prompt
    assert "The lesson must always use these six top-level sections in order" in prompt
    assert "Core Concept must define the concept" in prompt
    assert "If the Micro-Challenge is multiple choice" in prompt
    assert "For Topic 1 and other concept-only lessons, prefer open-ended micro-challenges" in prompt
    assert "For concept-only lessons, use only BSON/document-literal examples" in prompt
    assert "### 4. Exam Radar" in prompt
    assert "### 5. Micro-Challenge" in prompt
    assert "### 6. 30-Second Recall" in prompt
    assert "Type your answer, ask a question, or type practice when ready." in prompt


def test_build_followup_prompt_requires_gap_correction():
    from certcoach.core.persona import build_followup_prompt

    prompt = build_followup_prompt(
        "Querying Arrays & Embedded Documents",
        "dot notation",
        "I think I need {tags: ['mongodb']}",
        [{"role": "assistant", "content": "Answer the challenge."}],
    )

    assert "MODE: CHECK / CLARIFY" in prompt
    assert "Current concept: **dot notation**" in prompt
    assert "first state what they got right" in prompt
    assert "exact gap, code-smell, or casing trap" in prompt
    assert "type `practice` when ready" in prompt


def test_clean_lesson_explanation_normalizes_common_subsections():
    from certcoach.core.persona import clean_lesson_explanation

    text = """
    ### 1. Core Concept
    • Key Terms:
      • Document: A record.
      • Field: A key.
    • Mechanics:
      • BSON is compact.

    • Explanation:
      • Example: Use ObjectId for ids.
    """

    cleaned = clean_lesson_explanation(text)

    assert "#### Key Terms" in cleaned
    assert "#### Mechanics" in cleaned
    assert "#### Explanation" in cleaned
    assert "• Document: A record." in cleaned


def test_clean_lesson_explanation_normalizes_audience_labels():
    from certcoach.core.persona import clean_lesson_explanation

    text = """
    2. Level-Based Breakdown
    Beginners
    Intermediate Learners
    Advanced Developers
    """

    cleaned = clean_lesson_explanation(text)

    assert "#### Beginners" in cleaned
    assert "#### Intermediate Learners" in cleaned
    assert "#### Advanced Developers" in cleaned


def test_clean_lesson_explanation_strips_microchallenge_answers():
    from certcoach.core.persona import clean_lesson_explanation

    text = """
    ### 5. Micro-Challenge
    Question: Which BSON type stores multiple values?
    A
    B
    Correct Answer: B
    Explanation: Arrays store multiple values.
    """

    cleaned = clean_lesson_explanation(text)

    assert "### 5. Micro-Challenge" in cleaned
    assert "Question: Which BSON type stores multiple values?" in cleaned
    assert "Correct Answer:" not in cleaned
    assert "Explanation:" not in cleaned
    assert "\n- A" in cleaned or "\n- B" in cleaned


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


def test_build_lesson_repair_prompt_includes_validation_issues():
    from certcoach.core.persona import build_lesson_repair_prompt

    prompt = build_lesson_repair_prompt(
        "MongoDB Overview & The Document Model",
        "BSON Data Types",
        "Official doc content",
        "### 1. Core Concept\nDraft",
        ["missing heading: ### 2. Level-Based Breakdown"],
    )

    assert "The previous draft failed validation." in prompt
    assert "missing heading: ### 2. Level-Based Breakdown" in prompt
    assert "Previous draft to repair:" in prompt


def test_build_lesson_section_prompt_targets_one_section_only():
    from certcoach.core.persona import build_lesson_section_prompt

    prompt = build_lesson_section_prompt(
        "MongoDB Overview & The Document Model",
        "BSON Data Types",
        "Official doc content",
        "### 5. Micro-Challenge",
        "### 1. Core Concept\nDraft",
    )

    assert "Target section: **### 5. Micro-Challenge**" in prompt
    assert "Write only the body content for `### 5. Micro-Challenge`." in prompt
    assert "Do not repeat the heading." in prompt
