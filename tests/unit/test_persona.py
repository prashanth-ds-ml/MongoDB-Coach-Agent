import os
import sys
from unittest.mock import patch

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


def test_build_followup_prompt_grounds_in_reference_material_when_given():
    from certcoach.core.persona import build_followup_prompt

    prompt = build_followup_prompt(
        "BSON Data Types",
        "ObjectId",
        "What does the timestamp portion of an ObjectId represent?",
        [],
        md_context="ObjectId is a 12-byte value: a 4-byte timestamp, ...",
    )

    assert "ObjectId is a 12-byte value" in prompt
    assert "You MUST answer STRICTLY based on the Reference material provided above" in prompt
    assert "do not make up any content" in prompt
    assert "Do NOT invent invalid-syntax traps" in prompt


def test_build_followup_prompt_flags_missing_reference_material():
    from certcoach.core.persona import build_followup_prompt

    prompt = build_followup_prompt(
        "BSON Data Types", "ObjectId", "What does the timestamp portion represent?", [],
    )

    assert "No official reference material is loaded for this concept" in prompt


def test_build_scenario_prompt_grounds_and_guards_against_invention():
    from certcoach.core.persona import build_scenario_prompt

    prompt = build_scenario_prompt(
        "CRUD Operations - Read",
        md_context="find() returns a cursor over matching documents.",
    )

    assert "find() returns a cursor over matching documents" in prompt
    assert "Do NOT invent MongoDB behavior" in prompt
    assert "Type your approach or query below" in prompt


def test_build_scenario_prompt_flags_missing_reference_material():
    from certcoach.core.persona import build_scenario_prompt

    prompt = build_scenario_prompt("CRUD Operations - Read")

    assert "No official reference material is loaded for this topic" in prompt


def test_build_scenario_evaluation_prompt_grounds_and_guards_against_invention():
    from certcoach.core.persona import build_scenario_evaluation_prompt

    prompt = build_scenario_evaluation_prompt(
        "CRUD Operations - Read",
        scenario="Model a real-time leaderboard.",
        user_answer="db.scores.find({user_id: 1})",
        md_context="find() returns a cursor over matching documents.",
    )

    assert "find() returns a cursor over matching documents" in prompt
    assert "db.scores.find({user_id: 1})" in prompt
    assert "You MUST evaluate strictly based on the Reference material" in prompt
    assert "say so plainly rather than asserting it confidently" in prompt


def test_build_scenario_evaluation_prompt_flags_missing_reference_material():
    from certcoach.core.persona import build_scenario_evaluation_prompt

    prompt = build_scenario_evaluation_prompt(
        "CRUD Operations - Read", scenario="Model a leaderboard.", user_answer="db.scores.find()",
    )

    assert "No official reference material is loaded for this topic" in prompt


def test_build_section_check_prompt_grounds_in_section_text_only():
    from certcoach.core.persona import build_section_check_prompt

    prompt = build_section_check_prompt("BSON Data Types", "ObjectId is a 12-byte value.", num_questions=2)

    assert "ObjectId is a 12-byte value." in prompt
    assert "exactly 2 short questions" in prompt
    assert "mostly True/False" in prompt
    assert "3 or more comparable, clearly distinct items" in prompt
    assert "not that they've deeply understood it" in prompt
    assert "never invent a fact that isn't stated here" in prompt
    assert '"questions"' in prompt


def test_generate_section_check_parses_valid_json_response():
    from certcoach.core.persona import CoachPersona

    coach = CoachPersona()
    fake_response = (
        '{"questions": [{"question_text": "What is BSON?", "options": ['
        '{"option_letter": "A", "code_snippet": "Binary JSON", "is_correct": true}, '
        '{"option_letter": "B", "code_snippet": "Basic JSON", "is_correct": false}]}]}'
    )
    with patch.object(coach, "_call", return_value=fake_response) as mock_call:
        questions = coach.generate_section_check("BSON Data Types", "BSON is a binary representation of JSON.")

    assert len(questions) == 1
    assert questions[0]["question_text"] == "What is BSON?"
    mock_call.assert_called_once()


def test_generate_section_check_returns_empty_on_malformed_response():
    from certcoach.core.persona import CoachPersona

    coach = CoachPersona()
    with patch.object(coach, "_call", return_value="not json at all, and the model is confused"):
        questions = coach.generate_section_check("BSON Data Types", "some section text")

    assert questions == []


def test_generate_section_check_skips_the_model_call_for_blank_section_text():
    from certcoach.core.persona import CoachPersona

    coach = CoachPersona()
    with patch.object(coach, "_call") as mock_call:
        questions = coach.generate_section_check("BSON Data Types", "   ")

    assert questions == []
    mock_call.assert_not_called()


_VALID_SECTION_CHECK_JSON = (
    '{"questions": [{"question_text": "What is BSON?", "options": ['
    '{"option_letter": "A", "code_snippet": "Binary JSON", "is_correct": true}, '
    '{"option_letter": "B", "code_snippet": "Basic JSON", "is_correct": false}]}]}'
)


def test_close_unbalanced_json_repairs_a_response_missing_its_final_brace():
    """This is the dominant real-world failure mode, confirmed live: the
    local study model reliably stops generating exactly one closing brace
    short of a complete object -- a formatting habit, not random flakiness,
    so it recurs on retries too unless repaired directly."""
    from certcoach.core.persona import _close_unbalanced_json, _parse_section_check_response

    truncated = (
        '{"questions":[{"question_text":"What is BSON?", "options":['
        '{"option_letter":"A","code_snippet":"Binary JSON","is_correct":true},'
        '{"option_letter":"B","code_snippet":"Basic JSON","is_correct":false}]}]'
    )
    repaired = _close_unbalanced_json(truncated)

    import json
    parsed = json.loads(repaired)  # must not raise
    assert parsed["questions"][0]["question_text"] == "What is BSON?"

    questions = _parse_section_check_response(truncated)
    assert len(questions) == 1


def test_close_unbalanced_json_ignores_braces_inside_string_literals():
    from certcoach.core.persona import _close_unbalanced_json

    text = '{"question_text": "What does { mean in a filter like {a: 1}?"'
    repaired = _close_unbalanced_json(text)

    import json
    parsed = json.loads(repaired)  # must not raise
    assert parsed["question_text"] == "What does { mean in a filter like {a: 1}?"


def test_generate_section_check_retries_after_a_malformed_attempt():
    """Observed live: the small local study model drops the "code_snippet"
    key or truncates the closing brace on roughly 2 of 3 tries -- a single
    attempt would degrade to the empty-check fallback far more often than
    necessary, so a bad first attempt must not be the final answer."""
    from certcoach.core.persona import CoachPersona

    coach = CoachPersona()
    malformed = '{"questions": [{"question_text": "What is BSON?", "options": [{"option_letter": "A", "is_correct": true}]}]}'
    with patch.object(coach, "_call", side_effect=[malformed, _VALID_SECTION_CHECK_JSON]) as mock_call:
        questions = coach.generate_section_check("BSON Data Types", "some section text")

    assert len(questions) == 1
    assert questions[0]["question_text"] == "What is BSON?"
    assert mock_call.call_count == 2


def test_generate_section_check_gives_up_after_max_attempts():
    from certcoach.core.persona import CoachPersona

    coach = CoachPersona()
    with patch.object(coach, "_call", return_value="not json at all") as mock_call:
        questions = coach.generate_section_check("BSON Data Types", "some section text", max_attempts=3)

    assert questions == []
    assert mock_call.call_count == 3


def test_generate_section_check_rejects_a_question_with_no_correct_option_marked():
    from certcoach.core.persona import CoachPersona

    coach = CoachPersona()
    no_correct_marked = (
        '{"questions": [{"question_text": "What is BSON?", "options": ['
        '{"option_letter": "A", "code_snippet": "Binary JSON", "is_correct": false}, '
        '{"option_letter": "B", "code_snippet": "Basic JSON", "is_correct": false}]}]}'
    )
    with patch.object(coach, "_call", return_value=no_correct_marked):
        questions = coach.generate_section_check("BSON Data Types", "some section text", max_attempts=1)

    assert questions == []


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
