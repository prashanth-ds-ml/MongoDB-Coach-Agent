"""
CertCoach CLI — Main Application
=================================
Commands available at any prompt:
  q / quit / exit  →  save and quit immediately
  back             →  return to main menu
"""
import sys
import os
import time
import datetime
import random

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(__file__), "scripts/core"))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.table import Table
from rich.rule import Rule
from rich.text import Text
from rich import box

from certcoach.core import database, planner
from certcoach.core.persona import CoachPersona
import certcoach.core.memory_manager as memory_manager

console = Console()
coach = CoachPersona()
USER_ID = "local_user_1"

EXIT_COMMANDS = {"q", "quit", "exit"}
BACK_COMMANDS = {"back", "b", "menu"}


# ---------------------------------------------------------------------------
# UTILS
# ---------------------------------------------------------------------------

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def ask(prompt_text: str, choices: list = None) -> str:
    """
    Wrapper around Prompt.ask that handles exit/back commands globally.
    Raises SystemExit on quit, returns '__back__' on back.
    """
    try:
        if choices:
            # Add 'q' as always-valid meta-choice
            value = Prompt.ask(prompt_text, choices=choices + ["q"]).strip().lower()
        else:
            value = Prompt.ask(prompt_text).strip()
    except (KeyboardInterrupt, EOFError):
        raise SystemExit

    if value.lower() in EXIT_COMMANDS:
        raise SystemExit
    if value.lower() in BACK_COMMANDS:
        return "__back__"
    return value


def exit_message():
    console.print()
    console.print(Panel(
        "[bold green]Session saved. Keep grinding — the exam won't pass itself! 💪[/bold green]",
        border_style="green", box=box.ROUNDED
    ))
    console.print()


def print_paginated(renderable, title: str = "CertCoach"):
    """
    Renders a Rich renderable with dynamic scroll-back, line-by-line arrow key 
    scrolling, and page-up/down using standard msvcrt on Windows.
    """
    import shutil
    import sys
    
    try:
        import msvcrt
        is_windows = True
    except ImportError:
        is_windows = False
    
    # Get dynamic terminal dimensions
    _, term_height = shutil.get_terminal_size()
    
    # Capture styled console output (with full ANSI escapes preserved)
    with console.capture() as capture:
        console.print(renderable)
    rendered_text = capture.get()
    lines = rendered_text.splitlines()
    
    total_lines = len(lines)
    if total_lines <= term_height - 2:
        # Fits entirely within the current terminal view, print normally
        console.print(renderable)
        return

    # Visible window size (terminal height minus rules and metadata headers)
    visible_height = max(5, term_height - 5)
    current_scroll = 0

    if not is_windows:
        # Cross-platform fallback for non-Windows systems (basic scrolling)
        page_size = visible_height
        page_num = 1
        while current_scroll < total_lines:
            clear()
            console.print(Rule(f"[bold cyan]{title} — Page {page_num}[/bold cyan]"))
            console.print()
            end_line = min(current_scroll + page_size, total_lines)
            for idx in range(current_scroll, end_line):
                sys.stdout.write(lines[idx] + "\n")
            console.print()
            if end_line >= total_lines:
                Prompt.ask("  [dim]End of content. Press Enter to continue[/dim]")
                break
            try:
                action = Prompt.ask("  [bold cyan]❯[/bold cyan] [dim]Press Enter to read more, or type 'q' to stop[/dim]").lower()
            except (KeyboardInterrupt, EOFError):
                raise SystemExit
            if action in ("q", "quit"):
                break
            current_scroll += page_size
            page_num += 1
        return

    # Windows Keyboard Interactive Scroll Loop
    while True:
        clear()
        console.print(Rule(f"[bold cyan]{title} — Line {current_scroll + 1}-{min(current_scroll + visible_height, total_lines)} of {total_lines}[/bold cyan]"))
        console.print()
        
        # Display the visible slice of lines
        end_idx = min(current_scroll + visible_height, total_lines)
        for idx in range(current_scroll, end_idx):
            sys.stdout.write(lines[idx] + "\n")
            
        console.print()
        console.print(
            "  [dim]↑/↓ Arrows: Line scroll | PgUp/PgDn: Page scroll | Space: Page down | q: Quit[/dim]"
        )
        
        # Read character key-press
        try:
            ch = msvcrt.getch()
        except (KeyboardInterrupt, EOFError):
            raise SystemExit
            
        if ch in (b'\x00', b'\xe0'):
            # Special multi-byte key prefix, read secondary byte
            try:
                sub_ch = msvcrt.getch()
            except (KeyboardInterrupt, EOFError):
                raise SystemExit
                
            if sub_ch == b'H':  # Arrow Up (↑)
                current_scroll = max(0, current_scroll - 1)
            elif sub_ch == b'P':  # Arrow Down (↓)
                current_scroll = min(total_lines - visible_height, current_scroll + 1)
            elif sub_ch == b'I':  # Page Up (PgUp)
                current_scroll = max(0, current_scroll - visible_height)
            elif sub_ch == b'Q':  # Page Down (PgDn)
                current_scroll = min(total_lines - visible_height, current_scroll + visible_height)
        else:
            # Single-byte standard characters
            if ch.lower() == b'q':
                break
            elif ch == b' ':  # Space (Page Down)
                current_scroll = min(total_lines - visible_height, current_scroll + visible_height)
            elif ch.lower() == b'b':  # 'b' (Page Up)
                current_scroll = max(0, current_scroll - visible_height)
            elif ch in (b'\r', b'\n'):  # Enter (Line Down)
                current_scroll = min(total_lines - visible_height, current_scroll + 1)


# ---------------------------------------------------------------------------
# ONBOARDING
# ---------------------------------------------------------------------------

def run_onboarding():
    profile = database.get_user_profile(USER_ID)

    # If calendar already stored, skip
    if profile.get("exam_date") and profile.get("study_calendar"):
        return

    clear()
    console.print(Rule("[bold cyan]CertCoach — MongoDB Certification Prep[/bold cyan]"))
    console.print()
    console.print(Panel(
        "[bold white]I am CertCoach — your strict but friendly MongoDB Certification Instructor.[/bold white]\n\n"
        "I will build a personalised, day-by-day study plan and guide you through every topic. "
        "Full Mock Exams are [bold yellow]locked[/bold yellow] until you master "
        "[bold yellow]70%[/bold yellow] of the syllabus.\n\n"
        "[dim]Tip: Type [bold]q[/bold] at any prompt to save and quit.[/dim]",
        title="👋  Welcome", border_style="cyan", box=box.ROUNDED
    ))
    console.print()

    # --- Ask exam date ---
    while True:
        days_str = ask("[bold]How many days from today is your MongoDB exam?[/bold] (e.g. 30)")
        if days_str == "__back__":
            continue
        try:
            days = int(days_str)
            if days < 1:
                raise ValueError
            break
        except ValueError:
            console.print("[red]Please enter a valid number greater than 0.[/red]")

    exam_date = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    
    # --- Ask experience level ---
    console.print()
    exp_in = ask("[bold]What is your current MongoDB experience level?[/bold] (1=Beginner, 2=Intermediate, 3=Advanced)", choices=["1", "2", "3"])
    exp_map = {"1": "Beginner", "2": "Intermediate", "3": "Advanced"}
    if exp_in == "__back__": exp_in = "1"
    experience_level = exp_map.get(exp_in, "Beginner")

    diagnostic_mastered = []
    console.print()
    if Confirm.ask("[bold]Take a quick 10-question diagnostic to skip topics you already know?[/bold]"):
        all_topics = planner.load_syllabus()
        all_keys = []
        for item in all_topics:
            all_keys.extend(item.get("bank_topic_keys", []))
            
        run_practice_questions("Diagnostic Test", list(set(all_keys)), num=10, is_mock=True)
        stats = database.get_analytics(USER_ID)
        for ts in stats.get("topic_stats", []):
            if ts["attempts"] > 0 and (ts["correct"] / ts["attempts"]) >= 0.8:
                diagnostic_mastered.append(ts["topic"])
                planner.mark_topic_complete(USER_ID, ts["topic"])

    database.update_user_profile(USER_ID, {"exam_date": exam_date.isoformat(), "experience_level": experience_level})

    # --- Generate calendar ---
    console.print()
    console.print("[dim]Building your study plan...[/dim]")
    calendar = planner.generate_study_calendar(days, experience_level, diagnostic_mastered)
    database.update_user_profile(USER_ID, {"study_calendar": calendar})

    # --- Show the plan ---
    show_plan_preview(calendar, days)

    # --- Confirm ---
    console.print()
    answer = ask("[bold]Does this plan work for you? Start studying now?[/bold] (yes/no)", choices=["yes", "no", "y", "n"])
    if answer in ("no", "n"):
        console.print("[yellow]No problem — edit the plan by restarting and entering a different number of days.[/yellow]")
        time.sleep(2)


def show_plan_preview(calendar: list, total_days: int):
    """Renders the full study calendar as a rich table."""
    clear()
    console.print(Rule(f"[bold cyan]Your {total_days}-Day Study Plan[/bold cyan]"))
    console.print()

    table = Table(box=box.MINIMAL, header_style="bold blue", show_lines=False)
    table.add_column("Day", width=4, justify="right")
    table.add_column("Date", width=12)
    table.add_column("Phase", width=10)
    table.add_column("Topic", min_width=36)
    table.add_column("Weight", width=8, justify="center")

    weight_color = {"High": "red", "Medium": "yellow", "Low": "green"}
    phase_color = {"Study": "cyan", "Mock & Revision": "magenta"}

    for item in calendar:
        wc = weight_color.get(item["exam_weight"], "white")
        pc = phase_color.get(item["phase"], "white")
        table.add_row(
            str(item["day_num"]),
            item["date"],
            f"[{pc}]{item['phase']}[/{pc}]",
            item["topic"],
            f"[{wc}]{item['exam_weight']}[/{wc}]" if item["exam_weight"] else "",
        )

    from rich.console import Group
    from rich.text import Text
    
    footer_text = Text.from_markup(
        f"\n  📘 [bold]{sum(1 for i in calendar if i['phase']=='Study')}[/bold] study days  |  "
        f"🏆 [bold]{sum(1 for i in calendar if i['phase']=='Mock & Revision')}[/bold] mock/revision days  |  "
        f"🔒 Full Mock unlocks at [bold]70%[/bold] syllabus mastery"
    )
    group = Group(table, footer_text)
    print_paginated(group, title=f"{total_days}-Day Study Plan")


# ---------------------------------------------------------------------------
# TEACH → Q&A → PRACTICE FLOW
# ---------------------------------------------------------------------------

def run_teach_session(agenda_item: dict):
    """
    Full study session for a topic:
    1. Coach explains the topic.
    2. Open Q&A until user says 'done' / 'practice' / 'q'.
    3. Offer 5-question practice quiz.
    4. Mini-mock offer.
    """
    topic = agenda_item["topic"]
    subtopics = agenda_item.get("subtopics", [])
    md_files = agenda_item.get("md_files", [])
    bank_keys = agenda_item.get("bank_keys", [topic])
    question_keywords = agenda_item.get("question_keywords", [])

    console.print(Rule(f"[bold cyan]Today's Topic: {topic}[/bold cyan]"))
    console.print("[dim]  Type [bold]q[/bold] at any point to save and quit.\n[/dim]")

    # ---- 1. EXPLAIN & Q&A LOOP ----
    md_context = planner.load_md_context(md_files)
    
    chat_history = memory_manager.load_active_history()
    
    # Fallback if no subtopics defined
    if not subtopics:
        subtopics = [topic]

    for idx, subtopic in enumerate(subtopics):
        with console.status(f"[dim]🤖 Coach is preparing lesson for: {subtopic}...[/dim]", spinner="dots"):
            explanation = coach.explain_topic(topic, subtopic, md_context)
        
        panel = Panel(
            Markdown(explanation, code_theme="monokai"),
            title=f"🧑‍🏫  CertCoach teaches: {subtopic}",
            border_style="cyan", box=box.ROUNDED,
            padding=(1, 2),
        )
        print_paginated(panel, title=f"Lesson: {subtopic}")
        
        memory_manager.log_interaction("assistant", explanation)
        chat_history = memory_manager.load_active_history()
        console.print()
        console.print(
            "  [dim]Answer the micro-challenge, ask a question, or type [bold]next[/bold] to proceed.[/dim]"
        )

        while True:
            console.print()
            try:
                user_input = Prompt.ask("\n  [bold blue]❯[/bold blue]").strip()
            except (KeyboardInterrupt, EOFError):
                raise SystemExit

            if not user_input:
                continue

            if user_input.lower() in EXIT_COMMANDS:
                raise SystemExit

            if user_input.lower() in BACK_COMMANDS:
                return

            if user_input.lower() in ("done", "practice", "p", "next"):
                break

            # Generate follow-up answer
            memory_manager.log_interaction("user", user_input)
            chat_history = memory_manager.load_active_history()
            with console.status("[dim]🤖 CertCoach is thinking...[/dim]", spinner="dots"):
                answer = coach.handle_followup(topic, user_input, chat_history)
            memory_manager.log_interaction("assistant", answer)
            chat_history = memory_manager.load_active_history()

            console.print()
            console.print(Panel(
                Markdown(answer, code_theme="monokai"),
                title="🧑‍🏫  CertCoach",
                border_style="blue", box=box.ROUNDED,
                padding=(1, 2),
            ))

    # ---- 3. PRACTICE OFFER ----
    console.print()
    console.print(Panel(
        "[bold]Great — let's test what you just learned.[/bold]\n"
        "I'll pull 5 questions from the official question bank for this topic.",
        border_style="green", box=box.ROUNDED
    ))
    time.sleep(1)

    score = run_practice_questions(topic, bank_keys, question_keywords=question_keywords, num=5, is_mock=False)

    # ---- 4. MINI MOCK OFFER ----
    console.print()
    if Confirm.ask("  Want a quick [bold]5-question Mini-Mock[/bold] on this topic (no coaching, just speed)?"):
        run_practice_questions(topic, bank_keys, question_keywords=question_keywords, num=5, is_mock=True)

    # Mark mastered if good score
    if score is not None and score >= 4:
        planner.mark_topic_complete(USER_ID, topic)
        console.print(f"\n  [bold green]🏆 '{topic}' marked as mastered![/bold green]")

    try:
        ans = Prompt.ask("\n  [bold]Ready for the next agenda item?[/bold] (Y/n)", choices=["y", "n", "yes", "no", "q"]).lower()
    except (KeyboardInterrupt, EOFError):
        raise SystemExit

    if ans in EXIT_COMMANDS:
        raise SystemExit
    return ans in ("y", "yes")

def run_free_chat_session(initial_query: str):
    console.print(Rule("[bold cyan]💬 Free Chat with CertCoach[/bold cyan]"))
    console.print("[dim]  Type [bold]q[/bold] or [bold]back[/bold] at any point to leave.\n[/dim]")
    
    chat_history = memory_manager.load_active_history()
    user_input = initial_query
    
    # Compile Student Context
    status = planner.get_syllabus_status(USER_ID)
    stats = database.get_analytics(USER_ID)
    agenda = planner.generate_daily_agenda(USER_ID)
    
    topic_stats = stats.get("topic_stats", [])
    topic_stats.sort(key=lambda x: (x["correct"] / max(1, x["attempts"])))
    weak_topics = [ts["topic"] for ts in topic_stats if ts["attempts"] > 0][:3]
    weak_str = ", ".join(weak_topics) if weak_topics else "None (Keep practicing to generate data!)"
    next_topic = agenda[0]["topic"] if agenda else "All caught up!"
    
    student_context = (
        f"- Mastery: {status['mastery_percent']}%\n"
        f"- Next Agenda Topic: {next_topic}\n"
        f"- Weakest Topics: {weak_str}"
    )
    
    while True:
        if user_input:
            memory_manager.log_interaction("user", user_input)
            chat_history = memory_manager.load_active_history()
            with console.status("[dim]🤖 CertCoach is thinking...[/dim]", spinner="dots"):
                answer = coach.handle_free_chat(user_input, chat_history, student_context)
            memory_manager.log_interaction("assistant", answer)
            chat_history = memory_manager.load_active_history()
            
            console.print()
            panel = Panel(
                Markdown(answer, code_theme="monokai"),
                title="🧑‍🏫  CertCoach",
                border_style="blue", box=box.ROUNDED,
                padding=(1, 2),
            )
            console.print(panel)
            
        console.print()
        try:
            user_input = Prompt.ask("\n  [bold blue]❯[/bold blue]").strip()
        except (KeyboardInterrupt, EOFError):
            break
            
        if not user_input:
            continue
            
        if user_input.lower() in EXIT_COMMANDS:
            raise SystemExit
            
        if user_input.lower() in BACK_COMMANDS:
            break

def run_scenario_simulator():
    clear()
    console.print(Rule("[bold cyan]💻 Scenario Simulator[/bold cyan]"))
    console.print("[dim]  Apply your MongoDB knowledge to real-world product requirements.\n[/dim]")
    
    status = planner.get_syllabus_status(USER_ID)
    mastered = [s["topic"] for s in status["status_list"] if s["is_mastered"]]
    
    if not mastered:
        topic = "MongoDB Basics / Document Model"
    else:
        topic = random.choice(mastered)
        
    with console.status(f"[dim]🤖 Coach is generating a scenario for: {topic}...[/dim]", spinner="dots"):
        scenario = coach.generate_scenario(topic)
    
    console.print(Panel(Markdown(scenario, code_theme="monokai"), title="📋 Product Requirement", border_style="bright_black", box=box.ROUNDED, padding=(1, 2)))
    
    console.print()
    try:
        user_answer = Prompt.ask("\n  [bold blue]❯[/bold blue] Your Approach / Query [dim](or 'q' to quit)[/dim]").strip()
    except (KeyboardInterrupt, EOFError):
        return
        
    if user_answer.lower() in EXIT_COMMANDS:
        return
        
    with console.status("[dim]🤖 Coach is evaluating your approach...[/dim]", spinner="dots"):
        eval_text = coach.evaluate_scenario(topic, scenario, user_answer)
    
    panel = Panel(Markdown(eval_text, code_theme="monokai"), title="🧑‍🏫 CertCoach Evaluation", border_style="blue", box=box.ROUNDED, padding=(1, 2))
    print_paginated(panel, title="Scenario Evaluation")
    try:
        ans = Prompt.ask("\n  [bold blue]❯[/bold blue] [dim]Press Enter to return, or type a question to chat[/dim]")
        if ans.strip() and ans.strip().lower() not in EXIT_COMMANDS:
            run_free_chat_session(ans.strip())
    except (KeyboardInterrupt, EOFError):
        pass

# ---------------------------------------------------------------------------
# PRACTICE QUESTIONS
# ---------------------------------------------------------------------------

def run_practice_questions(topic: str, bank_keys: list, num: int = 5, is_mock: bool = False, question_keywords: list = None) -> int | None:
    clear()

    # Gather questions filtered by topic + keyword relevance
    questions = []
    for key in bank_keys:
        questions.extend(
            database.get_random_questions(
                topic=key,
                limit=num * 2,  # fetch extra so keyword filter has room to narrow
                subtopic_keywords=question_keywords
            )
        )

    # Deduplicate
    seen, unique = set(), []
    for q in questions:
        qt = q.get("question_text", "")
        if qt not in seen:
            seen.add(qt)
            unique.append(q)

    random.shuffle(unique)
    questions = unique[:num]

    if not questions:
        console.print(f"[yellow]  No questions found for this topic yet. AI generation not available offline.[/yellow]")
        time.sleep(2)
        return None

    score = 0
    label = "Mini-Mock" if is_mock else "Practice"
    console.print(Rule(f"[bold cyan]{label}: {topic}[/bold cyan]"))

    for idx, q in enumerate(questions):
        meta = q.get("metadata", {})
        context = q.get("context", {})
        q_topic = meta.get("topic", topic)

        console.print()
        console.print(f"  [dim]Q {idx + 1}/{len(questions)}[/dim]")

        if context.get("scenario_description"):
            console.print(Panel(context["scenario_description"], title="📋 Scenario", border_style="dim", box=box.ROUNDED, padding=(0, 1)))

        console.print(Panel(f"[bold]{q.get('question_text', '')}[/bold]", border_style="bright_black", box=box.ROUNDED, padding=(0, 2)))

        valid_options = []
        for opt in q.get("options", []):
            letter = opt.get("option_letter", "?")
            valid_options.append(letter.upper())
            console.print(f"    [bold yellow]{letter})[/bold yellow]  {opt.get('code_snippet', '')}")

        console.print()
        try:
            ans = Prompt.ask("  [bold]Answer[/bold]", choices=valid_options + ["q"]).upper()
        except (KeyboardInterrupt, EOFError):
            raise SystemExit

        if ans.lower() in EXIT_COMMANDS:
            raise SystemExit

        # Evaluate
        if not is_mock:
            try:
                conf_in = Prompt.ask("  Confidence? [bold](H)[/bold] / [bold](M)[/bold] / [bold](L)[/bold]",
                                     choices=["H", "M", "L", "q"]).upper()
            except (KeyboardInterrupt, EOFError):
                raise SystemExit
            if conf_in.lower() in EXIT_COMMANDS:
                raise SystemExit
            confidence = {"H": "High", "M": "Medium", "L": "Low"}.get(conf_in, "Medium")
        else:
            confidence = "High"

        correct_option = None
        user_feedback = ""
        is_correct = False
        for opt in q.get("options", []):
            if opt.get("is_correct"):
                correct_option = opt
            if opt.get("option_letter", "").upper() == ans:
                user_feedback = opt.get("feedback", "")
                is_correct = opt.get("is_correct", False)

        database.save_attempt(USER_ID, str(q.get("_id", "unknown")),
                              q_topic, ans, is_correct, confidence)

        if is_correct:
            score += 1
            console.print(f"\n  [bold green]✅ Correct![/bold green]")
        else:
            console.print(f"\n  [bold red]❌ Wrong.[/bold red]")
            if correct_option:
                console.print(f"  Correct answer: [bold]{correct_option.get('option_letter')}[/bold]")

        console.print(Panel(user_feedback or "—", title="📖 Official Feedback", border_style="yellow", box=box.ROUNDED, padding=(0, 2)))

        if not is_mock:
            with console.status("[dim]🤖 Coach is reflecting...[/dim]", spinner="dots"):
                fb = coach.get_answer_feedback(q_topic, is_correct, user_feedback, confidence)
            console.print(Panel(Markdown(fb, code_theme="monokai"), title="🧑‍🏫 CertCoach", border_style="blue", box=box.ROUNDED, padding=(0, 2)))

        if idx < len(questions) - 1:
            try:
                Prompt.ask("\n  [dim]Enter for next / q to quit[/dim]")
            except (KeyboardInterrupt, EOFError):
                raise SystemExit

    # Result summary
    clear()
    pct = score / len(questions) * 100
    col = "green" if pct >= 80 else "yellow" if pct >= 60 else "red"
    console.print(Rule("[bold]Results[/bold]"))
    console.print(f"\n  Score: [{col}][bold]{score}/{len(questions)}  ({pct:.0f}%)[/bold][/{col}]\n")

    if pct >= 80:
        console.print("  [green]Excellent — strong understanding![/green]")
    elif pct >= 60:
        console.print("  [yellow]Decent, but review the explanations above before moving on.[/yellow]")
    else:
        console.print("  [red]Below 60% — Coach will schedule a review session tomorrow.[/red]")

    return score


# ---------------------------------------------------------------------------
# SYLLABUS / GAP REPORT
# ---------------------------------------------------------------------------

def show_syllabus_status():
    clear()
    status = planner.get_syllabus_status(USER_ID)

    console.print(Rule("[bold cyan]📚 Syllabus Coverage Report[/bold cyan]"))
    console.print(
        f"\n  Mastery: [bold {'green' if status['mastery_percent'] >= 70 else 'yellow'}]"
        f"{status['mastery_percent']}%[/]  ({status['mastered_count']}/{status['total_topics']} topics)  |  "
        f"Full Mock: {'[green]🔓 Unlocked[/green]' if status['mock_exam_unlocked'] else '[red]🔒 Locked[/red]'}\n"
    )

    table = Table(box=box.MINIMAL, header_style="bold blue")
    table.add_column("#", width=3)
    table.add_column("Topic", min_width=32)
    table.add_column("Wt.", width=6, justify="center")
    table.add_column("Qs?", width=5, justify="center")
    table.add_column("Tries", width=6, justify="right")
    table.add_column("Acc.", width=6, justify="right")
    table.add_column("Status", width=12, justify="center")

    wc = {"High": "red", "Medium": "yellow", "Low": "green"}
    for s in status["status_list"]:
        acc_col = "green" if s["accuracy"] >= 80 else "yellow" if s["accuracy"] >= 50 else "red"
        table.add_row(
            str(s["id"]),
            s["topic"],
            f"[{wc.get(s['exam_weight'],'white')}]{s['exam_weight'][0]}[/]",
            "[green]✓[/green]" if s["has_questions"] else "[red]✗[/red]",
            str(s["attempts"]),
            f"[{acc_col}]{s['accuracy']}%[/]" if s["attempts"] > 0 else "—",
            "[bold green]✅[/bold green]" if s["is_mastered"] else "[dim]—[/dim]",
        )

    from rich.console import Group
    elements = []
    
    # Audit reference documentation files
    audit = planner.audit_documentation_files()
    if audit["incomplete"] or audit["empty"]:
        alert_lines = ["[bold yellow]⚠️  Missing Syllabus Reference Documentation Files:[/bold yellow]\n"]
        
        for item in audit["incomplete"]:
            missing_str = ", ".join(f"[bold red]{f}[/bold red]" for f in item["missing"])
            alert_lines.append(f"  • [cyan]Topic #{item['id']}[/cyan] ({item['topic']}) is missing: {missing_str}")
            
        for item in audit["empty"]:
            alert_lines.append(f"  • [red]Topic #{item['id']}[/red] ({item['topic']}) has no markdown reference files mapped")
            
        alert_lines.append("\n[dim]Please provide which topics to include in the docs (add these missing files to [bold cyan]data/raw_markdowns/[/bold cyan]) so that the Coach can help in learning those topics.[/dim]")
        
        missing_panel = Panel(
            "\n".join(alert_lines),
            title="[bold yellow]📂 Reference Files Audit Alert[/bold yellow]",
            border_style="yellow", box=box.ROUNDED
        )
        elements.append(missing_panel)
        elements.append(Text("\n"))
        
    elements.append(table)
    if status["gap_topics"]:
        elements.append(Panel(
            "\n".join(f"  [red]✗[/red] {t}" for t in status["gap_topics"]),
            title="⚠️  Topics Missing from Question Bank (AI will generate questions)",
            border_style="red"
        ))
    group = Group(*elements)
    print_paginated(group, title="Syllabus Status")

    console.print()
    console.print("  [bold blue]⚡ Sub-Options[/bold blue]")
    console.print("  [dim]" + "─"*40 + "[/dim]")
    console.print("  [bold cyan]a[/bold cyan].   📝  Run Documentation & Raw Files Audit")
    console.print("  [bold cyan]Enter[/bold cyan]. Return to Main Menu")
    console.print()

    try:
        ans = Prompt.ask("\n  [bold blue]❯[/bold blue] [dim]Select option (a) or type a question to chat[/dim]")
        if ans.strip().lower() == "a":
            show_documentation_audit()
        elif ans.strip() and ans.strip().lower() not in EXIT_COMMANDS:
            run_free_chat_session(ans.strip())
    except (KeyboardInterrupt, EOFError):
        raise SystemExit


def show_documentation_audit():
    clear()
    
    audit = planner.audit_documentation_files()
    
    elements = []
    
    # 1. Complete/Present
    if audit["complete"]:
        present_text = ["[bold green]✅ Complete Mappings (Files Present)[/bold green]"]
        for item in audit["complete"]:
            files_str = ", ".join(f"[dim]{f}[/dim]" for f in item["present"])
            present_text.append(f"  • [bold cyan]#{item['id']}[/bold cyan] {item['topic']} → {files_str}")
        elements.append("\n".join(present_text))

    # 2. Incomplete (Files missing)
    if audit["incomplete"]:
        inc_text = ["\n[bold yellow]⚠️  Incomplete Mappings (Expected files missing from data/raw_markdowns/)[/bold yellow]"]
        for item in audit["incomplete"]:
            missing_str = ", ".join(f"[bold red]{f}[/bold red]" for f in item["missing"])
            present_str = ", ".join(f"[dim]{f}[/dim]" for f in item["present"]) if item["present"] else "None"
            inc_text.append(f"  • [bold cyan]#{item['id']}[/bold cyan] {item['topic']}")
            inc_text.append(f"    Found: {present_str} | Missing: {missing_str}")
        elements.append("\n".join(inc_text))

    # 3. Empty (No files mapped yet)
    if audit["empty"]:
        emp_text = ["\n[bold red]❌ Gaps (No reference markdown files mapped to these topics)[/bold red]"]
        for item in audit["empty"]:
            emp_text.append(f"  • [bold cyan]#{item['id']}[/bold cyan] {item['topic']}")
            sub_str = ", ".join(item["subtopics"])
            emp_text.append(f"    Subtopics to cover: {sub_str}")
        elements.append("\n".join(emp_text))
        
    elements.append(Panel(
        "[bold white]To populate missing or empty documentation:[/bold white]\n"
        "1. Create a markdown file inside [bold cyan]data/raw_markdowns/[/bold cyan]\n"
        "2. Copy-paste official MongoDB documentation text into it\n"
        "3. (Optional) Associate it in [bold cyan]data/syllabus.json[/bold cyan] by adding its filename to the topic's [bold]\"md_files\"[/bold] array.",
        border_style="cyan"
    ))
    
    from rich.console import Group
    from rich.text import Text
    renderables = []
    for el in elements:
        if isinstance(el, str):
            renderables.append(Text.from_markup(el))
        else:
            renderables.append(el)
            
    group = Group(*renderables)
    print_paginated(group, title="Reference Documentation Audit")
    
    try:
        Prompt.ask("\n  [dim]Press Enter to return to the Syllabus Status menu[/dim]")
    except (KeyboardInterrupt, EOFError):
        raise SystemExit


# ---------------------------------------------------------------------------
# ANALYTICS
# ---------------------------------------------------------------------------

def show_analytics():
    clear()
    stats = database.get_analytics(USER_ID)
    total = stats["total_attempts"]
    correct = stats["correct_attempts"]
    overall = round(correct / max(1, total) * 100, 1)

    console.print(Rule("[bold cyan]📊 Performance Analytics[/bold cyan]"))
    console.print(f"\n  Total Attempts: [bold]{total}[/bold]  |  Overall Accuracy: [bold]{overall}%[/bold]\n")

    table = Table(box=box.MINIMAL, header_style="bold blue")
    table.add_column("Topic", min_width=36)
    table.add_column("Attempts", justify="right")
    table.add_column("Correct", justify="right")
    table.add_column("Accuracy", justify="right")
    table.add_column("", justify="center", width=3)

    for ts in stats["topic_stats"]:
        acc = round(ts["correct"] / max(1, ts["attempts"]) * 100, 1)
        col = "green" if acc >= 80 else "yellow" if acc >= 50 else "red"
        table.add_row(ts["topic"], str(ts["attempts"]), str(ts["correct"]),
                      f"[{col}]{acc}%[/]",
                      "✅" if acc >= 80 else "⚠️" if acc >= 50 else "❌")

    print_paginated(table, title="Performance Analytics")
    try:
        ans = Prompt.ask("\n  [bold blue]❯[/bold blue] [dim]Press Enter to return, or type a question to chat[/dim]")
        if ans.strip() and ans.strip().lower() not in EXIT_COMMANDS:
            run_free_chat_session(ans.strip())
    except (KeyboardInterrupt, EOFError):
        raise SystemExit


def show_study_journal():
    clear()
    import os
    from rich.markdown import Markdown
    
    brain_file = memory_manager.BRAIN_FILE
    if not os.path.exists(brain_file):
        console.print("[yellow]  No study journal found yet. Start studying to populate your log![/yellow]")
        time.sleep(2)
        return
        
    try:
        with open(brain_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        console.print(f"[red]  Error reading study journal: {e}[/red]")
        time.sleep(2)
        return
        
    md = Markdown(content, code_theme="monokai")
    print_paginated(md, title="📖 Your Study Journal (MongoDB Brain)")
    
    try:
        Prompt.ask("\n  [dim]Press Enter to return to menu[/dim]")
    except (KeyboardInterrupt, EOFError):
        raise SystemExit


def show_exam_traps():
    clear()
    from rich.console import Group
    from rich.text import Text
    
    profile = database.get_user_profile(USER_ID)
    completed = profile.get("progress", {}).get("completed_topics", [])
    
    # Proactively merge status mastery as a fallback/robustness helper
    status = planner.get_syllabus_status(USER_ID)
    for ts in status.get("status_list", []):
        if ts.get("is_mastered") and ts.get("topic") not in completed:
            completed.append(ts.get("topic"))
            
    traps_map = {
        "MongoDB Overview & The Document Model": "• [bold cyan]Topic 1: Overview & Document Model[/bold cyan]\n  - BSON maximum document size is strictly [bold red]16MB[/bold red]. Use GridFS for larger files.\n  - Key names are case-sensitive and have strict null/dot character restrictions.",
        "CRUD Operations - Create": "• [bold cyan]Topic 2: CRUD - Create[/bold cyan]\n  - `insertOne()` returns an object containing `acknowledged: true` and `insertedId`. It does NOT return the document itself.\n  - If you omit `_id`, the driver automatically assigns a 12-byte `ObjectId`.",
        "CRUD Operations - Read": "• [bold cyan]Topic 3: CRUD - Read[/bold cyan]\n  - Projections: You cannot mix inclusion (1) and exclusion (0) in a single projection, except for the `_id` field (e.g. `{name: 1, _id: 0}` is valid, but `{name: 1, age: 0}` is INVALID).\n  - Chained cursor methods (`.sort()`, `.limit()`, `.skip()`) are executed in a fixed priority order (Sort -> Skip -> Limit) regardless of code order.",
        "CRUD Operations - Update": "• [bold cyan]Topic 4: CRUD - Update[/bold cyan]\n  - `updateOne()` requires atomic operators (like `$set` or `$push`). Using replacements without operators requires `replaceOne()`.",
        "CRUD Operations - Delete": "• [bold cyan]Topic 5: CRUD - Delete[/bold cyan]\n  - `deleteOne()` only deletes the [bold yellow]first[/bold yellow] matching document. Use `deleteMany()` for bulk deletes.",
        "Query Operators & MQL": "• [bold cyan]Topic 6: Query Operators & MQL[/bold cyan]\n  - Implicit Array Matching: Querying `{tags: 'database'}` matches any document where the array `tags` contains `'database'`. You do not need to wrap it in array brackets.\n  - Comparison operators evaluate types based on standard BSON Type Bracketing collation order.",
        "Querying Arrays & Embedded Documents": "• [bold cyan]Topic 7: Querying Arrays & Embedded Docs[/bold cyan]\n  - `$elemMatch` matches documents where at least one array element satisfies [bold yellow]all[/bold yellow] specified query conditions. Without `$elemMatch`, conditions can match separate elements.\n  - Nested dot-notation paths (e.g., `'address.city'`) MUST be enclosed in quotes.",
        "Aggregation Framework": "• [bold cyan]Topic 8: Aggregation Framework[/bold cyan]\n  - Always place `$match` as early as possible in your pipeline to take advantage of indexes and optimize memory usage.",
        "Indexes & Performance": "• [bold cyan]Topic 9: Indexes & Performance[/bold cyan]\n  - Compound Indexes: An index on `{a: 1, b: 1, c: 1}` supports queries on `{a}`, `{a, b}`, and `{a, b, c}`, but cannot support queries on `{b}` or `{c}` alone (Prefix rule).\n  - Covered Queries: All query fields and projected fields must be index keys, and the `_id` field must be explicitly excluded (`_id: 0`).",
        "Data Modeling": "• [bold cyan]Topic 10: Data Modeling[/bold cyan]\n  - Embedding is preferred for low cardinality (1-to-few). Referencing is preferred for high cardinality (1-to-many) to prevent breaching the 16MB document size ceiling.",
        "MongoDB Drivers & PyMongo": "• [bold cyan]Topic 11: Drivers & PyMongo[/bold cyan]\n  - Method Casings: PyMongo uses `snake_case` (e.g. `insert_one()`, `find_one()`), while mongosh uses `camelCase` (e.g. `insertOne()`, `findOne()`).",
        "MongoDB Atlas & Operations": "• [bold cyan]Topic 12: MongoDB Atlas & Operations[/bold cyan]\n  - Free Tier: M0 tier clusters are limited to 512MB storage and do not support VPC Peering or advanced backup routines."
    }
    
    active_traps = []
    for topic_name, trap_text in traps_map.items():
        if topic_name in completed:
            active_traps.append(trap_text)
            
    header = "💡 [bold yellow]CRITICAL EXAM TRAPS & REMINDERS[/bold yellow]"
    divider = "━"*50
    
    renderables = [Text.from_markup(header), Text.from_markup(divider)]
    
    if not active_traps:
        renderables.append(Text.from_markup(
            "\n  [yellow]You haven't mastered any syllabus topics yet![/yellow]\n"
            "  As you master topics through practice and daily agendas, their critical syntactic traps\n"
            "  will unlock and populate this cheat sheet. Keep grinding! 💪\n"
        ))
    else:
        renderables.append(Text.from_markup(
            f"  [dim]Unlocked {len(active_traps)} of {len(traps_map)} syllabus cheat sheet modules based on your topic mastery.[/dim]\n"
        ))
        for t in active_traps:
            renderables.append(Text.from_markup(t))
            
    group = Group(*renderables)
    print_paginated(group, title="💡 Exam Cheat Sheet: Traps & Recall")
    
    try:
        Prompt.ask("\n  [dim]Press Enter to return to menu[/dim]")
    except (KeyboardInterrupt, EOFError):
        raise SystemExit


def recalibrate_study_plan():
    clear()
    console.print(Rule("[bold cyan]🔄 Recalibrate Study Plan[/bold cyan]"))
    console.print()
    console.print(Panel(
        "This option allows you to update your exam date, experience level,\n"
        "and regenerate your customized daily study calendar based on your current progress.",
        title="[bold yellow]Pacing Recalibration[/bold yellow]",
        border_style="yellow", box=box.ROUNDED
    ))
    console.print()
    
    # Ask for days remaining
    while True:
        days_str = ask("[bold]How many days from today is your updated MongoDB exam date?[/bold] (e.g. 30)")
        if days_str == "__back__":
            return
        try:
            days = int(days_str)
            if days < 1:
                raise ValueError
            break
        except ValueError:
            console.print("[red]Please enter a valid number greater than 0.[/red]")
            
    # Ask experience level
    console.print()
    exp_in = ask("[bold]What is your updated experience level?[/bold] (1=Beginner, 2=Intermediate, 3=Advanced)", choices=["1", "2", "3"])
    exp_map = {"1": "Beginner", "2": "Intermediate", "3": "Advanced"}
    if exp_in == "__back__":
        return
    experience_level = exp_map.get(exp_in, "Beginner")
    
    # Retrieve current mastered topics so they aren't lost
    profile = database.get_user_profile(USER_ID)
    completed_topics = profile.get("progress", {}).get("completed_topics", [])
    
    # Offer option to clear mastered topics to start completely fresh
    console.print()
    if Confirm.ask("[bold]Would you like to reset all topic mastery progress and start completely fresh?[/bold]"):
        completed_topics = []
        database.update_user_profile(USER_ID, {"progress": {"completed_topics": [], "current_agenda": []}})
        
    # Generate new study plan
    console.print()
    console.print("[dim]Regenerating and balancing your new study plan...[/dim]")
    exam_date = datetime.datetime.utcnow() + datetime.timedelta(days=days)
    calendar = planner.generate_study_calendar(days, experience_level, completed_topics)
    
    database.update_user_profile(USER_ID, {
        "exam_date": exam_date.isoformat(),
        "experience_level": experience_level,
        "study_calendar": calendar
    })
    
    console.print("\n[bold green]✅ Study plan successfully updated and recalibrated![/bold green]")
    time.sleep(2)


# ---------------------------------------------------------------------------
# MAIN MENU Helpers & Submenus
# ---------------------------------------------------------------------------

def run_full_mock():
    pep = coach.get_mock_exam_pep_talk()
    console.print(Panel(Markdown(pep, code_theme="monokai"), title="🧑‍🏫 CertCoach", border_style="cyan", box=box.ROUNDED))
    try:
        Prompt.ask("\n  Press Enter when ready...")
    except (KeyboardInterrupt, EOFError):
        return
    all_keys = []
    for item in planner.load_syllabus():
        all_keys.extend(item.get("bank_topic_keys", []))
    run_practice_questions("Full Mock", list(set(all_keys)), num=60, is_mock=True)

def run_timed_mock():
    pep = coach.get_mock_exam_pep_talk()
    console.print(Panel(Markdown(pep, code_theme="monokai"), title="🧑‍🏫 CertCoach", border_style="cyan", box=box.ROUNDED))
    try:
        Prompt.ask("\n  Press Enter when ready...")
    except (KeyboardInterrupt, EOFError):
        return
    all_keys = []
    for item in planner.load_syllabus():
        all_keys.extend(item.get("bank_topic_keys", []))
    start_time = time.time()
    score = run_practice_questions("Timed Mock Exam", list(set(all_keys)), num=20, is_mock=True)
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    console.print(f"\n  [bold cyan]⏱️ Time Taken: {minutes}m {seconds}s[/bold cyan]")
    console.print(f"  [dim]Target: ~28m (1.4m per question)[/dim]")
    try:
        Prompt.ask("\n  [dim]Press Enter to return[/dim]")
    except (KeyboardInterrupt, EOFError):
        return

def run_library_submenu():
    while True:
        console.print("\n  [bold blue]📖 Reference Library & Progress[/bold blue]")
        console.print("  [dim]  " + "─"*30 + "[/dim]")
        console.print("    [bold cyan]a.[/bold cyan] 📖 View Study Journal (MongoDB Brain)")
        console.print("    [bold cyan]b.[/bold cyan] 💡 View Exam Cheat Sheet (Traps & Reminders)")
        console.print("    [bold cyan]c.[/bold cyan] 📚 Syllabus Coverage & Gap Report")
        console.print("    [bold cyan]d.[/bold cyan] 📊 Performance Analytics Dashboard")
        console.print("    [bold cyan]e.[/bold cyan] ⬅️  Back to Main Menu")
        console.print()
        
        try:
            ans = Prompt.ask("  [bold blue]Library ❯[/bold blue]").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break
            
        if ans == "a":
            show_study_journal()
        elif ans == "b":
            show_exam_traps()
        elif ans == "c":
            show_syllabus_status()
        elif ans == "d":
            show_analytics()
        elif ans in ("e", "back", "b", "q"):
            break

def run_settings_submenu(profile, status):
    while True:
        console.print("\n  [bold blue]🛠️ Study Settings & Extras[/bold blue]")
        console.print("  [dim]  " + "─"*30 + "[/dim]")
        console.print("    [bold cyan]a.[/bold cyan] 🗓️  View Full Study Plan Table")
        console.print("    [bold cyan]b.[/bold cyan] 🔄 Update Study Plan & Recalibrate Pacing")
        
        # Gated Mock
        if status["mock_exam_unlocked"]:
            console.print("    [bold cyan]c.[/bold cyan] 🏆 Full Mock Exam (60 Questions)")
            console.print("    [bold cyan]d.[/bold cyan] ⏱️  Timed Mock Exam (20 Questions)")
        else:
            console.print("    [dim]c. 🔒 Full Mock Exam (Locked — need 70% mastery)[/dim]")
            console.print("    [dim]d. 🔒 Timed Mock Exam (Locked — need 70% mastery)[/dim]")
            
        console.print("    [bold cyan]e.[/bold cyan] 💻 Scenario Simulator (Apply Mode)")
        console.print("    [bold cyan]f.[/bold cyan] ❌ Quit CertCoach")
        console.print("    [bold cyan]g.[/bold cyan] ⬅️  Back to Main Menu")
        console.print()
        
        try:
            ans = Prompt.ask("  [bold blue]Settings ❯[/bold blue]").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break
            
        if ans == "a":
            if profile.get("study_calendar"):
                show_plan_preview(profile["study_calendar"], planner.calculate_days_left(profile.get("exam_date")))
                try:
                    Prompt.ask("\n  [dim]Press Enter to return[/dim]")
                except (KeyboardInterrupt, EOFError):
                    break
        elif ans == "b":
            recalibrate_study_plan()
        elif ans == "c":
            if status["mock_exam_unlocked"]:
                run_full_mock()
            else:
                console.print("[red]  Locked! Complete 70% of the syllabus first.[/red]")
        elif ans == "d":
            if status["mock_exam_unlocked"]:
                run_timed_mock()
            else:
                console.print("[red]  Locked! Complete 70% of the syllabus first.[/red]")
        elif ans == "e":
            run_scenario_simulator()
        elif ans in ("f", "q", "quit"):
            raise SystemExit
        elif ans in ("g", "back", "b"):
            break


# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------

def main_menu():
    database.check_connection()
    run_onboarding()

    database.update_streak(USER_ID)

    while True:
        profile = database.get_user_profile(USER_ID)
        days_left = planner.calculate_days_left(profile.get("exam_date"))
        status = planner.get_syllabus_status(USER_ID)
        agenda = planner.generate_daily_agenda(USER_ID)
        streak = profile.get("streak_days", 1)

        agenda_desc = "None"
        if agenda:
            first_item = agenda[0]
            agenda_desc = f"{first_item['topic']} ({first_item['desc']})"
            
        due_reviews = planner.get_due_review_topics(USER_ID)
        badge = " [bold red](🚨 Spaced-Repetition Quiz Due!)[/bold red]" if due_reviews else ""
        
        skipped_topics = status.get("skipped_unmapped_topics", [])
        skipped_badge = ""
        if skipped_topics:
            skipped_badge = f" [bold yellow](⚠️ {len(skipped_topics)} topics skipped due to missing docs)[/bold yellow]"
            
        lock_str = (
            "[bold green]🔓 Unlocked[/bold green]"
            if status["mock_exam_unlocked"]
            else (
                f"[yellow]🔒 Locked — need {status['unlock_threshold_percent']}% mastery[/yellow]"
            )
        )
        
        # Sleek horizontally consolidated Status Bar
        console.print(f"\n[bold blue]🧑‍🏫 CertCoach[/bold blue] | 📅 [bold]{days_left} days left[/bold] | 🔥 Streak: [bold yellow]{streak} days[/bold yellow] | 🏅 Mastery: [bold green]{status['mastery_percent']}%[/bold green] | Mock: {lock_str}")
        console.print("━"*80)
        console.print(f"  [bold cyan]1.[/bold cyan] 🚀 Start Today's Study Agenda: [bold]{agenda_desc}[/bold]{badge}{skipped_badge}")
        console.print(f"  [bold cyan]2.[/bold cyan] 📖 Reference Library (Journal, Cheat Sheet, Syllabus, Analytics)")
        console.print(f"  [bold cyan]3.[/bold cyan] 🛠️ Study Settings & Extras (Mock Exams, Pacing, Recalibrate, Quit)")
        console.print()
        console.print("[dim]Type 1-3 to navigate, or start typing to chat directly with your Coach![/dim]")
        
        try:
            choice_raw = Prompt.ask("\n[bold blue]Coach ❯[/bold blue]").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not choice_raw:
            continue

        if choice_raw.lower() in EXIT_COMMANDS:
            break

        if choice_raw == "1":
            # Show skipped topics notice if any
            if skipped_topics:
                console.print()
                alert_lines = [
                    "[bold yellow]⚠️  The following syllabus topics were bypassed because their official reference documentation does not exist:[/bold yellow]\n"
                ]
                for item in skipped_topics:
                    alert_lines.append(f"  • [cyan]Topic #{item['id']}[/cyan] ({item['topic']})")
                alert_lines.append(
                    "\n[bold]Action Required:[/bold] Please provide which topics to include in the docs (add their respective markdown files under [bold cyan]data/raw_markdowns/[/bold cyan]) so that CertCoach can help in learning those topics."
                )
                console.print(Panel(
                    "\n".join(alert_lines),
                    title="[bold yellow]📂 Bypassed Topics Notice[/bold yellow]",
                    border_style="yellow", box=box.ROUNDED
                ))
                console.print()
                
            # 1. Run due reviews first if any
            if due_reviews:
                console.print(Rule("[bold yellow]🚨 Pop Quiz Time! 🚨[/bold yellow]"))
                console.print(Panel(
                    "It's time for a quick Spaced-Repetition review of past topics before we start the daily agenda.",
                    border_style="yellow", box=box.ROUNDED
                ))
                if Confirm.ask("  Start 5-question Pop Quiz now?"):
                    run_practice_questions("Spaced Repetition", due_reviews, num=5, is_mock=True)
                    console.print("\n  [bold green]Great job! Let's get to today's agenda.[/bold green]")
                    time.sleep(2)
            
            # 2. Run the main daily agenda items
            if agenda:
                for item in agenda:
                    if item.get("type") in ("Review", "Learn"):
                        cont = run_teach_session(item)
                        if not cont:
                            break
                    elif item.get("type") == "BossFight":
                        console.print(Panel(item["desc"], title="👾 Boss Fight!", border_style="red"))
                        try:
                            Prompt.ask("\n  Press Enter when ready to start the boss fight...")
                        except (KeyboardInterrupt, EOFError):
                            break
                        all_keys = []
                        for s_item in planner.load_syllabus():
                            all_keys.extend(s_item.get("bank_topic_keys", []))
                        score = run_practice_questions(item["topic"], list(set(all_keys)), num=10, is_mock=True)
                        if score is not None and score >= 7:
                            planner.mark_boss_complete(USER_ID, item["boss_level"])
                            console.print(f"\n  [bold green]🏆 Boss Defeated! You may now proceed to the next topics.[/bold green]")
                        else:
                            console.print(f"\n  [bold red]❌ Boss Defeated You! You need 7/10 to pass. Try again tomorrow.[/bold red]")
                        try:
                            ans = Prompt.ask("\n  [bold blue]❯[/bold blue] [dim]Press Enter to return[/dim]")
                        except (KeyboardInterrupt, EOFError):
                            break
            else:
                console.print("[green]  You have completed all agenda items for today! Great job.[/green]")
                
        elif choice_raw == "2":
            run_library_submenu()
            
        elif choice_raw == "3":
            try:
                run_settings_submenu(profile, status)
            except SystemExit:
                break
                
        else: # Hybrid intercept (Direct Q&A chat)
            run_free_chat_session(choice_raw)

    exit_message()


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main_menu()
    except SystemExit:
        exit_message()
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]")
        exit_message()
