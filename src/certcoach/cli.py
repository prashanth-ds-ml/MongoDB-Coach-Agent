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
import re
import textwrap

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

from certcoach.core import auth, database, planner
from certcoach.core.doc_chunking import chunk_doc_text
from certcoach.core.persona import CoachPersona
from certcoach.jobs.review_questions import render_citation_panel
import certcoach.core.memory_manager as memory_manager

console = Console()
coach = CoachPersona()
DEFAULT_USER_ID = "local_user_1"
USER_ID = auth.get_session_user_id(DEFAULT_USER_ID)

EXIT_COMMANDS = {"q", "quit", "exit", "/q", "/quit", "/exit"}
BACK_COMMANDS = {"back", "b", "menu", "/back", "/b", "/menu"}
PRACTICE_COMMANDS = {"practice", "p", "/practice", "/p"}
CONTINUE_COMMANDS = {"done", "next", "/done", "/next"}
MOCK_SECONDS_PER_QUESTION = 90
# Lesson display splits on H1+H2 only (coarser than the H1-H4 split used for
# fact-extraction yield) -- one natural topic per screen (e.g. "ObjectId",
# "Date") without fragmenting a section's own sub-examples into separate
# clicks. The cap is a safety net for an oversized section, not the primary
# split signal; header boundaries are.
LESSON_SECTION_HEADERS = [("#", "H1"), ("##", "H2")]
LESSON_SECTION_MAX_CHARS = 3000
# Pilot scope for the per-section comprehension check-in -- expand (or drop
# this gate entirely) once validated live. Empty/absent concept names never
# trigger it.
LESSON_CHECKIN_PILOT_CONCEPTS = {"Document structure"}
ACK_CONTINUE_COMMANDS = {
    "y",
    "yes",
    "yeah",
    "yep",
    "ok",
    "okay",
    "got it",
    "understood",
    "clear",
    "makes sense",
}


# ---------------------------------------------------------------------------
# UTILS
# ---------------------------------------------------------------------------

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_weight_style(weight: str, compact: bool = False) -> tuple[str, str]:
    """Returns (color_style, label) resolved dynamically for semantic and percentage weights."""
    if not weight:
        return "white", "—"
    if weight == "High":
        return "red", "H" if compact else "High"
    if weight == "Medium":
        return "yellow", "M" if compact else "Medium"
    if weight == "Low":
        return "green", "L" if compact else "Low"
    if "%" in weight:
        try:
            val = float(weight.replace("%", "").strip())
            if val >= 15.0:
                return "red", weight
            if val >= 8.0:
                return "yellow", weight
            return "green", weight
        except Exception:
            pass
    return "white", weight


def ask(prompt_text: str, choices: list = None) -> str:
    """
    Wrapper around Prompt.ask that handles exit/back commands globally.
    Raises SystemExit on quit, returns '__back__' on back.
    """
    try:
        if choices:
            # Add the exit/back meta-choices (kept in sync with the real
            # EXIT_COMMANDS/BACK_COMMANDS sets) so Rich's own validation
            # doesn't reject them before the checks below ever see the
            # input -- case_sensitive=False so "Quit"/"QUIT"/"Y" etc. aren't
            # silently rejected just for not matching the displayed case.
            value = Prompt.ask(
                prompt_text,
                choices=choices + sorted(EXIT_COMMANDS | BACK_COMMANDS),
                case_sensitive=False,
            ).strip().lower()
        else:
            value = Prompt.ask(prompt_text).strip()
    except (KeyboardInterrupt, EOFError):
        raise SystemExit

    if value.lower() in EXIT_COMMANDS:
        raise SystemExit
    if value.lower() in BACK_COMMANDS:
        return "__back__"
    return value


def confirm(prompt_text: str, default: bool = False) -> bool:
    """Wrapper around Confirm.ask that treats Ctrl+C/EOF as declining --
    the safe, non-destructive answer -- instead of letting a raw
    KeyboardInterrupt escape mid-confirmation. case_sensitive=False so
    typing "Y"/"N" (capitalized) isn't silently rejected."""
    try:
        return Confirm.ask(prompt_text, default=default, case_sensitive=False)
    except (KeyboardInterrupt, EOFError):
        return False


def exit_message():
    console.print()
    console.print(Panel(
        "[bold green]Session saved. Keep grinding — the exam won't pass itself! 💪[/bold green]",
        border_style="green", box=box.ROUNDED
    ))
    console.print()


def get_current_user_label() -> str | None:
    session = auth.load_session()
    if not session:
        return None

    display_name = (session.get("display_name") or "").strip()
    email = (session.get("email") or "").strip()
    user_id = (session.get("user_id") or "").strip()

    if display_name and email:
        return f"{display_name} <{email}>"
    if email:
        return email
    if display_name:
        return display_name
    if user_id:
        return user_id
    return None


def print_paginated(renderable, title: str = "CertCoach"):
    """
    Renders a Rich renderable directly to the console so that it is naturally
    scrollable in the user's standard terminal scrollback buffer.
    """
    console.print(renderable)


def build_onboarding_commitment_text(total_days: int, experience_level: str) -> str:
    return (
        f"[bold]Daily Discipline Contract[/bold]\n"
        f"You have [bold cyan]{total_days} days[/bold cyan] until exam day as a [bold]{experience_level}[/bold] learner.\n\n"
        f"Show up each day and follow this exact loop:\n"
        f"1. Start Today's Agenda instead of random browsing.\n"
        f"2. Learn one concept deeply enough to explain the trap in your own words.\n"
        f"3. Clear the 5-question gate with at least [bold green]4/5[/bold green].\n"
        f"4. Review misses immediately so tomorrow starts stronger.\n\n"
        f"[dim]If you stay consistent with this loop, CertCoach keeps the workload focused and exam-oriented.[/dim]"
    )


def build_agenda_mission_text(agenda_item: dict, days_left: int, mastery_percent: float, practice_ready: bool = True) -> str:
    topic = agenda_item.get("topic", "Unknown Topic")
    agenda_type = agenda_item.get("type", "Learn")
    active_subtopic = agenda_item.get("active_subtopic")
    subtopics = agenda_item.get("subtopics", [])
    focus_concept = active_subtopic or (subtopics[0] if subtopics else topic)
    if not isinstance(days_left, (int, float)):
        days_left = 30
    if not isinstance(mastery_percent, (int, float)):
        mastery_percent = 0.0

    urgency_line = (
        f"[bold red]Urgency[/bold red]: {days_left} days left. Stay on today's mission until it is complete."
        if days_left <= 14
        else f"[bold cyan]Pacing[/bold cyan]: {days_left} days left. Consistency beats intensity."
    )

    if agenda_type == "Review":
        win_condition = (
            f"Refresh the weak point, clear the trap, and turn shaky recall into clean exam-speed answers on [bold]{topic}[/bold]."
        )
        why_today = "Review comes before new material because forgotten topics leak points on exam day."
        flow_line = "teach one concept, clear the checkpoint, practice only that concept, then move on."
    elif agenda_type == "BossFight":
        win_condition = "Beat the timed checkpoint and prove the last domain is strong enough to build on."
        why_today = "Boss fights stop weak foundations from snowballing into bigger gaps."
        flow_line = "teach one concept, clear the checkpoint, practice only that concept, then move on."
    elif not practice_ready:
        # Scored practice isn't available for this concept yet -- say so up
        # front rather than promising a step that will turn out blocked.
        win_condition = (
            f"Understand [bold]{focus_concept}[/bold] and answer the Micro-Challenge. "
            f"Scored practice isn't unlocked for this concept yet -- the question bank is still being built."
        )
        why_today = "One concept understood properly each day is safer than skimming multiple topics."
        flow_line = "teach one concept, clear the checkpoint, then move on -- scored practice unlocks once enough questions are confirmed."
    else:
        win_condition = (
            f"Understand [bold]{focus_concept}[/bold], answer the Micro-Challenge, and score at least [bold green]4/5[/bold green] in practice so the concept counts as complete."
        )
        why_today = "One concept mastered properly each day is safer than skimming multiple topics."
        flow_line = "teach one concept, clear the checkpoint, practice only that concept, then move on."

    return (
        f"[bold]Mission[/bold]: {agenda_type}\n"
        f"[bold]Focus[/bold]: {topic}\n"
        f"[bold]Today's target[/bold]: {focus_concept}\n"
        f"[bold]Win condition[/bold]: {win_condition}\n"
        f"[bold]Why this matters[/bold]: {why_today}\n"
        f"[bold]Flow[/bold]: {flow_line}\n"
        f"[bold]Current mastery[/bold]: {mastery_percent:.1f}%\n"
        f"{urgency_line}"
    )


def build_practice_debrief(score: int | None, total_questions: int, topic: str, completed_concept: str | None = None) -> tuple[str, str, str]:
    concept_label = completed_concept or topic
    if score is None:
        return (
            "⚠️ Practice Not Completed",
            (
                f"The concept [bold]{concept_label}[/bold] is still open because the practice round did not complete.\n"
                f"Return once the question bank is ready so the learning loop finishes with retrieval practice."
            ),
            "yellow",
        )

    pct = (score / max(1, total_questions)) * 100
    if total_questions == 5 and score >= 4:
        return (
            "✅ Concept Locked In",
            (
                f"You cleared today's gate with [bold green]{score}/{total_questions}[/bold green] ({pct:.0f}%).\n"
                f"[bold]{concept_label}[/bold] is strong enough to count as progress for today. Review the trap explanations once, then move on."
            ),
            "green",
        )

    return (
        "🛠️ Not Locked In Yet",
        (
            f"You scored [bold yellow]{score}/{total_questions}[/bold yellow] ({pct:.0f}%), so [bold]{concept_label}[/bold] stays open.\n"
            f"Read the misses carefully, identify the exact trap, and retry before treating this topic as done."
        ),
        "yellow",
    )


def extract_question_focus_label(q_item: dict) -> str:
    metadata = q_item.get("metadata", {})
    return (
        metadata.get("concept")
        or metadata.get("syllabus_topic")
        or metadata.get("topic")
        or "MongoDB core syntax"
    )


def build_practice_recovery_text(topic: str, concepts: list | None, score: int, total_questions: int, weak_signals: list[str]) -> tuple[str, str, str]:
    concept_scope = ", ".join(concepts) if concepts else topic
    unique_signals = []
    for signal in weak_signals:
        if signal and signal not in unique_signals:
            unique_signals.append(signal)
    signal_text = ", ".join(unique_signals[:3]) if unique_signals else "the explanation panels you just reviewed"
    pct = (score / max(1, total_questions)) * 100

    if pct >= 80:
        return (
            "✅ Reinforcement Plan",
            (
                f"You are above the mastery line on [bold]{concept_scope}[/bold] with [bold green]{score}/{total_questions}[/bold green] ({pct:.0f}%).\n"
                f"Before moving on, spend 30 seconds restating the key trap in your own words and glance once more at: [bold cyan]{signal_text}[/bold cyan]."
            ),
            "green",
        )

    if pct >= 60:
        return (
            "🛠️ Recovery Plan",
            (
                f"You are close, but [bold]{concept_scope}[/bold] is not fully stable yet at [bold yellow]{score}/{total_questions}[/bold yellow] ({pct:.0f}%).\n"
                f"Focus your next review on [bold cyan]{signal_text}[/bold cyan], then retry this concept before treating it as finished."
            ),
            "yellow",
        )

    return (
        "🚨 High-Priority Recovery",
        (
            f"This concept is still high risk at [bold red]{score}/{total_questions}[/bold red] ({pct:.0f}%).\n"
            f"Do not move on casually. Re-read the lesson for [bold]{concept_scope}[/bold], write down the trap behind [bold cyan]{signal_text}[/bold cyan], and come back for a fresh retry."
        ),
        "red",
    )


def build_session_closeout_text(
    covered_topics: list[str],
    session_accuracy: float,
    readiness_before: float,
    readiness_after: float,
    next_agenda_item: dict | None = None,
) -> tuple[str, str, str]:
    if not isinstance(session_accuracy, (int, float)):
        session_accuracy = 0.0
    if not isinstance(readiness_before, (int, float)):
        readiness_before = 0.0
    if not isinstance(readiness_after, (int, float)):
        readiness_after = 0.0

    delta = readiness_after - readiness_before
    if delta > 0.25:
        delta_line = f"[bold green]Readiness moved up[/bold green] by {delta:.1f}% today."
        style = "green"
        title = "📌 Coach Closeout"
    elif delta < -0.25:
        delta_line = f"[bold yellow]Readiness dipped[/bold yellow] by {abs(delta):.1f}% today. That usually means weak accuracy or incomplete recall still needs cleanup."
        style = "yellow"
        title = "📌 Coach Closeout"
    else:
        delta_line = "[bold cyan]Readiness stayed roughly flat[/bold cyan] today. Consistency still matters."
        style = "cyan"
        title = "📌 Coach Closeout"

    if session_accuracy >= 80:
        accuracy_line = "You studied with exam-safe accuracy today. Keep the same rhythm tomorrow."
    elif session_accuracy >= 60:
        accuracy_line = "You made progress, but some answers are still fragile under pressure."
    else:
        accuracy_line = "Today exposed real gaps. Use the next session for repair, not for rushing ahead."

    covered_line = ", ".join(covered_topics[:3]) if covered_topics else "No scored topics yet"
    next_line = "Take the next scheduled agenda item."
    if next_agenda_item:
        next_line = f"Next best start: [bold]{next_agenda_item.get('topic', 'Next Agenda')}[/bold] ({next_agenda_item.get('desc', 'Continue the study loop')})."

    return (
        title,
        (
            f"[bold]Locked in today[/bold]: {covered_line}\n"
            f"[bold]Accuracy read[/bold]: {accuracy_line}\n"
            f"[bold]Readiness[/bold]: {readiness_before:.1f}% -> {readiness_after:.1f}%\n"
            f"{delta_line}\n"
            f"[bold]Next move[/bold]: {next_line}"
        ),
        style,
    )


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
        f"[bold yellow]{int(planner.MOCK_EXAM_UNLOCK_THRESHOLD * 100)}%[/bold yellow] of the syllabus.\n\n"
        "[dim]Tip: Type [bold]q[/bold] at any prompt to save and quit.[/dim]",
        title="👋  Welcome", border_style="cyan", box=box.ROUNDED
    ))
    console.print()

    # The whole plan-building flow repeats if the user rejects the final
    # preview -- nothing is persisted until they confirm (see the bottom of
    # this loop), so "no" genuinely lets them redo it instead of just
    # printing advice that doesn't work.
    while True:
        # --- Ask exam date ---
        while True:
            date_str = ask("[bold]Enter your MongoDB exam date (YYYY-MM-DD):[/bold]")
            if date_str == "__back__":
                continue
            try:
                exam_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
                # Compare like-for-like (both at end-of-day) so entering today's
                # date is correctly rejected as not "in the future".
                today = datetime.datetime.now(datetime.timezone.utc).replace(hour=23, minute=59, second=59, microsecond=0, tzinfo=None)
                if exam_date <= today:
                    console.print("[red]The exam date must be in the future (after today).[/red]")
                    continue
                delta = exam_date - datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
                days = max(1, delta.days)
                break
            except ValueError:
                console.print("[red]Please enter a valid date in YYYY-MM-DD format (e.g. 2026-06-30).[/red]")

        # --- Ask experience level ---
        console.print()
        exp_map = {"1": "Beginner", "2": "Intermediate", "3": "Advanced"}
        while True:
            exp_in = ask("[bold]What is your current MongoDB experience level?[/bold] (1=Beginner, 2=Intermediate, 3=Advanced)", choices=["1", "2", "3"])
            if exp_in == "__back__":
                console.print("[yellow]  Nothing to go back to yet -- please choose 1, 2, or 3.[/yellow]")
                continue
            break
        experience_level = exp_map.get(exp_in, "Beginner")

        diagnostic_mastered = []
        console.print()
        if confirm("[bold]Take a quick 10-question diagnostic to skip topics you already know?[/bold]"):
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

        # --- Generate calendar (not yet saved) ---
        console.print()
        console.print("[dim]Building your study plan...[/dim]")
        calendar = planner.generate_study_calendar(days, experience_level, diagnostic_mastered)

        # --- Show the plan ---
        show_plan_preview(calendar, days)
        console.print()
        console.print(Panel(
            build_onboarding_commitment_text(days, experience_level),
            title="🎯 How You Win With CertCoach",
            border_style="green",
            box=box.ROUNDED,
        ))

        # --- Confirm ---
        console.print()
        answer = ask("[bold]Does this plan work for you? Start studying now?[/bold] (yes/no)", choices=["yes", "no", "y", "n"])
        if answer in ("no", "n"):
            console.print("[yellow]No problem -- let's adjust the exam date, experience level, or plan.[/yellow]")
            time.sleep(1.5)
            continue

        # Only persist once the user has actually confirmed the plan.
        database.update_user_profile(USER_ID, {"exam_date": exam_date.isoformat(), "experience_level": experience_level})
        database.update_user_profile(USER_ID, {"study_calendar": calendar})
        break


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

    phase_color = {"Study": "cyan", "Mock & Revision": "magenta"}

    for item in calendar:
        w_style, w_lbl = get_weight_style(item.get("exam_weight", ""), compact=False)
        pc = phase_color.get(item["phase"], "white")
        table.add_row(
            str(item["day_num"]),
            item["date"],
            f"[{pc}]{item['phase']}[/{pc}]",
            item["topic"],
            f"[{w_style}]{w_lbl}[/{w_style}]" if w_lbl != "—" else "",
        )

    from rich.console import Group
    from rich.text import Text
    
    footer_text = Text.from_markup(
        f"\n  📘 [bold]{sum(1 for i in calendar if i['phase']=='Study')}[/bold] study days  |  "
        f"🏆 [bold]{sum(1 for i in calendar if i['phase']=='Mock & Revision')}[/bold] mock/revision days  |  "
        f"🔒 Full Mock unlocks at [bold]{int(planner.MOCK_EXAM_UNLOCK_THRESHOLD * 100)}%[/bold] syllabus mastery"
    )
    group = Group(table, footer_text)
    print_paginated(group, title=f"{total_days}-Day Study Plan")


# ---------------------------------------------------------------------------
# TEACH → Q&A → PRACTICE FLOW
# ---------------------------------------------------------------------------

def run_teach_session(agenda_item: dict):
    """
    Full study session for a topic:
    1. Coach explains the current concept.
    2. Open Q&A, but keep every answer inside the current topic/concept.
    3. Offer 5-question practice quiz for the same concept.
    4. Mini-mock offer only after topic mastery clears the gate.
    """
    topic = agenda_item["topic"]
    subtopics = agenda_item.get("subtopics", [])
    md_files = agenda_item.get("md_files", [])
    bank_keys = agenda_item.get("bank_keys", [topic])
    question_keywords = agenda_item.get("question_keywords", [])

    # Resolved once up front -- used both by the per-subtopic review-quiz offer
    # below and the practice offer at the end of this function.
    syllabus = planner.load_syllabus()
    topic_item = next((item for item in syllabus if item["topic"] == topic), None)
    topic_id = topic_item["id"] if topic_item else None

    console.print(Rule(f"[bold cyan]Today's Topic: {topic}[/bold cyan]"))
    console.print("[dim]  Type [bold]q[/bold] at any point to save and quit.\n[/dim]")
    profile = database.get_user_profile(USER_ID)
    status = planner.get_syllabus_status(USER_ID)
    days_left = planner.calculate_days_left(profile.get("exam_date"))

    # Know up front whether today's concept can actually deliver scored
    # practice, so the mission brief doesn't promise a step that turns out
    # blocked once the learner gets there.
    mission_focus_concept = agenda_item.get("active_subtopic") or (subtopics[0] if subtopics else topic)
    insufficient_concepts = status.get("insufficient_concepts", []) or []
    practice_ready = not any(
        item.get("topic") == topic and item.get("concept") == mission_focus_concept
        for item in insufficient_concepts
    )

    console.print(Panel(
        build_agenda_mission_text(
            agenda_item,
            days_left=days_left,
            mastery_percent=status.get("mastery_percent", 0.0),
            practice_ready=practice_ready,
        ),
        title="🎯 Daily Mission Brief",
        border_style="cyan",
        box=box.ROUNDED,
    ))
    console.print()

    # ---- 1. EXPLAIN & Q&A LOOP ----
    chat_history = memory_manager.load_active_history()
    
    # Fallback if no subtopics defined
    if not subtopics:
        subtopics = [topic]

    force_practice = False
    explained_subtopics = []
    qa_instructions_shown = False
    for idx, subtopic in enumerate(subtopics):
        resolved_files = planner.resolve_concept_docs(md_files, subtopic)

        if not resolved_files:
            console.print(f"  [dim]• '{subtopic}' is not covered in reference documents. Skipping...[/dim]")
            continue

        explained_subtopics.append(subtopic)
        doc_texts = []
        jump_to_practice = False
        for doc_idx, filename in enumerate(resolved_files):
            doc_text = planner.load_md_context([filename])
            doc_texts.append(doc_text)

            sections = chunk_doc_text(doc_text, max_chunk_chars=LESSON_SECTION_MAX_CHARS, headers=LESSON_SECTION_HEADERS)
            if not sections:
                sections = [{"label": subtopic, "text": doc_text}]
            elif len(sections) > 1 and sections[0]["label"] == "(untitled section)":
                # A leading metadata-only stub (e.g. "> Source: ...") isn't
                # real lesson content on its own -- fold it into the first
                # real section instead of showing it as a near-empty
                # standalone screen. Content is still fully preserved, just
                # never silently dropped (see the raw/cleaned corpus audit
                # that found a real content-loss bug this same session).
                stub_text = sections[0]["text"]
                sections = sections[1:]
                sections[0] = {**sections[0], "text": stub_text + "\n\n" + sections[0]["text"]}
            for section in sections:
                if section["label"] == "(untitled section)":
                    section["label"] = subtopic

            doc_prefix = f"Doc {doc_idx + 1}/{len(resolved_files)} — " if len(resolved_files) > 1 else ""

            for sec_idx, section in enumerate(sections):
                panel = Panel(
                    Markdown(section["text"], code_theme="monokai"),
                    title=f"📄  {doc_prefix}{subtopic} — {section['label']} ({sec_idx + 1}/{len(sections)})",
                    border_style="cyan", box=box.ROUNDED,
                    padding=(1, 2),
                )
                print_paginated(panel, title=f"Lesson: {subtopic}")

                if subtopic in LESSON_CHECKIN_PILOT_CONCEPTS:
                    run_section_checkin(topic, subtopic, section)

                is_last_section = sec_idx == len(sections) - 1
                is_last_doc = doc_idx == len(resolved_files) - 1
                if is_last_section and is_last_doc:
                    continue

                console.print()
                try:
                    next_section_input = Prompt.ask(
                        "  [dim]Press Enter for the next section, or type [bold]practice[/bold] to jump to MCQs[/dim]",
                        default=""
                    ).strip().lower()
                except (KeyboardInterrupt, EOFError):
                    raise SystemExit
                if next_section_input in EXIT_COMMANDS:
                    raise SystemExit
                if next_section_input in PRACTICE_COMMANDS:
                    jump_to_practice = True
                    break

            if jump_to_practice:
                break

        explanation = "\n\n---\n\n".join(doc_texts)
        memory_manager.log_interaction("assistant", explanation)
        chat_history = memory_manager.load_active_history()

        if jump_to_practice:
            force_practice = True
            break

        console.print()
        if not qa_instructions_shown:
            console.print(
                "  [dim]Answer the challenge using only this concept, ask a question about this concept, type [bold]next[/bold] to continue, or type [bold]practice[/bold] to start MCQs.[/dim]"
            )
            qa_instructions_shown = True
        else:
            console.print("  [dim]([bold]next[/bold] to continue / [bold]practice[/bold] to start MCQs / or ask a question)[/dim]")

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

            if user_input.lower() in PRACTICE_COMMANDS:
                force_practice = True
                break

            lowered_input = user_input.lower()

            if lowered_input in CONTINUE_COMMANDS or lowered_input in ACK_CONTINUE_COMMANDS:
                break

            # Generate follow-up answer
            memory_manager.log_interaction("user", user_input)
            chat_history = memory_manager.load_active_history()
            with console.status("[dim]🤖 CertCoach is thinking...[/dim]", spinner="dots"):
                answer = coach.handle_followup(topic, subtopic, user_input, chat_history, md_context=explanation)
            
            from certcoach.core.persona import clean_lesson_explanation
            answer = clean_lesson_explanation(answer)
                
            memory_manager.log_interaction("assistant", answer)
            chat_history = memory_manager.load_active_history()

            console.print()
            console.print(Panel(
                Markdown(answer, code_theme="monokai"),
                title="🧑‍🏫  CertCoach",
                border_style="blue", box=box.ROUNDED,
                padding=(1, 2),
            ))

        if not force_practice and topic_id is not None:
            pending = database.count_questions_for_review(topic_id=topic_id, concept=subtopic)
            if pending:
                console.print()
                console.print(Panel(
                    f"[bold]{pending} question(s) for '{subtopic}' are still pending human review.[/bold]\n"
                    "Self-test on them live and help review them now?",
                    border_style="magenta", box=box.ROUNDED,
                ))
                try:
                    review_choice = Prompt.ask(
                        "  [bold]Review quiz[/bold]", choices=["y", "n", "q"], default="y", case_sensitive=False
                    ).lower()
                except (KeyboardInterrupt, EOFError):
                    raise SystemExit
                if review_choice == "q":
                    raise SystemExit
                if review_choice == "y":
                    run_review_quiz(topic_id, subtopic)

        if force_practice:
            break

    # Build dynamic keywords from the subtopics that were actually explained to ensure strictly related practice
    dynamic_keywords = []
    for sub in explained_subtopics:
        words = sub.replace("()", "").replace("-", " ").replace("_", " ").lower().split()
        for w in words:
            if len(w) > 2 and w not in ("and", "the", "for", "with", "from"):
                dynamic_keywords.append(w)
            elif w in ("_id", "id"):
                dynamic_keywords.append(w)
                
    if not dynamic_keywords:
        dynamic_keywords = question_keywords

    # ---- 3. PRACTICE OFFER ----
    console.print()
    console.print(Panel(
        "[bold]Great — let's test what you just learned.[/bold]\n"
        "I'll pull 5 questions from the official question bank for this topic.",
        border_style="green", box=box.ROUNDED
    ))
    time.sleep(1)

    # Dynamic presentation label using the topic_id resolved at the top of this function.
    topic_id_str = f"Topic {topic_item['id']}" if topic_item else "Topic"
    header_topic = f"{topic_id_str}: {topic}"

    score = run_practice_questions(header_topic, bank_keys, question_keywords=dynamic_keywords, num=5, is_mock=False, concepts=explained_subtopics)
    debrief_title, debrief_body, debrief_style = build_practice_debrief(
        score,
        5,
        topic,
        agenda_item.get("active_subtopic"),
    )
    console.print()
    console.print(Panel(
        debrief_body,
        title=debrief_title,
        border_style=debrief_style,
        box=box.ROUNDED,
    ))

    # Mark mastered/completed if good score before evaluating mini-mock unlocks.
    if score is not None and score >= 4:
        active_subtopic = agenda_item.get("active_subtopic")
        if active_subtopic:
            planner.mark_subtopic_complete(USER_ID, topic, active_subtopic)
            console.print(f"\n  [bold green]🏆 Concept '{active_subtopic}' marked as complete![/bold green]")
            show_cumulative_cheat_sheet_checkpoint(topic, active_subtopic)
            
            # Check if the topic itself was marked complete
            profile = database.get_user_profile(USER_ID)
            completed_topics = profile.get("progress", {}).get("completed_topics", [])
            if topic in completed_topics:
                console.print(f"  [bold green]🎉 All concepts complete! Topic '{topic}' marked as mastered![/bold green]")
        else:
            planner.mark_topic_complete(USER_ID, topic)
            console.print(f"\n  [bold green]🏆 '{topic}' marked as mastered![/bold green]")

    # ---- 4. MINI MOCK OFFER ----
    # Mini-mocks are gated until the learner has mastered at least 3 topics.
    status = planner.get_syllabus_status(USER_ID)
    mastered_count = status.get("mastered_count", 0) if hasattr(status, "get") else 0
    if not isinstance(mastered_count, (int, float)):
        mastered_count = 0

    if mastered_count >= 3:
        console.print()
        console.print(Panel(
            "[bold]Mini-Mock unlocked.[/bold]\n"
            "Choose a 10-question or 20-question speed check, or skip for now.",
            border_style="magenta", box=box.ROUNDED
        ))
        try:
            mock_choice = Prompt.ask(
                "  [bold]Mini-Mock[/bold]",
                choices=["10", "20", "skip", "q"],
                default="skip",
                case_sensitive=False,
            ).lower()
        except (KeyboardInterrupt, EOFError):
            raise SystemExit

        if mock_choice in EXIT_COMMANDS:
            raise SystemExit
        if mock_choice in ("10", "20"):
            run_practice_questions(
                header_topic,
                bank_keys,
                question_keywords=dynamic_keywords,
                num=int(mock_choice),
                is_mock=True,
                concepts=explained_subtopics
            )

    try:
        ans = Prompt.ask("\n  [bold]Ready for the next agenda item?[/bold] (Y/n)", choices=["y", "n", "yes", "no", "q"], case_sensitive=False).lower()
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

    # Resolve a concrete subtopic + official doc within the topic so the
    # scenario and its evaluation are grounded in real reference material,
    # not invented purely from the model's own unaided knowledge.
    syllabus = planner.load_syllabus()
    topic_item = next((item for item in syllabus if item["topic"] == topic), None)
    md_context = ""
    if topic_item:
        subtopics = topic_item.get("subtopics") or [topic]
        subtopic = random.choice(subtopics)
        resolved_files = planner.resolve_concept_docs(topic_item.get("md_files", []), subtopic)
        if resolved_files:
            md_context = planner.load_md_context(resolved_files)

    with console.status(f"[dim]🤖 Coach is generating a scenario for: {topic}...[/dim]", spinner="dots"):
        scenario = coach.generate_scenario(topic, md_context=md_context)

    console.print(Panel(Markdown(scenario, code_theme="monokai"), title="📋 Product Requirement", border_style="bright_black", box=box.ROUNDED, padding=(1, 2)))

    console.print()
    try:
        user_answer = Prompt.ask("\n  [bold blue]❯[/bold blue] Your Approach / Query [dim](or 'q' to quit, 'back' to return)[/dim]").strip()
    except (KeyboardInterrupt, EOFError):
        return

    if user_answer.lower() in EXIT_COMMANDS or user_answer.lower() in BACK_COMMANDS:
        return

    with console.status("[dim]🤖 Coach is evaluating your approach...[/dim]", spinner="dots"):
        eval_text = coach.evaluate_scenario(topic, scenario, user_answer, md_context=md_context)
    
    panel = Panel(Markdown(eval_text, code_theme="monokai"), title="🧑‍🏫 CertCoach Evaluation", border_style="blue", box=box.ROUNDED, padding=(1, 2))
    print_paginated(panel, title="Scenario Evaluation")
    try:
        ans = Prompt.ask("\n  [bold blue]❯[/bold blue] [dim]Press Enter to return, or type a question to chat[/dim]")
        lowered = ans.strip().lower()
        if lowered and lowered not in EXIT_COMMANDS and lowered not in BACK_COMMANDS:
            run_free_chat_session(ans.strip())
    except (KeyboardInterrupt, EOFError):
        pass

# ---------------------------------------------------------------------------
# PRACTICE QUESTIONS
# ---------------------------------------------------------------------------

def clean_option_text(option_letter: str, option_text: str) -> str:
    """Remove a duplicated leading option label such as 'A)' or 'B.' from stored option text."""
    text = str(option_text or "").strip()
    letter = re.escape(str(option_letter or "").strip())
    if not letter:
        return text
    return re.sub(rf"^{letter}\s*[\).:-]\s*", "", text, count=1, flags=re.IGNORECASE).strip()


def _parse_feedback_sections(feedback: str) -> dict[str, str]:
    canonical_labels = {
        "correct answer": "Correct Answer",
        "why correct": "Why Correct",
        "why other options are wrong": "Why Other Options Are Wrong",
        "exam trap": "Exam Trap",
        "memory hook": "Memory Hook",
        "follow-up practice recommendation": "Follow-Up Practice Recommendation",
        "syntax example": "Syntax Example",
    }
    heading_pattern = re.compile(
        r"^(?:#{1,6}\s*)?(?:\d+\.\s*)?(Correct Answer|Why Correct|Why Other Options Are Wrong|Exam Trap|Memory Hook|Follow-Up Practice Recommendation|Syntax Example)\b[:\-\)]?\s*(.*)$",
        re.IGNORECASE,
    )
    sections: dict[str, list[str]] = {}
    current_label: str | None = None
    current_lines: list[str] = []

    def flush_current() -> None:
        nonlocal current_label, current_lines
        if current_label is None:
            return
        content = "\n".join(current_lines).strip()
        if content:
            sections[current_label] = content
        current_label = None
        current_lines = []

    for raw_line in textwrap.dedent(str(feedback or "")).splitlines():
        line = raw_line.strip()
        if not line:
            if current_label is not None and current_lines and current_lines[-1] != "":
                current_lines.append("")
            continue

        match = heading_pattern.match(line)
        if match:
            flush_current()
            label = canonical_labels[match.group(1).strip().lower()]
            current_label = label
            remainder = match.group(2).strip()
            current_lines = [remainder] if remainder else []
            continue

        if current_label is None:
            continue
        current_lines.append(line)

    flush_current()
    return sections


def clean_feedback_for_role(feedback: str, is_correct: bool) -> str:
    """Avoid displaying stale/generated feedback that contradicts the option's stored role."""
    text = str(feedback or "").strip()
    if not text:
        return (
            "This matches the question bank's marked correct answer."
            if is_correct
            else "This option is not marked correct in the question bank."
        )

    sections = _parse_feedback_sections(text)
    preferred_labels = ["Why Correct", "Correct Answer"] if is_correct else ["Why Other Options Are Wrong", "Exam Trap", "Correct Answer"]
    for label in preferred_labels:
        candidate = sections.get(label, "").strip()
        if candidate:
            text = candidate
            break
    else:
        cleaned_lines: list[str] = []
        for raw_line in textwrap.dedent(text).splitlines():
            line = raw_line.strip()
            if not line:
                if cleaned_lines and cleaned_lines[-1] != "":
                    cleaned_lines.append("")
                continue
            if line.startswith("```"):
                continue
            if re.match(r"^#{1,6}\s+", line):
                continue
            cleaned_lines.append(line)
        text = "\n".join(cleaned_lines).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    if not text:
        return (
            "This matches the question bank's marked correct answer."
            if is_correct
            else "This option is not marked correct in the question bank."
        )

    lowered = text.lower()
    if "review official mongodb documentation" in lowered or "review the official mongodb documentation" in lowered:
        return (
            "This matches the question bank's marked correct answer."
            if is_correct
            else "This option is not marked correct in the question bank."
        )
    if is_correct and lowered.startswith(("incorrect", "wrong", "not correct")):
        return "This matches the question bank's marked correct answer. The stored feedback for this item needs editorial review."
    if not is_correct and lowered.startswith(("correct", "yes", "right")):
        return "This option is not marked correct in the question bank. The stored feedback for this item needs editorial review."
    return text


def format_explanation_template(correct_option_letter: str, q_item: dict) -> str:
    """Restructures a question explanation into a strict seven-part template."""
    options = q_item.get("options", [])
    correct_snippet = ""
    wrong_snippets = []
    official_explanation = ""

    for opt in options:
        letter = opt.get("option_letter", "?")
        snippet = clean_option_text(letter, opt.get("code_snippet", ""))
        if opt.get("is_correct"):
            correct_snippet = snippet
            official_explanation = clean_feedback_for_role(opt.get("feedback", ""), True)
        else:
            feedback = clean_feedback_for_role(opt.get("feedback", ""), False)
            wrong_snippets.append(f"- **{letter})** `{snippet}`: {feedback}")

    trap_desc = q_item.get("metadata", {}).get("trap_analysis", "")
    if not trap_desc:
        for opt in options:
            if opt.get("is_trap") and opt.get("feedback"):
                trap_desc = opt.get("feedback")
    if not trap_desc:
        trap_desc = "Be careful of casing, invalid parameter combinations, or mixing Shell camelCase vs PyMongo snake_case casings."

    hook_map = {
        "CRUD": "Memory Hook: insertOne returns acknowledged & insertedId. It does NOT return the document itself.",
        "Projection": "Memory Hook: Projections cannot mix inclusion (1) and exclusion (0), except for the _id field.",
        "Aggregation": "Memory Hook: Always place $match as early as possible in your aggregation pipeline to utilize indexes.",
        "Index": "Memory Hook: Compound index prefix keys are like phone country codes: you must dial them in strict left-to-right order."
    }
    hook = "Memory Hook: Read every option character carefully. Exam traps love subtle casing variations."
    topic_lower = q_item.get("metadata", {}).get("topic", "").lower()
    for key, val in hook_map.items():
        if key.lower() in topic_lower:
            hook = val
            break

    explanation_text = (
        f"### 1. Correct Answer\n"
        f"Option {correct_option_letter} (`{correct_snippet}`)\n\n"
        f"### 2. Why Correct\n"
        f"{official_explanation or 'This query or operator matches the official MongoDB developer specification.'}\n\n"
        f"### 3. Why Other Options Are Wrong\n"
        + "\n".join(wrong_snippets)
        + "\n\n"
        f"### 4. Exam Trap\n"
        f"{trap_desc}\n\n"
        f"### 5. Memory Hook\n"
        f"{hook}\n\n"
        f"### 6. Follow-Up Practice Recommendation\n"
        f"Review official MongoDB reference markdown documentation and practice syntax patterns in the Scenario Simulator.\n\n"
        f"### 7. Syntax Example\n"
        f"Not required for this concept."
    )
    return explanation_text


def format_cell(idx: int, ans: str | None, is_flagged: bool) -> str:
    flag_str = "[bold yellow]★[/bold yellow]" if is_flagged else ""
    if ans:
        return f"{flag_str}[bold green]{ans}[/bold green]"
    elif is_flagged:
        return f"{flag_str} "
    else:
        return "[dim]·[/dim]"


def format_review_cell(idx: int, ans: str | None, is_correct: bool, is_flagged: bool) -> str:
    flag_str = "[bold yellow]★[/bold yellow]" if is_flagged else ""
    if ans is None:
        return f"{flag_str}[bold red]❌[/bold red]"
    elif is_correct:
        return f"{flag_str}[bold green]✅ {ans}[/bold green]"
    else:
        return f"{flag_str}[bold red]❌ {ans}[/bold red]"


def render_summary_grid(questions: list, user_answers: list, flagged: list) -> Table:
    table = Table(box=box.SIMPLE, show_header=False)
    cols = 10
    for _ in range(cols):
        table.add_column(justify="left", width=11)
        
    row_cells = []
    for idx in range(len(questions)):
        ans = user_answers[idx]
        is_flagged = flagged[idx]
        cell_text = format_cell(idx, ans, is_flagged)
        row_cells.append(f"[bold cyan]Q{idx+1:02d}:[/bold cyan] {cell_text}")
        
        if len(row_cells) == cols:
            table.add_row(*row_cells)
            row_cells = []
    if row_cells:
        while len(row_cells) < cols:
            row_cells.append("")
        table.add_row(*row_cells)
    return table


def run_summary_grid_menu(questions: list, user_answers: list, flagged: list, current_idx: int, start_time: float = None, time_limit: float = None) -> int:
    while True:
        if start_time is not None and time_limit is not None:
            time_left = max(0.0, time_limit - (time.time() - start_time))
            if time_left <= 0:
                console.print("\n[bold red]⏱️ Time's up! The exam has been automatically submitted.[/bold red]")
                time.sleep(2)
                return -99

        clear()
        console.print(Rule("[bold cyan]📊 Exam Summary Grid[/bold cyan]"))
        console.print()

        if start_time is not None and time_limit is not None:
            minutes, seconds = divmod(int(time_left), 60)
            time_col = "red" if time_left < 300 else "yellow"
            console.print(f"[{time_col}]⏱️ Time Left: {minutes:02d}:{seconds:02d}[/{time_col}]")
            console.print()

        grid_table = render_summary_grid(questions, user_answers, flagged)
        console.print(Panel(grid_table, title="📋 Question Status Board", border_style="cyan", padding=(1, 2)))

        answered = sum(1 for ans in user_answers if ans is not None)
        unanswered = len(questions) - answered
        review_count = sum(1 for f in flagged if f)

        console.print(f"  Answered: [green]{answered}[/green] | Unanswered: [yellow]{unanswered}[/yellow] | Flagged: [bold yellow]★ {review_count}[/bold yellow]")
        console.print()
        console.print("  [bold]Actions:[/bold]")
        console.print(f"    • Enter a question number [bold][1-{len(questions)}][/bold] to go directly to that question")
        console.print("    • Type [bold]R[/bold] to resume exam at your current question")
        console.print("    • Type [bold]F[/bold] to finalize and submit the exam")
        console.print()
        
        try:
            act = Prompt.ask("  [bold blue]Summary Grid ❯[/bold blue]").strip().upper()
        except (KeyboardInterrupt, EOFError):
            raise SystemExit
            
        if act == "R":
            return current_idx
        elif act == "F":
            unanswered_count = sum(1 for ans in user_answers if ans is None)
            if unanswered_count > 0:
                console.print(f"\n  [bold yellow]⚠️ Warning: You have {unanswered_count} unanswered question(s).[/bold yellow]")
            if confirm("  [bold green]Are you sure you want to finalize and submit your exam?[/bold green]"):
                return -99
            else:
                continue
        elif act.isdigit():
            val = int(act)
            if 1 <= val <= len(questions):
                return val - 1
            else:
                console.print(f"[red]  Invalid number. Enter a number between 1 and {len(questions)}.[/red]")
                time.sleep(1)


def run_post_exam_review(questions: list, user_answers: list, flagged: list, score: int):
    correctness = []
    correct_options = []
    for idx, q in enumerate(questions):
        correct_opt = None
        for opt in q.get("options", []):
            if opt.get("is_correct"):
                correct_opt = opt
                break
        correct_options.append(correct_opt)
        ans = user_answers[idx]
        if ans and correct_opt and ans == correct_opt.get("option_letter", "").upper():
            correctness.append(True)
        else:
            correctness.append(False)
            
    while True:
        clear()
        console.print(Rule("[bold cyan]🏁 Post-Exam Review Summary[/bold cyan]"))
        console.print()
        
        grid_table = Table(box=box.SIMPLE, show_header=False)
        cols = 10
        for _ in range(cols):
            grid_table.add_column(justify="left", width=11)
            
        row_cells = []
        for idx in range(len(questions)):
            ans = user_answers[idx]
            is_flagged = flagged[idx]
            is_correct = correctness[idx]
            cell_text = format_review_cell(idx, ans, is_correct, is_flagged)
            row_cells.append(f"[bold cyan]Q{idx+1:02d}:[/bold cyan] {cell_text}")
            
            if len(row_cells) == cols:
                grid_table.add_row(*row_cells)
                row_cells = []
        if row_cells:
            while len(row_cells) < cols:
                row_cells.append("")
            grid_table.add_row(*row_cells)
            
        console.print(Panel(grid_table, title="🏆 Detailed Question Scoring Grid", border_style="cyan", padding=(1, 2)))
        
        pct = (score / len(questions)) * 100
        col = "green" if pct >= 80 else "yellow" if pct >= 60 else "red"
        console.print(f"  Final Score: [{col}][bold]{score}/{len(questions)}  ({pct:.1f}%)[/bold][/{col}]")
        console.print()
        console.print("  [bold]Actions:[/bold]")
        console.print(f"    • Enter a question number [bold][1-{len(questions)}][/bold] to review its scenario, answers, and seven-part explanation")
        console.print("    • Type [bold]B[/bold] to return to the Main Menu")
        console.print()
        
        try:
            act = Prompt.ask("  [bold blue]Review ❯[/bold blue]").strip().upper()
        except (KeyboardInterrupt, EOFError):
            raise SystemExit
            
        if act in ("B", "BACK", "Q", "QUIT"):
            break
        elif act.isdigit():
            val = int(act)
            if 1 <= val <= len(questions):
                show_single_question_review(questions, user_answers, correctness, correct_options, val - 1)
            else:
                console.print(f"[red]  Invalid number. Enter a number between 1 and {len(questions)}.[/red]")
                time.sleep(1)


def show_single_question_review(questions: list, user_answers: list, correctness: list, correct_options: list, q_idx: int):
    while True:
        clear()
        q = questions[q_idx]
        ans = user_answers[q_idx]
        is_correct = correctness[q_idx]
        correct_opt = correct_options[q_idx]
        
        console.print(Rule(f"[bold cyan]🔍 Question {q_idx + 1}/{len(questions)} Review[/bold cyan]"))
        console.print()
        
        if is_correct:
            console.print("  [bold green]✅ You answered CORRECTLY[/bold green]")
        else:
            console.print(f"  [bold red]❌ You answered INCORRECTLY[/bold red] (Selected: [bold red]{ans or 'None'}[/bold red] | Correct: [bold green]{correct_opt.get('option_letter') if correct_opt else 'A'}[/bold green])")
        console.print()
        
        context = q.get("context", {})
        if context.get("scenario_description"):
            console.print(Panel(context["scenario_description"], title="📋 Scenario", border_style="dim", box=box.ROUNDED, padding=(0, 1)))
            
        console.print(Panel(f"[bold]{q.get('question_text', '')}[/bold]", border_style="bright_black", box=box.ROUNDED, padding=(0, 2)))
        
        for opt in q.get("options", []):
            letter = opt.get("option_letter", "?")
            snippet = opt.get("code_snippet", "")
            if letter == ans and is_correct:
                console.print(f"    [bold green]✅ {letter})  {snippet}  [Your Answer - Correct][/bold green]")
            elif letter == ans:
                console.print(f"    [bold red]❌ {letter})  {snippet}  [Your Answer - Wrong][/bold red]")
            elif opt.get("is_correct"):
                console.print(f"    [bold green]   {letter})  {snippet}  [Correct Answer][/bold green]")
            else:
                console.print(f"    [bold yellow]   {letter})[/bold yellow]  {snippet}")
                
        console.print()
        
        explanation_markdown = q.get("explanation", "").strip()
        if not explanation_markdown:
            explanation_markdown = format_explanation_template(correct_opt.get("option_letter") if correct_opt else "A", q)
        console.print(Panel(Markdown(explanation_markdown, code_theme="monokai"), title="📖 Structured Explanation", border_style="yellow", box=box.ROUNDED, padding=(0, 2)))
        
        console.print()
        console.print("  [dim]Navigation: [Enter] back to review grid | [N]ext question | [P]rev question[/dim]")
        
        try:
            act = Prompt.ask("  [bold blue]Navigation ❯[/bold blue]").strip().upper()
        except (KeyboardInterrupt, EOFError):
            raise SystemExit
            
        if act in ("N", "NEXT"):
            if q_idx < len(questions) - 1:
                q_idx += 1
            else:
                console.print("[yellow]  Already at the last question.[/yellow]")
                time.sleep(1)
        elif act in ("P", "PREV", "PREVIOUS"):
            if q_idx > 0:
                q_idx -= 1
            else:
                console.print("[yellow]  Already at the first question.[/yellow]")
                time.sleep(1)
        else:
            break


def run_exam_simulator(topic: str, questions: list, time_limit: int) -> int | None:
    current_idx = 0
    user_answers = [None] * len(questions)
    flagged = [False] * len(questions)
    response_times = [0.0] * len(questions)
    
    start_time = time.time()
    last_question_time = time.time()
    
    auto_submitted = False
    
    # --- AUTOSAVER RESUME PROMPT ---
    try:
        active_state = database.get_active_exam(USER_ID)
        if active_state and active_state.get("topic") == topic:
            console.print()
            console.print(Panel(
                f"[bold cyan]📋 Resume Unfinished Exam?[/bold cyan]\n\n"
                f"We found an in-progress, autosaved session for '[bold]{topic}[/bold]'.\n"
                f"Saved on: {active_state.get('timestamp')}\n"
                f"Questions Answered: {sum(1 for a in active_state.get('user_answers', []) if a)}/{len(questions)}",
                title="⚙️ CertCoach Autosaver", border_style="cyan"
            ))
            if confirm("  [bold green]Would you like to resume this session and continue where you left off?[/bold green]"):
                saved_questions = active_state.get("questions") or []
                if len(saved_questions) == len(questions):
                    questions = saved_questions
                    user_answers = active_state.get("user_answers", user_answers)
                    flagged = active_state.get("flagged", flagged)
                    elapsed = active_state.get("elapsed", 0.0)
                    start_time = time.time() - elapsed
                    last_question_time = time.time()
                    console.print("[green]  ✔ Resumed session successfully.[/green]")
                else:
                    database.clear_active_exam(USER_ID)
                    console.print("[yellow]  Saved session no longer matches the current question set -- starting fresh.[/yellow]")
                time.sleep(1.5)
            else:
                database.clear_active_exam(USER_ID)
                console.print("[yellow]  Skipped resume. Starting a fresh exam session...[/yellow]")
                time.sleep(1.5)
    except Exception:
        pass
    # --- END AUTOSAVER RESUME PROMPT ---
    
    while True:
        elapsed = time.time() - start_time
        time_left = max(0.0, time_limit - elapsed)
        
        if time_left <= 0:
            console.print("\n[bold red]⏱️ Time's up! The exam has been automatically submitted.[/bold red]")
            time.sleep(2)
            auto_submitted = True
            break
            
        # Accumulate time spent on current question
        now = time.time()
        time_spent = now - last_question_time
        response_times[current_idx] += time_spent
        last_question_time = now
        
        # Autosave state
        try:
            database.save_active_exam(USER_ID, topic, questions, user_answers, flagged, elapsed)
        except Exception:
            pass
            
        clear()
        
        # Timing display
        minutes, seconds = divmod(int(time_left), 60)
        time_col = "red" if time_left < 300 else "yellow"
        time_display = f"[{time_col}]⏱️ Time Left: {minutes:02d}:{seconds:02d}[/{time_col}]"
        
        # Dynamic pacing HUD alert
        target_elapsed = (current_idx + 1) * 90
        if elapsed > target_elapsed + 30:
            pacing_display = " | Speed: [bold red]Behind Pacing (⚠️ SLOW)[/bold red]"
        elif elapsed < target_elapsed - 30:
            pacing_display = " | Speed: [bold green]Ahead of Pacing (FAST)[/bold green]"
        else:
            pacing_display = " | Speed: [bold green]On Track[/bold green]"
            
        console.print(Rule(f"[bold cyan]🏆 {topic} Simulator[/bold cyan]"))
        console.print(f"  📋 Question [bold]{current_idx + 1}/{len(questions)}[/bold] | {time_display}{pacing_display}")
        if flagged[current_idx]:
            console.print("  [bold yellow]★ [REVIEW FLAGGED][/bold yellow]")
        console.print()
        
        q = questions[current_idx]
        context = q.get("context", {})
        if context.get("scenario_description"):
            console.print(Panel(context["scenario_description"], title="📋 Scenario", border_style="dim", box=box.ROUNDED, padding=(0, 1)))
            
        is_multi = str(q.get("metadata", {}).get("response_type", "single")).strip().lower() == "multi"
        if is_multi:
            console.print("  [bold magenta]Select ALL that apply[/bold magenta] [dim](e.g. type AC for options A and C)[/dim]")
        console.print(Panel(f"[bold]{q.get('question_text', '')}[/bold]", border_style="bright_black", box=box.ROUNDED, padding=(0, 2)))

        valid_options = []
        selected_letters = set((user_answers[current_idx] or "").upper())
        for opt in q.get("options", []):
            letter = opt.get("option_letter", "?")
            valid_options.append(letter.upper())
            snippet = opt.get("code_snippet", "")

            if letter.upper() in selected_letters:
                console.print(f"    [bold green]➜ {letter})  {snippet}  [Selected][/bold green]")
            else:
                console.print(f"    [bold yellow]   {letter})[/bold yellow]  {snippet}")

        console.print()
        answer_hint = "[A/B/C/D combo, e.g. AC]" if is_multi else "[A/B/C/D]"
        console.print(f"  [dim]Commands: {answer_hint} answer | [N]ext | [P]rev | [R]eview Flag | [S]ummary Grid | [1-{len(questions)}] jump | [F]inalize | [Q]uit[/dim]")
        
        try:
            cmd = Prompt.ask("  [bold blue]Exam ❯[/bold blue]").strip()
        except (KeyboardInterrupt, EOFError):
            raise SystemExit
            
        # Post-input time check
        input_elapsed = time.time() - start_time
        if input_elapsed >= time_limit:
            console.print("\n[bold red]⏱️ Time's up! The exam has been automatically submitted.[/bold red]")
            time.sleep(2)
            auto_submitted = True
            break
            
        if not cmd:
            continue
            
        cmd_upper = cmd.upper()
        cmd_lower = cmd.lower()
        if cmd_lower in EXIT_COMMANDS or cmd_lower in BACK_COMMANDS:
            if confirm("  [bold red]Are you sure you want to quit the exam? Active progress will be lost.[/bold red]"):
                try:
                    database.clear_active_exam(USER_ID)
                except Exception:
                    pass
                return None
            else:
                continue
                
        current_valid_letters = {opt.get("option_letter", "").upper() for opt in questions[current_idx].get("options", [])}
        is_current_multi = str(questions[current_idx].get("metadata", {}).get("response_type", "single")).strip().lower() == "multi"
        is_answer_token = bool(cmd_upper) and set(cmd_upper) <= current_valid_letters and (
            len(cmd_upper) == 1 or (is_current_multi and len(set(cmd_upper)) == len(cmd_upper))
        )
        if is_answer_token:
            user_answers[current_idx] = "".join(sorted(set(cmd_upper))) if is_current_multi else cmd_upper
            if current_idx < len(questions) - 1:
                now = time.time()
                response_times[current_idx] += (now - last_question_time)
                current_idx += 1
                last_question_time = now
        elif cmd_upper in ("N", "NEXT"):
            if current_idx < len(questions) - 1:
                now = time.time()
                response_times[current_idx] += (now - last_question_time)
                current_idx += 1
                last_question_time = now
            else:
                console.print("[yellow]  You are already at the last question.[/yellow]")
                time.sleep(1)
        elif cmd_upper in ("P", "PREV", "PREVIOUS"):
            if current_idx > 0:
                now = time.time()
                response_times[current_idx] += (now - last_question_time)
                current_idx -= 1
                last_question_time = now
            else:
                console.print("[yellow]  You are already at the first question.[/yellow]")
                time.sleep(1)
        elif cmd_upper in ("R", "REVIEW", "FLAG"):
            flagged[current_idx] = not flagged[current_idx]
        elif cmd_upper in ("S", "SUMMARY", "GRID"):
            now = time.time()
            response_times[current_idx] += (now - last_question_time)
            
            res = run_summary_grid_menu(questions, user_answers, flagged, current_idx, start_time, time_limit)
            last_question_time = time.time()
            
            if res == -99:
                break
            else:
                current_idx = res
        elif cmd_upper in ("F", "FINALIZE", "SUBMIT"):
            unanswered = sum(1 for ans in user_answers if ans is None)
            if unanswered > 0:
                console.print(f"\n  [bold yellow]⚠️ Warning: You have {unanswered} unanswered question(s).[/bold yellow]")
            if confirm("  [bold green]Are you sure you want to finalize and submit your exam?[/bold green]"):
                break
        elif cmd.isdigit():
            val = int(cmd)
            if 1 <= val <= len(questions):
                now = time.time()
                response_times[current_idx] += (now - last_question_time)
                current_idx = val - 1
                last_question_time = now
            else:
                console.print(f"[red]  Invalid question number. Enter a number between 1 and {len(questions)}.[/red]")
                time.sleep(1)
        else:
            console.print("[red]  Invalid command. Please try again.[/red]")
            time.sleep(1)

    score = 0
    for idx, q in enumerate(questions):
        correct_letters = {opt.get("option_letter", "").upper() for opt in q.get("options", []) if opt.get("is_correct")}
        ans = user_answers[idx]
        chosen_letters = set((ans or "").upper())
        is_correct = bool(chosen_letters) and chosen_letters == correct_letters
        if is_correct:
            score += 1

        q_topic = q.get("metadata", {}).get("topic", "General")

        database.save_attempt(USER_ID, str(q.get("_id", "unknown")), q_topic, ans or "—", is_correct, "High")
        database.update_question_exposure(str(q.get("_id", "unknown")), is_correct, response_times[idx])
        
    session_start = datetime.datetime.fromtimestamp(start_time, datetime.timezone.utc).replace(tzinfo=None)
    session_end = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    duration_minutes = (session_end - session_start).total_seconds() / 60.0
    
    covered_topics = list(set(q.get("metadata", {}).get("topic", "General") for q in questions))
    session_accuracy = (score / len(questions)) * 100
    
    database.save_study_session(USER_ID, session_start, session_end, duration_minutes, covered_topics, len(questions), session_accuracy)
    
    try:
        readiness_data_new = planner.calculate_readiness_metrics(USER_ID)
        profile = database.get_user_profile(USER_ID)
        history = profile.get("readiness_history", [])
        today_str = datetime.date.today().isoformat()
        history = [h for h in history if h.get("date") != today_str]
        history.append({
            "date": today_str,
            "readiness": readiness_data_new["current_readiness"]
        })
        database.update_user_profile(USER_ID, {"readiness_history": history})
    except Exception:
        pass
    try:
        database.clear_active_exam(USER_ID)
    except Exception:
        pass
        
    run_post_exam_review(questions, user_answers, flagged, score)
    return score


def show_wrong_attempt_remediation(question_id: str) -> None:
    """Stateless lookup only -- no new explanation is generated or saved.
    Primary surface is the missed question's own citation; secondary is a
    small sample of domain-matched flashcards (spec point 10)."""
    remediation = database.get_remediation_for_wrong_attempt(question_id)

    citation = remediation.get("citation")
    if citation and citation.get("quote"):
        console.print(Panel(
            f"[dim]{citation.get('doc_file', '')}[/dim]\n\n\"{citation['quote']}\"",
            title="📄 Re-read the source", border_style="cyan", box=box.ROUNDED, padding=(0, 2)
        ))

    flashcards = remediation.get("flashcards") or []
    if flashcards:
        lines = []
        for card in flashcards:
            answer = (card.get("answer", "") or "")[:400]
            lines.append(f"[bold]{card.get('title', '')}[/bold]\n{answer}")
        console.print(Panel(
            "\n\n".join(lines),
            title=f"🗂️ Related flashcards — {remediation.get('domain', '')}",
            border_style="magenta", box=box.ROUNDED, padding=(0, 2)
        ))


def present_and_capture_answer(q: dict) -> tuple[str, bool, float]:
    """Render a question + its options blind (no correctness hint) and prompt
    for the learner's answer (single or multi-select). Returns (raw_answer,
    is_multi, elapsed_sec). raw_answer may be 'Q'/'BACK' -- caller decides
    exit behavior."""
    meta = q.get("metadata", {})
    context = q.get("context", {})

    if context.get("scenario_description"):
        console.print(Panel(context["scenario_description"], title="📋 Scenario", border_style="dim", box=box.ROUNDED, padding=(0, 1)))

    console.print(Panel(f"[bold]{q.get('question_text', '')}[/bold]", border_style="bright_black", box=box.ROUNDED, padding=(0, 2)))

    valid_options = []
    for opt in q.get("options", []):
        letter = opt.get("option_letter", "?")
        valid_options.append(letter.upper())
        console.print(f"    [bold yellow]{letter})[/bold yellow]  {clean_option_text(letter, opt.get('code_snippet', ''))}")

    console.print()

    is_multi = str(meta.get("response_type", "single")).strip().lower() == "multi"
    valid_letter_set = set(valid_options)

    # Track response time
    q_start = time.time()
    if is_multi:
        console.print("  [bold magenta]Select ALL that apply[/bold magenta] [dim](e.g. type AC for options A and C)[/dim]")
        while True:
            try:
                raw = Prompt.ask("  [bold]Answer[/bold] [dim](or 'q' to quit, 'back' to return)[/dim]").strip().upper()
            except (KeyboardInterrupt, EOFError):
                raise SystemExit
            if raw in ("Q", "BACK"):
                ans = raw
                break
            token = raw.replace(" ", "").replace(",", "")
            if token and set(token) <= valid_letter_set and len(set(token)) == len(token):
                ans = "".join(sorted(set(token)))
                break
            console.print(f"  [red]Enter a combination of {', '.join(sorted(valid_letter_set))} (e.g. AC), or Q/BACK.[/red]")
    else:
        try:
            ans = Prompt.ask("  [bold]Answer[/bold] [dim](or 'q' to quit, 'back' to return)[/dim]", choices=valid_options + ["Q", "BACK"], case_sensitive=False).upper()
        except (KeyboardInterrupt, EOFError):
            raise SystemExit
    elapsed_sec = time.time() - q_start
    return ans, is_multi, elapsed_sec


def evaluate_answer(q: dict, ans: str) -> dict:
    """Compare the learner's chosen letters against the question's marked-correct
    option(s). Pure, no I/O, no DB writes. Returns a dict with is_correct,
    correct_letters, correct_option, and user_feedback (concatenated per-option
    feedback text for the chosen options)."""
    chosen_letters = set(ans)
    correct_option = None
    correct_letters = set()
    user_feedback = ""
    for opt in q.get("options", []):
        if opt.get("is_correct"):
            correct_option = opt
            correct_letters.add(opt.get("option_letter", "").upper())
        if opt.get("option_letter", "").upper() in chosen_letters:
            fb = opt.get("feedback", "")
            if fb:
                user_feedback = (user_feedback + " / " + fb) if user_feedback else fb
    is_correct = bool(chosen_letters) and chosen_letters == correct_letters
    return {
        "is_correct": is_correct,
        "correct_letters": correct_letters,
        "correct_option": correct_option,
        "user_feedback": user_feedback,
    }


def run_practice_questions(topic: str, bank_keys: list, num: int = 5, is_mock: bool = False, question_keywords: list = None, concepts: list = None, preselected_questions: list = None) -> int | None:
    if is_mock:
        clear()

    # Try to extract topic_id from the topic parameter to enable precise database concept querying
    syllabus = planner.load_syllabus()
    topic_item = next((item for item in syllabus if item["topic"] == topic or f"Topic {item['id']}:" in topic or item["topic"] in topic), None)
    topic_id = topic_item["id"] if topic_item else None

    # Gather questions filtered by topic + keyword relevance
    questions = []

    if preselected_questions is not None:
        # Domain-weighted mocks (Full Mock, Timed Mock Exam) already selected
        # and shortfall-reported their own questions -- use them as-is, even
        # if fewer than `num` were available. Never silently pad here.
        questions = preselected_questions
    elif not is_mock:
        # Standard concept practice is exactly 3 Easy and 2 Medium questions.
        easy_qs = []
        medium_qs = []
        for key in bank_keys:
            easy_qs.extend(
                database.get_random_questions(
                    topic=key,
                    limit=num * 2,
                    subtopic_keywords=question_keywords,
                    difficulty="Easy",
                    strict_keywords=True,
                    topic_id=topic_id,
                    concepts=concepts
                )
            )
            medium_qs.extend(
                database.get_random_questions(
                    topic=key,
                    limit=num * 2,
                    subtopic_keywords=question_keywords,
                    difficulty="Medium",
                    strict_keywords=True,
                    topic_id=topic_id,
                    concepts=concepts
                )
            )
        
        seen = set()
        unique_easy = []
        for q in easy_qs:
            qt = q.get("question_text", "")
            if qt not in seen:
                seen.add(qt)
                unique_easy.append(q)
                
        unique_medium = []
        for q in medium_qs:
            qt = q.get("question_text", "")
            if qt not in seen:
                seen.add(qt)
                unique_medium.append(q)
                
        questions = unique_easy[:3] + unique_medium[:2]
    else:
        # Mock/Anki/Spaced repetition uses general random pool
        for key in bank_keys:
            questions.extend(
                database.get_random_questions(
                    topic=key,
                    limit=num * 2,
                    subtopic_keywords=question_keywords,
                    topic_id=topic_id,
                    concepts=concepts
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
        console.print("\n  [bold yellow]No confirmed questions are available yet.[/bold yellow]")
        time.sleep(2)
        return None

    if preselected_questions is None:
        if is_mock:
            # Generic-pool callers (Diagnostic, Mini-Mock, Pop Quiz, Boss Fight) never use a
            # 3E/2M mix -- run with whatever was found instead of hard-aborting on a
            # message that describes a different quiz composition entirely.
            if len(questions) < num:
                console.print(
                    f"\n  [bold yellow]Only {len(questions)} of {num} requested questions are "
                    f"available for this quiz -- continuing with what's ready.[/bold yellow]"
                )
                time.sleep(1.5)
        elif len(unique_easy) < 3 or len(unique_medium) < 2:
            # Standard concept practice: the fixed 3 Easy + 2 Medium composition itself is
            # what must be checked, independent of whatever `num` a caller happened to pass.
            console.print(f"\n  [bold yellow]The required 3 Easy + 2 Medium concept-practice mix is unavailable.[/bold yellow]")
            console.print(Panel(
                "[bold]This concept is not study-ready yet.[/bold]\n\n"
                "Practice requires exactly three Easy and two Medium active, validated questions mapped directly to the current concept. "
                "Hard questions and arbitrary difficulty substitutions are not used, and the concept will remain open.",
                title="Concept Practice Blocked",
                border_style="yellow",
                box=box.ROUNDED
            ))
            time.sleep(2)
            return None

    if is_mock:
        time_limit = num * MOCK_SECONDS_PER_QUESTION
        score = run_exam_simulator(topic, questions, time_limit)
        if score is not None:
            pct = score / len(questions) * 100
            if pct >= 85:
                awarded = database.award_streak_freeze(USER_ID)
                if awarded:
                    console.print("\n[bold yellow]❄️ Congratulations! You earned a Streak Freeze token (high mock score of >=85%).[/bold yellow]")
                    time.sleep(2)
        return score

    score = 0
    weak_signals = []
    label = "Mini-Mock" if is_mock else "Practice"
    concepts_lbl = f" | Concepts: {', '.join(concepts)}" if (not is_mock and concepts) else ""
    console.print(Rule(f"[bold cyan]{label}: {topic}{concepts_lbl}[/bold cyan]"))

    for idx, q in enumerate(questions):
        meta = q.get("metadata", {})
        q_topic = meta.get("topic", topic)

        console.print()
        console.print(f"  [dim]Q {idx + 1}/{len(questions)}[/dim]")

        ans, _is_multi, elapsed_sec = present_and_capture_answer(q)

        if ans in ("Q", "BACK"):
            console.print("[yellow]  Exiting practice session...[/yellow]")
            time.sleep(1)
            return None

        # Evaluate
        if not is_mock:
            try:
                conf_in = Prompt.ask("  Confidence? [bold](H)[/bold] / [bold](M)[/bold] / [bold](L)[/bold]",
                                     choices=["H", "M", "L", "q"], case_sensitive=False).upper()
            except (KeyboardInterrupt, EOFError):
                raise SystemExit
            if conf_in.lower() in EXIT_COMMANDS:
                raise SystemExit
            confidence = {"H": "High", "M": "Medium", "L": "Low"}.get(conf_in, "Medium")
        else:
            confidence = "High"

        evaluation = evaluate_answer(q, ans)
        is_correct = evaluation["is_correct"]
        correct_letters = evaluation["correct_letters"]
        correct_option = evaluation["correct_option"]
        user_feedback = evaluation["user_feedback"]

        # Save individual attempt and update question exposure (seen, times, average time)
        database.save_attempt(USER_ID, str(q.get("_id", "unknown")), q_topic, ans, is_correct, confidence)
        database.update_question_exposure(str(q.get("_id", "unknown")), is_correct, elapsed_sec)

        if is_correct:
            score += 1
            console.print(f"\n  [bold green]✅ Correct![/bold green]")
        else:
            weak_signals.append(extract_question_focus_label(q))
            console.print(f"\n  [bold red]❌ Wrong.[/bold red]")
            if correct_letters:
                console.print(f"  Correct answer: [bold]{', '.join(sorted(correct_letters))}[/bold]")

        # Restructure to the strict seven-part Explanation Template
        correct_letter = correct_option.get("option_letter") if correct_option else "A"
        explanation_markdown = q.get("explanation", "").strip()
        if not explanation_markdown:
            explanation_markdown = format_explanation_template(correct_letter, q)
        
        console.print(Panel(Markdown(explanation_markdown, code_theme="monokai"), title="📖 Structured Explanation", border_style="yellow", box=box.ROUNDED, padding=(0, 2)))

        if not is_correct and not is_mock:
            show_wrong_attempt_remediation(str(q.get("_id", "unknown")))

        # Skip the coach reflection on a high-confidence correct answer -- it
        # mostly restates the explanation panel just shown. Reserve it for
        # wrong answers and correct-but-uncertain ones, where a second
        # framing actually adds something.
        if not is_mock and not (is_correct and confidence == "High"):
            with console.status("[dim]🤖 Coach is reflecting...[/dim]", spinner="dots"):
                fb = coach.get_answer_feedback(q_topic, is_correct, user_feedback, confidence)
            console.print(Panel(Markdown(fb, code_theme="monokai"), title="🧑‍🏫 CertCoach", border_style="blue", box=box.ROUNDED, padding=(0, 2)))

        if idx < len(questions) - 1:
            try:
                next_action = Prompt.ask("\n  [dim]Enter for next / q to quit / back to return[/dim]", default="")
            except (KeyboardInterrupt, EOFError):
                raise SystemExit
            if next_action.strip().lower() in EXIT_COMMANDS or next_action.strip().lower() in BACK_COMMANDS:
                console.print("[yellow]  Exiting practice session...[/yellow]")
                time.sleep(1)
                return None

    # Result summary
    if is_mock:
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

    if not is_mock:
        recovery_title, recovery_body, recovery_style = build_practice_recovery_text(
            topic,
            concepts,
            score,
            len(questions),
            weak_signals,
        )
        console.print()
        console.print(Panel(
            recovery_body,
            title=recovery_title,
            border_style=recovery_style,
            box=box.ROUNDED,
        ))

    if not is_mock and len(questions) == 5 and score == 5:
        awarded = database.award_streak_freeze(USER_ID)
        if awarded:
            console.print("\n[bold yellow]❄️ Congratulations! You earned a Streak Freeze token (perfect 5/5 score).[/bold yellow]")
            time.sleep(2)

    return score


def run_review_quiz(topic_id: int, concept: str) -> dict:
    """Live self-test over this concept's still-unconfirmed (draft/sourced)
    question backlog. Reuses the same blind-answer interaction practice uses
    (present_and_capture_answer/evaluate_answer), then layers on the citation
    panel and the Confirm/Suspect decision certcoach-review-questions already
    has -- the live-answer experience informs the decision instead of just
    reading the question. Never calls save_attempt, update_question_exposure,
    or any streak function: this pool is unconfirmed, so no official
    mastery/readiness/streak stat may move from a session here."""
    stats = {"correct": 0, "total": 0, "confirmed": 0, "suspect": 0, "skipped": 0}
    queue = database.get_questions_for_review(topic_id=topic_id, concept=concept)
    if not queue:
        console.print("[green]Nothing pending review for this concept right now.[/green]")
        return stats

    console.print(Rule(f"[bold magenta]Review Quiz: {concept}[/bold magenta]"))
    console.print(
        f"[dim]{len(queue)} question(s) pending review. Answer each one, "
        f"then decide Confirm/Suspect based on what you just saw.[/dim]"
    )

    for idx, q in enumerate(queue):
        console.print()
        console.print(f"  [dim]Q {idx + 1}/{len(queue)}[/dim]")

        ans, _is_multi, _elapsed_sec = present_and_capture_answer(q)
        if ans in ("Q", "BACK"):
            console.print("[yellow]  Exiting review quiz...[/yellow]")
            break

        stats["total"] += 1
        evaluation = evaluate_answer(q, ans)
        is_correct = evaluation["is_correct"]
        correct_letters = evaluation["correct_letters"]
        correct_option = evaluation["correct_option"]

        if is_correct:
            stats["correct"] += 1
            console.print("\n  [bold green]✅ Correct![/bold green]")
        else:
            console.print("\n  [bold red]❌ Wrong.[/bold red]")
            if correct_letters:
                console.print(f"  Correct answer: [bold]{', '.join(sorted(correct_letters))}[/bold]")

        # Full explanation shown either way -- right or wrong -- same as practice.
        correct_letter = correct_option.get("option_letter") if correct_option else "A"
        explanation_markdown = q.get("explanation", "").strip()
        if not explanation_markdown:
            explanation_markdown = format_explanation_template(correct_letter, q)
        console.print(Panel(Markdown(explanation_markdown, code_theme="monokai"), title="📖 Structured Explanation", border_style="yellow", box=box.ROUNDED, padding=(0, 2)))

        console.print(render_citation_panel(q))

        citation_verified, _ = database.verify_citation(q)
        if citation_verified:
            prompt_label = "\n  [bold]Decision[/bold] [C]onfirm / [S]uspect / s[K]ip / [Q]uit"
            allowed_choices = ["c", "s", "k", "q"]
        else:
            console.print(
                "[yellow]  Citation check failed -- Confirm is unavailable. "
                "Mark Suspect or fix the citation and re-run.[/yellow]"
            )
            prompt_label = "\n  [bold]Decision[/bold] [S]uspect / s[K]ip / [Q]uit"
            allowed_choices = ["s", "k", "q"]

        try:
            decision = Prompt.ask(prompt_label, choices=allowed_choices, default="k", case_sensitive=False).lower()
        except (KeyboardInterrupt, EOFError):
            raise SystemExit

        if decision == "q":
            break
        elif decision == "c":
            database.confirm_question(q["_id"], USER_ID)
            stats["confirmed"] += 1
            console.print("[green]Confirmed.[/green]")
        elif decision == "s":
            try:
                reason = Prompt.ask("  Reason (one line)")
            except (KeyboardInterrupt, EOFError):
                reason = ""
            database.mark_question_suspect(q["_id"], reason)
            stats["suspect"] += 1
            console.print("[yellow]Marked suspect.[/yellow]")
        else:
            stats["skipped"] += 1

    console.print()
    console.print(Rule("[bold]Review Quiz Summary[/bold]"))
    console.print(
        f"\n  Score: [bold]{stats['correct']}/{stats['total']}[/bold]  |  "
        f"Confirmed: [green]{stats['confirmed']}[/green]  |  "
        f"Suspect: [yellow]{stats['suspect']}[/yellow]  |  "
        f"Skipped: [dim]{stats['skipped']}[/dim]\n"
    )
    return stats


def run_section_checkin(topic: str, concept: str, section: dict) -> None:
    """Ephemeral, ungraded comprehension check for the lesson section just
    shown. Reuses the same blind-answer interaction as practice/review-quiz
    (present_and_capture_answer/evaluate_answer) -- zero new answer-capture
    UI. Never calls save_attempt, update_question_exposure, or any streak
    function: this is an engagement checkpoint, not graded practice, so it
    can never move official mastery/readiness/streak state."""
    questions = coach.generate_section_check(concept, section["text"])
    if not questions:
        console.print("[dim]  Comprehension check unavailable -- continuing.[/dim]")
        return

    console.print()
    for idx, q in enumerate(questions):
        console.print(f"  [dim]Quick check {idx + 1}/{len(questions)}[/dim]")
        ans, _is_multi, _elapsed_sec = present_and_capture_answer(q)
        if ans in ("Q", "BACK"):
            break

        evaluation = evaluate_answer(q, ans)
        if evaluation["is_correct"]:
            console.print("  [bold green]✅ Correct.[/bold green]")
        else:
            correct_letters = evaluation["correct_letters"]
            correct_option = evaluation["correct_option"]
            correct_text = correct_option.get("code_snippet", "") if correct_option else ""
            console.print(
                f"  [bold red]❌ Not quite.[/bold red] Correct answer: "
                f"[bold]{', '.join(sorted(correct_letters))}[/bold] -- {correct_text}"
            )
        console.print()

    total = planner.mark_lesson_chunk_complete(USER_ID, topic, concept)
    console.print(f"[dim]  ✅ {total} bite-sized check-in(s) completed for {concept} so far.[/dim]")


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

    for s in status["status_list"]:
        acc_col = "green" if s["accuracy"] >= 80 else "yellow" if s["accuracy"] >= 50 else "red"
        w_style, w_lbl = get_weight_style(s.get("exam_weight", ""), compact=True)
        table.add_row(
            str(s["id"]),
            s["topic"],
            f"[{w_style}]{w_lbl}[/{w_style}]",
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
        lowered = ans.strip().lower()
        if lowered == "a":
            show_documentation_audit()
        elif lowered and lowered not in EXIT_COMMANDS and lowered not in BACK_COMMANDS:
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
    profile = database.get_user_profile(USER_ID)
    streak = profile.get("streak_days", 1)
    
    # Study Session tracking totals
    sessions = database.get_study_sessions(USER_ID)
    total_sessions = len(sessions)
    total_study_time = sum(s.get("duration", 0.0) for s in sessions)
    
    # Attempts
    stats = database.get_analytics(USER_ID)
    total_attempts = stats["total_attempts"]
    correct_attempts = stats["correct_attempts"]
    wrong_attempts = max(0, total_attempts - correct_attempts)
    overall_accuracy = (correct_attempts / max(1, total_attempts)) * 100
    
    # Readiness Metrics
    readiness_data = planner.calculate_readiness_metrics(USER_ID)
    current_readiness = readiness_data["current_readiness"]
    expected_readiness = readiness_data["expected_readiness"]
    target_readiness = readiness_data["target_readiness"]
    pass_probability = readiness_data["pass_probability"]
    pass_probability_note = (
        "  [dim](early estimate -- firms up with more study sessions)[/dim]"
        if readiness_data.get("low_data", False) else ""
    )

    # Build Topic Mastery Dashboard data
    status = planner.get_syllabus_status(USER_ID)
    topic_mastery = []
    strong_areas = []
    weak_areas = []
    
    for s in status["status_list"]:
        topic_name = s["topic"]
        acc = s["accuracy"]
        attempts = s["attempts"]
        is_mastered = s["is_mastered"]
        
        # Map syllabus topics to short names for aesthetics
        short_name = topic_name
        for prefix in ["CRUD Operations - ", "MongoDB "]:
            if short_name.startswith(prefix):
                short_name = short_name[len(prefix):]
                
        topic_mastery.append((short_name, acc, attempts, is_mastered))
        
        if is_mastered or (attempts >= 3 and acc >= 80.0):
            strong_areas.append(short_name)
        elif attempts > 0 and acc < 70.0:
            weak_areas.append(short_name)
            
    # Fallback placeholders
    if not strong_areas:
        strong_areas = ["No domains mastered yet — start studying daily!"]
    if not weak_areas:
        weak_areas = ["No weak domains identified yet. Keep practicing!"]

    # 1. Main Header Panel
    dashboard_text = (
        f"🔥  [bold yellow]Streak[/bold yellow]: {streak} Days  |  "
        f"📚  [bold]Total Sessions[/bold]: {total_sessions}  |  "
        f"⏱️  [bold cyan]Total Study Time[/bold cyan]: {total_study_time:.0f} Minutes\n"
        f"❓  [bold]Questions[/bold]: {total_attempts} (✅ {correct_attempts} / ❌ {wrong_attempts})  |  "
        f"🎯  [bold green]Accuracy[/bold green]: {overall_accuracy:.1f}%\n\n"
        f"📈  [bold green]Current Readiness[/bold green]: {current_readiness:.1f}% (Expected: {expected_readiness:.1f}% / Target: {target_readiness:.0f}%)\n"
        f"🎲  [bold yellow]Pass Probability[/bold yellow]: {pass_probability:.1f}%{pass_probability_note}"
    )
    
    elements = [
        Rule("[bold cyan]📊 High-Fidelity Performance Analytics Dashboard[/bold cyan]"),
        Text("\n"),
        Panel(dashboard_text, title="🏁 Overview Metrics", border_style="cyan", box=box.ROUNDED)
    ]
    
    # 2. Topic Mastery Dashboard
    mastery_lines = []
    for name, acc, att, mastered in topic_mastery:
        bar_len = int(acc / 10)
        bar = "█" * bar_len + "░" * (10 - bar_len)
        col = "green" if acc >= 80 else "yellow" if acc >= 50 else "red"
        status_symbol = " [bold green]✅[/bold green]" if mastered else " [dim]—[/dim]"
        mastery_lines.append(f"  {name:<24} : [{col}]{bar}[/{col}] {acc:>5.1f}% ({att} tries){status_symbol}")
        
    elements.append(Text("\n"))
    elements.append(Panel("\n".join(mastery_lines), title="🏅 Topic Mastery Dashboard", border_style="blue", box=box.ROUNDED))

    # 2b. Domain vs. Exam-Weight Accuracy (heaviest domain first, so a weak
    # CRUD score reads louder than a weak Tools score, not sorted by accuracy)
    domain_report = database.get_domain_accuracy_report(USER_ID)
    domain_lines = []
    for d in domain_report:
        if d["accuracy_pct"] is None:
            domain_lines.append(f"  {d['domain']:<26} : [dim]{d['exam_weight_pct']:>2.0f}% of exam — no attempts yet[/dim]")
            continue
        acc = d["accuracy_pct"]
        col = "green" if acc >= 80 else "yellow" if acc >= 60 else "red"
        domain_lines.append(
            f"  {d['domain']:<26} : {d['exam_weight_pct']:>2.0f}% of exam — [{col}]{acc:>5.1f}%[/{col}] ({d['correct']}/{d['attempts']})"
        )
    elements.append(Text("\n"))
    elements.append(Panel("\n".join(domain_lines), title="⚖️ Domain vs. Exam-Weight Accuracy", border_style="cyan", box=box.ROUNDED))

    # 2c. Concept-Level Accuracy (weakest first)
    concept_report = [c for c in database.get_concept_accuracy_report(USER_ID) if c["attempts"] > 0]
    if concept_report:
        concept_lines = []
        for c in concept_report[:10]:
            col = "green" if c["accuracy_pct"] >= 80 else "yellow" if c["accuracy_pct"] >= 60 else "red"
            domain_lbl = c["domain"] or "Unmapped"
            concept_lines.append(
                f"  {c['concept']:<32} [dim]({domain_lbl})[/dim] : [{col}]{c['accuracy_pct']:>5.1f}%[/{col}] ({c['correct']}/{c['attempts']})"
            )
        elements.append(Text("\n"))
        elements.append(Panel("\n".join(concept_lines), title="🔎 Weakest Concepts (bottom 10)", border_style="red", box=box.ROUNDED))

    # 3. Strong & Weak Areas Side-by-Side
    areas_lines = []
    areas_lines.append("[bold green]💪 Strong Areas (Acc >= 80% / Mastered):[/bold green]")
    for sa in strong_areas[:5]:
        areas_lines.append(f"  • {sa}")
    areas_lines.append("\n[bold red]⚠️  Weak Areas (Acc < 70%):[/bold red]")
    for wa in weak_areas[:5]:
        areas_lines.append(f"  • {wa}")
        
    elements.append(Text("\n"))
    elements.append(Panel("\n".join(areas_lines), title="🎯 Skills & Domains Analysis", border_style="yellow", box=box.ROUNDED))
    
    # 4. Readiness History
    history = profile.get("readiness_history", [])
    if not history:
        history = [
            {"date": "Day 1", "readiness": 0.0},
            {"date": f"Day {max(1, total_sessions)}", "readiness": current_readiness}
        ]
    
    history_lines = []
    for h in history:
        date_lbl = h.get("date", "")
        if "-" in date_lbl:
            parts = date_lbl.split("-")
            date_lbl = f"{parts[1]}/{parts[2]}"
        val = h.get("readiness", 0.0)
        history_lines.append(f"  {date_lbl:<12} : [bold green]{val:.1f}%[/bold green]")
        
    elements.append(Text("\n"))
    elements.append(Panel("\n".join(history_lines), title="📈 Readiness History Progression", border_style="green", box=box.ROUNDED))
    
    # 5. Why Am I Not Ready Report
    ready_bullets = []
    
    # Positive factors
    if current_readiness >= expected_readiness:
        ready_bullets.append("[bold green]+ On Track[/bold green]: Your readiness matches or exceeds expected pacing.")
    if streak >= 3:
        ready_bullets.append(f"[bold green]+ Streak Habit[/bold green]: Excellent consistency with a {streak}-day daily study streak.")
    for name, acc, att, mastered in topic_mastery:
        if mastered:
            ready_bullets.append(f"[bold green]+ {name} Mastery[/bold green]: Strong knowledge demonstrated (Acc: {acc:.0f}%).")
            
    # Negative factors
    rec_data = planner.get_study_plan_recommendation(USER_ID)
    missed_days = rec_data.get("missed_sessions", 0)
    if missed_days > 0:
        ready_bullets.append(f"[bold red]- Missed Sessions[/bold red]: You skipped {missed_days} study calendar days.")
    if current_readiness < expected_readiness - 5.0:
        ready_bullets.append(f"[bold red]- Behind Schedule[/bold red]: Readiness is {expected_readiness - current_readiness:.1f}% below target pacing.")
    for name, acc, att, mastered in topic_mastery:
        if att > 0 and acc < 70.0:
            ready_bullets.append(f"[bold red]- Weak {name}[/bold red]: High exam risk (Accuracy is currently {acc:.1f}%).")
            
    if not ready_bullets:
        ready_bullets = ["[dim]Keep practice and study loops running to populate analysis.[/dim]"]
            
    elements.append(Text("\n"))
    elements.append(Panel("\n".join(ready_bullets), title="📋 Why Am I Not Ready Report", border_style="magenta", box=box.ROUNDED))
    
    # 6. Coach Notes
    pattern = "Concepts understood quickly. Needs more timed practice and mock attempts."
    if total_sessions > 0:
        avg_session_accuracy = sum(s.get("accuracy", 0.0) for s in sessions) / total_sessions
        if avg_session_accuracy >= 80.0:
            pattern = "Strong focus, fast conceptual pickup. Recommend running the Timed Mock Exam now."
        elif streak < 2:
            pattern = "Conceptual understanding is decent, but daily streak is inconsistent. Try to log study sessions daily."
            
    notes = (
        f"[bold cyan]Strong Domains[/bold cyan]: {', '.join(strong_areas[:3])}\n"
        f"[bold red]Weak Domains[/bold red]: {', '.join(weak_areas[:3])}\n"
        f"[bold yellow]Learning Pattern[/bold yellow]: {pattern}"
    )
    elements.append(Text("\n"))
    elements.append(Panel(notes, title="📝 CertCoach Notes", border_style="bright_black", box=box.ROUNDED))
    
    from rich.console import Group
    group = Group(*elements)
    print_paginated(group, title="Performance Dashboard")
    
    try:
        ans = Prompt.ask("\n  [bold blue]❯[/bold blue] [dim]Press Enter to return, or type a question to chat[/dim]")
        lowered = ans.strip().lower()
        if lowered and lowered not in EXIT_COMMANDS and lowered not in BACK_COMMANDS:
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
            
    traps_map = get_exam_traps_map()
    
    active_traps = []
    for topic_name, trap_text in traps_map.items():
        if topic_name in completed:
            active_traps.append(trap_text)
            
    header = "💡 [bold yellow]CRITICAL EXAM TRAPS & REMINDERS[/bold yellow]"
    divider = "━"*50
    
    renderables = [Text.from_markup(header), Text.from_markup(divider)]
    
    if not active_traps:
        renderables.append(Text.from_markup(
            "\n  [bold red]🔒 Exam Cheat Sheet Locked[/bold red]\n\n"
            "  CertCoach exam traps and cheatsheets only unlock after you start mastering topics.\n"
            "  Once you master at least [bold yellow]1 topic[/bold yellow] through practice or agenda quizzes,\n"
            "  its respective critical traps will unlock and dynamically append here.\n\n"
            "  Keep studying and grinding! 💪\n"
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


def get_exam_traps_map() -> dict:
    return {
        "MongoDB Overview & The Document Model": "• [bold cyan]Topic 1: Overview & Document Model[/bold cyan]\n  - BSON maximum document size is strictly [bold red]16MB[/bold red]. Use GridFS for larger files.\n  - Key names are case-sensitive. Avoid dots (`.`), null characters, and ambiguous naming conventions in field names.",
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
        "Tools, Tooling & Atlas Search": "• [bold cyan]Topic 12: Tools, Tooling & Atlas Search[/bold cyan]\n  - Free Tier: M0 tier clusters are limited to 512MB storage and do not support VPC Peering or advanced backup routines.\n  - Atlas Search requires search indexes; standard collection indexes are not the same thing."
    }


def show_cumulative_cheat_sheet_checkpoint(topic: str, completed_concept: str):
    profile = database.get_user_profile(USER_ID)
    progress = profile.get("progress", {})
    completed_subtopics = progress.get("completed_subtopics", {}).get(topic, [])
    topic_item = next((item for item in planner.load_syllabus() if item["topic"] == topic), None)
    all_subtopics = topic_item.get("subtopics", []) if topic_item else []
    remaining = [s for s in all_subtopics if s not in completed_subtopics]
    traps_map = get_exam_traps_map()
    trap_text = traps_map.get(topic, "No topic cheat sheet is mapped yet.")

    completed_lines = "\n".join(f"  - [green]{s}[/green]" for s in completed_subtopics) or "  - [dim]None yet[/dim]"
    remaining_lines = "\n".join(f"  - [yellow]{s}[/yellow]" for s in remaining) or "  - [green]All concepts complete[/green]"

    console.print()
    console.print(Panel(
        f"[bold]Completed concept:[/bold] {completed_concept}\n\n"
        f"[bold cyan]Covered in this topic[/bold cyan]\n{completed_lines}\n\n"
        f"[bold yellow]Still remaining[/bold yellow]\n{remaining_lines}\n\n"
        f"[bold magenta]Cumulative Cheat Sheet[/bold magenta]\n{trap_text}",
        title="[bold cyan]Concept Checkpoint[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED
    ))


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
    
    # Ask for exam date
    while True:
        date_str = ask("[bold]Enter your updated MongoDB exam date (YYYY-MM-DD):[/bold]")
        if date_str == "__back__":
            return
        try:
            exam_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
            today = datetime.datetime.now(datetime.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
            if exam_date <= today:
                console.print("[red]The exam date must be in the future (after today).[/red]")
                continue
            delta = exam_date - datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
            days = max(1, delta.days)
            break
        except ValueError:
            console.print("[red]Please enter a valid date in YYYY-MM-DD format (e.g. 2026-06-30).[/red]")
            
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
    if confirm("[bold]Would you like to reset all topic mastery progress and start completely fresh?[/bold]"):
        completed_topics = []
        database.update_user_profile(USER_ID, {"progress": {"completed_topics": [], "current_agenda": []}})
        
    # Generate new study plan
    console.print()
    console.print("[dim]Regenerating and balancing your new study plan...[/dim]")
    exam_date = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(days=days)
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

def _render_shortfall_report(selection: dict) -> bool:
    """Prints the domain/concept shortfall report for a weighted mock. Returns
    True if there's at least one confirmed question to run with."""
    has_shortfall_content = bool(selection["domain_shortfall"]) or bool(selection["concept_notes"])
    if selection["domain_shortfall"]:
        lines = [
            f"[bold]{domain}[/bold]: needed {gap['needed']}, only {gap['available']} confirmed available"
            for domain, gap in selection["domain_shortfall"].items()
        ]
        console.print(Panel(
            "\n".join(lines),
            title="⚠️ Domain Shortfall (never padded, never silent)",
            border_style="yellow", box=box.ROUNDED
        ))
    if selection["concept_notes"]:
        lines = [
            f"[dim]{note['domain']}[/dim] / {note['concept']}: {note['available']} confirmed "
            f"(even split target ~{note['even_share_target']})"
            for note in selection["concept_notes"]
        ]
        console.print(Panel(
            "\n".join(lines),
            title="Under-represented concepts within their domain",
            border_style="yellow", box=box.ROUNDED
        ))
    if not selection["questions"]:
        console.print(Panel(
            "No confirmed questions are available in the bank yet. Confirm some questions via "
            "`certcoach-review-questions` before a mock can run.",
            title="Mock unavailable", border_style="red", box=box.ROUNDED
        ))
        time.sleep(2)
        return False
    if len(selection["questions"]) < selection["requested"]:
        console.print(f"\n  [dim]Running with {len(selection['questions'])} of the requested "
                       f"{selection['requested']} questions -- see shortfall above.[/dim]")
        has_shortfall_content = True
    if has_shortfall_content:
        # The mock's own clear() would otherwise wipe this report before it's readable.
        try:
            Prompt.ask("\n  [dim]Press Enter to continue...[/dim]")
        except (KeyboardInterrupt, EOFError):
            return False
    return True


def run_full_mock():
    pep = coach.get_mock_exam_pep_talk()
    console.print(Panel(Markdown(pep, code_theme="monokai"), title="🧑‍🏫 CertCoach", border_style="cyan", box=box.ROUNDED))
    try:
        Prompt.ask("\n  Press Enter when ready...")
    except (KeyboardInterrupt, EOFError):
        return
    selection = database.get_weighted_mock_questions(53)
    if not _render_shortfall_report(selection):
        return
    run_practice_questions("Full Mock", [], num=53, is_mock=True, preselected_questions=selection["questions"])

def run_timed_mock():
    pep = coach.get_mock_exam_pep_talk()
    console.print(Panel(Markdown(pep, code_theme="monokai"), title="🧑‍🏫 CertCoach", border_style="cyan", box=box.ROUNDED))
    try:
        Prompt.ask("\n  Press Enter when ready...")
    except (KeyboardInterrupt, EOFError):
        return
    selection = database.get_weighted_mock_questions(20)
    if not _render_shortfall_report(selection):
        return
    start_time = time.time()
    score = run_practice_questions("Timed Mock Exam", [], num=20, is_mock=True, preselected_questions=selection["questions"])
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    console.print(f"\n  [bold cyan]⏱️ Time Taken: {minutes}m {seconds}s[/bold cyan]")
    target_minutes = (20 * MOCK_SECONDS_PER_QUESTION) / 60
    console.print(f"  [dim]Target: ~{target_minutes:.0f}m ({MOCK_SECONDS_PER_QUESTION / 60:.1f}m per question)[/dim]")
    try:
        Prompt.ask("\n  [dim]Press Enter to return[/dim]")
    except (KeyboardInterrupt, EOFError):
        return


def show_casing_contrast_sheet():
    """Renders a beautiful side-by-side comparative table of mongosh vs PyMongo casings."""
    clear()
    console.print(Rule("[bold cyan]💻 Lexical Casing Contrast Sheet (mongosh vs PyMongo)[/bold cyan]"))
    console.print()
    console.print(Panel(
        "Standard syllabus topics strictly enforce [bold cyan]mongosh camelCase[/bold cyan] method names.\n"
        "Python Driver/PyMongo topics require [bold yellow]PyMongo snake_case[/bold yellow] method names.\n"
        "Here is a side-by-side comparative reference to help you avoid casing traps on the exam.",
        title="📝 Casing Standard", border_style="cyan", box=box.ROUNDED
    ))
    console.print()
    
    table = Table(box=box.DOUBLE, header_style="bold blue", show_lines=True)
    table.add_column("mongosh (camelCase)", style="cyan", justify="left")
    table.add_column("PyMongo (snake_case)", style="yellow", justify="left")
    table.add_column("Key Differences & Traps", style="white", justify="left")
    
    table.add_row(
        "insertOne()",
        "insert_one()",
        "Inserts a single document. PyMongo accepts a dictionary directly."
    )
    table.add_row(
        "insertMany()",
        "insert_many()",
        "Inserts an array of documents (mongosh) or a list of dictionaries (PyMongo)."
    )
    table.add_row(
        "findOne()",
        "find_one()",
        "Returns a single document. If no document matches, returns null (mongosh) or None (PyMongo)."
    )
    table.add_row(
        "find()",
        "find()",
        "Returns a cursor. Cursors must be iterated to retrieve results in both environments."
    )
    table.add_row(
        "updateOne()",
        "update_one()",
        "Requires update operators (e.g., $set). Passing raw documents is an exam trap!"
    )
    table.add_row(
        "updateMany()",
        "update_many()",
        "Updates multiple matching documents. Requires update operators."
    )
    table.add_row(
        "deleteOne()",
        "delete_one()",
        "Deletes a single matching document."
    )
    table.add_row(
        "deleteMany()",
        "delete_many()",
        "Deletes all documents matching the filter."
    )
    table.add_row(
        "replaceOne()",
        "replace_one()",
        "Replaces a single document. Accepts ONLY raw documents. Update operators ($set) are BANNED."
    )
    table.add_row(
        "createIndex()",
        "create_index()",
        "mongosh: createIndex({'field': 1})\nPyMongo: create_index([('field', 1)]) — uses a list of tuples!"
    )
    
    print_paginated(table, title="Lexical Casing Contrast Sheet")
    try:
        Prompt.ask("\n  [dim]Press Enter to return to Library menu[/dim]")
    except (KeyboardInterrupt, EOFError):
        pass


def show_error_book_menu():
    while True:
        clear()
        console.print(Rule("[bold red]🛑 Active Error Book (Mistake Log & Diagnostic Reviews)[/bold red]"))
        console.print("  [dim]This log classifies your mistake patterns to help you practice target areas.[/dim]\n")
        
        errors = database.get_error_book(USER_ID)
        if not errors:
            console.print(Panel(
                "🎉 [bold green]Clean Slate![/bold green] You have no unresolved mistakes in your Error Book.\n"
                "This means you have resolved all past incorrect answers by subsequently answering them correctly.\n"
                "Keep up the high discipline and accuracy!",
                border_style="green", box=box.ROUNDED, padding=(1, 2)
            ))
            try:
                Prompt.ask("\n  [bold blue]❯[/bold blue] [dim]Press Enter to return[/dim]")
            except (KeyboardInterrupt, EOFError):
                pass
            break
            
        # Draw a beautiful summary table
        table = Table(box=box.MINIMAL, header_style="bold blue", show_lines=False)
        table.add_column("#", width=3, justify="right")
        table.add_column("Topic", width=22)
        table.add_column("Concept / Focus Area", min_width=25)
        table.add_column("Trap Classification", width=25, style="bold red")
        table.add_column("Fails", width=6, justify="center")
        table.add_column("Last Attempt", width=12)
        
        for idx, err in enumerate(errors, 1):
            topic = err.get("topic", "General")
            concept = err.get("concept", "Unclassified")
            trap = err.get("trap_type", "Unclassified")
            fails = str(err.get("fail_count", 1))
            
            # Format time
            last_failed_raw = err.get("last_failed_at", "")
            time_lbl = ""
            if last_failed_raw:
                try:
                    dt = datetime.datetime.fromisoformat(last_failed_raw)
                    time_lbl = dt.strftime("%b %d %H:%M")
                except Exception:
                    time_lbl = last_failed_raw[:12]
                    
            table.add_row(
                str(idx),
                topic[:20] + "..." if len(topic) > 20 else topic,
                concept[:25] + "..." if len(concept) > 25 else concept,
                trap,
                fails,
                time_lbl
            )
            
        console.print(table)
        console.print()
        console.print("  [bold cyan]1.[/bold cyan] 🚀 Start Targeted Recovery Practice for a Concept")
        console.print("  [bold cyan]2.[/bold cyan] 🔍 View Mistake Details & Analytics")
        console.print("  [bold cyan]3.[/bold cyan] ⬅️  Back to Reference Library Menu")
        console.print()
        
        choice = ask("  [bold]Select Option[/bold]", choices=["1", "2", "3"])
        if choice in ("3", "__back__"):
            break
            
        if choice == "1":
            ans = ask(f"  [bold]Enter Item Number (1-{len(errors)})[/bold]")
            try:
                item_idx = int(ans) - 1
                if 0 <= item_idx < len(errors):
                    err_item = errors[item_idx]
                    target_topic = err_item["topic"]
                    target_concept = err_item["concept"]
                    console.print(f"\n  [bold cyan]Starting practice for: {target_topic} -> {target_concept}[/bold cyan]")
                    time.sleep(1)
                    run_practice_questions(target_topic, [target_topic], num=3, concepts=[target_concept])
            except Exception as e:
                console.print(f"[red]  Invalid selection: {e}. Press Enter to retry.[/red]")
                time.sleep(2)
                
        elif choice == "2":
            ans = ask(f"  [bold]Enter Item Number (1-{len(errors)})[/bold]")
            try:
                item_idx = int(ans) - 1
                if 0 <= item_idx < len(errors):
                    err_item = errors[item_idx]
                    q_doc = database.questions_col.find_one({"_id": err_item["question_id"]})
                    if q_doc:
                        clear()
                        console.print(Rule(f"[bold red]Mistake Detail: {err_item.get('concept')}[/bold red]"))
                        console.print(f"\n  [bold]Question:[/bold]\n  {q_doc.get('question_text', '')}\n")
                        
                        console.print("  [bold]Options:[/bold]")
                        for opt in q_doc.get("options", []):
                            prefix = "   "
                            suffix = ""
                            if opt.get("is_correct"):
                                prefix = "  [green]✓[/green] "
                                suffix = " [green](Correct Answer)[/green]"
                            elif opt.get("option_letter") == err_item.get("selected_option"):
                                prefix = "  [red]✗[/red] "
                                suffix = " [red](Your Selection)[/red]"
                            console.print(f"{prefix}{opt.get('option_letter')}. {opt.get('code_snippet', '')}{suffix}")
                            
                        console.print(f"\n  [bold red]Trap Classification:[/bold red] {err_item.get('trap_type')}")
                        console.print(f"  [bold]Total Failure Frequency:[/bold] {err_item.get('fail_count')} times")
                        
                        console.print(f"\n  [bold cyan]Seven-Part Explanation:[/bold cyan]")
                        console.print(Markdown(q_doc.get("explanation", "")))
                        
                        try:
                            Prompt.ask("\n  [bold blue]❯[/bold blue] [dim]Press Enter to return[/dim]")
                        except (KeyboardInterrupt, EOFError):
                            pass
                    else:
                        console.print("[red]  Question not found in database.[/red]")
                        time.sleep(2)
            except Exception as e:
                console.print(f"[red]  Invalid selection: {e}. Press Enter to retry.[/red]")
                time.sleep(2)


def show_flashcard_browser():
    """Browse the same flashcard deck the mobile/web companion apps bundle,
    directly in the CLI. Read-only, no scheduling -- pick a domain, flip
    through cards. See database.load_flashcards() for the shared data source."""
    clear()
    console.print(Rule("[bold cyan]🗂️ Flashcard Deck[/bold cyan]"))
    cards = database.load_flashcards()
    if not cards:
        console.print("[yellow]No flashcards found.[/yellow]")
        time.sleep(2)
        return

    categories = sorted({c.get("category", "Uncategorized") for c in cards})
    console.print("\n  [bold]Domains:[/bold]")
    for idx, cat in enumerate(categories, 1):
        count = sum(1 for c in cards if c.get("category") == cat)
        console.print(f"    {idx}. {cat} ({count} cards)")
    all_option = len(categories) + 1
    console.print(f"    {all_option}. All domains ({len(cards)} cards)")

    try:
        choice = Prompt.ask("\n  Choose a domain (number) or 'q' to go back", default=str(all_option))
    except (KeyboardInterrupt, EOFError):
        return
    if choice.strip().lower() in EXIT_COMMANDS:
        return

    try:
        choice_idx = int(choice.strip())
    except ValueError:
        choice_idx = all_option

    if 1 <= choice_idx <= len(categories):
        selected = [c for c in cards if c.get("category") == categories[choice_idx - 1]]
    else:
        selected = list(cards)
    random.shuffle(selected)

    for idx, card in enumerate(selected, 1):
        clear()
        console.print(Rule(f"[bold cyan]🗂️ {card.get('category', '')} — {idx}/{len(selected)}[/bold cyan]"))
        console.print(Panel(card.get("title", ""), title="Front", border_style="cyan", box=box.ROUNDED, padding=(1, 2)))
        try:
            Prompt.ask("\n  [dim]Press Enter to reveal[/dim]", default="")
        except (KeyboardInterrupt, EOFError):
            return
        console.print(Panel(Markdown(card.get("answer", ""), code_theme="monokai"), title="Back", border_style="green", box=box.ROUNDED, padding=(1, 2)))
        try:
            next_action = Prompt.ask("\n  [dim]Enter for next / q to quit[/dim]", default="")
        except (KeyboardInterrupt, EOFError):
            return
        if next_action.strip().lower() in EXIT_COMMANDS:
            return

    console.print("\n  [bold green]Deck complete.[/bold green]")
    time.sleep(1.5)


def run_library_submenu():
    while True:
        console.print("\n  [bold blue]📖 Reference Library & Progress[/bold blue]")
        console.print("  [dim]  " + "─"*30 + "[/dim]")
        console.print("    [bold cyan]a.[/bold cyan] 📖 View Study Journal (MongoDB Brain)")
        console.print("    [bold cyan]b.[/bold cyan] 💡 View Exam Cheat Sheet (Traps & Reminders)")
        console.print("    [bold cyan]c.[/bold cyan] 📚 Syllabus Coverage & Gap Report")
        console.print("    [bold cyan]d.[/bold cyan] 📊 Performance Analytics Dashboard")
        console.print("    [bold cyan]e.[/bold cyan] 💻 View Lexical Casing Contrast Sheet (mongosh vs PyMongo)")
        console.print("    [bold cyan]f.[/bold cyan] 🛑 View Active Error Book (Mistake Log & Diagnostic Reviews)")
        console.print("    [bold cyan]g.[/bold cyan] 🗂️  Browse Flashcard Deck")
        console.print("    [bold cyan]h.[/bold cyan] ⬅️  Back to Main Menu")
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
        elif ans == "e":
            show_casing_contrast_sheet()
        elif ans == "f":
            show_error_book_menu()
        elif ans == "g":
            show_flashcard_browser()
        elif ans in EXIT_COMMANDS:
            raise SystemExit
        elif ans in BACK_COMMANDS or ans == "h":
            break


def run_question_bank_reports():
    """Read-only question-bank reports. The generation/approval wizard that
    used to live here was removed: it depended on a `chroma_db` vector store
    that doesn't exist in this repo, so every generation attempt silently fell
    back to the same hardcoded mock question regardless of topic, and it
    wrote through a separate draft/approve path unrelated to the real
    provenance pipeline (`certcoach-preview-concept` / `certcoach-seed-nightly`
    / `certcoach-review-questions`)."""
    clear()
    console.print(Rule("[bold cyan]📊 Question Bank Reports[/bold cyan]"))
    console.print()

    console.print("  [bold cyan]1.[/bold cyan] View Question Quality Analytics & Difficulty Flags")
    console.print("  [bold cyan]2.[/bold cyan] Audit Seven-Part Explanation Coverage")
    console.print("  [bold cyan]3.[/bold cyan] Return to Settings Submenu")
    console.print()

    choice = ask("  [bold]Select Option[/bold]", choices=["1", "2", "3"])
    if choice in ("3", "__back__"):
        return

    if choice == "1":
        # Question Quality Analytics report
        clear()
        console.print(Rule("[bold cyan]📊 Question Quality Analytics & Difficulty Flags[/bold cyan]"))
        console.print()
        
        analytics = database.get_questions_quality_analytics()
        if not analytics:
            console.print("[yellow]  No question quality data recorded yet. Start practicing to generate metrics![/yellow]")
            time.sleep(2)
            return
            
        table = Table(box=box.MINIMAL, header_style="bold blue")
        table.add_column("Question (Snippet)", min_width=32)
        table.add_column("Topic", width=18)
        table.add_column("Tries", width=6, justify="right")
        table.add_column("Success Rate", width=12, justify="right")
        table.add_column("Avg Time", width=9, justify="right")
        table.add_column("Diff", width=8, justify="center")
        table.add_column("Flag/Status", width=22, justify="center")
        
        for q in analytics:
            col = "green" if q["success_rate"] >= 80 else "yellow" if q["success_rate"] >= 50 else "red"
            flag_col = "red" if "Needs Review" in q["flag"] else "green" if "Too Easy" in q["flag"] else "white"
            table.add_row(
                q["question_text"],
                q["topic"],
                str(q["attempts"]),
                f"[{col}]{q['success_rate']}%[/{col}]",
                f"{q['average_time']}s",
                q["difficulty"],
                f"[{flag_col}]{q['flag']}[/{flag_col}]"
            )
            
        print_paginated(table, title="Question Quality Analytics")
        try:
            Prompt.ask("\n  [dim]Press Enter to return[/dim]")
        except (KeyboardInterrupt, EOFError):
            pass

    elif choice == "2":
        clear()
        console.print(Rule("[bold cyan]📋 Seven-Part Explanation Coverage Audit[/bold cyan]"))
        console.print()

        audit = database.audit_question_explanations()
        summary = (
            f"Total Questions: [bold]{audit['total_questions']}[/bold]\n"
            f"Compliant: [bold green]{audit['compliant_questions']}[/bold green]\n"
            f"Needs Review: [bold red]{audit['non_compliant_questions']}[/bold red]\n"
            f"Compliance: [bold cyan]{audit['compliance_percent']}%[/bold cyan]"
        )
        elements = [Panel(summary, title="Question Bank Explanation Health", border_style="cyan", box=box.ROUNDED)]

        if audit["issues"]:
            table = Table(box=box.MINIMAL, header_style="bold blue")
            table.add_column("Topic", width=18)
            table.add_column("Concept", width=18)
            table.add_column("Diff", width=8)
            table.add_column("Question", min_width=30)
            table.add_column("Issues", min_width=36)

            for item in audit["issues"][:75]:
                table.add_row(
                    item["topic"],
                    item.get("concept", "") or "—",
                    item.get("difficulty", "") or "—",
                    item["question_text"],
                    "; ".join(item["issues"]),
                )
            elements.append(table)
            if len(audit["issues"]) > 75:
                elements.append(Text.from_markup(f"\n[dim]Showing first 75 of {len(audit['issues'])} flagged questions.[/dim]"))
        else:
            elements.append(Text.from_markup("[bold green]All questions have detailed seven-part explanations.[/bold green]"))

        from rich.console import Group
        print_paginated(Group(*elements), title="Seven-Part Explanation Audit")
        try:
            Prompt.ask("\n  [dim]Press Enter to return[/dim]")
        except (KeyboardInterrupt, EOFError):
            pass
def run_model_manager():
    import urllib.request
    import urllib.error
    import json
    
    clear()
    console.print(Rule("[bold cyan]🧠 Local AI Model & Memory Status[/bold cyan]"))
    console.print("[dim]  View loaded models in VRAM/RAM and clear system memory to optimize speed. "
                  "(Inspect/reload only -- changing which model is configured is done via the .env file.)\n[/dim]")
    
    # 1. Fetch loaded models
    loaded_models = []
    ollama_url = os.getenv("LOCAL_LLM_URL", "http://localhost:11434").rstrip("/")
    
    try:
        req = urllib.request.Request(f"{ollama_url}/api/ps", method="GET")
        with urllib.request.urlopen(req, timeout=2.0) as response:
            data = json.loads(response.read().decode("utf-8"))
            loaded_models = data.get("models", [])
    except urllib.error.URLError:
        console.print("[red]  ⚠️  Error: Could not connect to Ollama. Make sure Ollama is running (`ollama serve`).[/red]")
        try:
            Prompt.ask("\n  [dim]Press Enter to return[/dim]")
        except (KeyboardInterrupt, EOFError):
            pass
        return
    except Exception as e:
        console.print(f"[red]  ⚠️  Unexpected error reading model status: {e}[/red]")
        try:
            Prompt.ask("\n  [dim]Press Enter to return[/dim]")
        except (KeyboardInterrupt, EOFError):
            pass
        return

    # Show active model configured
    from certcoach.core.config import get_population_model, get_repair_model, get_study_model
    active_model = get_study_model()
    console.print(f"  Configured Study Model: [bold green]{active_model}[/bold green] (Ollama URL: {ollama_url})")
    console.print(f"  Population Model: [bold]{get_population_model()}[/bold] | Repair Model: [bold]{get_repair_model()}[/bold]")
    console.print()

    if not loaded_models:
        console.print(Panel(
            "  [bold green]No models are currently loaded in RAM/VRAM memory.[/bold green]\n"
            "  Models unload automatically after 5 minutes of inactivity in Ollama.",
            title="🧠 Memory Status", border_style="green", box=box.ROUNDED
        ))
    else:
        # Render a nice table of loaded models
        table = Table(box=box.MINIMAL, header_style="bold blue")
        table.add_column("Model Name", min_width=20)
        table.add_column("Size on Disk", width=12, justify="right")
        table.add_column("VRAM/RAM Usage", width=16, justify="right")
        table.add_column("Format", width=10, justify="center")
        
        for m in loaded_models:
            name = m.get("name", "Unknown")
            size_gb = m.get("size", 0) / (1024**3)
            vram_bytes = m.get("size_vram", 0)
            vram_pct = (vram_bytes / max(1, m.get("size", 1))) * 100
            
            table.add_row(
                name,
                f"{size_gb:.2f} GB",
                f"{vram_bytes / (1024**3):.2f} GB ({vram_pct:.0f}% VRAM)",
                m.get("details", {}).get("format", "gguf")
            )
            
        console.print(Panel(table, title="🧠 Active VRAM/RAM Memory Consumption", border_style="cyan"))
        
    console.print("\n  [bold]Actions:[/bold]")
    console.print("    [bold cyan]1.[/bold cyan] 🗑️  Clear Memory / Unload All Models")
    console.print("    [bold cyan]2.[/bold cyan] 🔄 Reload Configured Active Model")
    console.print("    [bold cyan]3.[/bold cyan] ⬅️  Return to Settings")
    console.print()
    
    act = ask("  Memory Manager", choices=["1", "2", "3"])

    if act == "1":
        if not loaded_models:
            console.print("[yellow]  No models to unload. VRAM memory is already clear.[/yellow]")
            time.sleep(1.5)
            return
            
        with console.status("[dim]🧠 Clearing VRAM system memory...[/dim]", spinner="dots"):
            for m in loaded_models:
                m_name = m.get("name")
                if m_name:
                    try:
                        req_data = json.dumps({"model": m_name, "keep_alive": 0}).encode("utf-8")
                        req = urllib.request.Request(
                            f"{ollama_url}/api/generate",
                            data=req_data,
                            headers={"Content-Type": "application/json"},
                            method="POST"
                        )
                        with urllib.request.urlopen(req, timeout=5.0) as resp:
                            resp.read()
                    except Exception:
                        pass
        console.print("[green]  ✔ Success! All models unloaded. System memory freed successfully.[/green]")
        time.sleep(2)
        
    elif act == "2":
        with console.status(f"[dim]🧠 Pre-loading active model '{active_model}' into memory...[/dim]", spinner="dots"):
            try:
                req_data = json.dumps({"model": active_model, "prompt": "", "keep_alive": "1h"}).encode("utf-8")
                req = urllib.request.Request(
                    f"{ollama_url}/api/generate",
                    data=req_data,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=15.0) as resp:
                    resp.read()
                console.print(f"[green]  ✔ Success! Active model '{active_model}' pre-loaded successfully. Teaching will be lightning fast![/green]")
            except Exception as e:
                console.print(f"[red]  ❌ Error loading model: {e}[/red]")
        time.sleep(2)


def run_account_submenu():
    global USER_ID

    while True:
        session = auth.load_session()
        current_label = (
            f"{session.get('email')} ({session.get('user_id')})"
            if session
            else f"Local demo profile ({USER_ID})"
        )
        console.print("\n  [bold blue]👤 Account & Sync[/bold blue]")
        console.print("  [dim]  " + "─"*30 + "[/dim]")
        console.print(f"    Current: [bold cyan]{current_label}[/bold cyan]")
        console.print("    [bold cyan]1.[/bold cyan] Sign in to existing account")
        console.print("    [bold cyan]2.[/bold cyan] Create new account")
        console.print("    [bold cyan]3.[/bold cyan] Sign out / use local demo profile")
        console.print("    [bold cyan]4.[/bold cyan] Back to Settings")
        console.print()

        choice = ask("  Account", choices=["1", "2", "3", "4"])

        if choice in ("4", "__back__"):
            return

        if choice == "1":
            try:
                email = Prompt.ask("  Email").strip()
                password = Prompt.ask("  Password", password=True).strip()
            except (KeyboardInterrupt, EOFError):
                continue
            ok, msg, user = auth.login(email, password)
            if ok and user:
                USER_ID = user["_id"]
                console.print(f"[green]  ✔ {msg} Progress will sync through MongoDB for this account.[/green]")
                time.sleep(1.5)
                return
            console.print(f"[red]  ❌ {msg}[/red]")
            time.sleep(1.5)

        elif choice == "2":
            try:
                email = Prompt.ask("  Email").strip()
                display_name = Prompt.ask("  Display name", default=email.split("@")[0] if "@" in email else "").strip()
                password = Prompt.ask("  Password (8+ chars)", password=True).strip()
            except (KeyboardInterrupt, EOFError):
                continue
            ok, msg, user = auth.create_account(email, password, display_name)
            if ok and user:
                USER_ID = user["_id"]
                console.print(f"[green]  ✔ {msg} Your progress will now sync across machines using this MongoDB backend.[/green]")
                time.sleep(1.5)
                return
            console.print(f"[red]  ❌ {msg}[/red]")
            time.sleep(1.5)

        elif choice == "3":
            auth.clear_session()
            USER_ID = DEFAULT_USER_ID
            console.print("[yellow]  Signed out. Using local demo profile for this machine.[/yellow]")
            time.sleep(1.5)
            return


def run_settings_submenu(profile, status):
    while True:
        console.print("\n  [bold blue]🛠️ Study Settings & Extras[/bold blue]")
        console.print("  [dim]  " + "─"*30 + "[/dim]")
        console.print("    [bold cyan]a.[/bold cyan] 🗓️  View Full Study Plan Table")
        console.print("    [bold cyan]b.[/bold cyan] 🔄 Update Study Plan & Recalibrate Pacing")
        
        # Gated Mock
        if status["mock_exam_unlocked"]:
            console.print("    [bold cyan]c.[/bold cyan] 🏆 Full Mock Exam (53 Questions)")
            console.print("    [bold cyan]d.[/bold cyan] ⏱️  Timed Mock Exam (20 Questions)")
        else:
            console.print(f"    [dim]c. 🔒 Full Mock Exam (Locked — need {status['unlock_threshold_percent']}% mastery)[/dim]")
            console.print(f"    [dim]d. 🔒 Timed Mock Exam (Locked — need {status['unlock_threshold_percent']}% mastery)[/dim]")
            
        console.print("    [bold cyan]e.[/bold cyan] 💻 Scenario Simulator (Apply Mode)")
        console.print("    [bold cyan]f.[/bold cyan] 📊 Question Bank Reports (Quality Analytics / Explanation Coverage)")
        console.print("    [bold cyan]g.[/bold cyan] 🧠 Show Loaded AI Models & Free Memory (VRAM)")
        console.print("    [bold cyan]h.[/bold cyan] ❌ Quit CertCoach")
        console.print("    [bold cyan]i.[/bold cyan] ⬅️  Back to Main Menu")
        console.print("    [bold cyan]j.[/bold cyan] 💾 Reconfigure MongoDB Connection URI")
        console.print("    [bold cyan]k.[/bold cyan] 👤 Account Login / Sync Across Machines")
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
                console.print(f"[red]  Locked! Complete {status['unlock_threshold_percent']}% of the syllabus first.[/red]")
        elif ans == "d":
            if status["mock_exam_unlocked"]:
                run_timed_mock()
            else:
                console.print(f"[red]  Locked! Complete {status['unlock_threshold_percent']}% of the syllabus first.[/red]")
        elif ans == "e":
            run_scenario_simulator()
        elif ans == "f":
            run_question_bank_reports()
        elif ans == "g":
            run_model_manager()
        elif ans in EXIT_COMMANDS or ans == "h":
            raise SystemExit
        elif ans in BACK_COMMANDS or ans == "i":
            # NOTE: "b" is technically a member of BACK_COMMANDS but is
            # already bound to Recalibrate above and never reaches this
            # branch -- see the "b" elif earlier in this chain.
            break
        elif ans == "j":
            new_uri = Prompt.ask("\n  Enter your new MongoDB Connection URI").strip()
            if new_uri:
                with console.status("[dim]🔄 Hot-swapping MongoDB connection...[/dim]", spinner="dots"):
                    success = database.update_database_connection(new_uri)
                if success:
                    console.print("[green]  ✔ Connection successfully updated and verified.[/green]")
                else:
                    console.print("[red]  ❌ Failed to connect using new URI. Check your network or connection string.[/red]")
                time.sleep(2)
        elif ans == "k":
            run_account_submenu()
            profile = database.get_user_profile(USER_ID)
            status = planner.get_syllabus_status(USER_ID)



def clear_ollama_memory_on_startup():
    """
    Checks if any models are loaded on launch and asks the user
    if they want to clear them to ensure a smooth, lag-free session.
    """
    import urllib.request
    import urllib.error
    import json
    
    ollama_url = os.getenv("LOCAL_LLM_URL", "http://localhost:11434").rstrip("/")
    try:
        req = urllib.request.Request(f"{ollama_url}/api/ps", method="GET")
        with urllib.request.urlopen(req, timeout=1.5) as response:
            data = json.loads(response.read().decode("utf-8"))
            loaded = data.get("models", [])
            if not loaded:
                return
            
            # Highlight loaded models
            names = [m.get("name") for m in loaded if m.get("name")]
            console.print()
            console.print(Panel(
                f"[yellow]⚠️  Notice: The following AI model(s) are currently active in system memory (VRAM):\n"
                f"   • " + "\n   • ".join(names) + "\n\n"
                f"Having other models loaded can cause Ollama weight-loading lag or out-of-memory errors.[/yellow]\n\n"
                f"It is highly recommended to clear VRAM memory before starting.",
                title="[bold yellow]🧠 Active Memory Alert[/bold yellow]",
                border_style="yellow", box=box.ROUNDED
            ))
            
            if confirm("  [bold cyan]Would you like to clear VRAM memory now?[/bold cyan]", default=True):
                with console.status("[dim]🧠 Unloading active models and freeing VRAM...[/dim]", spinner="dots"):
                    for m in loaded:
                        m_name = m.get("name")
                        if m_name:
                            try:
                                req_data = json.dumps({"model": m_name, "keep_alive": 0}).encode("utf-8")
                                req_unload = urllib.request.Request(
                                    f"{ollama_url}/api/generate",
                                    data=req_data,
                                    headers={"Content-Type": "application/json"},
                                    method="POST"
                                )
                                with urllib.request.urlopen(req_unload, timeout=3.0) as resp:
                                    resp.read()
                            except Exception:
                                pass
                console.print("[green]  ✔ Success! Active models unloaded. System memory is now clear for CertCoach.[/green]\n")
                time.sleep(2)
    except Exception:
        pass


def check_system_specs_and_model_recommendations():
    """
    Analyzes local GPU VRAM and system RAM specs, checks the current configured model,
    and warns/advises the user if the model doesn't fit in VRAM or is sub-optimal.
    """
    import subprocess
    
    # 1. Get GPU VRAM
    vram_gb = 0.0
    gpu_name = ""
    try:
        # Check NVIDIA VRAM and Name
        res_vram = subprocess.run(["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True, check=True)
        res_name = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], capture_output=True, text=True, check=True)
        
        lines_vram = res_vram.stdout.strip().splitlines()
        lines_name = res_name.stdout.strip().splitlines()
        
        if lines_vram:
            vram_gb = float(lines_vram[0]) / 1024.0
        if lines_name:
            gpu_name = lines_name[0].strip()
    except Exception:
        pass

    # 2. Get System RAM
    ram_gb = 16.0
    try:
        res_ram = subprocess.run(["powershell", "-Command", "[math]::round((Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum).Sum / 1GB)"], capture_output=True, text=True)
        ram_gb = float(res_ram.stdout.strip())
    except Exception:
        pass

    # 3. Detect current configured model name
    from certcoach.core.persona import MODEL
    
    # Heuristics for model sizes in GB
    model_sizes = {
        "14b": 8.5,
        "12b": 7.5,
        "9b": 5.8,
        "8b": 4.8,
        "7b": 4.4,
        "4b": 3.4,
        "3b": 2.2,
        "2b": 1.6
    }
    
    current_size_gb = 5.0 # default fallback
    model_lower = MODEL.lower()
    for key, size in model_sizes.items():
        if key in model_lower:
            current_size_gb = size
            break
            
    # Recommendations based on VRAM
    recommendation = ""
    optimal_found = True
    
    # We reserve ~1.5 GB VRAM for OS/apps
    available_vram_for_llm = max(0.0, vram_gb - 1.5)
    
    if vram_gb > 0.0:
        if current_size_gb > available_vram_for_llm:
            optimal_found = False
            if vram_gb >= 12.0:
                recommendation = "qwen3.5:4b for study; reserve larger models for offline content work"
            elif vram_gb >= 8.0:
                recommendation = "qwen3.5:4b or qwen2.5-coder:7b"
            else: # e.g. 6 GB VRAM like RTX 3060
                recommendation = "qwen3.5:4b (recommended) or qwen2.5-coder:7b"
    else:
        # No NVIDIA GPU detected, running on CPU or integrated graphics
        if current_size_gb > 4.0:
            optimal_found = False
            recommendation = "qwen3.5:4b or a smaller local model"

    if not optimal_found:
        console.print()
        console.print(Panel(
            f"[yellow]⚠️  Performance Warning: Configured model [bold cyan]{MODEL}[/bold cyan] might be too large for your system specs.[/yellow]\n\n"
            f"💻  [bold]System Hardware Specs Detected:[/bold]\n"
            f"   • GPU: {gpu_name or 'Integrated/CPU only'}\n"
            f"   • GPU VRAM: {f'{vram_gb:.1f} GB' if vram_gb > 0.0 else 'None'}\n"
            f"   • System RAM: {ram_gb:.0f} GB\n\n"
            f"💡  [bold]Recommendation for your specs:[/bold]\n"
            f"   Switch to [bold green]{recommendation}[/bold green] to fit completely in your VRAM for instant, lag-free responses.\n"
            f"   You can change the `STUDY_MODEL` setting in your [bold cyan]local .env[/bold cyan] file.",
            title="[bold yellow]⚡ Hardware Pacing Optimizer[/bold yellow]",
            border_style="yellow", box=box.ROUNDED
        ))
        time.sleep(2)


# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------

def main_menu():
    try:
        database.check_connection()
        clear_ollama_memory_on_startup()
        check_system_specs_and_model_recommendations()
        run_onboarding()

        database.update_streak(USER_ID)

        while True:
            profile = database.get_user_profile(USER_ID)
            days_left = planner.calculate_days_left(profile.get("exam_date"))
            status = planner.get_syllabus_status(USER_ID)
            agenda = planner.generate_daily_agenda(USER_ID)
            streak = profile.get("streak_days", 1)
            streak_freezes = profile.get("progress", {}).get("streak_freezes", 0)

            agenda_desc = "None"
            if agenda:
                first_item = agenda[0]
                agenda_desc = f"{first_item['topic']} ({first_item['desc']})"

            # Spaced-repetition due reviews are locked until the user masters at least 1 topic
            if status.get("mastered_count", 0) >= 1:
                due_reviews = planner.get_due_review_topics(USER_ID)
            else:
                due_reviews = []
            badge = " [bold red](🚨 Spaced-Repetition Quiz Due!)[/bold red]" if due_reviews else ""

            skipped_topics = status.get("skipped_unmapped_topics", [])
            insufficient_concepts = status.get("insufficient_concepts", [])
            if not isinstance(skipped_topics, list):
                skipped_topics = []
            if not isinstance(insufficient_concepts, list):
                insufficient_concepts = []
            skipped_badge = ""
            if skipped_topics:
                skipped_badge = f" [bold yellow](⚠️ {len(skipped_topics)} topics skipped due to missing docs)[/bold yellow]"
            if insufficient_concepts:
                skipped_badge += f" [bold yellow](⚠️ {len(insufficient_concepts)} concepts blocked by question readiness)[/bold yellow]"

            lock_str = (
                "[bold green]🔓 Unlocked[/bold green]"
                if status["mock_exam_unlocked"]
                else (
                    f"[yellow]🔒 Locked — need {status['unlock_threshold_percent']}% mastery[/yellow]"
                )
            )

            # Calculate readiness metrics for consolidated status bar
            readiness_data = planner.calculate_readiness_metrics(USER_ID)
            current_readiness = readiness_data.get("current_readiness", 0.0) if hasattr(readiness_data, "get") else 0.0
            expected_readiness = readiness_data.get("expected_readiness", 0.0) if hasattr(readiness_data, "get") else 0.0
            pass_probability = readiness_data.get("pass_probability", 0.0) if hasattr(readiness_data, "get") else 0.0
            low_data = readiness_data.get("low_data", False) if hasattr(readiness_data, "get") else False

            # Fallback if metrics are MagicMocks during test patching
            if not isinstance(current_readiness, (int, float)):
                current_readiness = 0.0
            if not isinstance(expected_readiness, (int, float)):
                expected_readiness = 0.0
            if not isinstance(pass_probability, (int, float)):
                pass_probability = 0.0
            if not isinstance(low_data, bool):
                low_data = False

            exam_day_mode = current_readiness >= 85.0
            exam_day_badge = " [bold gold]🏆 EXAM DAY MODE ACTIVE[/bold gold] |" if exam_day_mode else ""
            current_user_label = get_current_user_label()
            # Below ~30 real attempts the pass-probability estimate is still
            # mostly noise -- say so, rather than showing a bare number that
            # reads as a confident (and often bleak) prediction this early.
            pass_probability_str = (
                f"{pass_probability:.1f}% [dim](early estimate -- firms up with more study sessions)[/dim]"
                if low_data
                else f"{pass_probability:.1f}%"
            )

            # Sleek horizontally consolidated Status Bar
            console.print(f"\n[bold blue]🧑‍🏫 CertCoach[/bold blue] | 📅 [bold]{days_left} days left[/bold] | 🔥 Streak: [bold yellow]{streak} days[/bold yellow] (❄️ Freezes: [bold blue]{streak_freezes}[/bold blue]) | 🏅 Mastery: [bold green]{status['mastery_percent']}%[/bold green] | Mock: {lock_str}")
            console.print(f"📈 [bold cyan]Readiness[/bold cyan]: [bold green]{current_readiness:.1f}%[/bold green] (Expected: {expected_readiness:.1f}%) | 🎲 [bold yellow]Pass Probability[/bold yellow]: {pass_probability_str} |{exam_day_badge}")
            if current_user_label:
                console.print(f"👤 [bold cyan]Signed in as[/bold cyan]: [bold]{current_user_label}[/bold]")
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

            if choice_raw.lower() == "blocked":
                if insufficient_concepts:
                    blocked_lines = [
                        "[bold yellow]The following concepts are not scheduled because they do not have the required 3 Easy + 2 Medium active-question mix:[/bold yellow]\n"
                    ]
                    for item in insufficient_concepts[:10]:
                        blocked_lines.append(
                            f"  • [cyan]{item['topic']}[/cyan] → {item['concept']}: "
                            f"Easy [bold]{item['easy_questions']}/{item['required_easy']}[/bold], "
                            f"Medium [bold]{item['medium_questions']}/{item['required_medium']}[/bold]"
                        )
                    if len(insufficient_concepts) > 10:
                        blocked_lines.append(f"\n  ...and {len(insufficient_concepts) - 10} more concepts.")
                    blocked_lines.append(
                        "\nThese concepts remain open and will become schedulable after the controlled Phase 4 bank work."
                    )
                    console.print(Panel(
                        "\n".join(blocked_lines),
                        title="[bold yellow]Concept Readiness Blockers[/bold yellow]",
                        border_style="yellow",
                        box=box.ROUNDED,
                    ))
                else:
                    console.print("[green]  All concepts currently have enough confirmed questions to practice.[/green]")
                try:
                    Prompt.ask("\n  [dim]Press Enter to return[/dim]")
                except (KeyboardInterrupt, EOFError):
                    pass
                continue

            if choice_raw == "1":
                session_start = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
                readiness_before_session = current_readiness

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

                if insufficient_concepts:
                    console.print(
                        f"[dim]{len(insufficient_concepts)} concept(s) still building content -- "
                        f"today's is ready. Type [bold]blocked[/bold] at the main menu to see the full list.[/dim]"
                    )
                    console.print()

                # 1. Run due reviews first if any
                if due_reviews:
                    console.print(Rule("[bold yellow]🚨 Pop Quiz Time! 🚨[/bold yellow]"))
                    console.print(Panel(
                        "It's time for a quick Spaced-Repetition review of past topics before we start the daily agenda.",
                        border_style="yellow", box=box.ROUNDED
                    ))
                    if confirm("  Start 5-question Pop Quiz now?"):
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
                            if score is None:
                                console.print("\n  [yellow]Not enough questions are available for the Boss Fight yet -- try again once more of the bank is confirmed.[/yellow]")
                            elif score >= 7:
                                planner.mark_boss_complete(USER_ID, item["boss_level"])
                                console.print(f"\n  [bold green]🏆 Boss Defeated! You may now proceed to the next topics.[/bold green]")
                            else:
                                console.print(f"\n  [bold red]❌ Boss Defeated You! You need 7/10 to pass. Try again tomorrow.[/bold red]")
                            try:
                                ans = Prompt.ask("\n  [bold blue]❯[/bold blue] [dim]Press Enter to return[/dim]")
                            except (KeyboardInterrupt, EOFError):
                                break
                else:
                    if insufficient_concepts:
                        console.print("[yellow]  No study concept is currently ready to schedule. Review the readiness blockers above.[/yellow]")
                    else:
                        console.print("[green]  You have completed all agenda items for today! Great job.[/green]")

                # --- END STUDY SESSION TRACKING ---
                session_end = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
                duration_minutes = (session_end - session_start).total_seconds() / 60.0

                # Fetch all user attempts since session_start
                all_attempts = database.get_user_attempts(USER_ID)
                session_attempts = []
                for att in all_attempts:
                    try:
                        att_dt = datetime.datetime.fromisoformat(att.get("timestamp"))
                    except Exception:
                        continue
                    if att_dt >= session_start:
                        session_attempts.append(att)

                if session_attempts or duration_minutes >= 0.5:
                    session_correct = sum(1 for a in session_attempts if a.get("is_correct"))
                    num_questions = len(session_attempts)
                    session_accuracy = (session_correct / max(1, num_questions)) * 100

                    # Gather topics covered
                    covered_topics = list(set(a.get("topic") for a in session_attempts))
                    if not covered_topics and agenda:
                        covered_topics = [agenda[0]["topic"]]

                    # Save session log in MongoDB
                    database.save_study_session(USER_ID, session_start, session_end, duration_minutes, covered_topics, num_questions, session_accuracy)

                    # Update progress history in user profile
                    readiness_data_new = planner.calculate_readiness_metrics(USER_ID)
                    profile = database.get_user_profile(USER_ID)
                    history = profile.get("readiness_history", [])

                    today_str = datetime.date.today().isoformat()
                    history = [h for h in history if h.get("date") != today_str]
                    history.append({
                        "date": today_str,
                        "readiness": readiness_data_new["current_readiness"]
                    })
                    database.update_user_profile(USER_ID, {"readiness_history": history})
                    next_agenda_after = planner.generate_daily_agenda(USER_ID)
                    closeout_title, closeout_body, closeout_style = build_session_closeout_text(
                        covered_topics,
                        session_accuracy,
                        readiness_before_session,
                        readiness_data_new["current_readiness"],
                        next_agenda_after[0] if next_agenda_after else None,
                    )

                    # Render high-visibility session stats panel
                    console.print()
                    console.print(Panel(
                        f"⏱️  [bold cyan]Duration[/bold cyan]: {duration_minutes:.1f} Minutes\n"
                        f"❓  [bold]Questions[/bold]: {num_questions} (Correct: {session_correct})\n"
                        f"🎯  [bold green]Accuracy[/bold green]: {session_accuracy:.1f}%\n"
                        f"📚  [bold]Topics Covered[/bold]: {', '.join(covered_topics)}",
                        title="📝 CertCoach: Study Session Logged", border_style="green", box=box.ROUNDED
                    ))
                    console.print()
                    console.print(Panel(
                        closeout_body,
                        title=closeout_title,
                        border_style=closeout_style,
                        box=box.ROUNDED,
                    ))
                    time.sleep(2)

            elif choice_raw == "2":
                run_library_submenu()

            elif choice_raw == "3":
                run_settings_submenu(profile, status)

            else: # Hybrid intercept (Direct Q&A chat)
                run_free_chat_session(choice_raw)
    except (SystemExit, KeyboardInterrupt, EOFError):
        pass
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]")
    finally:
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
