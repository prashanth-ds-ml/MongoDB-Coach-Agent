import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
def test_show_exam_traps(mock_planner, mock_database, mock_console):
    from certcoach.cli import show_exam_traps
    
    mock_database.get_user_profile.return_value = {
        "progress": {
            "completed_topics": ["CRUD Operations - Create"]
        }
    }
    mock_planner.get_syllabus_status.return_value = {
        "status_list": []
    }
    
    with patch("certcoach.cli.print_paginated") as mock_print_paginated, \
         patch("certcoach.cli.Prompt.ask") as mock_prompt_ask:
        
        show_exam_traps()
        
        mock_print_paginated.assert_called_once()
        args, kwargs = mock_print_paginated.call_args
        assert kwargs.get("title") == "💡 Exam Cheat Sheet: Traps & Recall"
        mock_prompt_ask.assert_called_once()


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.memory_manager")
def test_show_study_journal(mock_memory, mock_planner, mock_database, mock_console, tmp_path):
    from certcoach.cli import show_study_journal
    
    dummy_brain = tmp_path / "MongoDB_Brain.md"
    mock_memory.BRAIN_FILE = str(dummy_brain)
    
    # Case 1: File does not exist
    with patch("time.sleep"):
        show_study_journal()
        mock_console.print.assert_called_with("[yellow]  No study journal found yet. Start studying to populate your log![/yellow]")
    
    # Case 2: File exists
    dummy_brain.write_text("# Chapter 1\nLearned about CRUD.", encoding="utf-8")
    mock_console.print.reset_mock()
    
    with patch("certcoach.cli.print_paginated") as mock_print_paginated, \
         patch("certcoach.cli.Prompt.ask") as mock_prompt_ask:
        
        show_study_journal()
        mock_print_paginated.assert_called_once()
        args, kwargs = mock_print_paginated.call_args
        assert kwargs.get("title") == "📖 Your Study Journal (MongoDB Brain)"
        mock_prompt_ask.assert_called_once()


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.run_onboarding")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_library_submenu")
@patch("certcoach.cli.run_settings_submenu")
def test_main_menu_option_routing(mock_settings, mock_library, mock_prompt_ask, mock_onboarding, mock_coach, mock_planner, mock_database, mock_console):
    from certcoach.cli import main_menu
    
    mock_planner.get_due_review_topics.return_value = []
    mock_coach.get_daily_greeting.return_value = "Hello Student!"
    
    # Mock status to avoid iterating on status list
    mock_planner.get_syllabus_status.return_value = {
        "mastery_percent": 0.0,
        "mastered_count": 0,
        "total_topics": 12,
        "mock_exam_unlocked": False,
        "unlock_threshold_percent": 70
    }
    mock_planner.generate_daily_agenda.return_value = []
    
    # First loop returns '2' (opens library), second loop raises KeyboardInterrupt to exit
    mock_prompt_ask.side_effect = ["2", KeyboardInterrupt()]
    
    try:
        main_menu()
    except (KeyboardInterrupt, SystemExit):
        pass
        
    mock_library.assert_called_once()


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.run_onboarding")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_library_submenu")
@patch("certcoach.cli.run_settings_submenu")
def test_main_menu_blocked_command_shows_full_list_on_demand(mock_settings, mock_library, mock_prompt_ask, mock_onboarding, mock_coach, mock_planner, mock_database, mock_console):
    from certcoach.cli import main_menu

    mock_planner.get_due_review_topics.return_value = []
    mock_coach.get_daily_greeting.return_value = "Hello Student!"
    mock_planner.get_syllabus_status.return_value = {
        "mastery_percent": 0.0,
        "mastered_count": 0,
        "total_topics": 12,
        "mock_exam_unlocked": False,
        "unlock_threshold_percent": 70,
        "insufficient_concepts": [
            {"topic": "Topic A", "concept": "Concept X", "easy_questions": 0, "required_easy": 3, "medium_questions": 0, "required_medium": 2},
        ],
    }
    mock_planner.generate_daily_agenda.return_value = []

    # "blocked" must show the full breakdown and return to the menu loop
    # (not consume the "1" agenda-start path), then a second loop exits.
    mock_prompt_ask.side_effect = ["blocked", "", KeyboardInterrupt()]

    try:
        main_menu()
    except (KeyboardInterrupt, SystemExit):
        pass

    panel_titles = [
        str(call.args[0].title) for call in mock_console.print.call_args_list
        if call.args and hasattr(call.args[0], "title")
    ]
    assert any("Concept Readiness Blockers" in title for title in panel_titles)
    mock_library.assert_not_called()
    mock_settings.assert_not_called()


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.run_onboarding")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_library_submenu")
@patch("certcoach.cli.run_settings_submenu")
def test_main_menu_softens_pass_probability_when_data_is_early(mock_settings, mock_library, mock_prompt_ask, mock_onboarding, mock_coach, mock_planner, mock_database, mock_console):
    from certcoach.cli import main_menu

    mock_planner.get_due_review_topics.return_value = []
    mock_coach.get_daily_greeting.return_value = "Hello Student!"
    mock_planner.get_syllabus_status.return_value = {
        "mastery_percent": 0.0,
        "mastered_count": 0,
        "total_topics": 12,
        "mock_exam_unlocked": False,
        "unlock_threshold_percent": 70,
        "insufficient_concepts": [],
    }
    mock_planner.generate_daily_agenda.return_value = []
    mock_planner.calculate_readiness_metrics.return_value = {
        "current_readiness": 0.0,
        "expected_readiness": 20.0,
        "pass_probability": 0.6,
        "low_data": True,
    }

    mock_prompt_ask.side_effect = [KeyboardInterrupt()]

    try:
        main_menu()
    except (KeyboardInterrupt, SystemExit):
        pass

    printed_text = [
        str(call.args[0]) for call in mock_console.print.call_args_list
        if call.args and isinstance(call.args[0], str)
    ]
    assert any("early estimate" in t for t in printed_text)


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.ask")
def test_recalibrate_study_plan(mock_ask, mock_confirm, mock_planner, mock_database, mock_console):
    import datetime
    from certcoach.cli import recalibrate_study_plan
    
    future_date = (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    mock_ask.side_effect = [future_date, "2"]
    mock_confirm.return_value = False
    
    mock_database.get_user_profile.return_value = {
        "progress": {
            "completed_topics": ["Topic 1"]
        }
    }
    mock_planner.generate_study_calendar.return_value = [{"day_num": 1, "topic": "Topic 1"}]
    
    with patch("time.sleep"):
        recalibrate_study_plan()
        
    mock_planner.generate_study_calendar.assert_called_once_with(30, "Intermediate", ["Topic 1"])
    mock_database.update_user_profile.assert_called_once()


def test_has_topic_documentation_and_get_syllabus_status(tmp_path):
    import os
    from certcoach.core import planner
    
    # Save original DATA_DIR
    original_data_dir = planner.DATA_DIR
    try:
        planner.DATA_DIR = str(tmp_path)
        raw_dir = tmp_path / "raw_markdowns"
        clean_dir = tmp_path / "cleaned_markdowns"
        raw_dir.mkdir(parents=True)
        clean_dir.mkdir(parents=True)
        
        t1 = {"id": 1, "topic": "T1", "md_files": []}
        t2 = {"id": 2, "topic": "T2", "md_files": ["f2.md"]}
        t3 = {"id": 3, "topic": "T3", "md_files": ["f3.md"]}
        (raw_dir / "f3.md").write_text("content3", encoding="utf-8")
        t4 = {"id": 4, "topic": "T4", "md_files": ["f4.md"]}
        (clean_dir / "f4.md").write_text("content4", encoding="utf-8")
        
        assert not planner.has_topic_documentation(t1)
        assert not planner.has_topic_documentation(t2)
        assert planner.has_topic_documentation(t3)
        assert planner.has_topic_documentation(t4)
    finally:
        planner.DATA_DIR = original_data_dir


@patch("certcoach.core.database.get_analytics")
@patch("certcoach.core.database.get_user_profile")
@patch("certcoach.core.database.get_active_question_counts_by_difficulty")
@patch("certcoach.core.planner.load_syllabus")
def test_get_syllabus_status_skipping(mock_load_syllabus, mock_difficulty_counts, mock_get_profile, mock_get_analytics, tmp_path):
    from certcoach.core import planner
    
    original_data_dir = planner.DATA_DIR
    try:
        planner.DATA_DIR = str(tmp_path)
        raw_dir = tmp_path / "raw_markdowns"
        clean_dir = tmp_path / "cleaned_markdowns"
        raw_dir.mkdir(parents=True, exist_ok=True)
        clean_dir.mkdir(parents=True, exist_ok=True)
        
        mock_get_profile.return_value = {"progress": {"completed_topics": []}}
        mock_get_analytics.return_value = {"topic_stats": []}
        mock_difficulty_counts.return_value = {"Easy": 3, "Medium": 2, "Hard": 0, "Other": 0}
        
        t1 = {"id": 1, "topic": "Topic 1", "md_files": ["missing.md"]}
        t2 = {"id": 2, "topic": "Topic 2", "md_files": ["present.md"]}
        (raw_dir / "present.md").write_text("grounded content", encoding="utf-8")
        
        mock_load_syllabus.return_value = [t1, t2]
        
        status = planner.get_syllabus_status("test_user")
        assert status["next_topic"]["topic"] == t2["topic"]
        assert len(status["skipped_unmapped_topics"]) == 1
        assert status["skipped_unmapped_topics"][0]["topic"] == "Topic 1"
    finally:
        planner.DATA_DIR = original_data_dir


@patch("certcoach.core.database.get_analytics")
@patch("certcoach.core.database.get_user_profile")
@patch("certcoach.core.database.get_active_question_counts_by_difficulty")
@patch("certcoach.core.planner.load_syllabus")
def test_get_syllabus_status_does_not_skip_uncompleted_concepts(mock_load_syllabus, mock_difficulty_counts, mock_get_profile, mock_get_analytics, tmp_path):
    from certcoach.core import planner

    original_data_dir = planner.DATA_DIR
    try:
        planner.DATA_DIR = str(tmp_path)
        raw_dir = tmp_path / "raw_markdowns"
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / "present.md").write_text("grounded content", encoding="utf-8")

        mock_get_profile.return_value = {
            "progress": {
                "completed_subtopics": {
                    "Topic 1": ["Concept A"]
                },
                "completed_topics": []
            }
        }
        mock_get_analytics.return_value = {
            "topic_stats": [
                {"topic": "Topic 1 Bank", "attempts": 5, "correct": 5}
            ]
        }
        mock_difficulty_counts.return_value = {"Easy": 3, "Medium": 2, "Hard": 0, "Other": 0}
        mock_load_syllabus.return_value = [
            {
                "id": 1,
                "topic": "Topic 1",
                "subtopics": ["Concept A", "Concept B"],
                "md_files": ["present.md"],
                "bank_topic_keys": ["Topic 1 Bank"],
                "in_question_bank": True,
            },
            {
                "id": 2,
                "topic": "Topic 2",
                "subtopics": ["Concept C"],
                "md_files": ["present.md"],
                "bank_topic_keys": ["Topic 2 Bank"],
                "in_question_bank": True,
            },
        ]

        status = planner.get_syllabus_status("test_user")

        assert status["mastered_count"] == 0
        assert status["next_topic"]["topic"] == "Topic 1"
        first = status["status_list"][0]
        assert first["accuracy"] == 100.0
        assert first["concept_coverage"] == 50.0
        assert first["uncompleted_subtopics"] == ["Concept B"]
        assert not first["is_mastered"]
    finally:
        planner.DATA_DIR = original_data_dir


def test_build_onboarding_commitment_text_sets_daily_loop():
    from certcoach.cli import build_onboarding_commitment_text

    text = build_onboarding_commitment_text(45, "Beginner")

    assert "45 days" in text
    assert "Beginner" in text
    assert "Start Today's Agenda" in text
    assert "4/5" in text


def test_get_current_user_label_prefers_display_name_and_email():
    from certcoach import cli

    with patch.object(cli.auth, "load_session", return_value={
        "user_id": "abc123",
        "email": "prash@example.com",
        "display_name": "Prash",
    }):
        assert cli.get_current_user_label() == "Prash <prash@example.com>"


def test_get_current_user_label_returns_none_when_not_signed_in():
    from certcoach import cli

    with patch.object(cli.auth, "load_session", return_value=None):
        assert cli.get_current_user_label() is None


def test_build_agenda_mission_text_for_learn_agenda():
    from certcoach.cli import build_agenda_mission_text

    text = build_agenda_mission_text(
        {
            "type": "Learn",
            "topic": "CRUD Operations - Read",
            "active_subtopic": "findOne()",
            "subtopics": ["findOne()"],
        },
        days_left=10,
        mastery_percent=25.0,
    )

    assert "Mission" in text
    assert "findOne()" in text
    assert "4/5" in text
    assert "10 days left" in text


def test_build_agenda_mission_text_when_practice_not_ready():
    from certcoach.cli import build_agenda_mission_text

    text = build_agenda_mission_text(
        {
            "type": "Learn",
            "topic": "CRUD Operations - Read",
            "active_subtopic": "findOne()",
            "subtopics": ["findOne()"],
        },
        days_left=10,
        mastery_percent=25.0,
        practice_ready=False,
    )

    # Must not promise a scored-practice step it can't deliver yet.
    assert "4/5" not in text
    assert "findOne()" in text
    assert "isn't unlocked" in text or "not unlocked" in text


def test_build_practice_debrief_for_pass_and_retry():
    from certcoach.cli import build_practice_debrief

    success_title, success_body, success_style = build_practice_debrief(4, 5, "CRUD", "find()")
    retry_title, retry_body, retry_style = build_practice_debrief(2, 5, "CRUD", "find()")

    assert success_title == "✅ Concept Locked In"
    assert "4/5" in success_body
    assert success_style == "green"

    assert retry_title == "🛠️ Not Locked In Yet"
    assert "2/5" in retry_body
    assert retry_style == "yellow"


def test_build_practice_recovery_text_surfaces_weak_signals():
    from certcoach.cli import build_practice_recovery_text

    title, body, style = build_practice_recovery_text(
        "Query Arrays",
        ["$elemMatch"],
        2,
        5,
        ["$elemMatch", "dot notation", "$elemMatch"],
    )

    assert title == "🚨 High-Priority Recovery"
    assert "$elemMatch, dot notation" in body
    assert "2/5" in body
    assert style == "red"


def test_build_session_closeout_text_includes_readiness_and_next_step():
    from certcoach.cli import build_session_closeout_text

    title, body, style = build_session_closeout_text(
        ["CRUD Operations - Read"],
        80.0,
        24.0,
        28.5,
        {"topic": "Query Operators & MQL", "desc": "📘 Topic #6 | Concept: $in"},
    )

    assert title == "📌 Coach Closeout"
    assert "24.0% -> 28.5%" in body
    assert "Query Operators & MQL" in body
    assert style == "green"


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.run_onboarding")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
def test_main_menu_skipped_topics_notice(mock_practice, mock_prompt_ask, mock_onboarding, mock_coach, mock_planner, mock_database, mock_console):
    from certcoach.cli import main_menu
    
    mock_planner.get_due_review_topics.return_value = []
    mock_coach.get_daily_greeting.return_value = "Hello!"
    
    mock_planner.get_syllabus_status.return_value = {
        "mastery_percent": 10.0,
        "mastered_count": 1,
        "total_topics": 5,
        "mock_exam_unlocked": False,
        "unlock_threshold_percent": 70,
        "skipped_unmapped_topics": [{"id": 1, "topic": "Skipped Topic"}]
    }
    mock_planner.generate_daily_agenda.return_value = []
    
    mock_prompt_ask.side_effect = ["1", KeyboardInterrupt()]
    
    try:
        main_menu()
    except (KeyboardInterrupt, SystemExit):
        pass
        
    panel_called = False
    for call in mock_console.print.call_args_list:
        args, kwargs = call
        if args and hasattr(args[0], "title") and args[0].title == "[bold yellow]📂 Bypassed Topics Notice[/bold yellow]":
            panel_called = True
            break
    assert panel_called


@patch("certcoach.core.database.get_user_attempts")
@patch("certcoach.core.database.get_analytics")
@patch("certcoach.core.database.get_user_profile")
@patch("certcoach.core.database.get_active_question_counts_by_difficulty")
@patch("certcoach.core.planner.load_syllabus")
def test_generate_daily_agenda_skipping_reviews(mock_load_syllabus, mock_difficulty_counts, mock_get_profile, mock_get_analytics, mock_get_attempts, tmp_path):
    import datetime
    from certcoach.core import planner
    
    original_data_dir = planner.DATA_DIR
    try:
        planner.DATA_DIR = str(tmp_path)
        raw_dir = tmp_path / "raw_markdowns"
        clean_dir = tmp_path / "cleaned_markdowns"
        raw_dir.mkdir(parents=True, exist_ok=True)
        clean_dir.mkdir(parents=True, exist_ok=True)
        
        mock_get_profile.return_value = {"progress": {"completed_topics": []}}
        mock_get_analytics.return_value = {"topic_stats": []}
        mock_difficulty_counts.return_value = {"Easy": 5, "Medium": 5, "Hard": 0, "Other": 0}
        
        mock_get_attempts.return_value = [
            {
                "topic": "Topic 1",
                "timestamp": (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) - datetime.timedelta(days=5)).isoformat(),
                "is_correct": False,
                "confidence_level": "Low"
            }
        ]
        
        t1 = {"id": 1, "topic": "Topic 1", "bank_topic_keys": ["Topic 1"], "md_files": ["missing.md"]}
        
        mock_load_syllabus.return_value = [t1]
        
        agenda = planner.generate_daily_agenda("test_user")
        
        assert not any(item["type"] == "Review" for item in agenda)
        
    finally:
        planner.DATA_DIR = original_data_dir


@patch("certcoach.cli.database")
@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
def test_run_teach_session_skipping_and_practice_jump(mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console, mock_database):
    from certcoach.cli import run_teach_session
    
    mock_confirm_ask.return_value = False
    mock_practice.return_value = 5
    mock_database.get_user_profile.return_value = {"exam_date": None, "streak_freeze_tokens": 0}
    mock_database.get_lesson_artifact.return_value = None

    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Subtopic A", "Subtopic B", "Subtopic C"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }

    def mock_resolve_concept_docs(md_files, concept):
        if concept == "Subtopic A":
            return []
        return [f"{concept.lower().replace(' ', '_')}.md"]

    mock_planner.resolve_concept_docs.side_effect = mock_resolve_concept_docs
    mock_planner.load_md_context.side_effect = lambda md_files, prioritize_concept=None: f"Official doc content for {md_files[0]}"
    mock_prompt_ask.side_effect = ["practice", "n"]

    with patch("time.sleep"):
        run_teach_session(agenda_item)

    mock_planner.resolve_concept_docs.assert_any_call([], "Subtopic A")
    mock_planner.resolve_concept_docs.assert_any_call([], "Subtopic B")

    called_subtopics = [call.args[1] for call in mock_planner.resolve_concept_docs.call_args_list]
    assert "Subtopic C" not in called_subtopics

    mock_practice.assert_called_with("Topic: Topic A", ["Topic A"], question_keywords=["subtopic"], num=5, is_mock=False, concepts=["Subtopic B"])


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
def test_run_practice_questions_clean_exit(mock_prompt_ask, mock_database, mock_console):
    from certcoach.cli import run_practice_questions
    
    mock_database.get_random_questions.return_value = [
        {
            "_id": "q1",
            "question_text": "Is MongoDB document-based?",
            "options": [
                {"option_letter": "A", "code_snippet": "Yes", "is_correct": True, "feedback": "Indeed."}
            ],
            "metadata": {"topic": "Topic A"},
            "context": {}
        }
    ]
    
    mock_prompt_ask.return_value = "q"
    
    with patch("time.sleep"):
        score = run_practice_questions("Topic A", ["Topic A"], num=1, is_mock=False)
        
    assert score is None


def _filler_question(qid, correct_letter="A"):
    """A minimal, always-correct-when-answered-A filler question, used to pad
    a non-mock practice fixture up to the real fixed 3 Easy + 2 Medium
    composition without changing what the test under study actually
    exercises."""
    return {
        "_id": qid,
        "question_text": f"Filler question {qid}?",
        "options": [{"option_letter": correct_letter, "code_snippet": "Yes", "is_correct": True, "feedback": "Correct."}],
        "metadata": {"topic": "Topic A"},
        "context": {},
    }


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.coach")
def test_run_practice_questions_allows_option_b_answer(mock_coach, mock_prompt_ask, mock_database, mock_console):
    from certcoach.cli import run_practice_questions

    real_question = {
        "_id": "q1",
        "question_text": "Which option is correct?",
        "options": [
            {"option_letter": "A", "code_snippet": "No", "is_correct": False, "feedback": "No."},
            {"option_letter": "B", "code_snippet": "Yes", "is_correct": True, "feedback": "Correct."},
            {"option_letter": "C", "code_snippet": "No", "is_correct": False, "feedback": "No."},
            {"option_letter": "D", "code_snippet": "No", "is_correct": False, "feedback": "No."},
        ],
        "metadata": {"topic": "Topic A"},
        "context": {},
    }
    # Real concept practice always requires 3 Easy + 2 Medium -- pad with
    # trivial filler questions (answered "A", always correct) so the fixed
    # composition gate passes; the question under test stays first in the
    # Easy list, so its own answer/feedback path is still exactly what's
    # verified below.
    mock_database.get_random_questions.side_effect = [
        [real_question, _filler_question("q_easy2"), _filler_question("q_easy3")],
        [_filler_question("q_med1"), _filler_question("q_med2")],
    ]
    # Per question: Answer, Confidence, and (for all but the last) a "next" prompt.
    mock_prompt_ask.side_effect = ["B", "H", "", "A", "H", "", "A", "H", "", "A", "H", "", "A", "H"]
    mock_coach.get_answer_feedback.return_value = "Good."

    with patch("time.sleep"):
        score = run_practice_questions("Topic A", ["Topic A"], num=1, is_mock=False)

    assert score == 5
    assert mock_database.save_attempt.call_count == 5
    first_call = mock_database.save_attempt.call_args_list[0]
    assert first_call.args[3] == "B"
    assert first_call.args[4] is True


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.coach")
def test_run_practice_questions_skips_coach_panel_on_high_confidence_correct(mock_coach, mock_prompt_ask, mock_database, mock_console):
    from certcoach.cli import run_practice_questions

    mock_database.get_random_questions.side_effect = [
        [_filler_question("q_easy1"), _filler_question("q_easy2"), _filler_question("q_easy3")],
        [_filler_question("q_med1"), _filler_question("q_med2")],
    ]
    # Correct answer + High confidence, all 5 questions.
    mock_prompt_ask.side_effect = ["A", "H", "", "A", "H", "", "A", "H", "", "A", "H", "", "A", "H"]

    with patch("time.sleep"):
        score = run_practice_questions("Topic A", ["Topic A"], num=1, is_mock=False)

    assert score == 5
    mock_coach.get_answer_feedback.assert_not_called()


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.coach")
def test_run_practice_questions_shows_coach_panel_on_low_confidence_correct(mock_coach, mock_prompt_ask, mock_database, mock_console):
    from certcoach.cli import run_practice_questions

    mock_database.get_random_questions.side_effect = [
        [_filler_question("q_easy1"), _filler_question("q_easy2"), _filler_question("q_easy3")],
        [_filler_question("q_med1"), _filler_question("q_med2")],
    ]
    mock_coach.get_answer_feedback.return_value = "Good."
    # Correct answer + Medium confidence, all 5 questions -- a second framing
    # can still add something when the learner wasn't sure.
    mock_prompt_ask.side_effect = ["A", "M", "", "A", "M", "", "A", "M", "", "A", "M", "", "A", "M"]

    with patch("time.sleep"):
        score = run_practice_questions("Topic A", ["Topic A"], num=1, is_mock=False)

    assert score == 5
    assert mock_coach.get_answer_feedback.call_count == 5


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.coach")
def test_run_practice_questions_shows_coach_panel_on_wrong_answer_regardless_of_confidence(mock_coach, mock_prompt_ask, mock_database, mock_console):
    from certcoach.cli import run_practice_questions

    wrong_question = {
        "_id": "q1",
        "question_text": "Which is correct?",
        "options": [
            {"option_letter": "A", "code_snippet": "No", "is_correct": False, "feedback": "No."},
            {"option_letter": "B", "code_snippet": "Yes", "is_correct": True, "feedback": "Correct."},
        ],
        "metadata": {"topic": "Topic A"},
        "context": {},
    }
    mock_database.get_random_questions.side_effect = [
        [wrong_question, _filler_question("q_easy2"), _filler_question("q_easy3")],
        [_filler_question("q_med1"), _filler_question("q_med2")],
    ]
    mock_database.get_remediation_for_wrong_attempt.return_value = {}
    mock_coach.get_answer_feedback.return_value = "Try again."
    # First question answered wrong ("A") with High confidence -- a wrong
    # answer must always show the coach panel, confidence notwithstanding.
    mock_prompt_ask.side_effect = ["A", "H", "", "A", "H", "", "A", "H", "", "A", "H", "", "A", "H"]

    with patch("time.sleep"):
        score = run_practice_questions("Topic A", ["Topic A"], num=1, is_mock=False)

    assert score == 4
    assert mock_coach.get_answer_feedback.call_count == 1


def test_format_explanation_template_strips_labels_and_sanitizes_feedback():
    from certcoach.cli import format_explanation_template

    q = {
        "metadata": {"topic": "BSON Data Types"},
        "options": [
            {
                "option_letter": "A",
                "code_snippet": "A) String",
                "is_correct": False,
                "feedback": "### 1. Correct Answer\nWrong feedback.\n### 2. Why Correct\nStill wrong.",
            },
            {
                "option_letter": "B",
                "code_snippet": "B) Array",
                "is_correct": True,
                "feedback": "### 1. Correct Answer\n### 2. Why Correct\nArray is the right container.\n### 3. Why Other Options Are Wrong\nNo.",
            },
        ],
        "metadata": {"topic": "BSON Data Types", "trap_analysis": "### 4. Exam Trap\nUse the right BSON type."},
    }

    explanation = format_explanation_template("B", q)

    assert "### 1. Correct Answer" in explanation
    assert "Option B (`Array`)" in explanation
    assert "Wrong feedback." in explanation
    assert "Still wrong." not in explanation
    assert "[bold yellow]" not in explanation
    assert "Array is the right container." in explanation
    assert "Use the right BSON type." in explanation


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.coach")
def test_run_practice_questions_next_prompt_q_exits(mock_coach, mock_prompt_ask, mock_database, mock_console):
    from certcoach.cli import run_practice_questions

    question_1 = {
        "_id": "q1",
        "question_text": "Question 1",
        "options": [
            {"option_letter": "A", "code_snippet": "A) Yes", "is_correct": True, "feedback": "Correct."},
            {"option_letter": "B", "code_snippet": "B) No", "is_correct": False, "feedback": "Incorrect."},
        ],
        "metadata": {"topic": "Topic A"},
        "context": {},
    }
    question_2 = {
        "_id": "q2",
        "question_text": "Question 2",
        "options": [
            {"option_letter": "A", "code_snippet": "A) Yes", "is_correct": True, "feedback": "Correct."},
            {"option_letter": "B", "code_snippet": "B) No", "is_correct": False, "feedback": "Incorrect."},
        ],
        "metadata": {"topic": "Topic A"},
        "context": {},
    }
    # Real concept practice always requires 3 Easy + 2 Medium -- pad with
    # filler questions so the fixed composition gate passes. question_1/
    # question_2 stay first in the Easy list, so they're still exactly the
    # two questions reached before "q" quits at question_2's answer prompt;
    # the fillers are never rendered.
    mock_database.get_random_questions.side_effect = [
        [question_1, question_2, _filler_question("q_easy3")],
        [_filler_question("q_med1"), _filler_question("q_med2")],
    ]
    mock_prompt_ask.side_effect = ["A", "H", "q"]
    mock_coach.get_answer_feedback.return_value = "Good."

    with patch("time.sleep"):
        score = run_practice_questions("Topic A", ["Topic A"], num=2, is_mock=False)

    assert score is None
    assert mock_database.save_attempt.call_count == 1


@patch("certcoach.cli.console")
@patch("certcoach.cli.Prompt.ask")
def test_present_and_capture_answer_single_select(mock_prompt_ask, mock_console):
    from certcoach.cli import present_and_capture_answer

    q = {
        "question_text": "Which is correct?",
        "options": [
            {"option_letter": "A", "code_snippet": "No"},
            {"option_letter": "B", "code_snippet": "Yes"},
        ],
        "metadata": {"response_type": "single"},
        "context": {},
    }
    mock_prompt_ask.return_value = "B"

    ans, is_multi, elapsed = present_and_capture_answer(q)

    assert ans == "B"
    assert is_multi is False
    assert elapsed >= 0
    _, kwargs = mock_prompt_ask.call_args
    assert kwargs["choices"] == ["A", "B", "Q", "BACK"]


@patch("certcoach.cli.console")
@patch("certcoach.cli.Prompt.ask")
def test_present_and_capture_answer_multi_select(mock_prompt_ask, mock_console):
    from certcoach.cli import present_and_capture_answer

    q = {
        "question_text": "Select all that apply",
        "options": [
            {"option_letter": "A", "code_snippet": "Yes"},
            {"option_letter": "B", "code_snippet": "No"},
            {"option_letter": "C", "code_snippet": "Yes"},
        ],
        "metadata": {"response_type": "multi"},
        "context": {},
    }
    mock_prompt_ask.return_value = "ac"

    ans, is_multi, elapsed = present_and_capture_answer(q)

    assert ans == "AC"
    assert is_multi is True


def test_evaluate_answer_correct_and_incorrect():
    from certcoach.cli import evaluate_answer

    q = {
        "options": [
            {"option_letter": "A", "code_snippet": "No", "is_correct": False, "feedback": "Nope."},
            {"option_letter": "B", "code_snippet": "Yes", "is_correct": True, "feedback": "Correct!"},
        ]
    }

    correct = evaluate_answer(q, "B")
    assert correct["is_correct"] is True
    assert correct["correct_letters"] == {"B"}
    assert correct["correct_option"]["option_letter"] == "B"
    assert correct["user_feedback"] == "Correct!"

    wrong = evaluate_answer(q, "A")
    assert wrong["is_correct"] is False
    assert wrong["correct_letters"] == {"B"}
    assert wrong["user_feedback"] == "Nope."


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
def test_run_review_quiz_empty_queue(mock_database, mock_console):
    from certcoach.cli import run_review_quiz

    mock_database.get_questions_for_review.return_value = []

    stats = run_review_quiz(1, "BSON Data Types")

    assert stats == {"correct": 0, "total": 0, "confirmed": 0, "suspect": 0, "skipped": 0}
    mock_database.confirm_question.assert_not_called()


@patch("certcoach.cli.console")
@patch("certcoach.cli.render_citation_panel")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
def test_run_review_quiz_confirm_flow_never_touches_attempts(mock_prompt_ask, mock_database, mock_render_citation, mock_console):
    from certcoach.cli import run_review_quiz, USER_ID

    question = {
        "_id": "q1",
        "question_text": "Which BSON type is a 128-bit decimal?",
        "options": [
            {"option_letter": "A", "code_snippet": "Double", "is_correct": False, "feedback": "No."},
            {"option_letter": "B", "code_snippet": "Decimal128", "is_correct": True, "feedback": "Correct."},
        ],
        "metadata": {"response_type": "single"},
        "context": {},
        "explanation": "Decimal128 stores exact decimal values.",
    }
    mock_database.get_questions_for_review.return_value = [question]
    mock_database.verify_citation.return_value = (True, "citation verified")
    mock_render_citation.return_value = MagicMock()

    # Q1: blind answer ("B"); Q2: confirm/suspect decision ("c").
    mock_prompt_ask.side_effect = ["B", "c"]

    stats = run_review_quiz(1, "BSON Data Types")

    assert stats == {"correct": 1, "total": 1, "confirmed": 1, "suspect": 0, "skipped": 0}
    mock_database.confirm_question.assert_called_once_with("q1", USER_ID)
    mock_database.save_attempt.assert_not_called()
    mock_database.update_question_exposure.assert_not_called()


@patch("certcoach.cli.console")
@patch("certcoach.cli.render_citation_panel")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
def test_run_review_quiz_blocks_confirm_when_citation_fails(mock_prompt_ask, mock_database, mock_render_citation, mock_console):
    from certcoach.cli import run_review_quiz

    question = {
        "_id": "q1",
        "question_text": "Q",
        "options": [{"option_letter": "A", "code_snippet": "X", "is_correct": True, "feedback": ""}],
        "metadata": {"response_type": "single"},
        "context": {},
        "explanation": "Some explanation.",
    }
    mock_database.get_questions_for_review.return_value = [question]
    mock_database.verify_citation.return_value = (False, "quote does not appear verbatim")
    mock_render_citation.return_value = MagicMock()

    # Q1: blind answer ("A"); Q2: suspect decision ("s"); Q3: reason text.
    mock_prompt_ask.side_effect = ["A", "s", "bad citation"]

    stats = run_review_quiz(1, "Concept")

    assert stats["suspect"] == 1
    mock_database.confirm_question.assert_not_called()
    mock_database.mark_question_suspect.assert_called_once_with("q1", "bad citation")

    decision_call = mock_prompt_ask.call_args_list[1]
    assert "c" not in decision_call.kwargs["choices"]
    assert "s" in decision_call.kwargs["choices"]


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
def test_run_review_quiz_quit_at_answer_prompt(mock_prompt_ask, mock_database, mock_console):
    from certcoach.cli import run_review_quiz

    question = {
        "_id": "q1",
        "question_text": "Q",
        "options": [{"option_letter": "A", "code_snippet": "X", "is_correct": True}],
        "metadata": {"response_type": "single"},
        "context": {},
    }
    mock_database.get_questions_for_review.return_value = [question]
    mock_prompt_ask.return_value = "Q"

    stats = run_review_quiz(1, "Concept")

    assert stats == {"correct": 0, "total": 0, "confirmed": 0, "suspect": 0, "skipped": 0}
    mock_database.confirm_question.assert_not_called()
    mock_database.mark_question_suspect.assert_not_called()


def test_command_sets_recognize_slash_prefixed_aliases():
    from certcoach.cli import EXIT_COMMANDS, BACK_COMMANDS, PRACTICE_COMMANDS, CONTINUE_COMMANDS

    assert {"/q", "/quit", "/exit"} <= EXIT_COMMANDS
    assert {"/back", "/b", "/menu"} <= BACK_COMMANDS
    assert {"/practice", "/p"} <= PRACTICE_COMMANDS
    assert {"/done", "/next"} <= CONTINUE_COMMANDS


@patch("certcoach.cli.Prompt.ask")
def test_ask_wrapper_recognizes_full_word_quit(mock_prompt_ask):
    from certcoach.cli import ask, EXIT_COMMANDS, BACK_COMMANDS

    # Previously the ask() wrapper only added the literal ["q", "back", "b",
    # "menu"] to Rich's choices= validation, so Rich rejected "quit"/"exit"
    # before the wrapper's own EXIT_COMMANDS check ever ran. It must now
    # offer the real, current EXIT_COMMANDS/BACK_COMMANDS sets and be
    # case-insensitive.
    mock_prompt_ask.return_value = "quit"

    with pytest.raises(SystemExit):
        ask("Pick one", choices=["1", "2"])

    _, kwargs = mock_prompt_ask.call_args
    assert kwargs["case_sensitive"] is False
    assert EXIT_COMMANDS <= set(kwargs["choices"])
    assert BACK_COMMANDS <= set(kwargs["choices"])


@patch("certcoach.cli.Prompt.ask")
def test_ask_wrapper_returns_back_sentinel(mock_prompt_ask):
    from certcoach.cli import ask

    mock_prompt_ask.return_value = "back"

    assert ask("Pick one", choices=["1", "2"]) == "__back__"


@patch("certcoach.cli.Confirm.ask")
def test_confirm_wrapper_is_case_insensitive(mock_confirm_ask):
    from certcoach.cli import confirm

    mock_confirm_ask.return_value = True

    assert confirm("Are you sure?") is True
    _, kwargs = mock_confirm_ask.call_args
    assert kwargs["case_sensitive"] is False


@patch("certcoach.cli.console")
@patch("certcoach.cli.Prompt.ask")
def test_library_submenu_q_fully_exits(mock_prompt_ask, mock_console):
    from certcoach.cli import run_library_submenu

    # "q" used to just break back to the main menu here (no dedicated Quit
    # option existed in this submenu) -- it must now match the documented
    # global "q / quit / exit -> save and quit immediately" contract.
    mock_prompt_ask.return_value = "q"

    with pytest.raises(SystemExit):
        run_library_submenu()


@patch("certcoach.cli.console")
@patch("certcoach.cli.Prompt.ask")
def test_library_submenu_back_returns_without_exit(mock_prompt_ask, mock_console):
    from certcoach.cli import run_library_submenu

    mock_prompt_ask.return_value = "back"

    run_library_submenu()  # must return normally, not raise


@patch("certcoach.cli.console")
@patch("certcoach.cli.Prompt.ask")
def test_settings_submenu_recognizes_exit_word(mock_prompt_ask, mock_console):
    from certcoach.cli import run_settings_submenu

    # Previously only "quit"/"q"/"h" exited; "exit" itself was missing.
    mock_prompt_ask.return_value = "exit"

    with pytest.raises(SystemExit):
        run_settings_submenu({}, {"mock_exam_unlocked": False, "unlock_threshold_percent": 70})


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
@patch("certcoach.cli.database")
def test_run_teach_session_qa_loop_recognizes_slash_exit(mock_database, mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session

    mock_planner.load_md_context.return_value = "dummy context"
    mock_database.get_user_profile.return_value = {"progress": {"completed_topics": []}}

    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Concept X"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }
    # A user typing the slash-prefixed form of "exit" mid-Q&A must be recognized
    # as an exit command, not sent to the coach as a real follow-up question.
    mock_prompt_ask.side_effect = ["/exit"]

    with patch("time.sleep"), pytest.raises(SystemExit):
        run_teach_session(agenda_item)

    mock_coach.handle_followup.assert_not_called()


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.Confirm.ask")
def test_exam_simulator_recognizes_full_word_quit(mock_confirm_ask, mock_prompt_ask, mock_planner, mock_database, mock_console):
    from certcoach.cli import run_exam_simulator

    mock_questions = [
        {
            "_id": "q1",
            "question_text": "Question 1",
            "options": [
                {"option_letter": "A", "code_snippet": "opt A1", "is_correct": True},
            ],
            "metadata": {"topic": "Topic A"}
        }
    ]
    # Previously, cmd was uppercased before comparing against the lowercase
    # EXIT_COMMANDS/BACK_COMMANDS sets, so only the bare letter "q" actually
    # matched -- typing the full word "quit" mid-exam silently fell through
    # to "Invalid command" instead of quitting.
    mock_prompt_ask.side_effect = ["quit"]
    mock_confirm_ask.return_value = True

    with patch("time.sleep"):
        score = run_exam_simulator("Test Mock", mock_questions, time_limit=300)

    assert score is None
    mock_database.clear_active_exam.assert_called_once()
    mock_database.save_study_session.assert_not_called()


@patch("certcoach.core.planner.get_syllabus_status")
@patch("certcoach.core.database.get_analytics")
@patch("certcoach.core.database.get_user_profile")
def test_calculate_readiness_metrics(mock_get_profile, mock_get_analytics, mock_get_status):
    from certcoach.core import planner
    
    mock_get_status.return_value = {"mastery_percent": 50.0}
    mock_get_analytics.return_value = {"total_attempts": 30, "correct_attempts": 24}
    mock_get_profile.return_value = {
        "study_calendar": [{"day_num": i} for i in range(10)],
        "exam_date": None
    }
    
    metrics = planner.calculate_readiness_metrics("user1")

    # 50.0 * 0.6 + 80.0 * 0.4 = 30.0 + 32.0 = 62.0%
    assert metrics["current_readiness"] == 62.0
    assert metrics["target_readiness"] == 80.0
    assert metrics["pass_probability"] >= 0.0
    # 30 attempts is exactly the dampener's own saturation point -- no
    # longer "low data" at that threshold.
    assert metrics["low_data"] is False


@patch("certcoach.core.planner.get_syllabus_status")
@patch("certcoach.core.database.get_analytics")
@patch("certcoach.core.database.get_user_profile")
def test_calculate_readiness_metrics_flags_low_data_early_on(mock_get_profile, mock_get_analytics, mock_get_status):
    from certcoach.core import planner

    mock_get_status.return_value = {"mastery_percent": 0.0}
    mock_get_analytics.return_value = {"total_attempts": 5, "correct_attempts": 5}
    mock_get_profile.return_value = {
        "study_calendar": [{"day_num": i} for i in range(10)],
        "exam_date": None
    }

    metrics = planner.calculate_readiness_metrics("user1")

    assert metrics["low_data"] is True


@patch("certcoach.core.planner.calculate_readiness_metrics")
@patch("certcoach.core.database.get_user_profile")
@patch("certcoach.core.database.get_study_sessions")
def test_get_study_plan_recommendation(mock_sessions, mock_get_profile, mock_metrics):
    from certcoach.core import planner
    
    # Ahead of Schedule
    mock_metrics.return_value = {"current_readiness": 75.0, "expected_readiness": 40.0}
    mock_get_profile.return_value = {
        "study_calendar": [{"day_num": i} for i in range(10)],
        "exam_date": None
    }
    mock_sessions.return_value = []
    
    rec = planner.get_study_plan_recommendation("user1")
    assert rec["status"] == "Ahead of Schedule"
    
    # Postpone Recommendation
    mock_metrics.return_value = {"current_readiness": 30.0, "expected_readiness": 60.0}
    with patch("certcoach.core.planner.calculate_days_left") as mock_days_left:
        mock_days_left.return_value = 3
        rec = planner.get_study_plan_recommendation("user1")
        assert "postponement" in rec["recommendation"].lower()


@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.Confirm.ask")
def test_run_question_bank_reports_quality_analytics(mock_confirm, mock_prompt, mock_database):
    from certcoach.cli import run_question_bank_reports

    # Test quality analytics report viewing
    mock_prompt.side_effect = ["1", ""]  # Select View Quality report, then Press Enter
    mock_database.get_questions_quality_analytics.return_value = [
        {"question_text": "Q1", "topic": "CRUD", "attempts": 5, "success_rate": 20.0, "average_time": 10.0, "difficulty": "Hard", "flag": "Needs Review"}
    ]

    with patch("certcoach.cli.print_paginated") as mock_print:
        run_question_bank_reports()
        mock_print.assert_called_once()


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
def test_show_exam_traps_locked(mock_planner, mock_database, mock_console):
    from certcoach.cli import show_exam_traps
    
    mock_database.get_user_profile.return_value = {
        "progress": {
            "completed_topics": []
        }
    }
    mock_planner.get_syllabus_status.return_value = {
        "status_list": []
    }
    
    with patch("certcoach.cli.print_paginated") as mock_print_paginated, \
         patch("certcoach.cli.Prompt.ask") as mock_prompt_ask:
        
        show_exam_traps()
        
        mock_print_paginated.assert_called_once()
        args, kwargs = mock_print_paginated.call_args
        group = args[0]
        # Verify locked text is present in the rendered group elements
        locked_found = False
        for child in group.renderables:
            plain_text = getattr(child, "plain", str(child))
            if "🔒 Exam Cheat Sheet Locked" in plain_text or "Locked" in plain_text:
                locked_found = True
                break
        assert locked_found
        mock_prompt_ask.assert_called_once()


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
def test_show_exam_traps_unlocked_ordered(mock_planner, mock_database, mock_console):
    from certcoach.cli import show_exam_traps
    
    mock_database.get_user_profile.return_value = {
        "progress": {
            "completed_topics": [
                "CRUD Operations - Read",
                "MongoDB Overview & The Document Model"
            ]
        }
    }
    mock_planner.get_syllabus_status.return_value = {
        "status_list": []
    }
    
    with patch("certcoach.cli.print_paginated") as mock_print_paginated, \
         patch("certcoach.cli.Prompt.ask") as mock_prompt_ask:
        
        show_exam_traps()
        
        mock_print_paginated.assert_called_once()
        args, kwargs = mock_print_paginated.call_args
        group = args[0]
        
        rendered_texts = [getattr(child, "plain", str(child)) for child in group.renderables]
        
        # Verify the traps are rendered in syllabus order:
        # Overview & The Document Model (Topic 1) should be before CRUD Operations - Read (Topic 3)
        t1_idx = -1
        t3_idx = -1
        for idx, text in enumerate(rendered_texts):
            if "Topic 1: Overview" in text:
                t1_idx = idx
            elif "Topic 3: CRUD - Read" in text:
                t3_idx = idx
        
        assert t1_idx != -1
        assert t3_idx != -1
        assert t1_idx < t3_idx
        mock_prompt_ask.assert_called_once()


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
def test_cumulative_cheat_sheet_checkpoint_shows_completed_and_remaining(mock_planner, mock_database, mock_console):
    from certcoach.cli import show_cumulative_cheat_sheet_checkpoint

    mock_database.get_user_profile.return_value = {
        "progress": {
            "completed_subtopics": {
                "MongoDB Overview & The Document Model": ["BSON Data Types"]
            }
        }
    }
    mock_planner.load_syllabus.return_value = [
        {
            "topic": "MongoDB Overview & The Document Model",
            "subtopics": ["BSON Data Types", "Document structure", "Collections vs Tables"],
        }
    ]

    show_cumulative_cheat_sheet_checkpoint("MongoDB Overview & The Document Model", "BSON Data Types")

    panel = next(call[0][0] for call in mock_console.print.call_args_list if call[0] and hasattr(call[0][0], "renderable"))
    rendered = str(panel.renderable)
    assert "Concept Checkpoint" in panel.title
    assert "BSON Data Types" in rendered
    assert "Document structure" in rendered
    assert "Cumulative Cheat Sheet" in rendered


@patch("certcoach.core.planner.get_syllabus_status")
@patch("certcoach.core.database.get_user_profile")
def test_generate_daily_agenda_no_mastery_skips_spaced_rep(mock_get_profile, mock_get_status):
    from certcoach.core import planner
    
    mock_get_profile.return_value = {"progress": {"completed_topics": []}}
    mock_get_status.return_value = {
        "mastered_count": 0,
        "next_topic": {"id": 1, "topic": "Topic 1", "md_files": ["f1.md"]},
        "status_list": [
            {
                "topic": "Topic 1",
                "bank_keys": ["Topic 1"],
                "attempts": 2,
                "accuracy": 30.0,
                "is_mastered": False,
                "md_files": ["f1.md"],
                "subtopics": []
            }
        ]
    }
    
    with patch("certcoach.core.planner.has_topic_documentation") as mock_has_doc, \
         patch("certcoach.core.planner.calculate_readiness_metrics") as mock_metrics:
        mock_has_doc.return_value = True
        mock_metrics.return_value = {"current_readiness": 10.0}
        
        agenda = planner.generate_daily_agenda("user1")
        
        # Spaced repetition reviews should be skipped completely
        assert not any(item["type"] == "Review" for item in agenda)


@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
def test_run_practice_questions_adaptive_selection(mock_prompt, mock_database):
    from certcoach.cli import run_practice_questions
    
    # Mock database to return questions depending on difficulty argument
    def mock_get_random(topic=None, limit=10, subtopic_keywords=None, difficulty=None, strict_keywords=False, *args, **kwargs):
        if difficulty == "Easy":
            return [
                {"_id": f"easy_{i}", "question_text": f"Easy Q {i}", "metadata": {"topic": topic, "difficulty": "Easy"}, "options": [{"option_letter": "A", "code_snippet": "ans", "is_correct": True}]}
                for i in range(limit)
            ]
        elif difficulty == "Medium":
            return [
                {"_id": f"med_{i}", "question_text": f"Medium Q {i}", "metadata": {"topic": topic, "difficulty": "Medium"}, "options": [{"option_letter": "A", "code_snippet": "ans", "is_correct": True}]}
                for i in range(limit)
            ]
        return []

    mock_database.get_random_questions.side_effect = mock_get_random
    mock_prompt.return_value = "q"  # Exit practice cleanly on first prompt
    
    with patch("time.sleep"):
        run_practice_questions("Topic A", ["Topic A"], num=5, is_mock=False, concepts=["concept_x"])
    
    # Assert get_random_questions was called separately for Easy and Medium difficulties
    mock_database.get_random_questions.assert_any_call(
        topic="Topic A", limit=10, subtopic_keywords=None, difficulty="Easy", strict_keywords=True, topic_id=None, concepts=["concept_x"]
    )
    mock_database.get_random_questions.assert_any_call(
        topic="Topic A", limit=10, subtopic_keywords=None, difficulty="Medium", strict_keywords=True, topic_id=None, concepts=["concept_x"]
    )


def test_clean_lesson_explanation_basic():
    from certcoach.core.persona import clean_lesson_explanation
    raw_lesson = """
        1 Core Concept
        BSON is a binary representation of JSON.
        
        ```
            from pymongo import MongoClient
            client = MongoClient()
        ```
        
        2. Level-Based Breakdown
        - For beginners: Analogies are great.
        
        3. Rich Examples (Do's & Don'ts)
        ```
            db.collection.insertOne({ _id: ObjectId() })
        ```
        
        4. Micro-Challenge
        Answer the challenge.
    """
    cleaned = clean_lesson_explanation(raw_lesson)
    
    assert "### 1. Core Concept" in cleaned
    assert "### 2. Level-Based Breakdown" in cleaned
    assert "### 3. Syntax & Code Examples (Do's & Don'ts)" in cleaned
    assert "### 4. Micro-Challenge" in cleaned
    
    assert "```python" in cleaned
    assert "from pymongo import MongoClient" in cleaned
    assert "```javascript" in cleaned
    assert "db.collection.insertOne" in cleaned


@patch("certcoach.core.planner.database")
@patch("certcoach.core.planner.load_syllabus")
def test_mark_subtopic_complete(mock_load_syllabus, mock_database):
    from certcoach.core.planner import mark_subtopic_complete
    
    mock_database.get_user_profile.return_value = {
        "progress": {
            "completed_subtopics": {
                "Topic 1": ["Concept A"]
            },
            "completed_topics": []
        }
    }
    
    mock_load_syllabus.return_value = [
        {
            "id": 1,
            "topic": "Topic 1",
            "subtopics": ["Concept A", "Concept B"]
        }
    ]
    
    mark_subtopic_complete("user123", "Topic 1", "Concept B")
    
    calls = mock_database.update_user_profile.call_args_list
    assert len(calls) > 0
    args, kwargs = calls[-1]
    profile_updates = args[1]
    progress = profile_updates["progress"]
    assert "Concept B" in progress["completed_subtopics"]["Topic 1"]
    assert "Topic 1" in progress["completed_topics"]


@patch("certcoach.core.planner.database")
@patch("certcoach.core.planner.get_syllabus_status")
def test_generate_daily_agenda_concept_level(mock_status, mock_database):
    from certcoach.core.planner import generate_daily_agenda
    
    mock_database.get_user_profile.return_value = {
        "progress": {
            "completed_subtopics": {
                "Topic 1": ["Concept A"]
            }
        }
    }
    
    mock_status.return_value = {
        "mastered_count": 0,
            "next_topic": {
                "id": 1,
                "topic": "Topic 1",
                "subtopics": ["Concept A", "Concept B", "Concept C"],
                "next_ready_subtopic": "Concept B",
                "bank_topic_keys": ["Topic 1"]
        },
        "status_list": []
    }
    
    with patch("certcoach.core.planner.calculate_readiness_metrics") as mock_metrics:
        mock_metrics.return_value = {"current_readiness": 10.0}
        
        agenda = generate_daily_agenda("user123")
        
        learn_item = next(item for item in agenda if item["type"] == "Learn")
        assert learn_item["active_subtopic"] == "Concept B"
        assert learn_item["subtopics"] == ["Concept B"]
        assert "Concept: Concept B" in learn_item["desc"]


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
@patch("certcoach.cli.database")
def test_run_teach_session_concept_completion(mock_database, mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session
    
    mock_planner.load_md_context.return_value = "dummy context"
    mock_confirm_ask.return_value = False
    mock_practice.return_value = 5
    
    agenda_item = {
        "topic": "Topic A",
        "active_subtopic": "Concept X",
        "subtopics": ["Concept X"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }
    
    mock_coach.explain_topic.return_value = "### 1. Core Concept\nExplanation\nType your answer or ask any questions."
    mock_prompt_ask.side_effect = ["next", "n"]
    
    mock_database.get_user_profile.return_value = {
        "progress": {
            "completed_topics": []
        }
    }
    mock_planner.get_syllabus_status.return_value = {"mastered_count": 0}
    
    with patch("time.sleep"):
        run_teach_session(agenda_item)
        
    from certcoach.cli import USER_ID

    mock_planner.mark_subtopic_complete.assert_called_once_with(USER_ID, "Topic A", "Concept X")


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
@patch("certcoach.cli.database")
def test_run_teach_session_acknowledgement_advances_after_followup(mock_database, mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session

    mock_planner.load_md_context.return_value = "dummy context"
    mock_planner.get_syllabus_status.return_value = {"mastered_count": 0}
    mock_practice.return_value = 5
    mock_coach.explain_topic.return_value = "### 1. Core Concept\nExplanation\nType your answer or ask any questions."
    mock_coach.handle_followup.return_value = "Correct. Does that clear it up?"
    mock_prompt_ask.side_effect = ["Dates should use new Date()", "yes", "n"]
    mock_database.get_user_profile.return_value = {"progress": {"completed_topics": []}}

    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Concept X"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }

    with patch("time.sleep"):
        run_teach_session(agenda_item)

    mock_coach.handle_followup.assert_called_once()
    mock_practice.assert_called_once_with("Topic: Topic A", ["Topic A"], question_keywords=["concept"], num=5, is_mock=False, concepts=["Concept X"])


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
@patch("certcoach.cli.database")
def test_run_teach_session_mini_mock_locked_until_three_topics(mock_database, mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session

    mock_planner.load_md_context.return_value = "dummy context"
    mock_planner.get_syllabus_status.return_value = {"mastered_count": 2}
    mock_practice.return_value = 5
    mock_coach.explain_topic.return_value = "### 1. Core Concept\nExplanation\nType your answer or ask any questions."
    mock_prompt_ask.side_effect = ["next", "n"]
    mock_database.get_user_profile.return_value = {"progress": {"completed_topics": []}}

    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Concept X"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }

    with patch("time.sleep"):
        run_teach_session(agenda_item)

    assert mock_practice.call_count == 1
    mock_practice.assert_called_once_with("Topic: Topic A", ["Topic A"], question_keywords=["concept"], num=5, is_mock=False, concepts=["Concept X"])


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
@patch("certcoach.cli.database")
def test_run_teach_session_unlocked_mini_mock_choice(mock_database, mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session

    mock_planner.load_md_context.return_value = "dummy context"
    mock_planner.get_syllabus_status.return_value = {"mastered_count": 3}
    mock_practice.return_value = 5
    mock_coach.explain_topic.return_value = "### 1. Core Concept\nExplanation\nType your answer or ask any questions."
    mock_prompt_ask.side_effect = ["next", "10", "n"]
    mock_database.get_user_profile.return_value = {"progress": {"completed_topics": []}}

    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Concept X"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }

    with patch("time.sleep"):
        run_teach_session(agenda_item)

    assert mock_practice.call_count == 2
    mock_practice.assert_any_call("Topic: Topic A", ["Topic A"], question_keywords=["concept"], num=5, is_mock=False, concepts=["Concept X"])
    mock_practice.assert_any_call("Topic: Topic A", ["Topic A"], question_keywords=["concept"], num=10, is_mock=True, concepts=["Concept X"])


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
@patch("certcoach.cli.run_review_quiz")
@patch("certcoach.cli.database")
def test_run_teach_session_offers_review_quiz_when_pending(mock_database, mock_review_quiz, mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session

    mock_planner.load_md_context.return_value = "dummy context"
    mock_planner.get_syllabus_status.return_value = {"mastered_count": 0}
    mock_planner.load_syllabus.return_value = [{"id": 1, "topic": "Topic A"}]
    mock_practice.return_value = 5
    mock_review_quiz.return_value = {"correct": 1, "total": 1, "confirmed": 1, "suspect": 0, "skipped": 0}
    mock_coach.explain_topic.return_value = "### 1. Core Concept\nExplanation\nType your answer or ask any questions."
    mock_database.get_user_profile.return_value = {"progress": {"completed_topics": []}}
    mock_database.count_questions_for_review.return_value = 3

    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Concept X"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }
    # "next" advances the Q&A loop normally; "y" accepts the review-quiz offer;
    # "n" declines the trailing "ready for the next agenda item?" prompt.
    mock_prompt_ask.side_effect = ["next", "y", "n"]

    with patch("time.sleep"):
        run_teach_session(agenda_item)

    mock_database.count_questions_for_review.assert_called_once_with(topic_id=1, concept="Concept X")
    mock_review_quiz.assert_called_once_with(1, "Concept X")


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
@patch("certcoach.cli.run_review_quiz")
@patch("certcoach.cli.database")
def test_run_teach_session_skips_review_quiz_when_declined(mock_database, mock_review_quiz, mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session

    mock_planner.load_md_context.return_value = "dummy context"
    mock_planner.get_syllabus_status.return_value = {"mastered_count": 0}
    mock_planner.load_syllabus.return_value = [{"id": 1, "topic": "Topic A"}]
    mock_practice.return_value = 5
    mock_coach.explain_topic.return_value = "### 1. Core Concept\nExplanation\nType your answer or ask any questions."
    mock_database.get_user_profile.return_value = {"progress": {"completed_topics": []}}
    mock_database.count_questions_for_review.return_value = 3

    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Concept X"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }
    # "next" advances the Q&A loop normally; "n" declines the review-quiz offer;
    # "n" declines the trailing "ready for the next agenda item?" prompt.
    mock_prompt_ask.side_effect = ["next", "n", "n"]

    with patch("time.sleep"):
        run_teach_session(agenda_item)

    mock_review_quiz.assert_not_called()


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
@patch("certcoach.cli.database")
def test_run_teach_session_shows_qa_instructions_once_per_session(mock_database, mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session

    mock_planner.load_md_context.return_value = "dummy context"
    mock_planner.get_syllabus_status.return_value = {"mastered_count": 0}
    mock_planner.resolve_concept_docs.return_value = ["doc.md"]
    mock_practice.return_value = 5
    mock_database.get_user_profile.return_value = {"progress": {"completed_topics": []}}

    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Concept A", "Concept B"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }
    # "next" advances each concept's Q&A loop; "n" declines the trailing
    # "ready for the next agenda item?" prompt.
    mock_prompt_ask.side_effect = ["next", "next", "n"]

    with patch("time.sleep"):
        run_teach_session(agenda_item)

    printed_text = [
        call.args[0] for call in mock_console.print.call_args_list
        if call.args and isinstance(call.args[0], str)
    ]
    full_instruction_count = sum(1 for t in printed_text if "Answer the challenge using only this concept" in t)
    short_reminder_count = sum(1 for t in printed_text if "or ask a question)" in t)

    assert full_instruction_count == 1
    assert short_reminder_count == 1


_MULTI_SECTION_LESSON_DOC = (
    "# Widgets\n\n"
    "Widgets are the core building block of the system and every widget has a "
    "unique identifier assigned at creation time.\n\n"
    "## Advanced Widgets\n\n"
    "Advanced widgets support extra configuration options that are not "
    "available on basic widgets, including custom validators.\n"
)


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
@patch("certcoach.cli.database")
def test_run_teach_session_splits_lesson_doc_into_sections(mock_database, mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session

    mock_planner.load_md_context.return_value = _MULTI_SECTION_LESSON_DOC
    mock_planner.get_syllabus_status.return_value = {"mastered_count": 0}
    mock_planner.resolve_concept_docs.return_value = ["doc.md"]
    mock_practice.return_value = 5
    mock_database.get_user_profile.return_value = {"progress": {"completed_topics": []}}

    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Concept A"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }
    # "" accepts the default at the "next section" prompt (section 1 -> 2);
    # "next" advances the Q&A loop; "n" declines the trailing agenda prompt.
    mock_prompt_ask.side_effect = ["", "next", "n"]

    with patch("time.sleep"):
        run_teach_session(agenda_item)

    panel_titles = [
        str(call.args[0].title) for call in mock_console.print.call_args_list
        if call.args and hasattr(call.args[0], "title")
    ]
    assert any("Widgets (1/2)" in t for t in panel_titles)
    assert any("Widgets > Advanced Widgets (2/2)" in t for t in panel_titles)

    section_prompts = [
        call for call in mock_prompt_ask.call_args_list
        if call.args and "next section" in call.args[0]
    ]
    assert len(section_prompts) == 1


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
@patch("certcoach.cli.database")
def test_run_teach_session_jump_to_practice_from_section_prompt(mock_database, mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session

    mock_planner.load_md_context.return_value = _MULTI_SECTION_LESSON_DOC
    mock_planner.get_syllabus_status.return_value = {"mastered_count": 0}
    mock_planner.resolve_concept_docs.return_value = ["doc.md"]
    mock_practice.return_value = 5
    mock_database.get_user_profile.return_value = {"progress": {"completed_topics": []}}

    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Concept A"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }
    # "practice" at the first "next section" prompt jumps straight to MCQs,
    # skipping section 2 and the Q&A loop entirely.
    mock_prompt_ask.side_effect = ["practice", "n"]

    with patch("time.sleep"):
        run_teach_session(agenda_item)

    panel_titles = [
        str(call.args[0].title) for call in mock_console.print.call_args_list
        if call.args and hasattr(call.args[0], "title")
    ]
    assert any("Widgets (1/2)" in t for t in panel_titles)
    assert not any("Advanced Widgets (2/2)" in t for t in panel_titles)
    mock_coach.handle_followup.assert_not_called()


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
@patch("certcoach.cli.database")
def test_run_teach_session_mission_brief_reflects_blocked_practice(mock_database, mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session

    mock_planner.load_md_context.return_value = "dummy context"
    mock_planner.resolve_concept_docs.return_value = ["doc.md"]
    mock_planner.get_syllabus_status.return_value = {
        "mastered_count": 0,
        "mastery_percent": 0.0,
        "insufficient_concepts": [
            {"topic": "Topic A", "concept": "Concept X", "easy_questions": 0, "required_easy": 3, "medium_questions": 0, "required_medium": 2},
        ],
    }
    mock_practice.return_value = None
    mock_database.get_user_profile.return_value = {"progress": {"completed_topics": []}}

    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Concept X"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }
    mock_prompt_ask.side_effect = ["next", "n"]

    with patch("time.sleep"):
        run_teach_session(agenda_item)

    panel = next(
        call.args[0] for call in mock_console.print.call_args_list
        if call.args and hasattr(call.args[0], "title") and call.args[0].title == "🎯 Daily Mission Brief"
    )
    rendered = str(panel.renderable)
    assert "4/5" not in rendered
    assert "isn't unlocked" in rendered


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.Confirm.ask")
def test_exam_simulator_navigation_and_review(mock_confirm_ask, mock_prompt_ask, mock_planner, mock_database, mock_console):
    from certcoach.cli import run_exam_simulator
    
    mock_questions = [
        {
            "_id": "q1",
            "question_text": "Question 1",
            "options": [
                {"option_letter": "A", "code_snippet": "opt A1", "is_correct": True},
                {"option_letter": "B", "code_snippet": "opt B1", "is_correct": False},
                {"option_letter": "C", "code_snippet": "opt C1", "is_correct": False},
                {"option_letter": "D", "code_snippet": "opt D1", "is_correct": False}
            ],
            "metadata": {"topic": "Topic A"}
        },
        {
            "_id": "q2",
            "question_text": "Question 2",
            "options": [
                {"option_letter": "A", "code_snippet": "opt A2", "is_correct": False},
                {"option_letter": "B", "code_snippet": "opt B2", "is_correct": True},
                {"option_letter": "C", "code_snippet": "opt C2", "is_correct": False},
                {"option_letter": "D", "code_snippet": "opt D2", "is_correct": False}
            ],
            "metadata": {"topic": "Topic A"}
        }
    ]
    
    mock_database.get_user_profile.return_value = {
        "progress": {"completed_topics": []},
        "readiness_history": []
    }
    mock_planner.calculate_readiness_metrics.return_value = {"current_readiness": 50.0}
    
    mock_prompt_ask.side_effect = [
        "A",        # Answer Q1, auto-advances to Q2
        "R",        # Toggle Flag on Q2
        "P",        # Go Prev (moves back to Q1)
        "2",        # Jump to Q2
        "S",        # Open Summary Grid
        "R",        # Summary Grid Action: Resume
        "S",        # Open Summary Grid again
        "F",        # Summary Grid Action: Finalize
        "1",        # Post-Exam Review Action: View Q1 explanation
        "",         # Single Q explanation review: Exit back to grid
        "B"         # Post-Exam Review Action: Back to main menu
    ]
    mock_confirm_ask.side_effect = [
        True,       # Confirm finalize
        True        # Confirm finalize from summary grid
    ]
    
    with patch("time.sleep"):
        score = run_exam_simulator("Test Mock", mock_questions, time_limit=300)
        
    assert score == 1
    assert mock_database.save_attempt.call_count == 2
    assert mock_database.update_question_exposure.call_count == 2
    assert mock_database.save_study_session.call_count == 1


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.Confirm.ask")
def test_exam_simulator_timer_expiration(mock_confirm_ask, mock_prompt_ask, mock_planner, mock_database, mock_console):
    from certcoach.cli import run_exam_simulator
    
    mock_questions = [
        {
            "_id": "q1",
            "question_text": "Question 1",
            "options": [
                {"option_letter": "A", "code_snippet": "opt A1", "is_correct": True},
                {"option_letter": "B", "code_snippet": "opt B1", "is_correct": False},
                {"option_letter": "C", "code_snippet": "opt C1", "is_correct": False},
                {"option_letter": "D", "code_snippet": "opt D1", "is_correct": False}
            ],
            "metadata": {"topic": "Topic A"}
        }
    ]
    
    mock_database.get_user_profile.return_value = {
        "progress": {"completed_topics": []},
        "readiness_history": []
    }
    mock_planner.calculate_readiness_metrics.return_value = {"current_readiness": 50.0}
    
    mock_prompt_ask.side_effect = ["B"]
    
    with patch("time.sleep"):
        score = run_exam_simulator("Test Mock", mock_questions, time_limit=-1)
        
    assert score == 0
    assert mock_database.save_attempt.call_count == 1
    assert mock_database.save_study_session.call_count == 1


def test_validate_lexical_syntax_guard():
    from certcoach.core.planner import validate_lexical_syntax_guard
    
    # 1. Standard topic - mongosh syntax - should pass
    ok, err = validate_lexical_syntax_guard(
        "CRUD Operations - Create",
        "Which command inserts a document?",
        ["db.coll.insertOne({x: 1})", "db.coll.insertMany([])"]
    )
    assert ok is True
    
    # 2. Standard topic - contains PyMongo snake_case - should fail
    ok, err = validate_lexical_syntax_guard(
        "CRUD Operations - Create",
        "Which command inserts a document?",
        ["db.coll.insert_one({x: 1})", "db.coll.insertOne({x: 1})"]
    )
    assert ok is False
    assert "contains PyMongo snake_case method" in err

    # 3. Standard topic with explicit PyMongo context - should pass
    ok, err = validate_lexical_syntax_guard(
        "CRUD Operations - Read",
        "Which PyMongo method returns the first matching document?",
        ["client.db.coll.find_one({'x': 1})", "client.db.coll.find()"]
    )
    assert ok is True

    # 4. Python topic - contains PyMongo snake_case - should pass
    ok, err = validate_lexical_syntax_guard(
        "MongoDB Drivers & PyMongo",
        "How do you insert a document in PyMongo?",
        ["client.db.coll.insert_one({'x': 1})", "client.db.coll.insertOne()"]
    )
    assert ok is True
    
    # 5. Python topic - lacks PyMongo snake_case - should fail
    ok, err = validate_lexical_syntax_guard(
        "MongoDB Drivers & PyMongo",
        "How do you query documents?",
        ["client.db.coll.find()", "client.db.coll.aggregate()"]
    )
    assert ok is False
    assert "lacks PyMongo snake_case driver syntax" in err


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.Confirm.ask")
def test_exam_simulator_autosaver_resume(mock_confirm_ask, mock_prompt_ask, mock_planner, mock_database, mock_console):
    from certcoach.cli import run_exam_simulator
    
    mock_questions = [
        {
            "_id": "q1",
            "question_text": "Question 1",
            "options": [
                {"option_letter": "A", "code_snippet": "opt A1", "is_correct": True},
                {"option_letter": "B", "code_snippet": "opt B1", "is_correct": False}
            ],
            "metadata": {"topic": "Topic A"}
        }
    ]
    
    mock_database.get_active_exam.return_value = {
        "topic": "Test Mock",
        "timestamp": "2026-06-01 12:00:00",
        "user_answers": ["A"],
        "flagged": [True],
        "elapsed": 120.0,
        "questions": mock_questions
    }
    
    mock_database.get_user_profile.return_value = {
        "progress": {"completed_topics": []},
        "readiness_history": []
    }
    mock_planner.calculate_readiness_metrics.return_value = {"current_readiness": 50.0}
    
    mock_confirm_ask.side_effect = [
        True,  # Confirm resume exam
        True,  # Confirm finalize from summary grid
        True   # Finalize confirm dialog
    ]
    mock_prompt_ask.side_effect = [
        "S",   # Command input
        "F",   # Summary grid action
        "B"    # Exit review grid
    ]
    
    with patch("time.sleep"):
        score = run_exam_simulator("Test Mock", mock_questions, time_limit=300)
        
    assert score == 1
    assert mock_database.get_active_exam.call_count == 1
    assert mock_database.save_active_exam.call_count >= 1
    assert mock_database.clear_active_exam.call_count == 1


def test_streak_freeze_retention_and_decrement():
    from certcoach.core import database
    from datetime import datetime, timedelta, timezone
    
    mock_profile = {
        "_id": "local_user_1",
        "streak_days": 5,
        "last_login_date": (datetime.now(timezone.utc).date() - timedelta(days=2)).isoformat(),
        "progress": {"streak_freezes": 2}
    }
    
    with patch("certcoach.core.database.get_user_profile", return_value=mock_profile), \
         patch("certcoach.core.database.update_user_profile") as mock_update_profile, \
         patch("rich.console.Console.print") as mock_print:
         
        database.update_streak("local_user_1")
        
        # Verify that streak freezes decremented to 1 and is updated
        assert mock_update_profile.call_count >= 1
        # The update call to user profile includes progress with decremented streak_freezes
        first_call_args = mock_update_profile.call_args_list[0][0][1]
        assert first_call_args["progress"]["streak_freezes"] == 1
        
        # The final call updates the streak to be retained (5) and sets today as last login
        second_call_args = mock_update_profile.call_args_list[1][0][1]
        assert second_call_args["streak_days"] == 5
        assert second_call_args["last_login_date"] == datetime.now(timezone.utc).date().isoformat()
        
        # Verify announcement printed
        mock_print.assert_called_once()
        assert "Streak Freeze Active!" in mock_print.call_args[0][0]


def test_award_streak_freeze_capped():
    from certcoach.core import database
    
    # Case 1: Under cap (freezes = 1) -> should succeed and increment to 2
    mock_profile_1 = {
        "_id": "local_user_1",
        "progress": {"streak_freezes": 1}
    }
    with patch("certcoach.core.database.get_user_profile", return_value=mock_profile_1), \
         patch("certcoach.core.database.update_user_profile") as mock_update_profile:
        res = database.award_streak_freeze("local_user_1")
        assert res is True
        mock_update_profile.assert_called_once_with("local_user_1", {"progress": {"streak_freezes": 2}})
        
    # Case 2: At cap (freezes = 3) -> should fail and return False
    mock_profile_2 = {
        "_id": "local_user_1",
        "progress": {"streak_freezes": 3}
    }
    with patch("certcoach.core.database.get_user_profile", return_value=mock_profile_2), \
         patch("certcoach.core.database.update_user_profile") as mock_update_profile:
        res = database.award_streak_freeze("local_user_1")
        assert res is False
        mock_update_profile.assert_not_called()


@patch("certcoach.core.database.MongoClient")
@patch("certcoach.core.database.open", create=True)
@patch("os.path.exists", return_value=True)
def test_update_database_connection(mock_exists, mock_open, mock_mongo_client):
    from certcoach.core import database
    
    # Mocking env files read/write
    mock_file = MagicMock()
    mock_file.readlines.return_value = ["MONGO_URI=mongodb://old_uri\n", "MODEL=qwen\n"]
    mock_open.return_value.__enter__.return_value = mock_file
    
    mock_client_instance = MagicMock()
    mock_mongo_client.return_value = mock_client_instance
    
    res = database.update_database_connection("mongodb://new_uri")
    
    assert res is True
    assert database.MONGO_URI == "mongodb://new_uri"
    # Ensure write was called with updated MONGO_URI
    write_calls = mock_file.writelines.call_args_list
    assert len(write_calls) > 0
    written_lines = write_calls[0][0][0]
    assert any("MONGO_URI=mongodb://new_uri\n" in line for line in written_lines)
    # Ensure server selection ping was invoked to verify connection
    mock_client_instance.admin.command.assert_called_with("ping")


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
def test_show_casing_contrast_sheet(mock_prompt_ask, mock_database, mock_console):
    from certcoach.cli import show_casing_contrast_sheet
    
    with patch("certcoach.cli.print_paginated") as mock_print_paginated:
        show_casing_contrast_sheet()
        mock_print_paginated.assert_called_once()
        mock_prompt_ask.assert_called_once()


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.Prompt.ask")
def test_practice_questions_awards_freeze(mock_prompt_ask, mock_coach, mock_database, mock_console):
    from certcoach.cli import run_practice_questions
    
    def mock_get_random(topic=None, limit=10, subtopic_keywords=None, difficulty=None, strict_keywords=False, *args, **kwargs):
        prefix = difficulty or "Any"
        return [
            {
                "_id": f"{prefix.lower()}_{i}",
                "question_text": f"{prefix} Q{i}",
                "metadata": {"topic": topic, "difficulty": prefix},
                "options": [{"option_letter": "A", "code_snippet": "c1", "is_correct": True, "feedback": "good"}],
            }
            for i in range(limit)
        ]

    mock_database.get_random_questions.side_effect = mock_get_random
    mock_database.award_streak_freeze.return_value = True
    mock_coach.get_answer_feedback.return_value = "Mocked feedback response."
    
    # 5/5 score on 5-question practice quiz
    mock_prompt_ask.side_effect = ["A", "H", ""] * 5
    
    with patch("time.sleep"):
        score = run_practice_questions("Topic 1", ["Topic 1"], num=5, is_mock=False)
        
    assert score == 5
    from certcoach.cli import USER_ID

    mock_database.award_streak_freeze.assert_called_once_with(USER_ID)
    # Verify streak freeze announcement printed
    printed_text = "\n".join(
        str(call[0][0]) for call in mock_console.print.call_args_list if call[0]
    )
    assert "earned a Streak Freeze token" in printed_text


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
def test_run_practice_questions_missing_bank_does_not_insert_fallback(mock_database, mock_console):
    from certcoach.cli import run_practice_questions

    mock_database.get_random_questions.return_value = []
    mock_database.questions_col.insert_one = MagicMock()

    with patch("time.sleep"):
        score = run_practice_questions("Topic A", ["Topic A"], num=5, is_mock=False)

    assert score is None
    mock_database.questions_col.insert_one.assert_not_called()


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
def test_run_practice_questions_blocks_missing_difficulty_mix(mock_database, mock_console):
    from certcoach.cli import run_practice_questions

    def get_questions(**kwargs):
        difficulty = kwargs.get("difficulty")
        count = 2 if difficulty == "Easy" else 3 if difficulty == "Medium" else 5
        return [
            {
                "_id": f"{difficulty}_{i}",
                "question_text": f"{difficulty} Question {i}",
                "metadata": {"topic": "Topic A", "concept": "Concept X", "difficulty": difficulty},
                "options": [{"option_letter": "A", "code_snippet": "answer", "is_correct": True}],
            }
            for i in range(count)
        ]

    mock_database.get_random_questions.side_effect = get_questions

    with patch("time.sleep"):
        score = run_practice_questions(
            "Topic A",
            ["Topic A"],
            num=5,
            is_mock=False,
            concepts=["Concept X"],
        )

    assert score is None
    mock_database.save_attempt.assert_not_called()


@patch("certcoach.core.database.get_analytics")
@patch("certcoach.core.database.get_user_profile")
@patch("certcoach.core.database.get_active_question_counts_by_difficulty")
@patch("certcoach.core.planner.load_syllabus")
def test_get_syllabus_status_reports_shortfall_but_still_schedules_lesson(
    mock_load_syllabus,
    mock_difficulty_counts,
    mock_get_profile,
    mock_get_analytics,
    tmp_path,
):
    from certcoach.core import planner

    original_data_dir = planner.DATA_DIR
    try:
        planner.DATA_DIR = str(tmp_path)
        raw_dir = tmp_path / "raw_markdowns"
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / "present.md").write_text("grounded content", encoding="utf-8")

        mock_get_profile.return_value = {"progress": {"completed_topics": [], "completed_subtopics": {}}}
        mock_get_analytics.return_value = {"topic_stats": []}
        mock_difficulty_counts.return_value = {"Easy": 2, "Medium": 2, "Hard": 4, "Other": 0}
        mock_load_syllabus.return_value = [{
            "id": 1,
            "topic": "Topic 1",
            "subtopics": ["Concept A"],
            "md_files": ["present.md"],
            "bank_topic_keys": ["Topic 1"],
        }]

        status = planner.get_syllabus_status("test_user")

        # Doc coverage exists, so the lesson is still schedulable even though the
        # concept falls short of the 3E+2M practice-readiness floor -- only the
        # practice step (not the lesson/Q&A) should be gated by question counts.
        assert status["next_topic"] is not None
        assert status["next_topic"]["next_ready_subtopic"] == "Concept A"
        assert status["insufficient_concepts"] == [{
            "topic_id": 1,
            "topic": "Topic 1",
            "concept": "Concept A",
            "active_questions": 8,
            "required_questions": 5,
            "easy_questions": 2,
            "required_easy": 3,
            "medium_questions": 2,
            "required_medium": 2,
        }]
    finally:
        planner.DATA_DIR = original_data_dir




