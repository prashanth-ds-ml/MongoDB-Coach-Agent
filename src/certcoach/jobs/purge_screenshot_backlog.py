"""One-time cleanup: delete the pics_qa-screenshot-sourced question shells
whose content was found to have drifted from their actual source.

A live test of recover_screenshot_citations.py against real transcripts
showed the original screenshot-to-question extraction (image_extractor.py's
Pass 2 restructuring) didn't just fail to save a citation -- it materially
rewrote several questions away from what the screenshot actually said (e.g.
one question's four options no longer even named a MongoDB method, where the
real screenshot tested insertOne() vs insertMany() with per-option
feedback). These shells are not safe to keep as-is or to treat as
regeneration targets; the underlying screenshots remain valuable as source
material for the normal generate-and-cite pipeline once OCR'd.

Only targets provenance.state='suspect' questions whose citation_source
starts with 'pics_qa/'. The remaining ~43 suspect questions with no
citation_source at all are a separate, still-undecided bucket and are left
untouched. Takes a backup first, same as every other migration here.
"""
from __future__ import annotations

import argparse
import sys

from certcoach.core import database
from certcoach.jobs.backup_questions import backup_questions


def _is_screenshot_sourced_suspect(question: dict) -> bool:
    if (question.get("provenance") or {}).get("state") != "suspect":
        return False
    source = str(question.get("metadata", {}).get("citation_source", "") or question.get("citation_source", ""))
    return source.startswith("pics_qa/")


def find_targets() -> list:
    return [
        q for q in database.questions_col.find({"provenance.state": "suspect"})
        if _is_screenshot_sourced_suspect(q)
    ]


def run_purge(dry_run: bool = False, skip_backup: bool = False) -> dict:
    targets = find_targets()
    if dry_run:
        return {"would_delete": len(targets)}

    if not skip_backup:
        backup_questions()

    ids = [q["_id"] for q in targets]
    if ids:
        database.questions_col.delete_many({"_id": {"$in": ids}})
    return {"deleted": len(ids)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Delete screenshot-sourced suspect question shells found to have drifted from their source."
    )
    parser.add_argument("--dry-run", action="store_true", help="Report the count without deleting.")
    parser.add_argument("--skip-backup", action="store_true", help="Skip the pre-deletion backup (not recommended).")
    args = parser.parse_args(argv)

    database.check_connection()

    if args.dry_run:
        result = run_purge(dry_run=True)
        print(f"Would delete {result['would_delete']} screenshot-sourced suspect questions.")
        return 0

    if not args.skip_backup:
        print("Taking a backup before deletion...")
    result = run_purge(dry_run=False, skip_backup=args.skip_backup)
    print(f"Deleted {result['deleted']} screenshot-sourced suspect questions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
