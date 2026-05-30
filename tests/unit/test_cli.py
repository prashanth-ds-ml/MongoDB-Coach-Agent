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
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.ask")
def test_recalibrate_study_plan(mock_ask, mock_confirm, mock_planner, mock_database, mock_console):
    from certcoach.cli import recalibrate_study_plan
    
    mock_ask.side_effect = ["30", "2"]
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
@patch("certcoach.core.planner.load_syllabus")
def test_get_syllabus_status_skipping(mock_load_syllabus, mock_get_profile, mock_get_analytics, tmp_path):
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
        
        t1 = {"id": 1, "topic": "Topic 1", "md_files": ["missing.md"]}
        t2 = {"id": 2, "topic": "Topic 2", "md_files": ["present.md"]}
        (raw_dir / "present.md").write_text("grounded content", encoding="utf-8")
        
        mock_load_syllabus.return_value = [t1, t2]
        
        status = planner.get_syllabus_status("test_user")
        assert status["next_topic"] == t2
        assert len(status["skipped_unmapped_topics"]) == 1
        assert status["skipped_unmapped_topics"][0]["topic"] == "Topic 1"
    finally:
        planner.DATA_DIR = original_data_dir


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
@patch("certcoach.core.planner.load_syllabus")
def test_generate_daily_agenda_skipping_reviews(mock_load_syllabus, mock_get_profile, mock_get_analytics, mock_get_attempts, tmp_path):
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
        
        mock_get_attempts.return_value = [
            {
                "topic": "Topic 1",
                "timestamp": (datetime.datetime.utcnow() - datetime.timedelta(days=5)).isoformat(),
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


@patch("certcoach.cli.console")
@patch("certcoach.cli.coach")
@patch("certcoach.cli.planner")
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.run_practice_questions")
def test_run_teach_session_skipping_and_practice_jump(mock_practice, mock_prompt_ask, mock_confirm_ask, mock_planner, mock_coach, mock_console):
    from certcoach.cli import run_teach_session
    
    mock_planner.load_md_context.return_value = "dummy context"
    mock_confirm_ask.return_value = False
    mock_practice.return_value = 5
    
    agenda_item = {
        "topic": "Topic A",
        "subtopics": ["Subtopic A", "Subtopic B", "Subtopic C"],
        "md_files": [],
        "bank_keys": ["Topic A"],
        "question_keywords": []
    }
    
    def mock_explain(topic, subtopic, context):
        if subtopic == "Subtopic A":
            return "This is not covered in my official docs."
        return f"Explanation for {subtopic}\n**Micro-Challenge**:\nWhat is 1+1?\nType your answer or ask any questions."
        
    mock_coach.explain_topic.side_effect = mock_explain
    mock_prompt_ask.side_effect = ["practice", "n"]
    
    with patch("time.sleep"):
        run_teach_session(agenda_item)
        
    mock_coach.explain_topic.assert_any_call("Topic A", "Subtopic A", "dummy context")
    mock_coach.explain_topic.assert_any_call("Topic A", "Subtopic B", "dummy context")
    
    called_subtopics = [call[0][1] for call in mock_coach.explain_topic.call_args_list]
    assert "Subtopic C" not in called_subtopics
    
    mock_practice.assert_called_with("Topic A", ["Topic A"], question_keywords=[], num=5, is_mock=False)


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




