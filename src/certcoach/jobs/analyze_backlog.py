"""Read-only diagnostic report on the `suspect` legacy backlog (spec point 16).

These 376 questions were moved to `suspect` because their citation quote is
empty and can never pass the deterministic check as-is -- there is no repair
path that fabricates a citation after the fact. This script only classifies
what's there so a human can decide, per item class, whether to delete it
(duplicate or unusable) or keep it as a regeneration target (a real official
doc exists for that topic/concept, so the cite-and-confirm pipeline can
produce a proper replacement). It writes nothing to the database.
"""
from __future__ import annotations

import argparse
import os

from rich.console import Console
from rich.table import Table

from certcoach.core import database
from certcoach.jobs.dedupe_questions import find_duplicate_groups

console = Console()

CLEANED_MARKDOWNS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "cleaned_markdowns"
)


def _topic_has_cleaned_markdowns(topic_id: int) -> bool:
    """Whether any official-doc file for this syllabus topic exists under
    cleaned_markdowns/ -- files there are named `topic_{NN}_...`, one per
    source doc, so this is a topic-level lookup, not a per-question one."""
    try:
        prefix = f"topic_{int(topic_id):02d}_"
    except (TypeError, ValueError):
        return False
    if not os.path.isdir(CLEANED_MARKDOWNS_DIR):
        return False
    return any(name.startswith(prefix) for name in os.listdir(CLEANED_MARKDOWNS_DIR))


def _has_real_doc_lead(question: dict) -> bool:
    """A usable lead means either (a) the recorded citation doc_file names an
    actual file under cleaned_markdowns/, or (b) the question's syllabus
    topic has official docs on file at all -- legacy citation_source values
    are human-readable titles or mongodb.com URLs, never the corpus's actual
    filenames, so (a) alone misses virtually every legacy record even when a
    real doc exists for that topic. A question with no topic_id and no exact
    filename match has no lead a regenerator could use."""
    provenance = question.get("provenance") or {}
    doc_file = (provenance.get("citation") or {}).get("doc_file", "")
    if not doc_file:
        doc_file = question.get("metadata", {}).get("citation_source", "") or question.get("citation_source", "")
    doc_file = str(doc_file or "").strip()
    if doc_file and os.path.exists(os.path.join(CLEANED_MARKDOWNS_DIR, doc_file)):
        return True

    topic_id = question.get("metadata", {}).get("topic_id")
    return _topic_has_cleaned_markdowns(topic_id)


def analyze_suspect_backlog() -> dict:
    all_questions = list(database.questions_col.find({}))
    state_counts: dict[str, int] = {}
    for q in all_questions:
        state = str((q.get("provenance") or {}).get("state", "no_provenance"))
        state_counts[state] = state_counts.get(state, 0) + 1

    suspect_questions = [q for q in all_questions if (q.get("provenance") or {}).get("state") == "suspect"]

    duplicate_groups = find_duplicate_groups()
    duplicate_remove_ids = {
        item["_id"] for group in duplicate_groups for item in group["remove"]
    }

    buckets = {"duplicate": [], "has_doc_lead": [], "no_doc_lead": []}
    by_topic: dict[int, dict[str, int]] = {}

    for q in suspect_questions:
        topic_id = q.get("metadata", {}).get("topic_id")
        topic_entry = by_topic.setdefault(topic_id, {"duplicate": 0, "has_doc_lead": 0, "no_doc_lead": 0})

        if q["_id"] in duplicate_remove_ids:
            bucket = "duplicate"
        elif _has_real_doc_lead(q):
            bucket = "has_doc_lead"
        else:
            bucket = "no_doc_lead"

        buckets[bucket].append(q)
        topic_entry[bucket] += 1

    return {
        "state_counts": state_counts,
        "suspect_total": len(suspect_questions),
        "buckets": buckets,
        "by_topic": by_topic,
    }


def print_report(result: dict) -> None:
    console.print("\n[bold cyan]Provenance state overview (entire bank)[/bold cyan]")
    for state, count in sorted(result["state_counts"].items(), key=lambda kv: -kv[1]):
        console.print(f"  {state:<14}: {count}")

    console.print(f"\n[bold cyan]Suspect backlog breakdown[/bold cyan] ({result['suspect_total']} total)")
    buckets = result["buckets"]
    console.print(f"  [red]duplicate[/red]      : {len(buckets['duplicate'])}  (a better version already exists elsewhere -- safe to delete)")
    console.print(f"  [green]has_doc_lead[/green]   : {len(buckets['has_doc_lead'])}  (real official doc on file -- keep as a regeneration target)")
    console.print(f"  [yellow]no_doc_lead[/yellow]    : {len(buckets['no_doc_lead'])}  (no real doc citation possible, e.g. image-sourced -- safe to delete)")

    table = Table(title="By topic (suspect only)")
    table.add_column("Topic ID")
    table.add_column("Duplicate", justify="right")
    table.add_column("Has doc lead", justify="right")
    table.add_column("No doc lead", justify="right")
    for topic_id in sorted(result["by_topic"], key=lambda t: (t is None, t)):
        counts = result["by_topic"][topic_id]
        table.add_row(str(topic_id), str(counts["duplicate"]), str(counts["has_doc_lead"]), str(counts["no_doc_lead"]))
    console.print(table)

    console.print(
        "\n[dim]No repair-in-place path exists for this backlog: a citation cannot be fabricated after the "
        "fact. 'has_doc_lead' items are not directly usable either -- they are a target list telling the "
        "generation pipeline which topic/concept pairs already have a plausible source to regenerate from. "
        "This script wrote nothing; review before deleting or regenerating anything.[/dim]"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only report on the suspect question backlog.")
    parser.parse_args(argv)
    database.check_connection()
    result = analyze_suspect_backlog()
    print_report(result)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
