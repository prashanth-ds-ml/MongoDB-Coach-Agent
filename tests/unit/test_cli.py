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
    import datetime
    from certcoach.cli import recalibrate_study_plan
    
    future_date = (datetime.datetime.utcnow() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
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


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.coach")
def test_run_practice_questions_allows_option_b_answer(mock_coach, mock_prompt_ask, mock_database, mock_console):
    from certcoach.cli import run_practice_questions

    mock_database.get_random_questions.return_value = [
        {
            "_id": "q1",
            "question_text": "Which option is correct?",
            "options": [
                {"option_letter": "A", "code_snippet": "No", "is_correct": False, "feedback": "No."},
                {"option_letter": "B", "code_snippet": "Yes", "is_correct": True, "feedback": "Correct."},
                {"option_letter": "C", "code_snippet": "No", "is_correct": False, "feedback": "No."},
                {"option_letter": "D", "code_snippet": "No", "is_correct": False, "feedback": "No."},
            ],
            "metadata": {"topic": "Topic A"},
            "context": {}
        }
    ]
    mock_prompt_ask.side_effect = ["B", "H"]
    mock_coach.get_answer_feedback.return_value = "Good."

    score = run_practice_questions("Topic A", ["Topic A"], num=1, is_mock=False)

    assert score == 1
    mock_database.save_attempt.assert_called_once()


def test_format_explanation_template_strips_labels_and_sanitizes_feedback():
    from certcoach.cli import format_explanation_template

    q = {
        "metadata": {"topic": "BSON Data Types"},
        "options": [
            {"option_letter": "A", "code_snippet": "A) String", "is_correct": False, "feedback": "Correct. This stale feedback is wrong."},
            {"option_letter": "B", "code_snippet": "B) Array", "is_correct": True, "feedback": "Incorrect. This stale feedback is wrong."},
        ],
    }

    explanation = format_explanation_template("B", q)

    assert "Option B (`Array`)" in explanation
    assert "`A) String`" not in explanation
    assert "`String`" in explanation
    assert "stored feedback for this item needs editorial review" in explanation


@patch("certcoach.cli.console")
@patch("certcoach.cli.database")
@patch("certcoach.cli.Prompt.ask")
@patch("certcoach.cli.coach")
def test_run_practice_questions_next_prompt_q_exits(mock_coach, mock_prompt_ask, mock_database, mock_console):
    from certcoach.cli import run_practice_questions

    mock_database.get_random_questions.return_value = [
        {
            "_id": "q1",
            "question_text": "Question 1",
            "options": [
                {"option_letter": "A", "code_snippet": "A) Yes", "is_correct": True, "feedback": "Correct."},
                {"option_letter": "B", "code_snippet": "B) No", "is_correct": False, "feedback": "Incorrect."},
            ],
            "metadata": {"topic": "Topic A"},
            "context": {},
        },
        {
            "_id": "q2",
            "question_text": "Question 2",
            "options": [
                {"option_letter": "A", "code_snippet": "A) Yes", "is_correct": True, "feedback": "Correct."},
                {"option_letter": "B", "code_snippet": "B) No", "is_correct": False, "feedback": "Incorrect."},
            ],
            "metadata": {"topic": "Topic A"},
            "context": {},
        },
    ]
    mock_prompt_ask.side_effect = ["A", "H", "q"]
    mock_coach.get_answer_feedback.return_value = "Good."

    with patch("time.sleep"):
        score = run_practice_questions("Topic A", ["Topic A"], num=2, is_mock=False)

    assert score is None
    assert mock_database.save_attempt.call_count == 1


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
def test_run_ai_question_wizard(mock_confirm, mock_prompt, mock_database):
    from certcoach.cli import run_ai_question_wizard
    
    # Test quality analytics report viewing
    mock_prompt.side_effect = ["2", ""] # Select View Quality report, then Press Enter
    mock_database.get_questions_quality_analytics.return_value = [
        {"question_text": "Q1", "topic": "CRUD", "attempts": 5, "success_rate": 20.0, "average_time": 10.0, "difficulty": "Hard", "flag": "Needs Review"}
    ]
    
    with patch("certcoach.cli.print_paginated") as mock_print:
        run_ai_question_wizard()
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
    def mock_get_random(topic=None, limit=10, subtopic_keywords=None, difficulty=None, strict_keywords=False):
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
        topic="Topic A", limit=10, subtopic_keywords=None, difficulty="Easy", strict_keywords=True
    )
    mock_database.get_random_questions.assert_any_call(
        topic="Topic A", limit=10, subtopic_keywords=None, difficulty="Medium", strict_keywords=True
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
        
    mock_planner.mark_subtopic_complete.assert_called_once_with("local_user_1", "Topic A", "Concept X")


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
    from certcoach.cli import validate_lexical_syntax_guard
    
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
    
    # 3. Python topic - contains PyMongo snake_case - should pass
    ok, err = validate_lexical_syntax_guard(
        "MongoDB Drivers & PyMongo",
        "How do you insert a document in PyMongo?",
        ["client.db.coll.insert_one({'x': 1})", "client.db.coll.insertOne()"]
    )
    assert ok is True
    
    # 4. Python topic - lacks PyMongo snake_case - should fail
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
    from datetime import datetime, timedelta
    
    mock_profile = {
        "_id": "local_user_1",
        "streak_days": 5,
        "last_login_date": (datetime.utcnow().date() - timedelta(days=2)).isoformat(),
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
        assert second_call_args["last_login_date"] == datetime.utcnow().date().isoformat()
        
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
    
    def mock_get_random(topic=None, limit=10, subtopic_keywords=None, difficulty=None, strict_keywords=False):
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
    mock_database.award_streak_freeze.assert_called_once_with("local_user_1")
    # Verify streak freeze announcement printed
    printed_text = "\n".join(
        str(call[0][0]) for call in mock_console.print.call_args_list if call[0]
    )
    assert "earned a Streak Freeze token" in printed_text




