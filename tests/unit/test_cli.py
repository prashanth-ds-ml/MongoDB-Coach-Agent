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
@patch("certcoach.cli.Confirm.ask")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.show_exam_traps")
def test_main_menu_startup_briefing(mock_show_traps, mock_prompt_ask, mock_confirm_ask, mock_onboarding, mock_coach, mock_planner, mock_database, mock_console):
    from certcoach.cli import main_menu
    
    mock_planner.get_due_review_topics.return_value = []
    mock_coach.get_daily_greeting.return_value = "Hello Student!"
    
    # Mock status to avoid iterating on agenda/status list inside main_menu
    mock_planner.get_syllabus_status.return_value = {
        "mastery_percent": 0.0,
        "mastered_count": 0,
        "total_topics": 12,
        "mock_exam_unlocked": False,
        "unlock_threshold_percent": 70
    }
    mock_planner.generate_daily_agenda.return_value = []
    
    # Force Confirm to return True, then prompt ask to raise SystemExit or KeyboardInterrupt to break loop
    mock_confirm_ask.return_value = True
    mock_prompt_ask.side_effect = KeyboardInterrupt()
    
    try:
        main_menu()
    except (KeyboardInterrupt, SystemExit):
        pass
        
    mock_confirm_ask.assert_called_once_with("  Would you like to review the Exam Cheat Sheet now?")
    mock_show_traps.assert_called_once()


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
