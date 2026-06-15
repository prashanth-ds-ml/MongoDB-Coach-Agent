from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from bson import json_util

from certcoach.core import database


def backup_questions(output_dir: str | Path = "backups") -> Path:
    database.check_connection()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = Path(output_dir) / f"questions-{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)
    data_path = backup_dir / "questions.jsonl"

    digest = hashlib.sha256()
    count = 0
    with data_path.open("wb") as handle:
        for question in database.questions_col.find({}):
            line = (json_util.dumps(question, json_options=json_util.CANONICAL_JSON_OPTIONS) + "\n").encode("utf-8")
            handle.write(line)
            digest.update(line)
            count += 1

    manifest = {
        "database": "certcoach_db",
        "collection": "questions",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "record_count": count,
        "sha256": digest.hexdigest(),
        "data_file": data_path.name,
    }
    (backup_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    verify_backup(backup_dir)
    return backup_dir


def verify_backup(backup_dir: str | Path) -> dict:
    backup_dir = Path(backup_dir)
    manifest = json.loads((backup_dir / "manifest.json").read_text(encoding="utf-8"))
    data_path = backup_dir / manifest["data_file"]
    digest = hashlib.sha256()
    count = 0

    with data_path.open("rb") as handle:
        for line in handle:
            digest.update(line)
            json_util.loads(line.decode("utf-8"))
            count += 1

    if count != manifest["record_count"]:
        raise ValueError(f"Backup count mismatch: expected {manifest['record_count']}, found {count}")
    if digest.hexdigest() != manifest["sha256"]:
        raise ValueError("Backup SHA-256 mismatch")
    return manifest


def restore_questions(backup_dir: str | Path, *, confirm_replace: bool = False) -> int:
    if not confirm_replace:
        raise ValueError("Restore requires confirm_replace=True because it replaces the questions collection")
    database.check_connection()
    manifest = verify_backup(backup_dir)
    data_path = Path(backup_dir) / manifest["data_file"]
    questions = [
        json_util.loads(line)
        for line in data_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    database.questions_col.delete_many({})
    if questions:
        database.questions_col.insert_many(questions, ordered=True)
    return len(questions)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Back up, verify, or restore the CertCoach questions collection.")
    parser.add_argument("--output-dir", default="backups", help="Parent directory for a new backup.")
    parser.add_argument("--verify", default=None, help="Verify an existing backup directory.")
    parser.add_argument("--restore", default=None, help="Restore an existing backup directory.")
    parser.add_argument("--confirm-replace", action="store_true", help="Required with --restore.")
    args = parser.parse_args(argv)

    if args.verify:
        manifest = verify_backup(args.verify)
        print(f"Verified {args.verify}: {manifest['record_count']} records, SHA-256 {manifest['sha256']}")
        return 0
    if args.restore:
        count = restore_questions(args.restore, confirm_replace=args.confirm_replace)
        print(f"Restored {count} questions from {args.restore}")
        return 0

    backup_dir = backup_questions(args.output_dir)
    manifest = verify_backup(backup_dir)
    print(f"Created verified backup: {backup_dir}")
    print(f"Records: {manifest['record_count']}")
    print(f"SHA-256: {manifest['sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
