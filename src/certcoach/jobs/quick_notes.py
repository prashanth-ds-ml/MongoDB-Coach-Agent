"""Standalone companion command (`certcoach-notes`) meant to run in a second
terminal alongside the main `certcoach` session. Lets the learner jot down a
freeform note the moment something's worth remembering -- a trap they nearly
missed, a fact worth a cheat-sheet entry -- without pausing the main app or
navigating its menus. Notes are timestamped and saved immediately, one per
line, and are separate from `add_question_review_note` (which is tied to a
specific question and meant to flag content for improvement, not personal
study notes).

View saved notes from the main app's Library menu ("My Notes"), or here by
running with `--view`.
"""
from __future__ import annotations

import argparse

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

from certcoach.core import auth, database

console = Console()


def run_capture_loop(user_id: str) -> None:
    console.print(Panel(
        "[bold]Quick Notes[/bold]\n"
        "Type a note and press Enter to save it instantly -- no menus, nothing to interrupt.\n"
        "Leave this terminal open alongside your main certcoach session.\n"
        "[dim]Type 'q' or press Ctrl+C to exit.[/dim]",
        title="📝 CertCoach Quick Notes", border_style="cyan", box=box.ROUNDED, padding=(1, 2),
    ))

    while True:
        try:
            note = Prompt.ask("\n  [bold cyan]❯[/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        if note.lower() in ("q", "quit", "exit"):
            console.print("[dim]Goodbye.[/dim]")
            break
        if not note:
            continue

        saved = database.add_quick_note(user_id, note)
        if saved:
            console.print("  [dim green]saved[/dim green]")
        else:
            console.print("  [dim]nothing to save[/dim]")


def print_notes(user_id: str) -> None:
    notes = database.get_quick_notes(user_id)
    if not notes:
        console.print("[dim]No notes saved yet.[/dim]")
        return
    for entry in notes:
        console.print(f"[dim]{entry.get('created_at', '')[:19]}[/dim]  {entry.get('note', '')}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Quick, freeform note capture alongside a certcoach session.")
    parser.add_argument("--view", action="store_true", help="Print all saved notes and exit, instead of capturing new ones.")
    args = parser.parse_args(argv)

    user_id = auth.get_session_user_id("local_user_1")

    if args.view:
        print_notes(user_id)
        return 0

    run_capture_loop(user_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
