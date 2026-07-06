"""One-time migration: backfill `provenance` onto every existing question.

Every question in the bank today predates the provenance/trust mechanism, so
none of it has been verified against the new citation-check standard -- it
all starts at `draft`, the same as the 12-topic audit's own conclusion (bugs
were found in every topic). This migration does not delete or reinterpret
any existing field; it only adds the missing `provenance` sub-document so the
practice/mock/spaced-repetition paths (which now require `provenance.state
== "confirmed"`, see `database.is_practice_ready`) can filter correctly.

Idempotent: questions that already have a `provenance` field are left alone,
so re-running this is safe.
"""
from __future__ import annotations

import argparse
import sys

from certcoach.core import database
from certcoach.core.content_contract import DEFAULT_PROVENANCE_STATE, provenance_metadata
from certcoach.jobs.backup_questions import backup_questions


def backfill_provenance(dry_run: bool = False) -> dict:
    to_update = list(database.questions_col.find({"provenance": {"$exists": False}}))
    already_done = database.questions_col.count_documents({"provenance": {"$exists": True}})

    if dry_run:
        return {"would_update": len(to_update), "already_has_provenance": already_done}

    updated = 0
    for question in to_update:
        metadata = question.get("metadata", {}) or {}
        citation_doc_file = metadata.get("citation_source", "") or ""
        # A pre-migration citation_source is a filename hint at best -- it was
        # never verified against a specific quote, so it starts at "draft",
        # not "sourced". Only new, citation-checked generation earns "sourced".
        provenance = provenance_metadata(
            state=DEFAULT_PROVENANCE_STATE,
            citation_doc_file=citation_doc_file,
            citation_quote="",
            model=None,
        )
        database.questions_col.update_one(
            {"_id": question["_id"]},
            {"$set": {"provenance": provenance}},
        )
        updated += 1

    return {"updated": updated, "already_had_provenance": already_done}


def suspect_uncited_drafts(dry_run: bool = False) -> dict:
    """One-time follow-up: the legacy generator only ever recorded a source
    *filename*, never a verbatim quote, so every backfilled `draft` question
    fails the deterministic citation check by construction -- it can never
    earn `confirmed` as-is. Rather than leave 376 guaranteed-fails sitting in
    the active review queue, park them at `suspect` directly. They stay
    available as human inspiration when generating real cited replacements,
    but only re-enter the bank through the normal generate->cite->confirm
    pipeline -- there is no shortcut back into `confirmed`.
    """
    query = {"provenance.state": "draft", "provenance.citation.quote": ""}
    to_update = list(database.questions_col.find(query))

    if dry_run:
        return {"would_suspect": len(to_update)}

    updated = 0
    for question in to_update:
        database.mark_question_suspect(
            question["_id"],
            reason="legacy backlog: no verbatim citation quote on record",
        )
        updated += 1

    return {"suspected": updated}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Backfill provenance.state=draft onto every existing question.")
    parser.add_argument("--dry-run", action="store_true", help="Report counts without writing.")
    parser.add_argument("--skip-backup", action="store_true", help="Skip the pre-migration backup (not recommended).")
    parser.add_argument(
        "--suspect-uncited",
        action="store_true",
        help="Follow-up migration: move draft questions with no citation quote to suspect.",
    )
    args = parser.parse_args(argv)

    database.check_connection()

    if args.suspect_uncited:
        if args.dry_run:
            result = suspect_uncited_drafts(dry_run=True)
            print(f"Would mark {result['would_suspect']} uncited draft questions as suspect.")
            return 0
        if not args.skip_backup:
            backup_dir = backup_questions()
            print(f"Pre-migration backup created: {backup_dir}")
        result = suspect_uncited_drafts(dry_run=False)
        print(f"Marked {result['suspected']} uncited draft questions as suspect.")
        print("The review queue now only shows questions that could plausibly earn 'confirmed'.")
        return 0

    if args.dry_run:
        result = backfill_provenance(dry_run=True)
        print(f"Would backfill {result['would_update']} questions to provenance.state='draft'.")
        print(f"{result['already_has_provenance']} questions already have a provenance field and would be left alone.")
        return 0

    if not args.skip_backup:
        backup_dir = backup_questions()
        print(f"Pre-migration backup created: {backup_dir}")

    result = backfill_provenance(dry_run=False)
    print(f"Backfilled {result['updated']} questions to provenance.state='draft'.")
    print(f"{result['already_had_provenance']} questions already had provenance and were left alone.")
    print("\nAll practice/mock/spaced-repetition question serving now requires "
          "provenance.state=='confirmed'. Run `certcoach-review-questions` to "
          "start confirming questions against their citations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
