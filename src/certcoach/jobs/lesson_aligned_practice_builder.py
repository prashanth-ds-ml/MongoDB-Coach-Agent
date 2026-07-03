"""Job to audit and build lesson-aligned and general practice questions using local Ollama only."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple

from certcoach.core import database, planner, config
from certcoach.core.model_runner import get_model_runner
from certcoach.core.lesson_bank import get_validated_lesson, validate_lesson_markdown
from certcoach.core.judge_questions import judge_question
from certcoach.jobs.repair_explanations import generate_repair, apply_repair
from certcoach.jobs.next_phase4_topic import get_next_topic
from certcoach.jobs.nightly_seed_questions import (
    SeedMCQ,
    validate_question_quality,
    is_duplicate_question,
    make_question_id,
    question_fingerprint,
    _next_question_number,
    _difficulty_key,
    _resolve_correct_answer,
)

# Force local Ollama only for population and repair
os.environ["POPULATION_MODEL_CHAIN"] = "gemma4:12b"
os.environ["REPAIR_MODEL_CHAIN"] = "gemma4:12b"
os.environ["JUDGE_ENABLED"] = "false"  # Disable remote judge checks to stay strictly local-only
os.environ["POPULATION_NUM_CTX"] = "8192"
os.environ["REPAIR_NUM_CTX"] = "8192"

def ensure_local_only():
    # Double enforce in config overrides
    os.environ["POPULATION_MODEL_CHAIN"] = "gemma4:12b"
    os.environ["REPAIR_MODEL_CHAIN"] = "gemma4:12b"
    os.environ["JUDGE_ENABLED"] = "false"
    os.environ["POPULATION_NUM_CTX"] = "8192"
    os.environ["REPAIR_NUM_CTX"] = "8192"

class QuestionTargetDummy:
    """Helper dummy class to mimic nightly_seed_questions target expected by functions."""
    def __init__(self, topic_id: int, topic: str, concept: str, difficulty: str):
        self.topic_id = topic_id
        self.topic = topic
        self.concept = concept
        self.difficulty = difficulty
        self.bank_topic = topic
        self.exam_weight = 0.05
        self.concept_weight = 0.10
        self.style_type = "Type A" if difficulty == "Medium" else "Type B"

def log_to_vault(message: str) -> None:
    """Logs progress to the Obsidian vault under memory/lesson_aligned_practice_log.md."""
    vault_dir = os.path.join(os.getcwd(), "memory")
    os.makedirs(vault_dir, exist_ok=True)
    log_path = os.path.join(vault_dir, "lesson_aligned_practice_log.md")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    # Prepend or append to log
    mode = "a" if os.path.exists(log_path) else "w"
    with open(log_path, mode, encoding="utf-8") as f:
        f.write(log_entry)
    print(f"Vault Log: {message}")

def audit_and_repair_micro_challenge(topic_id: int, concept: str) -> bool:
    """Audits the micro-challenge (Section 5) of the concept's lesson and repairs it if not aligned."""
    ensure_local_only()
    lesson_doc = get_validated_lesson(topic_id, concept)
    if not lesson_doc:
        log_to_vault(f"Target T{topic_id} '{concept}' does not have a validated lesson artifact.")
        return False
        
    lesson_md = lesson_doc.get("lesson_markdown", "")
    
    # Extract Micro-Challenge section
    micro_match = re.search(
        r"### 5\. Micro-Challenge(.*?)(?:### 6\. 30-Second Recall|\Z)",
        lesson_md,
        flags=re.DOTALL,
    )
    if not micro_match:
        log_to_vault(f"T{topic_id} '{concept}': Missing ### 5. Micro-Challenge section. Regenerating section.")
        return repair_lesson_micro_section(topic_id, concept, lesson_doc, "Section is missing.")
        
    micro_text = micro_match.group(1).strip()
    if not micro_text:
        log_to_vault(f"T{topic_id} '{concept}': Empty ### 5. Micro-Challenge section. Regenerating section.")
        return repair_lesson_micro_section(topic_id, concept, lesson_doc, "Section is empty.")
        
    # Query local Ollama to audit alignment of this micro-challenge question against the lesson context
    # Extract Sections 1-4 of the lesson as the grounding context
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
            log_to_vault(f"T{topic_id} '{concept}': Audit call returned empty response.")
            return False
            
        # Parse JSON
        result = json.loads(re.search(r"\{.*\}", response, re.DOTALL).group(0))
        is_aligned = result.get("is_aligned", False)
        explanation = result.get("explanation", "")
        
        if is_aligned:
            log_to_vault(f"T{topic_id} '{concept}': Micro-Challenge is aligned. ({explanation})")
            return True
        else:
            log_to_vault(f"T{topic_id} '{concept}': Micro-Challenge audit failed: {explanation}. Repairing...")
            return repair_lesson_micro_section(topic_id, concept, lesson_doc, explanation)
            
    except Exception as e:
        log_to_vault(f"T{topic_id} '{concept}': Exception during micro-challenge audit: {e}")
        return False

def repair_lesson_micro_section(topic_id: int, concept: str, lesson_doc: dict, repair_reason: str) -> bool:
    """Regenerates Section 5 (Micro-Challenge) of the lesson markdown and updates the database."""
    ensure_local_only()
    lesson_md = lesson_doc.get("lesson_markdown", "")
    
    # Extract Sections 1-4
    context_match = re.search(
        r"(.*?)(?:### 5\. Micro-Challenge|\Z)",
        lesson_md,
        flags=re.DOTALL,
    )
    lesson_context = context_match.group(1).strip() if context_match else lesson_md
    
    repair_prompt = f"""You are CertCoach, an expert MongoDB question writer.
Write a simple, conceptual, and highly-relevant Micro-Challenge (concept quiz) question for the lesson below.
The question MUST be answerable strictly using only the facts, rules, and code snippets in the lesson text.
DO NOT include the correct answer, explanation, hint, or worked solution in the output.
Only include the question itself and the multiple choice options (A, B, C, D) if applicable, or a clear conceptual question stem.
Avoid transactions, sharding configuration, BSON types (unless this is Topic 1), and JavaScript .forEach iterations.

Lesson Text:
\"\"\"
{lesson_context}
\"\"\"

Audit Issue to Address:
{repair_reason}

Respond with a JSON object exactly formatted as:
{{
  "micro_challenge_markdown": "### 5. Micro-Challenge\\n\\n[Write the question and choices here. Do not leak the correct answer or explanations.]"
}}
"""
    
    runner = get_model_runner()
    model_config = {"provider": "ollama", "model": config.get_population_model()}
    
    try:
        response = runner._call_model(model_config, repair_prompt, num_ctx=4096)
        if not response:
            return False
            
        result = json.loads(re.search(r"\{.*\}", response, re.DOTALL).group(0))
        new_micro_section = result.get("micro_challenge_markdown", "").strip()
        
        if not new_micro_section:
            return False
            
        # Re-assemble lesson markdown
        # Find 30-Second Recall section
        recall_match = re.search(
            r"(### 6\. 30-Second Recall.*)",
            lesson_md,
            flags=re.DOTALL,
        )
        recall_section = recall_match.group(1).strip() if recall_match else "### 6. 30-Second Recall\n- Core points."
        
        # Build the new markdown
        updated_md = f"{lesson_context}\n\n{new_micro_section}\n\n{recall_section}"
        
        # Validate the updated markdown
        validation = validate_lesson_markdown(updated_md, topic_id=topic_id, concept=concept)
        if not validation["is_valid"]:
            log_to_vault(f"T{topic_id} '{concept}': Repaired lesson failed validation: {validation['issues']}")
            
        # Update the document in MongoDB
        lesson_doc["lesson_markdown"] = validation["cleaned_markdown"]
        lesson_doc["status"] = "validated" if validation["is_valid"] else "needs_review"
        lesson_doc["validation_issues"] = validation["issues"]
        lesson_doc["validated_at"] = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
        
        database.upsert_lesson_artifact(lesson_doc)
        log_to_vault(f"T{topic_id} '{concept}': Successfully repaired and updated micro-challenge section in database.")
        return True
        
    except Exception as e:
        log_to_vault(f"T{topic_id} '{concept}': Exception during micro-challenge repair: {e}")
        return False

def audit_and_tag_existing_questions(topic_id: int, concept: str) -> None:
    """Audits existing practice questions for this concept and tags them as lesson-aligned or general."""
    ensure_local_only()
    lesson_doc = get_validated_lesson(topic_id, concept)
    if not lesson_doc:
        log_to_vault(f"T{topic_id} '{concept}': Cannot audit question alignment without a validated lesson.")
        return
        
    lesson_md = lesson_doc.get("lesson_markdown", "")
    
    # Fetch questions mapped to this topic/concept
    query = {
        "metadata.topic_id": int(topic_id),
        "metadata.concept": concept
    }
    questions = list(database.questions_col.find(query))
    log_to_vault(f"T{topic_id} '{concept}': Found {len(questions)} existing questions to audit and tag.")
    
    runner = get_model_runner()
    model_config = {"provider": "ollama", "model": config.get_population_model()}
    
    for q in questions:
        q_id = q["_id"]
        meta = q.get("metadata", {})
        
        # Check if already tagged
        if "aligned_to_lesson" in meta:
            continue
            
        # We classify if the question aligns with the lesson
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
        try:
            response = runner._call_model(model_config, classify_prompt, num_ctx=4096)
            if not response:
                continue
                
            result = json.loads(re.search(r"\{.*\}", response, re.DOTALL).group(0))
            aligned = result.get("aligned_to_lesson", False)
            reason = result.get("reason", "")
            
            # Update database
            database.questions_col.update_one(
                {"_id": q_id},
                {"$set": {
                    "metadata.aligned_to_lesson": aligned,
                    "metadata.alignment_reason": reason
                }}
            )
            log_to_vault(f"Question {q_id}: Tagged aligned_to_lesson={aligned}. Reason: {reason}")
            
        except Exception as e:
            log_to_vault(f"Question {q_id}: Exception during tagging: {e}")

def populate_aligned_or_general_question(
    topic_id: int,
    topic: str,
    concept: str,
    difficulty: str,
    aligned: bool,
    extra: bool = False
) -> bool:
    """Generates, validates, repairs, and saves exactly one question (aligned or general)."""
    ensure_local_only()
    lesson_doc = get_validated_lesson(topic_id, concept)
    if not lesson_doc and aligned:
        log_to_vault(f"T{topic_id} '{concept}': Cannot generate aligned question without a lesson.")
        return False
        
    lesson_md = lesson_doc.get("lesson_markdown", "") if lesson_doc else ""
    dummy_target = QuestionTargetDummy(topic_id, topic, concept, difficulty)
    
    # Load official doc context
    syllabus_by_id = {item["id"]: item for item in planner.load_syllabus()}
    topic_item = syllabus_by_id.get(topic_id, {})
    md_files = topic_item.get("md_files", [])
    context_text = planner.load_md_context(md_files, prioritize_concept=concept)
    weak_focus_context = planner.load_topic_benchmark_focus(topic_id, concept)
    if isinstance(weak_focus_context, str) and weak_focus_context.strip():
        context_text = "\n\n---\n\n".join(
            part for part in (weak_focus_context, context_text)
            if isinstance(part, str) and part.strip()
        )
        
    # Build prompt based on whether it is lesson-aligned or general
    is_pymongo = "pymongo" in topic.lower() or "driver" in topic.lower()
    syntax_rule = (
        "Use PyMongo snake_case where the question is driver-specific, and contrast with mongosh only when useful."
        if is_pymongo
        else "Use strictly mongosh camelCase syntax. Do not use PyMongo snake_case in non-driver topics."
    )
    
    # Style choice allocation
    style_choice = "Type A" if difficulty == "Medium" else "Type B"
    if style_choice == "Type A":
        style_prompt = """
Style Target: Type A - Syntax Selection & Trap Spotting
- Design a coding scenario and select the syntactically correct query, command, or method call.
- The options should look extremely similar to test precise knowledge of syntax rules (quotes, braces, case).
"""
    else:
        style_prompt = """
Style Target: Type B - Theory, Constraints & Data Modeling
- Design a conceptual, rule-based, or architectural question.
- Focus on MongoDB limitations, indexing rules, or modeling trade-offs.
"""

    # Existing question samples to avoid duplicates
    avoid_questions = []
    nearby = list(database.questions_col.find({
        "metadata.topic_id": int(topic_id),
        "metadata.concept": concept,
        "metadata.difficulty": difficulty
    }))
    for existing in nearby:
        avoid_questions.append(existing.get("question_text", ""))
        
    avoid_block = ""
    if avoid_questions:
        avoid_lines = "\n".join(f"- {text[:240]}" for text in avoid_questions[:10])
        avoid_block = f"\nExisting questions to avoid for this concept/difficulty:\n{avoid_lines}\n"

    if aligned:
        prompt = f"""You are CertCoach, an expert MongoDB question writer.
Generate exactly one weighted exam MCQ. The question MUST be answerable strictly and entirely using only the concepts, facts, syntax rules, and code examples taught in the Lesson Markdown below.
Do NOT test any MongoDB command, operator, option, limit, or detail that is not explicitly covered in the Lesson Markdown.

Lesson Markdown:
\"\"\"
{lesson_md}
\"\"\"

Topic: {topic}
Concept: {concept}
Difficulty: {difficulty}
Syntax rule: {syntax_rule}
{style_prompt}
{avoid_block}

Critical Output Format:
You MUST output a single flat JSON object with exactly these keys:
- "question": string (under 70 words)
- "options": a list of exactly four short strings (strictly strings, do NOT use dictionaries or objects inside this list!)
- "correct_answer" or "correct_option_letter": the exact correct option text or single letter (A, B, C, D)
- "citation_source": string (the lesson name)
- "trap_analysis": string (under 40 words)

Do NOT include the seven-part explanation or feedbacks in this shell. Keep it lean.
"""
    else:
        prompt = f"""You are CertCoach, an expert MongoDB question writer.
Generate exactly one weighted exam MCQ targeting the general domain of the concept '{concept}'.
You can use the broader official documentation context below to design a robust, realistic exam-level question.

Official Reference Docs Context:
\"\"\"
{context_text}
\"\"\"

Topic: {topic}
Concept: {concept}
Difficulty: {difficulty}
Syntax rule: {syntax_rule}
{style_prompt}
{avoid_block}

Critical Output Format:
You MUST output a single flat JSON object with exactly these keys:
- "question": string (under 70 words)
- "options": a list of exactly four short strings (strictly strings, do NOT use dictionaries or objects inside this list!)
- "correct_answer" or "correct_option_letter": the exact correct option text or single letter (A, B, C, D)
- "citation_source": string (official filename or section)
- "trap_analysis": string (under 40 words)

Do NOT include the seven-part explanation or feedbacks in this shell. Keep it lean.
"""

    runner = get_model_runner()
    model_chain = [{"provider": "ollama", "model": config.get_population_model()}]
    
    # Generate question shell
    result = runner.generate_with_quality_gate(
        prompt=prompt,
        model_chain=model_chain,
        max_retries=2,
        source_files=[md_files[0]] if md_files else [],
        context_text=lesson_md if aligned else context_text,
        response_kind="question_shell"
    )
    
    if not result["success"]:
        log_to_vault(f"Failed to generate aligned={aligned} question for {concept} ({difficulty}): {result['quality_issues']}")
        return False
        
    mcq_data = result["result"]
    mcq = SeedMCQ(**mcq_data)
    if not mcq or len(mcq.options) != 4:
        return False
        
    correct_answer = _resolve_correct_answer(mcq)
    if not correct_answer:
        return False
        
    correct_idx = mcq.options.index(correct_answer)
    fingerprint = question_fingerprint(topic, concept, mcq.question)
    question_number = _next_question_number(dummy_target)
    q_id = make_question_id(dummy_target, question_number, fingerprint)
    
    # Prepare the question document
    question_doc = {
        "_id": q_id,
        "metadata": {
            "topic": topic,
            "syllabus_topic": topic,
            "topic_id": topic_id,
            "concept": concept,
            "difficulty": difficulty,
            "question_style": "Syntax Selection" if style_choice == "Type A" else "Theory/Concepts",
            "question_style_type": style_choice,
            "question_number": question_number,
            "question_fingerprint": fingerprint,
            "aligned_to_lesson": aligned,
            "extra_practice": extra,
            "generation_source": "lesson_aligned_practice_builder",
            "created_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + "Z",
            "content_contract_version": 1,
            "content_contract_status": "needs_explanation_repair",
            "content_contract_source": "lesson_aligned_practice_builder",
        },
        "context": {
            "scenario_description": f"Lesson-Aligned {difficulty.lower()} practice" if aligned else f"General {difficulty.lower()} practice",
            "database_info": "",
        },
        "question_text": mcq.question,
        "options": [
            {"code_snippet": opt, "is_correct": (idx == correct_idx), "feedback": ""}
            for idx, opt in enumerate(mcq.options)
        ],
        "explanation": "",
        "trap_analysis": ""
    }
    
    # Duplicate check
    is_dup, reason = is_duplicate_question(question_doc, dummy_target)
    if is_dup:
        log_to_vault(f"Generated question is duplicate: {reason}. Skipping.")
        return False
        
    # Save the shell
    database.questions_col.insert_one(question_doc)
    log_to_vault(f"Inserted shell {q_id} (aligned={aligned}, extra={extra}) for {concept} ({difficulty}). Running repair...")
    
    # Perform immediate repair
    try:
        repair_candidate = database.questions_col.find_one({"_id": q_id})
        if not repair_candidate:
            return False
            
        repair = generate_repair(repair_candidate)
        if repair:
            apply_repair(repair_candidate, repair)
            # Activate the question
            database.questions_col.update_one(
                {"_id": q_id},
                {"$set": {"status": "active", "metadata.content_contract_status": "active"}}
            )
            log_to_vault(f"Successfully repaired and activated question {q_id}.")
            return True
        else:
            log_to_vault(f"Explanation repair failed for question {q_id}. Question remains in needs_explanation_repair.")
            return False
            
    except Exception as e:
        log_to_vault(f"Exception during explanation repair of {q_id}: {e}")
        return False

def run_loop_for_concept(
    topic_id: int,
    topic: str,
    concept: str,
    target_aligned_easy: int = 3,
    target_aligned_medium: int = 2,
    target_general_easy: int = 5,
    target_general_medium: int = 5,
    extra_easy: int = 0,
    extra_medium: int = 0
) -> None:
    """Executes the complete audit, repair, classification, and population loop for a single concept."""
    log_to_vault(f"=== Starting Loop for Topic {topic_id} | Concept: {concept} ===")
    
    # 1. Audit and Repair Micro-Challenge
    log_to_vault("Step 1: Auditing lesson micro-challenge...")
    micro_ok = audit_and_repair_micro_challenge(topic_id, concept)
    
    # 2. Tag Existing Questions
    log_to_vault("Step 2: Auditing and tagging existing question bank...")
    audit_and_tag_existing_questions(topic_id, concept)
    
    # 3. Count aligned vs general active questions
    aligned_easy_count = database.questions_col.count_documents({
        "metadata.topic_id": int(topic_id),
        "metadata.concept": concept,
        "metadata.difficulty": "Easy",
        "metadata.aligned_to_lesson": True,
        "status": "active"
    })
    aligned_medium_count = database.questions_col.count_documents({
        "metadata.topic_id": int(topic_id),
        "metadata.concept": concept,
        "metadata.difficulty": "Medium",
        "metadata.aligned_to_lesson": True,
        "status": "active"
    })
    general_easy_count = database.questions_col.count_documents({
        "metadata.topic_id": int(topic_id),
        "metadata.concept": concept,
        "metadata.difficulty": "Easy",
        "metadata.aligned_to_lesson": {"$ne": True},  # General (false or not set)
        "status": "active"
    })
    general_medium_count = database.questions_col.count_documents({
        "metadata.topic_id": int(topic_id),
        "metadata.concept": concept,
        "metadata.difficulty": "Medium",
        "metadata.aligned_to_lesson": {"$ne": True},
        "status": "active"
    })
    
    log_to_vault(f"Current Active Pools: "
                 f"Aligned [Easy: {aligned_easy_count}/{target_aligned_easy}, Medium: {aligned_medium_count}/{target_aligned_medium}] | "
                 f"General [Easy: {general_easy_count}/{target_general_easy}, Medium: {general_medium_count}/{target_general_medium}]")
                 
    # 4. Populate Aligned Pool Deficits
    log_to_vault("Step 3: Populating Lesson-Aligned pool deficits...")
    while aligned_easy_count < target_aligned_easy:
        success = populate_aligned_or_general_question(topic_id, topic, concept, "Easy", aligned=True)
        if success:
            aligned_easy_count += 1
        else:
            time.sleep(1) # simple backoff
            
    while aligned_medium_count < target_aligned_medium:
        success = populate_aligned_or_general_question(topic_id, topic, concept, "Medium", aligned=True)
        if success:
            aligned_medium_count += 1
        else:
            time.sleep(1)
            
    # 5. Populate General Pool Deficits
    log_to_vault("Step 4: Populating General Concept pool deficits...")
    while general_easy_count < target_general_easy:
        success = populate_aligned_or_general_question(topic_id, topic, concept, "Easy", aligned=False)
        if success:
            general_easy_count += 1
        else:
            time.sleep(1)
            
    while general_medium_count < target_general_medium:
        success = populate_aligned_or_general_question(topic_id, topic, concept, "Medium", aligned=False)
        if success:
            general_medium_count += 1
        else:
            time.sleep(1)
            
    # 6. Generate Extra Aligned Practice Questions
    if extra_easy > 0 or extra_medium > 0:
        log_to_vault(f"Step 5: Generating requested extra practice (Easy: {extra_easy}, Medium: {extra_medium})...")
        for _ in range(extra_easy):
            populate_aligned_or_general_question(topic_id, topic, concept, "Easy", aligned=True, extra=True)
        for _ in range(extra_medium):
            populate_aligned_or_general_question(topic_id, topic, concept, "Medium", aligned=True, extra=True)
            
    log_to_vault(f"=== Completed Loop for Concept: {concept} ===\n")

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit lessons, tag questions, and build lesson-aligned practice questions.")
    parser.add_argument("--topic", type=int, default=None, help="Specific topic id to run.")
    parser.add_argument("--concept", type=str, default=None, help="Specific concept name to run.")
    parser.add_argument("--extra-easy", type=int, default=0, help="Number of extra Easy aligned questions to generate.")
    parser.add_argument("--extra-medium", type=int, default=0, help="Number of extra Medium aligned questions to generate.")
    parser.add_argument("--all-concepts", action="store_true", help="Iterate over all incomplete concepts sequentially.")
    
    args = parser.parse_args(argv)
    database.check_connection()
    ensure_local_only()
    
    if args.all_concepts:
        # Loop over all incomplete concepts sequentially using next_phase4_topic selector
        log_to_vault("Starting batch run for all incomplete syllabus concepts...")
        while True:
            target = get_next_topic()
            if not target:
                log_to_vault("All concepts are study-ready and populated!")
                break
                
            topic_id = target["topic_id"]
            topic_name = target["topic"]
            concept = target["concept"]
            
            run_loop_for_concept(
                topic_id=topic_id,
                topic=topic_name,
                concept=concept,
                extra_easy=args.extra_easy,
                extra_medium=args.extra_medium
            )
            # Break if single pass desired, or let it repeat until clean
            break
    elif args.topic is not None:
        syllabus = planner.load_syllabus()
        topic_item = next((t for t in syllabus if int(t["id"]) == args.topic), None)
        if not topic_item:
            print(f"Unknown topic ID: {args.topic}")
            return 1
            
        concepts = topic_item.get("subtopics", [topic_item["topic"]])
        if args.concept:
            if args.concept not in concepts:
                print(f"Concept '{args.concept}' is not in Topic {args.topic}")
                return 1
            run_loop_for_concept(
                topic_id=args.topic,
                topic=topic_item["topic"],
                concept=args.concept,
                extra_easy=args.extra_easy,
                extra_medium=args.extra_medium
            )
        else:
            for concept in concepts:
                run_loop_for_concept(
                    topic_id=args.topic,
                    topic=topic_item["topic"],
                    concept=concept,
                    extra_easy=args.extra_easy,
                    extra_medium=args.extra_medium
                )
    else:
        # Run next incomplete concept automatically
        target = get_next_topic()
        if not target:
            log_to_vault("All concepts are study-ready and populated!")
            return 0
            
        run_loop_for_concept(
            topic_id=target["topic_id"],
            topic=target["topic"],
            concept=target["concept"],
            extra_easy=args.extra_easy,
            extra_medium=args.extra_medium
        )
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
