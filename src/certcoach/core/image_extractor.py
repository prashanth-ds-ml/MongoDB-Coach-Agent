import os
import sys
import json
import uuid
from datetime import datetime
import ollama
from pymongo import MongoClient

# Add source path to import database config
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, "../..")))

from certcoach.core import database

IMAGE_DIR = os.path.abspath(os.path.join(_HERE, "../data/pics_qa"))
MANIFEST_FILE = os.path.join(IMAGE_DIR, "extraction_manifest.json")

def load_manifest() -> dict:
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_manifest(manifest: dict):
    try:
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4)
    except Exception as e:
        print(f"Warning: Could not save extraction manifest: {e}")

def check_vision_model_loaded() -> bool:
    """Verifies if the 'llava' vision model is pulled and available in Ollama."""
    try:
        models_list = ollama.list()
        for m in models_list.get("models", []):
            if "llava" in m.get("name", ""):
                return True
    except Exception:
        pass
    return False

def extract_question_from_image(image_path: str) -> dict:
    """
    Extracts question, options, correct answer, and explanation from a screenshot.
    Uses 'llava' local vision model and enforces the strict Question Generation Rulebook.
    """
    prompt = (
        "You are CertCoach, an expert MongoDB Certification Instructor.\n"
        "Extract the MongoDB multiple-choice question from this screenshot.\n\n"
        "STRICT QUESTION GENERATION RULES:\n"
        "1. Identify the question text, code snippets, and 4 multiple-choice options (labeled A, B, C, D).\n"
        "2. Identify the single correct option based on standard MongoDB functionality.\n"
        "3. Map this question to one of these exact syllabus topics:\n"
        "   - MongoDB Overview & The Document Model\n"
        "   - CRUD Operations - Create\n"
        "   - CRUD Operations - Read (Basic & Cursor)\n"
        "   - CRUD Operations - Update\n"
        "   - CRUD Operations - Delete\n"
        "   - Query Operators (L2/L3/L5)\n"
        "   - Querying Arrays & Subdocuments\n"
        "   - Aggregation Framework\n"
        "   - Indexes & Performance\n"
        "   - Data Modeling\n"
        "   - MongoDB Drivers & PyMongo\n"
        "   - Tools, Tooling & Atlas Search\n"
        "4. Compose a comprehensive explanation following the 6-part structure:\n"
        "   - Correct Answer: [Letter and exact syntax]\n"
        "   - Why Correct: [Brief detailed rationale]\n"
        "   - Why Other Options Are Wrong: [Teardown of each incorrect option]\n"
        "   - Exam Trap: [Common misconception warning]\n"
        "   - Memory Hook: [Short mnemonic or conceptual rule]\n"
        "   - Follow-Up Practice Recommendation: [Doc citation suggestion]\n\n"
        "Return the output strictly in a valid JSON structure (no markdown wrapper, no extra text) matching this schema:\n"
        "{\n"
        "  \"topic\": \"Syllabus Topic String\",\n"
        "  \"difficulty\": \"Easy\" | \"Medium\" | \"High\",\n"
        "  \"question\": \"The clear prompt text.\",\n"
        "  \"options\": [\n"
        "    \"Option A text or code\",\n"
        "    \"Option B text or code\",\n"
        "    \"Option C text or code\",\n"
        "    \"Option D text or code\"\n"
        "  ],\n"
        "  \"correct_answer\": \"Option A text or code matching exactly\",\n"
        "  \"trap_analysis\": \"The detailed 6-part explanation template here\"\n"
        "}"
    )

    try:
        response = ollama.chat(
            model='llava',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_path]
            }],
            options={"temperature": 0.1}
        )
        content = response.get("message", {}).get("content", "").strip()
        
        # Strip markdown json blocks if present
        if content.startswith("```"):
            lines = content.splitlines()
            if lines[0].startswith("```json") or lines[0].startswith("```"):
                content = "\n".join(lines[1:-1])
                
        mcq_data = json.loads(content)
        return mcq_data
    except Exception as e:
        print(f"Error during vision extraction on {os.path.basename(image_path)}: {e}")
        return None

def process_pics_qa(limit: int = None, dry_run: bool = False):
    """
    Main extraction pipeline scanning pics_qa and populating the MongoDB bank.
    """
    database.check_connection()
    
    if not os.path.exists(IMAGE_DIR):
        print(f"Error: Directory {IMAGE_DIR} does not exist.")
        return
        
    if not check_vision_model_loaded() and not dry_run:
        print("\n[!] Local vision model 'llava' is not loaded in Ollama.")
        print("Please run 'ollama pull llava' in your terminal and verify it via 'ollama list' before running extraction.\n")
        return

    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not images:
        print("No screenshots found in pics_qa.")
        return

    print(f"Found {len(images)} screenshots in pics_qa.")
    manifest = load_manifest()
    
    processed_count = 0
    extracted_count = 0
    
    for idx, img_name in enumerate(images):
        if limit and processed_count >= limit:
            break
            
        img_path = os.path.join(IMAGE_DIR, img_name)
        
        # Check if already successfully processed
        if manifest.get(img_name, {}).get("status") == "success":
            continue
            
        print(f"\n[{processed_count + 1}] Processing {img_name}...")
        processed_count += 1
        
        if dry_run:
            print(f"[Dry-Run] Would extract {img_name} using llava.")
            continue
            
        mcq_data = extract_question_from_image(img_path)
        if not mcq_data:
            manifest[img_name] = {
                "status": "failed",
                "processed_at": datetime.utcnow().isoformat(),
                "error": "Failed to parse model output"
            }
            save_manifest(manifest)
            continue
            
        # Structure question matching standard Ultimate Schema
        mcq_data["topic"] = mcq_data.get("topic", "MongoDB Overview & The Document Model")
        mcq_data["difficulty"] = mcq_data.get("difficulty", "Medium")
        mcq_data["citation_source"] = f"pics_qa/{img_name}"
        mcq_data["explanation"] = mcq_data.get("trap_analysis", "")
        
        try:
            # Check duplicate in production bank
            existing = database.questions_col.find_one({"question_text": mcq_data.get("question")})
            if existing:
                print(f"-> Question from {img_name} already exists in production bank. Skipping insertion.")
                manifest[img_name] = {
                    "status": "success",
                    "processed_at": datetime.utcnow().isoformat(),
                    "question_id": existing["_id"],
                    "note": "duplicate skipped"
                }
                save_manifest(manifest)
                continue
                
            # Insert into database
            q_id = database.save_generated_question(mcq_data)
            extracted_count += 1
            print(f"-> Successfully extracted and saved question from {img_name} with ID: {q_id}")
            
            manifest[img_name] = {
                "status": "success",
                "processed_at": datetime.utcnow().isoformat(),
                "question_id": q_id
            }
            save_manifest(manifest)
            
        except Exception as e:
            print(f"Error saving question from {img_name}: {e}")
            manifest[img_name] = {
                "status": "failed",
                "processed_at": datetime.utcnow().isoformat(),
                "error": str(e)
            }
            save_manifest(manifest)

    print(f"\nProcessing finished. Attempted: {processed_count}, Successfully Extracted & Saved: {extracted_count}.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CertCoach Visual Question Extractor")
    parser.add_argument("--limit", type=int, help="Limit number of images to process")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without calling LLM or writing to DB")
    args = parser.parse_args()
    
    process_pics_qa(limit=args.limit, dry_run=args.dry_run)
