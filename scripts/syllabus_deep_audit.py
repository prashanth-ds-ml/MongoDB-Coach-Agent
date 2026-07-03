"""Script to run a syllabus-wide deep audit of lessons and questions, generating a unified dashboard."""
from __future__ import annotations

import os
import sys
import re
import json
import time
from datetime import datetime, timezone

from certcoach.core import database, planner, config
from certcoach.core.model_runner import get_model_runner
from certcoach.core.lesson_bank import get_validated_lesson, validate_lesson_markdown

# Force local Ollama only
os.environ["POPULATION_MODEL_CHAIN"] = "gemma4:12b"
os.environ["REPAIR_MODEL_CHAIN"] = "gemma4:12b"
os.environ["JUDGE_ENABLED"] = "false"
os.environ["POPULATION_NUM_CTX"] = "8192"

def ensure_local_only():
    os.environ["POPULATION_MODEL_CHAIN"] = "gemma4:12b"
    os.environ["REPAIR_MODEL_CHAIN"] = "gemma4:12b"
    os.environ["JUDGE_ENABLED"] = "false"
    os.environ["POPULATION_NUM_CTX"] = "8192"

def audit_micro_challenge_text(lesson_md: str, topic_id: int, concept: str) -> tuple[bool, str]:
    """Audits the micro-challenge in the lesson using local Ollama."""
    ensure_local_only()
    micro_match = re.search(
        r"### 5\. Micro-Challenge(.*?)(?:### 6\. 30-Second Recall|\Z)",
        lesson_md,
        flags=re.DOTALL,
    )
    if not micro_match:
        return False, "Missing ### 5. Micro-Challenge section."
        
    micro_text = micro_match.group(1).strip()
    if not micro_text:
        return False, "Empty ### 5. Micro-Challenge section."
        
    context_match = re.search(
        r"(.*?)(?:### 5\. Micro-Challenge|\Z)",
        lesson_md,
        flags=re.DOTALL,
    )
    lesson_context = context_match.group(1).strip() if context_match else lesson_md
    
    audit_prompt = f"""You are a MongoDB exam quality auditor.
Review if the Micro-Challenge question below is strictly aligned to the lesson context.
The question MUST be answerable strictly and entirely using only facts, syntax, and rules explained in the lesson text.
It must NOT leak any future/past topics (e.g. transactions, sharding config, JavaScript `.forEach` loop iterations, BSON types if they are not the subject of this lesson).
Also, it must NOT contain the correct answer, hints, or worked solutions in the question text.

Lesson Context:
\"\"\"
{lesson_context}
\"\"\"

Micro-Challenge:
\"\"\"
{micro_text}
\"\"\"

Respond with a JSON object exactly formatted as:
{{
  "is_aligned": true or false,
  "explanation": "Why the question is aligned or what scope leaks/inaccuracies it contains."
}}
"""
    runner = get_model_runner()
    model_config = {"provider": "ollama", "model": config.get_population_model()}
    
    try:
        response = runner._call_model(model_config, audit_prompt, num_ctx=4096)
        if not response:
            return False, "Empty model response."
        result = json.loads(re.search(r"\{.*\}", response, re.DOTALL).group(0))
        return result.get("is_aligned", False), result.get("explanation", "")
    except Exception as e:
        return False, f"Exception: {e}"

def classify_question_alignment(q: dict, lesson_md: str) -> tuple[bool, str]:
    """Classifies a question's alignment to the lesson using local Ollama."""
    ensure_local_only()
    classify_prompt = f"""You are a MongoDB exam quality auditor.
Review if the multiple-choice question below is strictly aligned to the lesson context.
Can the student solve this question strictly and entirely using only the concepts, rules, and code examples explained in the lesson?
If the question references methods, operators, limitations, or APIs not mentioned in the lesson, it is NOT lesson-aligned.

Lesson Context:
\"\"\"
{lesson_md}
\"\"\"

Question:
\"\"\"
{q.get('question_text')}
\"\"\"
Options:
{chr(10).join(f"- {o.get('code_snippet')}" for o in q.get('options', []))}

Respond with a JSON object exactly formatted as:
{{
  "aligned_to_lesson": true or false,
  "reason": "Brief explanation of why it aligns or what is missing in the lesson to answer it."
}}
"""
    runner = get_model_runner()
    model_config = {"provider": "ollama", "model": config.get_population_model()}
    
    try:
        response = runner._call_model(model_config, classify_prompt, num_ctx=4096)
        if not response:
            return False, "Empty model response."
        result = json.loads(re.search(r"\{.*\}", response, re.DOTALL).group(0))
        return result.get("aligned_to_lesson", False), result.get("reason", "")
    except Exception as e:
        return False, f"Exception: {e}"

def run_syllabus_audit() -> None:
    database.check_connection()
    ensure_local_only()
    syllabus = planner.load_syllabus()
    
    dashboard_lines = []
    dashboard_lines.append("# Syllabus-Wide Deep Audit Dashboard")
    dashboard_lines.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    dashboard_lines.append("This dashboard summarizes the lesson-alignment and practice question audit across all 12 syllabus topics.\n")
    dashboard_lines.append(f"{'Topic ID':<8} | {'Concept':<30} | {'Micro-Challenge':<15} | {'Aligned Qs':<12} | {'General Qs':<10} | {'Total Qs':<8}")
    dashboard_lines.append("-" * 95)
    
    detail_lines = []
    detail_lines.append("# Syllabus Audit Details: Gaps & Unaligned Questions\n")
    
    total_bank_qs = 0
    total_aligned_qs = 0
    total_general_qs = 0
    
    for topic in syllabus:
        topic_id = int(topic["id"])
        topic_name = topic["topic"]
        subtopics = topic.get("subtopics", [topic_name])
        
        detail_lines.append(f"## Topic {topic_id}: {topic_name}\n")
        
        for concept in subtopics:
            print(f"Auditing T{topic_id} | '{concept}'...")
            lesson_doc = get_validated_lesson(topic_id, concept)
            
            if not lesson_doc:
                dashboard_lines.append(f"{topic_id:<8} | {concept[:30]:<30} | {'No Lesson':<15} | {'0':<12} | {'0':<10} | {'0':<8}")
                detail_lines.append(f"### Concept: {concept}\n* **No validated lesson found.**\n")
                continue
                
            lesson_md = lesson_doc.get("lesson_markdown", "")
            
            # 1. Audit Micro-Challenge if not already audited or needs review
            micro_ok, micro_reason = lesson_doc.get("micro_challenge_aligned", None), lesson_doc.get("micro_challenge_reason", "")
            if micro_ok is None:
                micro_ok, micro_reason = audit_micro_challenge_text(lesson_md, topic_id, concept)
                # Save audit back to lesson_doc
                database.lessons_col.update_one(
                    {"topic_id": topic_id, "concept": concept},
                    {"$set": {
                        "micro_challenge_aligned": micro_ok,
                        "micro_challenge_reason": micro_reason
                    }}
                )
                
            micro_status = "Aligned" if micro_ok else "Not Aligned"
            
            # 2. Audit and Tag questions for this concept
            query = {"metadata.topic_id": int(topic_id), "metadata.concept": concept}
            questions = list(database.questions_col.find(query))
            
            aligned_count = 0
            general_count = 0
            
            concept_unaligned_details = []
            
            for q in questions:
                meta = q.get("metadata", {})
                q_id = q["_id"]
                
                # Check if already tagged
                if "aligned_to_lesson" in meta:
                    aligned = meta.get("aligned_to_lesson")
                    reason = meta.get("alignment_reason", "")
                else:
                    # Classify
                    aligned, reason = classify_question_alignment(q, lesson_md)
                    database.questions_col.update_one(
                        {"_id": q_id},
                        {"$set": {
                            "metadata.aligned_to_lesson": aligned,
                            "metadata.alignment_reason": reason
                        }}
                    )
                    
                if aligned:
                    aligned_count += 1
                    total_aligned_qs += 1
                else:
                    general_count += 1
                    total_general_qs += 1
                    concept_unaligned_details.append(
                        f"  - **Q ID**: `{q_id}`\n"
                        f"    * **Text**: {q.get('question_text')}\n"
                        f"    * **Reason**: {reason}\n"
                    )
            
            total_bank_qs += len(questions)
            
            # Append dashboard row
            dashboard_lines.append(
                f"{topic_id:<8} | {concept[:30]:<30} | {micro_status:<15} | {aligned_count:<12} | {general_count:<10} | {len(questions):<8}"
            )
            
            # Append concept detail
            detail_lines.append(f"### Concept: {concept}")
            detail_lines.append(f"* **Micro-Challenge Status**: {micro_status} ({micro_reason})")
            detail_lines.append(f"* **Total Questions**: {len(questions)} (Aligned: {aligned_count}, General: {general_count})")
            if concept_unaligned_details:
                detail_lines.append("* **Unaligned Gaps Detail**:")
                detail_lines.extend(concept_unaligned_details)
            detail_lines.append("")
            
            # Write Dashboard dynamically
            vault_dir = os.path.join(os.getcwd(), "memory")
            os.makedirs(vault_dir, exist_ok=True)
            dashboard_path = os.path.join(vault_dir, "syllabus_deep_audit_dashboard.md")
            with open(dashboard_path, "w", encoding="utf-8") as f:
                f.write("\n".join(dashboard_lines))
                f.write(f"\n\n## Summary Statistics (Running Counts)\n")
                f.write(f"* **Total Syllabus Concepts**: 58\n")
                f.write(f"* **Total Questions Audited**: {total_bank_qs}\n")
                f.write(f"* **Total Aligned Questions**: {total_aligned_qs}\n")
                f.write(f"* **Total General Questions**: {total_general_qs}\n")

            # Write Details dynamically
            details_path = os.path.join(vault_dir, "syllabus_deep_audit_details.md")
            with open(details_path, "w", encoding="utf-8") as f:
                f.write("\n".join(detail_lines))

            # Brief sleep between concepts to prevent local system congestion
            time.sleep(0.5)
            
    print(f"Audit completed successfully!")
    print(f"Dashboard: {dashboard_path}")
    print(f"Details: {details_path}")

def main():
    run_syllabus_audit()
    return 0

if __name__ == "__main__":
    main()
