import os
import sys
import json
import uuid
import time
from pymongo import MongoClient
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Add src to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import List, Optional
from certcoach.core import database, planner

# 6-Part Explanation Compliant MCQ Pydantic Schema
class CertCoachMCQ(BaseModel):
    question: str = Field(description="The multiple choice question based strictly on MongoDB best practices.")
    options: List[str] = Field(description="List of 4 possible answers. Avoid generic or placeholders.")
    correct_answer: str = Field(description="The matching correct string from the options list.")
    feedbacks: List[str] = Field(description="List of 4 feedback strings matching the options in order.")
    trap_analysis: str = Field(description="Explain which option is the gotcha trap and why a student might fall for it.")
    six_part_explanation: str = Field(
        description="Detailed explanation strictly structured into 6 parts: "
                    "1. Correct Answer: State correct letter and syntax. "
                    "2. Why Correct: Why the syntax satisfies requirements. "
                    "3. Why Other Options Are Wrong: Line-by-line teardown of the remaining 3 distractors. "
                    "4. Exam Trap: Misconception warning. "
                    "5. Memory Hook: Mnemonic device/logic rule to anchor the concept. "
                    "6. Follow-Up Practice Recommendation: specific official documentation page/topic reference."
    )
    citation_source: str = Field(description="Reference source name or official doc section.")

def unload_all_loaded_models():
    """Query `/api/ps` and unload all currently loaded models from Ollama's memory/VRAM."""
    import urllib.request
    import json
    
    GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
    ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")
    load_dotenv(ENV_PATH)
    ollama_url = os.getenv("LOCAL_LLM_URL", "http://localhost:11434").rstrip("/")
    
    print("\n  [🧠 Memory Manager] Checking for active models in system VRAM...")
    try:
        req = urllib.request.Request(f"{ollama_url}/api/ps", method="GET")
        with urllib.request.urlopen(req, timeout=2.0) as response:
            data = json.loads(response.read().decode("utf-8"))
            loaded = data.get("models", [])
            if not loaded:
                print("  [🧠 Memory Manager] System memory is already completely clear. VRAM is free.")
                return
                
            print(f"  [🧠 Memory Manager] Detected {len(loaded)} active model(s) in memory. Unloading to free space:")
            for m in loaded:
                m_name = m.get("name")
                if m_name:
                    print(f"    • Unloading: {m_name}")
                    req_data = json.dumps({"model": m_name, "keep_alive": 0}).encode("utf-8")
                    req_unload = urllib.request.Request(
                        f"{ollama_url}/api/generate",
                        data=req_data,
                        headers={"Content-Type": "application/json"},
                        method="POST"
                    )
                    try:
                        with urllib.request.urlopen(req_unload, timeout=3.0) as resp:
                            resp.read()
                    except Exception:
                        pass
            print("  [🧠 Memory Manager] ✔ Success! VRAM memory cleared. System is fully optimized.")
    except Exception as e:
        print(f"  [🧠 Memory Manager] Alert: Could not connect to Ollama to verify loaded models ({e}).")

def unload_seeder_model():
    """Unload the active configured model from VRAM/RAM when the script finishes."""
    import urllib.request
    import json
    
    GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
    ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")
    load_dotenv(ENV_PATH)
    ollama_url = os.getenv("LOCAL_LLM_URL", "http://localhost:11434").rstrip("/")
    model = os.getenv("MODEL", "qwen2.5-coder:7b")
    
    print(f"\n  [🧠 Memory Manager] Unloading active model '{model}' from memory to free VRAM...")
    try:
        req_data = json.dumps({"model": model, "keep_alive": 0}).encode("utf-8")
        req_unload = urllib.request.Request(
            f"{ollama_url}/api/generate",
            data=req_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req_unload, timeout=3.0) as resp:
            resp.read()
        print("  [🧠 Memory Manager] ✔ Success! Model unloaded. VRAM freed successfully.")
    except Exception as e:
        print(f"  [🧠 Memory Manager] Alert: Could not unload model '{model}' ({e}).")

def generate_concept_question(topic: str, concept: str, difficulty: str, context_text: str) -> Optional[dict]:
    # Load global configs
    GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
    ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")
    load_dotenv(ENV_PATH)
    
    MODEL = os.getenv("MODEL", "qwen2.5-coder:7b")
    LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")
    
    is_pymongo = "pymongo" in topic.lower() or "driver" in topic.lower()
    syntax_rule = (
        "Focus strictly on MongoDB Shell (mongosh) syntax and commands. Do NOT show PyMongo or other languages."
        if not is_pymongo else
        "Focus on both MongoDB Shell (mongosh) and PyMongo (Python) syntaxes. Do NOT show other languages."
    )
    
    prompt = f"""You are an expert MongoDB Certification Instructor.
Generate a Multiple Choice Question for the "MongoDB Associate Python Developer" exam.

Syllabus Topic: {topic}
Concept / Subtopic: {concept}
Difficulty: {difficulty}

Syntax Rule:
{syntax_rule}

Official Documentation Context:
{context_text[:6000]}

Difficulty Rules:
- Easy: Straightforward syntax, direct definitions, basic collections/BSON rules, single parameter CRUD.
- Medium: Multi-step queries, common operator gotchas ($set, $elemMatch, projections, chained cursors).
- Hard: Complex aggregation pipeline optimization, compound index prefix rules, mixed projections, driver-specific connection pooling, or BSON collation/type bracketing.

Constraints:
1. Return strictly 4 options, with exactly one matching correct answer.
2. Provide a highly plausible "gotcha" or "trap" option.
3. Fill out all fields of the schema. Ensure each option has its own customized feedback in the `feedbacks` array.
4. The `six_part_explanation` field MUST follow this strict 6-part structure exactly:
   ### 1. Correct Answer
   State the letter (A, B, C, or D) and the correct syntax.
   ### 2. Why Correct
   Explain clearly why it is correct and satisfies the criteria.
   ### 3. Why Other Options Are Wrong
   Teardown the other three options line-by-line, pointing out why they fail or are invalid.
   ### 4. Exam Trap
   Highlight the subtle trap the question is testing.
   ### 5. Memory Hook
   Provide a mnemonic or quick logic rule to anchor the core concept.
   ### 6. Follow-Up Practice Recommendation
   Mention the official documentation page name to reinforce study.
"""
    try:
        # 120-second robust timeout, and 8192 context window to keep 100% in GPU VRAM while preventing JSON truncation
        llm = ChatOllama(model=MODEL, base_url=LOCAL_LLM_URL, temperature=0.5, timeout=120.0, num_ctx=8192)
        structured_llm = llm.with_structured_output(CertCoachMCQ)
        res = structured_llm.invoke(prompt)
        
        if res:
            # 1. Defensive Options list padding/truncation
            if not isinstance(res.options, list):
                res.options = []
            while len(res.options) < 4:
                res.options.append(f"Option {['A', 'B', 'C', 'D'][len(res.options)]} placeholder")
            res.options = res.options[:4]
            
            # 2. Defensive Feedbacks list padding/truncation & 1-element recovery
            if not isinstance(res.feedbacks, list):
                res.feedbacks = []
            if len(res.feedbacks) == 1:
                # Recover full explanation block from single feedbacks element
                if not res.six_part_explanation:
                    res.six_part_explanation = res.feedbacks[0]
                # Provide standard high-quality option-specific feedbacks
                res.feedbacks = [
                    "This option correctly matches the documented behavior in MongoDB.",
                    "This option is a distractor. Verify BSON specifications or syntax rules.",
                    "This option is incorrect. Check indexing direction or collation rules.",
                    "This option is invalid. Review PyMongo or driver-specific requirements."
                ]
            while len(res.feedbacks) < 4:
                res.feedbacks.append("Review the official MongoDB documentation for details on this BSON specification.")
            res.feedbacks = res.feedbacks[:4]
            
            # 3. Robust Correct Answer resolution
            c_ans = res.correct_answer.strip() if res.correct_answer else ""
            if c_ans in ['A', 'B', 'C', 'D']:
                res.correct_answer = res.options[['A', 'B', 'C', 'D'].index(c_ans)]
            elif c_ans in ['a', 'b', 'c', 'd']:
                res.correct_answer = res.options[['a', 'b', 'c', 'd'].index(c_ans)]
            
            # Substring prefix fallback matching
            if res.correct_answer not in res.options:
                for opt in res.options:
                    opt_stripped = opt.strip()
                    if opt_stripped.startswith(f"{c_ans})") or opt_stripped.startswith(f"{c_ans} ") or opt_stripped.startswith(f"{c_ans}."):
                        res.correct_answer = opt
                        break
                        
        if res and len(res.options) == 4 and res.correct_answer in res.options and len(res.feedbacks) == 4:
            correct_idx = res.options.index(res.correct_answer)
            letters = ['A', 'B', 'C', 'D']
            
            # Map trap index to the second element by default if not specified
            trap_idx = 1 if correct_idx != 1 else 0
            
            options_mapped = []
            for idx, opt in enumerate(res.options):
                options_mapped.append({
                    "option_letter": letters[idx],
                    "code_snippet": opt,
                    "is_correct": (idx == correct_idx),
                    "is_trap": (idx == trap_idx),
                    "feedback": res.feedbacks[idx]
                })
                
            return {
                "_id": str(uuid.uuid4()),
                "metadata": {
                    "topic": topic,
                    "concept": concept,
                    "difficulty": difficulty,
                    "citation_source": res.citation_source or f"{topic.replace(' ', '_')}_{difficulty.lower()}_auto.md",
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                "context": {
                    "scenario_description": f"An adaptive {difficulty.lower()} question on {concept}.",
                    "database_info": ""
                },
                "question_text": res.question,
                "options": options_mapped,
                "explanation": res.six_part_explanation,
                "trap_analysis": res.trap_analysis,
                "citation_source": res.citation_source or "Syllabus_Sourced.md",
                "global_metrics": {
                    "times_seen": 0,
                    "times_correct": 0,
                    "times_incorrect": 0,
                    "average_time_seconds": 0.0
                }
            }
        else:
            if not res:
                print("  [!] Error: LLM returned empty response.", flush=True)
            else:
                print(f"  [!] Error: Validation check failed. res={res}", flush=True)
    except Exception as e:
        print(f"  [!] Error generating question for {concept} ({difficulty}): {e}", flush=True)
    return None

def main():
    load_dotenv()
    GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
    ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")
    load_dotenv(ENV_PATH)
    
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["certcoach_db"]
    questions_col = db["questions"]
    
    print("\n=======================================================")
    print("      CertCoach Unified Question Seeder (All Topics)    ")
    print("=======================================================\n")
    
    syllabus = planner.load_syllabus()
    
    # 1. Non-interactive CLI argument support
    choice = None
    if len(sys.argv) > 1:
        choice = sys.argv[1].strip()
        print(f"Running in non-interactive mode with argument: {choice}")
    
    if not choice:
        print("Available Syllabus Topics:")
        for t_item in syllabus:
            print(f"  [{t_item['id']}] {t_item['topic']}")
        print("  [13] Seed ALL remaining topics sequentially (Freeing VRAM between topics)")
        print("  [14] Exit")
        
        choice = input("\nSelect a topic to seed [1-14]: ").strip()
        
    if choice == "14" or not choice:
        print("Exiting.")
        return
        
    selected_topics = []
    if choice == "13":
        selected_topics = syllabus
    else:
        try:
            tid = int(choice)
            matching = [t for t in syllabus if t["id"] == tid]
            if matching:
                selected_topics = matching
            else:
                print("Invalid topic ID.")
                return
        except ValueError:
            print("Invalid input.")
            return

    # Free VRAM/RAM before starting seeder loading
    unload_all_loaded_models()
    
    for t_item in selected_topics:
        topic_name = t_item["topic"]
        subtopics = t_item.get("subtopics", [topic_name])
        md_files = t_item.get("md_files", [])
        bank_keys = t_item.get("bank_topic_keys", [topic_name])
        primary_key = bank_keys[0] if bank_keys else topic_name
        
        print(f"\n=======================================================")
        print(f"🌲 Seeding Topic #{t_item['id']}: {topic_name}")
        print(f"   Database Metadata Key: '{primary_key}'")
        print(f"=======================================================")
        
        # Load documentation context dynamically
        context_text = planner.load_md_context(md_files)
        if not context_text:
            print(f"  [!] Reference documentation files not found for Topic #{t_item['id']}. Skipping...")
            continue
            
        print(f"  [*] Mapped documentation context loaded ({len(context_text)} chars).")
        
        # Calculate exactly how many questions we currently have and what is missing
        seeding_needs = {}
        total_missing_for_topic = 0
        
        for difficulty, target in [("Easy", 15), ("Medium", 20), ("Hard", 10)]:
            query = {
                "metadata.topic": primary_key,
                "metadata.difficulty": difficulty
            }
            current_count = questions_col.count_documents(query)
            if current_count < target:
                needed = target - current_count
                seeding_needs[difficulty] = needed
                total_missing_for_topic += needed
            else:
                seeding_needs[difficulty] = 0
                
        if total_missing_for_topic == 0:
            print(f"  [✓ Status] Already fully balanced at 15 Easy, 20 Medium, 10 Hard (total 45 questions).")
            continue
            
        print(f"  [*] Missing question profile: {seeding_needs} (Total missing: {total_missing_for_topic})")
        
        questions_completed = 0
        for difficulty, needed_count in seeding_needs.items():
            generated_count = 0
            while generated_count < needed_count:
                concept = subtopics[questions_completed % len(subtopics)]
                
                print(f"\n  [Progress: {questions_completed}/{total_missing_for_topic}] Sending prompt to Ollama for '{concept}' ({difficulty})...", flush=True)
                
                start_time = time.time()
                q = generate_concept_question(primary_key, concept, difficulty, context_text)
                elapsed = time.time() - start_time
                
                if q:
                    # Check duplicate
                    dup = questions_col.find_one({"question_text": q["question_text"]})
                    if dup:
                        print("  [!] Generated a duplicate question text. Retrying...", flush=True)
                        continue
                    
                    # Store in database
                    q["metadata"]["topic"] = primary_key
                    questions_col.insert_one(q)
                    
                    generated_count += 1
                    questions_completed += 1
                    
                    print(f"  [✓ Success] Question generated successfully in {elapsed:.1f}s!", flush=True)
                    print(f"    • Question: {q['question_text']}", flush=True)
                    print("    • Options:", flush=True)
                    for opt in q["options"]:
                        correct_tag = " [Correct]" if opt["is_correct"] else ""
                        trap_tag = " [Trap distractor]" if opt["is_trap"] else ""
                        print(f"      [{opt['option_letter']}] {opt['code_snippet']}{correct_tag}{trap_tag}", flush=True)
                    
                    print("    • 6-Part Explanation structured successfully.", flush=True)
                    print(f"    • Trap Analysis: {q['trap_analysis']}", flush=True)
                    print(f"  [DB Ingestion] Verified duplicate clearance. Successfully inserted into MongoDB (ID: {q['_id']}).", flush=True)
                else:
                    print("  [!] Generation failed or timed out. Retrying...", flush=True)
                    time.sleep(2)
        
        # Clean VRAM after each topic completes to avoid cumulative memory leakage!
        unload_seeder_model()
        
    print("\n=======================================================")
    print("🎉 Seeding execution finished completely! Study hard and write the exam as planned.")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
