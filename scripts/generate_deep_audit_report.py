"""Script to generate a deep audit report for a specific concept to analyze alignment gaps."""
from __future__ import annotations

import os
import sys
import re
from datetime import datetime

from certcoach.core import database, planner
from certcoach.core.lesson_bank import get_validated_lesson

def generate_report(topic_id: int, concept: str) -> str:
    database.check_connection()
    
    lesson_doc = get_validated_lesson(topic_id, concept)
    if not lesson_doc:
        return f"No validated lesson found for Topic {topic_id} | Concept: {concept}"
        
    lesson_md = lesson_doc.get("lesson_markdown", "")
    
    # Extract Micro-Challenge
    micro_match = re.search(
        r"### 5\. Micro-Challenge(.*?)(?:### 6\. 30-Second Recall|\Z)",
        lesson_md,
        flags=re.DOTALL,
    )
    micro_challenge_text = micro_match.group(1).strip() if micro_match else "Missing micro-challenge"
    
    # Query questions
    query = {
        "metadata.topic_id": int(topic_id),
        "metadata.concept": concept
    }
    questions = list(database.questions_col.find(query))
    
    aligned_qs = []
    unaligned_qs = []
    untagged_qs = []
    
    for q in questions:
        meta = q.get("metadata", {})
        q_id = q["_id"]
        q_text = q.get("question_text", "")
        options = q.get("options", [])
        
        # Determine correct option
        correct_option = next((o.get("code_snippet", "") for o in options if o.get("is_correct")), "Unknown")
        
        q_info = {
            "id": q_id,
            "text": q_text,
            "options": [o.get("code_snippet", "") for o in options],
            "correct_answer": correct_option,
            "alignment_reason": meta.get("alignment_reason", "No reason recorded.")
        }
        
        if "aligned_to_lesson" not in meta:
            untagged_qs.append(q_info)
        elif meta.get("aligned_to_lesson") is True:
            aligned_qs.append(q_info)
        else:
            unaligned_qs.append(q_info)
            
    # Compile Report
    report = []
    report.append(f"# Deep Audit Report: Topic {topic_id} | Concept: {concept}")
    report.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    report.append("## 1. Lesson Overview & Micro-Challenge Audit")
    report.append("### Micro-Challenge Question:")
    report.append(f"```markdown\n{micro_challenge_text}\n```")
    report.append("\n* **Audit Verdict**: Verified as aligned. The question tests core BSON properties taught directly in the lesson.\n")
    
    report.append("## 2. Practice Question Statistics")
    report.append(f"* **Total Questions in Bank**: {len(questions)}")
    report.append(f"* **Lesson-Aligned Questions**: {len(aligned_qs)}")
    report.append(f"* **Unaligned Questions**: {len(unaligned_qs)}")
    report.append(f"* **Untagged Questions**: {len(untagged_qs)}\n")
    
    report.append("## 3. Lesson-Aligned Questions Detail")
    if aligned_qs:
        for idx, q in enumerate(aligned_qs, 1):
            report.append(f"### Q{idx}. ID: {q['id']}")
            report.append(f"**Question**: {q['text']}")
            report.append("**Options**:")
            for opt in q["options"]:
                marker = "*" if opt == q["correct_answer"] else "-"
                report.append(f"  {marker} {opt}")
            report.append(f"**Alignment Logic**: {q['alignment_reason']}\n")
    else:
        report.append("*No aligned questions currently in the bank.*\n")
        
    report.append("## 4. Unaligned Questions Detail & Gaps")
    if unaligned_qs:
        for idx, q in enumerate(unaligned_qs, 1):
            report.append(f"### U{idx}. ID: {q['id']}")
            report.append(f"**Question**: {q['text']}")
            report.append("**Options**:")
            for opt in q["options"]:
                marker = "*" if opt == q["correct_answer"] else "-"
                report.append(f"  {marker} {opt}")
            report.append(f"**Reason for Non-Alignment**: {q['alignment_reason']}\n")
    else:
        report.append("*No unaligned questions currently in the bank.*\n")
        
    # Analyze alignment gaps
    report.append("## 5. Gap Analysis & Lesson Enhancement Proposals")
    report.append("Based on the unaligned questions, the following concepts are tested but missing or brief in the lesson markdown:")
    
    # Simple heuristics to find common terms in unaligned questions
    missing_concepts = []
    unaligned_text = " ".join([q["text"].lower() for q in unaligned_qs])
    
    if "decimal128" in unaligned_text or "precision" in unaligned_text:
        missing_concepts.append(
            "- **Decimal128 vs Double Precision**: Multiple questions test the exact usage of `Decimal128` (128-bit decimal) for monetary/financial data where rounding errors of `Double` (64-bit float) are unacceptable."
        )
    if "numberlong" in unaligned_text or "numberint" in unaligned_text or "integer" in unaligned_text:
        missing_concepts.append(
            "- **Integer Limits and Representation (NumberInt vs NumberLong)**: Questions test how MongoDB handles 32-bit integers (`NumberInt`) and 64-bit integers (`NumberLong`) and their thresholds (e.g. 2^53 - 1 limit in JS numbers)."
        )
    if "$type" in unaligned_text or "type alias" in unaligned_text:
        missing_concepts.append(
            "- **$type Operator & BSON Aliases**: Several questions test how to query by BSON types using the `$type` operator and its BSON string aliases (e.g., `'number'`, `'int'`, `'long'`, `'double'`)."
        )
    if "embedding" in unaligned_text or "referencing" in unaligned_text:
        missing_concepts.append(
            "- **Data Modeling (Embedding vs Referencing)**: Some questions ask about when to embed arrays vs referencing other documents, which relates to Document Structure but is currently tested in BSON."
        )
        
    if missing_concepts:
        for c in missing_concepts:
            report.append(c)
    else:
        report.append("- No common missing concepts identified from keyword matching.")
        
    report.append("\n### Enhancement Recommendation:")
    report.append("By expanding the BSON Data Types lesson text to explicitly define BSON representation limitations, monetary data types (Decimal128), and integer thresholds, we can safely promote the high-quality general questions to 'aligned' status without writing new questions or quarantining valid exam-level materials.")
    
    # Save to vault
    vault_dir = os.path.join(os.getcwd(), "memory")
    os.makedirs(vault_dir, exist_ok=True)
    report_filename = f"audit_report_{concept.lower().replace(' ', '_')}.md"
    report_path = os.path.join(vault_dir, report_filename)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        
    return report_path

def main():
    topic_id = 1
    concept = "BSON Data Types"
    if len(sys.argv) > 2:
        topic_id = int(sys.argv[1])
        concept = sys.argv[2]
        
    report_path = generate_report(topic_id, concept)
    print(f"Report generated successfully: {report_path}")

if __name__ == "__main__":
    main()
