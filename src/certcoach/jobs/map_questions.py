from __future__ import annotations

import argparse
import re
from certcoach.core import database
from certcoach.core import planner
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, MofNCompleteColumn

console = Console()


def clean_keyword(kw: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_$]+", "", kw).lower()


def find_best_concept(question_text: str, options: list[dict], subtopics: list[str]) -> str:
    """Finds the most relevant subtopic concept using keyword token matching."""
    text_corpus = (question_text + " " + " ".join(opt.get("code_snippet", "") for opt in options)).lower()
    
    best_concept = subtopics[0] if subtopics else "General"
    max_score = 0
    
    for sub in subtopics:
        # Calculate matching score based on token overlaps
        sub_tokens = [clean_keyword(t) for t in sub.replace("()", " ").replace("/", " ").split() if len(clean_keyword(t)) > 1]
        if not sub_tokens:
            continue
            
        score = 0
        for token in sub_tokens:
            # Exact word boundaries match
            if re.search(r"\b" + re.escape(token) + r"\b", text_corpus):
                score += 2
            elif token in text_corpus:
                score += 1
                
        if score > max_score:
            max_score = score
            best_concept = sub
            
    return best_concept


def run_mapping(dry_run: bool = False) -> dict:
    database.check_connection()
    syllabus = planner.load_syllabus()
    
    # Pre-parse syllabus structures
    syllabus_map = {}
    for item in syllabus:
        for key in item.get("bank_topic_keys", []):
            key_lower = key.lower()
            if key_lower not in syllabus_map:
                syllabus_map[key_lower] = []
            syllabus_map[key_lower].append(item)
            
    questions = list(database.questions_col.find({}))
    total_qs = len(questions)
    mapped_count = 0
    updated_count = 0
    
    console.print(f"[bold cyan][*] Scanning {total_qs} questions in database...[/bold cyan]")
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Mapping questions", total=total_qs)
        
        for q in questions:
            meta = q.get("metadata", {})
            q_topic = meta.get("topic", "General")
            
            # Find candidate syllabus topics
            candidates = syllabus_map.get(q_topic.lower(), [])
            
            # Fallback check: try to match syllabus topic directly
            if not candidates:
                for item in syllabus:
                    if item["topic"].lower() == q_topic.lower():
                        candidates = [item]
                        break
                        
            if not candidates:
                # General topic or no match
                progress.advance(task)
                continue
                
            best_topic = candidates[0]
            subtopics = best_topic.get("subtopics", [])
            
            best_concept = find_best_concept(q.get("question_text", ""), q.get("options", []), subtopics)
            
            # Check if current mappings differ
            needs_update = False
            updates = {}
            
            if meta.get("topic_id") != best_topic["id"]:
                updates["metadata.topic_id"] = best_topic["id"]
                needs_update = True
                
            if meta.get("syllabus_topic") != best_topic["topic"]:
                updates["metadata.syllabus_topic"] = best_topic["topic"]
                needs_update = True
                
            if meta.get("concept") != best_concept:
                updates["metadata.concept"] = best_concept
                needs_update = True
                
            if needs_update:
                updated_count += 1
                if not dry_run:
                    database.questions_col.update_one({"_id": q["_id"]}, {"$set": updates})
                    
            mapped_count += 1
            progress.advance(task)
            
    action_word = "Would update" if dry_run else "Updated"
    console.print(f"\n[bold green]Mapping Scan Complete![/bold green]")
    console.print(f"  - Total Mapped to Syllabus: {mapped_count}/{total_qs}")
    console.print(f"  - {action_word} mappings for: {updated_count} questions")
    
    return {
        "total": total_qs,
        "mapped": mapped_count,
        "updated": updated_count
    }


def main():
    parser = argparse.ArgumentParser(description="Map legacy database questions to explicit syllabus topics and concepts.")
    parser.add_argument("--dry-run", action="store_true", help="Perform mapping checks without writing to MongoDB.")
    args = parser.parse_args()
    
    run_mapping(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
