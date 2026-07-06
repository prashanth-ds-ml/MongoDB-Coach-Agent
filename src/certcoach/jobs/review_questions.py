"""One-at-a-time confirm/suspect review screen for the provenance queue.

This is the actual trust mechanism: a question generated (or backfilled) as
`draft`/`sourced` is shown next to its citation, and a human decides whether
it's correct. No question reaches practice, a mock, or spaced repetition
without living through this screen -- see `database.is_practice_ready`.

Deliberately one question at a time, not a batch table: reviewing a table of
N questions at once turns confirmation into rubber-stamping, which defeats
the whole point (the review IS the fact-check).
"""
from __future__ import annotations

import argparse
import os
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

from certcoach.core import database

console = Console()

USER_ID = "local_user_1"

_HERE = os.path.dirname(os.path.abspath(__file__))
_SOURCE_DIRS = ("cleaned_markdowns", "pics_qa_transcripts")


def _doc_absolute_path(doc_file: str) -> str | None:
    """Resolve doc_file to an absolute path under any of the citable source
    dirs, checked in the same order as database.verify_citation."""
    if not doc_file:
        return None
    for source_dir in _SOURCE_DIRS:
        candidate = os.path.join(_HERE, "..", "data", source_dir, doc_file)
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    return None


def _clickable_doc_link(doc_file: str) -> str:
    """Render doc_file as a terminal hyperlink (OSC 8, via Rich's [link=]
    markup) pointing at the local file, so a terminal that supports clickable
    links (e.g. Windows Terminal) can open it directly -- same idea as a
    clickable source URL, just for a local path instead of a website."""
    abs_path = _doc_absolute_path(doc_file)
    if not abs_path:
        return doc_file or "(none on record)"
    file_uri = "file:///" + abs_path.replace("\\", "/")
    return f"[link={file_uri}]{doc_file}[/link]"


def render_question(question: dict) -> None:
    metadata = question.get("metadata", {}) or {}
    provenance = question.get("provenance", {}) or {}
    citation = provenance.get("citation", {}) or {}

    header = (
        f"Topic {metadata.get('topic_id', '?')} | {metadata.get('concept', 'Unknown concept')} | "
        f"{metadata.get('difficulty', '?')} | {metadata.get('response_type', 'single')}"
    )
    console.print(Panel(header, border_style="cyan", box=box.ROUNDED))

    console.print(Panel(question.get("question_text", ""), title="Question", border_style="bright_black", box=box.ROUNDED))

    for opt in question.get("options", []):
        letter = opt.get("option_letter", "?")
        marker = "[bold green]<- marked correct[/bold green]" if opt.get("is_correct") else ""
        console.print(f"  {letter}) {opt.get('code_snippet', '')}  {marker}")

    explanation = question.get("explanation", "")
    if explanation:
        # Full seven-part explanation, rendered as Markdown (not truncated) --
        # a reviewer fact-checking the question needs every section, including
        # the Exam Trap/Memory Hook/Practice Recommendation/Syntax Example
        # parts that a fixed character cutoff used to silently drop.
        console.print(Panel(Markdown(explanation, code_theme="monokai"), title="Explanation", border_style="dim", box=box.ROUNDED))

    doc_file = citation.get("doc_file", "")
    quote = citation.get("quote", "")
    verified, msg = database.verify_citation(question)

    verify_style = "green" if verified else "yellow"
    console.print(Panel(
        f"[bold]Source file:[/bold] {_clickable_doc_link(doc_file)}\n"
        f"[bold]Cited quote:[/bold] \"{quote}\"" + ("" if quote else " (none on record)") + "\n"
        f"[bold]Deterministic check:[/bold] [{verify_style}]{msg}[/{verify_style}]",
        title="Citation", border_style=verify_style, box=box.ROUNDED
    ))


def run_review_session(topic_id: int | None = None, limit: int = 50) -> dict:
    stats = {"confirmed": 0, "suspect": 0, "skipped": 0}
    queue = database.get_questions_for_review(limit=limit, topic_id=topic_id)
    total_remaining = database.count_questions_for_review(topic_id=topic_id)

    if not queue:
        console.print("[green]Nothing waiting for review.[/green]")
        return stats

    console.print(f"[bold]{total_remaining} question(s) awaiting review.[/bold] Showing up to {limit} this session.\n")

    for i, question in enumerate(queue, 1):
        console.print(f"\n[dim]--- {i}/{len(queue)} this session ---[/dim]")
        render_question(question)

        citation_verified, _ = database.verify_citation(question)
        if citation_verified:
            prompt_label = "\n  [bold]Decision[/bold] [C]onfirm / [S]uspect / s[K]ip / [Q]uit"
            allowed_choices = ["c", "s", "k", "q"]
        else:
            console.print(
                "[yellow]Citation check failed -- Confirm is unavailable. "
                "Mark Suspect or fix the citation and re-run.[/yellow]"
            )
            prompt_label = "\n  [bold]Decision[/bold] [S]uspect / s[K]ip / [Q]uit"
            allowed_choices = ["s", "k", "q"]

        try:
            choice = Prompt.ask(
                prompt_label,
                choices=allowed_choices,
                default="k",
            ).lower()
        except (KeyboardInterrupt, EOFError):
            break

        if choice == "q":
            break
        elif choice == "c":
            database.confirm_question(question["_id"], USER_ID)
            stats["confirmed"] += 1
            console.print("[green]Confirmed.[/green]")
        elif choice == "s":
            try:
                reason = Prompt.ask("  Reason (one line)")
            except (KeyboardInterrupt, EOFError):
                reason = ""
            database.mark_question_suspect(question["_id"], reason)
            stats["suspect"] += 1
            console.print("[yellow]Marked suspect.[/yellow]")
        else:
            stats["skipped"] += 1

    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="One-at-a-time confirm/suspect review for questions awaiting provenance decisions.")
    parser.add_argument("--topic", type=int, default=None, help="Restrict review to one topic_id.")
    parser.add_argument("--limit", type=int, default=50, help="Max questions to review this session.")
    args = parser.parse_args(argv)

    database.check_connection()
    stats = run_review_session(topic_id=args.topic, limit=args.limit)

    console.print(
        f"\n[bold]Session summary:[/bold] {stats['confirmed']} confirmed, "
        f"{stats['suspect']} marked suspect, {stats['skipped']} skipped."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
