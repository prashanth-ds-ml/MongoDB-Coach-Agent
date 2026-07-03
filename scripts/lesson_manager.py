"""General script to export, validate, and import lesson markdown artifacts from/to MongoDB."""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone

from certcoach.core import database, planner
from certcoach.core.lesson_bank import get_validated_lesson, validate_lesson_markdown, LESSON_CONTRACT_VERSION
from certcoach.core.content_contract import CONTENT_CONTRACT_VERSION

def export_lesson(topic_id: int, concept: str, out_path: str) -> None:
    database.check_connection()
    art = database.get_lesson_artifact(topic_id, concept)
    if not art:
        print(f"Error: Lesson not found for Topic {topic_id} | Concept: {concept}")
        return
        
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(art["lesson_markdown"])
    print(f"Successfully exported Topic {topic_id} | '{concept}' to: {out_path}")

def import_lesson(topic_id: int, concept: str, file_path: str) -> None:
    database.check_connection()
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
        
    with open(file_path, "r", encoding="utf-8") as f:
        lesson_md = f.read()
        
    # Validate the edited markdown
    validation = validate_lesson_markdown(lesson_md, topic_id=topic_id, concept=concept)
    if not validation["is_valid"]:
        print("[-] Lesson validation FAILED with the following issues:")
        for issue in validation["issues"]:
            print(f"  * {issue}")
        confirm = input("Do you still want to import this lesson as 'needs_review'? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Import aborted.")
            return
            
    # Load existing or prepare new artifact
    existing = database.get_lesson_artifact(topic_id, concept) or {}
    
    timestamp = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    syllabus = planner.load_syllabus()
    topic_name = next((t["topic"] for t in syllabus if int(t["id"]) == int(topic_id)), f"Topic {topic_id}")
    artifact = {
        "topic_id": int(topic_id),
        "topic": existing.get("topic") or topic_name,
        "concept": concept,
        "lesson_markdown": validation["cleaned_markdown"],
        "source_files": existing.get("source_files") or [],
        "status": "validated" if validation["is_valid"] else "needs_review",
        "validation_issues": validation["issues"],
        "lesson_contract_version": LESSON_CONTRACT_VERSION,
        "content_contract_version": CONTENT_CONTRACT_VERSION,
        "generated_at": existing.get("generated_at") or timestamp,
        "validated_at": timestamp if validation["is_valid"] else None,
        "updated_at": timestamp
    }
    
    database.upsert_lesson_artifact(artifact)
    print(f"[+] Successfully imported and updated Topic {topic_id} | '{concept}' in MongoDB.")

def list_lessons() -> None:
    database.check_connection()
    syllabus = planner.load_syllabus()
    print("Syllabus Lessons Status:")
    print(f"{'Topic':<6} | {'Concept':<35} | {'Status':<15}")
    print("-" * 65)
    for topic in syllabus:
        topic_id = int(topic["id"])
        subtopics = topic.get("subtopics", [topic["topic"]])
        for concept in subtopics:
            art = database.get_lesson_artifact(topic_id, concept)
            status = art.get("status", "missing") if art else "missing"
            print(f"{topic_id:<6} | {concept:<35} | {status:<15}")

def main():
    parser = argparse.ArgumentParser(description="Manage CertCoach lesson markdown artifacts.")
    subparsers = parser.add_add_parser = parser.add_subparsers(dest="command", required=True)
    
    # Export parser
    parser_export = subparsers.add_parser("export", help="Export a lesson to a markdown file.")
    parser_export.add_argument("--topic", type=int, required=True, help="Topic ID of the lesson.")
    parser_export.add_argument("--concept", type=str, required=True, help="Concept name of the lesson.")
    parser_export.add_argument("--out", type=str, required=True, help="Path to write the markdown file.")
    
    # Import parser
    parser_import = subparsers.add_parser("import", help="Import/Update a lesson from a markdown file.")
    parser_import.add_argument("--topic", type=int, required=True, help="Topic ID of the lesson.")
    parser_import.add_argument("--concept", type=str, required=True, help="Concept name of the lesson.")
    parser_import.add_argument("--file", type=str, required=True, help="Path to the lesson markdown file.")
    
    # List parser
    subparsers.add_parser("list", help="List all lessons and their status in MongoDB.")
    
    args = parser.parse_args()
    
    if args.command == "export":
        export_lesson(args.topic, args.concept, args.out)
    elif args.command == "import":
        import_lesson(args.topic, args.concept, args.file)
    elif args.command == "list":
        list_lessons()

if __name__ == "__main__":
    main()
