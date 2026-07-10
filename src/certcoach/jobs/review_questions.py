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


def render_citation_panel(question: dict) -> Panel:
    """The doc-file link, cited quote in its source paragraph, and the
    deterministic verify message, as a standalone Panel -- shared by the
    review screen and the CLI's live review-quiz mode."""
    citation = (question.get("provenance", {}) or {}).get("citation", {}) or {}
    doc_file = citation.get("doc_file", "")
    excerpt = database.get_citation_excerpt(question)
    verified, msg = excerpt["verified"], excerpt["message"]

    verify_style = "green" if verified else "yellow"
    if excerpt["excerpt_before"] or excerpt["excerpt_after"]:
        # Quote located in its own source paragraph -- same contextual view
        # Docket shows, instead of just the bare quote string.
        quote_display = (
            f"[dim]{excerpt['excerpt_before']}[/dim]"
            f"[bold {verify_style}]{excerpt['excerpt_match']}[/bold {verify_style}]"
            f"[dim]{excerpt['excerpt_after']}[/dim]"
        )
    else:
        quote_display = f"\"{excerpt['quote']}\"" if excerpt["quote"] else "(none on record)"

    return Panel(
        f"[bold]Source file:[/bold] {_clickable_doc_link(doc_file)}\n\n"
        f"[bold]Cited quote in context:[/bold]\n{quote_display}\n\n"
        f"[bold]Deterministic check:[/bold] [{verify_style}]{msg}[/{verify_style}]",
        title="Citation", border_style=verify_style, box=box.ROUNDED
    )


def render_question(question: dict) -> None:
    metadata = question.get("metadata", {}) or {}

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

    console.print(render_citation_panel(question))


def render_legacy_reference(topic_id: int | None, concept: str | None) -> None:
    """Read-only panel of old-bank `suspect` questions already mapped to this
    same topic/concept, for context while reviewing fresh ones -- never an
    actionable confirm/suspect target, matching Docket's legacy panel."""
    legacy = database.get_legacy_reference_questions(topic_id, concept)
    if not legacy:
        return
    lines = [f"[dim]{q.get('question_text', '')}[/dim]" for q in legacy]
    console.print(Panel(
        "\n\n".join(lines),
        title=f"Legacy reference ({len(legacy)}) -- not actionable, for context only",
        border_style="bright_black", box=box.ROUNDED,
    ))


def run_review_session(topic_id: int | None = None, concept: str | None = None, limit: int = 50) -> dict:
    stats = {"confirmed": 0, "suspect": 0, "skipped": 0}
    queue = database.get_questions_for_review(limit=limit, topic_id=topic_id, concept=concept)
    total_remaining = database.count_questions_for_review(topic_id=topic_id, concept=concept)

    if not queue:
        console.print("[green]Nothing waiting for review.[/green]")
        return stats

    console.print(f"[bold]{total_remaining} question(s) awaiting review.[/bold] Showing up to {limit} this session.\n")

    for i, question in enumerate(queue, 1):
        console.print(f"\n[dim]--- {i}/{len(queue)} this session ---[/dim]")
        render_question(question)
        q_meta = question.get("metadata", {}) or {}
        render_legacy_reference(q_meta.get("topic_id"), q_meta.get("concept"))

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
                case_sensitive=False,
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
    parser.add_argument("--concept", default=None, help="Restrict review to one concept (requires --topic).")
    parser.add_argument("--limit", type=int, default=50, help="Max questions to review this session.")
    args = parser.parse_args(argv)

    database.check_connection()
    stats = run_review_session(topic_id=args.topic, concept=args.concept, limit=args.limit)

    console.print(
        f"\n[bold]Session summary:[/bold] {stats['confirmed']} confirmed, "
        f"{stats['suspect']} marked suspect, {stats['skipped']} skipped."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
