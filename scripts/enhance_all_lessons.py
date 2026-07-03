"""Script to enhance all remaining lessons in the syllabus using OpenRouter Llama 3.1 8B."""
import os
import sys
import re
from datetime import datetime, timezone

# Add parent directory to path so we can import certcoach
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from certcoach.core import database, planner
from certcoach.core.lesson_bank import resolve_lesson_target, build_lesson_source_bundle, validate_lesson_markdown, LESSON_CONTRACT_VERSION
from certcoach.core.content_contract import CONTENT_CONTRACT_VERSION
from certcoach.core.model_runner import get_model_runner
from scripts.enhance_lesson_llm import get_syntax_instructions, get_enhance_prompt, clean_topic_1_leaks

def enhance_single_concept(topic_id: int, concept: str) -> bool:
    try:
        database.check_connection()
        target = resolve_lesson_target(topic_id, concept)
        source_bundle = build_lesson_source_bundle(target)
        
        # Retrieve tested concepts from question bank
        query = {"metadata.topic_id": int(topic_id), "metadata.concept": concept}
        questions = list(database.questions_col.find(query))
        
        tested_concepts = []
        for q in questions:
            stem = q.get("question_text", "")
            options = q.get("options", [])
            correct = next((o.get("code_snippet", "") for o in options if o.get("is_correct")), "")
            if any(junk in stem.lower() for junk in ["food item", "yahoo", "support"]):
                continue
            tested_concepts.append(f"- Question: {stem}\n  Correct/Key Concept: {correct}")
            
        tested_block = ""
        if tested_concepts:
            tested_lines = "\n".join(tested_concepts[:10])
            tested_block = f"""
EXAM KNOWLEDGE REQUIREMENTS TO TEACH:
You MUST ensure that the lesson text fully covers and explains the concepts, rules, bit-lengths, limits, and behaviors tested by these exam questions. The learner must be able to answer these questions strictly using what you teach in the lesson:
{tested_lines}
"""
        
        prompt = get_enhance_prompt(topic_id, concept, source_bundle["md_context"], tested_block)
        runner = get_model_runner()
        model_config = {"provider": "openrouter", "model": "openrouter/free"}
        if os.getenv("NVIDIA_API_KEY") or os.getenv("nvidia"):
            model_config = {"provider": "nvidia", "model": "meta/llama-3.1-70b-instruct"}
            cb_key = f"nvidia:meta/llama-3.1-70b-instruct"
        else:
            cb_key = f"openrouter:openrouter/free"
        
        # Try up to 3 times in case of validation failures or minor LLM issues
        for attempt in range(1, 4):
            print(f"  [Attempt {attempt}] Generating lesson for Topic {topic_id} | Concept: {concept}...")
            response = runner._call_model(model_config, prompt, temperature=0.3, num_ctx=8192)
            if not response:
                print("  [-] Empty response from model. Waiting 30 seconds for rate limit cooldown...")
                import time
                time.sleep(30)
                # Reset circuit breaker
                if cb_key in runner.circuit_breakers:
                    runner.circuit_breakers[cb_key].failure_count = 0
                    runner.circuit_breakers[cb_key].cooldown_until = 0
                continue
                
            lesson_md = response.strip()
            if lesson_md.startswith("```"):
                lines = lesson_md.splitlines()
                lesson_md = "\n".join(lines[1:-1]).strip()
            
            if topic_id == 1:
                lesson_md = clean_topic_1_leaks(lesson_md, concept)
                
            validation = validate_lesson_markdown(lesson_md, topic_id=topic_id, concept=concept)
            if validation["is_valid"]:
                cleaned_md = validation["cleaned_markdown"]
                
                # Check if micro-challenge question stem got completely sanitized/deleted.
                # If there are options but no question text inside ### 5. Micro-Challenge, we patch it.
                if "### 5. Micro-Challenge" in cleaned_md:
                    parts = cleaned_md.split("### 5. Micro-Challenge")
                    challenge_sec = parts[1].split("### 6. 30-Second Recall")[0].strip()
                    lines = [l.strip() for l in challenge_sec.splitlines() if l.strip()]
                    
                    # If the section starts directly with choices and no descriptive question stem:
                    starts_with_choice = False
                    if lines:
                        first_line = lines[0].lower()
                        if first_line.startswith("a)") or first_line.startswith("a.") or first_line.startswith("- a"):
                            starts_with_choice = True
                            
                    if starts_with_choice or len(lines) < 2:
                        print("  [*] Patching missing question stem in Micro-Challenge...")
                        # Insert a generic fallback scenario-based stem that avoids the word "transaction"
                        stem = "A developer is designing a schema and needs to select the most appropriate representation. Which BSON type is the correct choice?"
                        if "decimal128" in challenge_sec.lower():
                            stem = "A developer needs to store a high-precision monetary value in a document. Which BSON type is the correct choice to guarantee exact decimal representation and avoid floating-point rounding errors?"
                        elif "array" in challenge_sec.lower() or "list" in challenge_sec.lower():
                            stem = "Which design pattern is best suited for matching nested structures or variable-length elements within a document?"
                        elif "insertone" in challenge_sec.lower():
                            stem = "Which statement correctly describes the outcome when a document is inserted using insertOne()?"
                            
                        # Re-insert the stem before the choices
                        cleaned_md = cleaned_md.replace("### 5. Micro-Challenge\n", f"### 5. Micro-Challenge\n{stem}\n\n")
                        cleaned_md = cleaned_md.replace("### 5. Micro-Challenge\r\n", f"### 5. Micro-Challenge\n{stem}\n\n")
                
                # Save to database
                timestamp = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
                artifact = {
                    "topic_id": int(topic_id),
                    "topic": target.topic,
                    "concept": concept,
                    "lesson_markdown": cleaned_md,
                    "source_files": source_bundle["source_files"],
                    "status": "validated",
                    "validation_issues": [],
                    "lesson_contract_version": LESSON_CONTRACT_VERSION,
                    "content_contract_version": CONTENT_CONTRACT_VERSION,
                    "generated_at": timestamp,
                    "validated_at": timestamp,
                    "updated_at": timestamp
                }
                database.upsert_lesson_artifact(artifact)
                
                # Export to local directory
                concept_snake = re.sub(r'[^a-z0-9]+', '_', concept.lower()).strip('_')
                export_dir = os.path.join("memory", "lessons")
                os.makedirs(export_dir, exist_ok=True)
                export_path = os.path.join(export_dir, f"topic_{topic_id:02d}_{concept_snake}.md")
                with open(export_path, "w", encoding="utf-8") as f:
                    f.write(cleaned_md)
                
                print(f"  [+] Success! Saved and exported to {export_path}")
                return True
            else:
                print("  [-] Validation failed:")
                for issue in validation["issues"]:
                    print(f"    * {issue}")
                    
        print(f"  [-] Failed to enhance {concept} after 3 attempts.")
        return False
        
    except Exception as e:
        print(f"  [-] Exception during enhancement: {e}")
        return False

def main():
    print("=== CertCoach Bulk Lesson Enhancer ===")
    syllabus = planner.load_syllabus()
    if not syllabus:
        print("[-] Error: Failed to load syllabus.")
        sys.exit(1)
        
    # Define concepts to skip (already enhanced)
    skipped_concepts = {
        (1, "BSON Data Types"),
        (1, "Document structure"),
        (1, "Collections vs Tables"),
        (2, "insertOne()"),
        (2, "insertMany()"),
        (2, "_id and ObjectId"),
        (3, "find()")
    }
    
    success_count = 0
    fail_count = 0
    
    for topic in syllabus:
        topic_id = int(topic["id"])
        topic_name = topic["topic"]
        concepts = topic["subtopics"]
        
        print(f"\nProcessing Topic {topic_id}: {topic_name}")
        print("-" * 50)
        
        for concept in concepts:
            concept_snake = re.sub(r'[^a-z0-9]+', '_', concept.lower()).strip('_')
            export_path = os.path.join("memory", "lessons", f"topic_{topic_id:02d}_{concept_snake}.md")
            
            # Check for hardcoded skips, topic_id=1/2/3_find files, or if the export file already exists.
            # BSON Data Types, Document structure, Collections vs Tables, insertOne, insertMany, id_and_objectid, and find were exported to memory/ directly.
            special_skips = {
                "bson_data_types", "document_structure", "collections_vs_tables",
                "insert_one", "insert_many", "id_and_objectid", "find"
            }
            is_special = concept_snake in special_skips or (concept_snake == "findone" and os.path.exists(os.path.join("memory", "lessons", "topic_03_findone.md")))
            
            if (topic_id, concept) in skipped_concepts or os.path.exists(export_path) or is_special:
                print(f"Skipping {concept} (already enhanced)")
                continue
                
            import time
            print(f"Enhancing Concept: {concept}...")
            time.sleep(10)
            if enhance_single_concept(topic_id, concept):
                success_count += 1
            else:
                fail_count += 1
                
    print("\n=== Enhancement Run Complete ===")
    print(f"Successfully Enhanced: {success_count}")
    print(f"Failed: {fail_count}")

if __name__ == "__main__":
    main()
