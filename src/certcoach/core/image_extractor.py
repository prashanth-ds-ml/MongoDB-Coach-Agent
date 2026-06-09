import os
import sys
import json
import uuid
from datetime import datetime, timezone
import ollama
from pymongo import MongoClient

# Add source path to import database config
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, "../..")))

from certcoach.core import database

IMAGE_DIR = os.path.abspath(os.path.join(_HERE, "../data/pics_qa"))
MANIFEST_FILE = os.path.join(IMAGE_DIR, "extraction_manifest.json")

TOPIC_ALIASES = {
    "CRUD Operations - Read (Basic & Cursor)": "CRUD Operations - Read",
    "Query Operators (L2/L3/L5)": "Query Operators & MQL",
    "Querying Arrays & Subdocuments": "Querying Arrays & Embedded Documents",
    "MongoDB Atlas & Operations": "Tools, Tooling & Atlas Search",
}


def normalize_topic_name(topic: str) -> str:
    topic = (topic or "").strip()
    return TOPIC_ALIASES.get(topic, topic)

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
    """Verifies if any supported vision model (glm-ocr or llava) is pulled and available in Ollama."""
    return get_available_vision_model() is not None

def get_available_vision_model() -> str:
    """Returns 'glm-ocr' if present, fallback to 'llava' if present, otherwise None."""
    try:
        models_list = ollama.list()
        models = getattr(models_list, "models", [])
        model_names = [getattr(m, "model", "") for m in models]
        
        # Prioritize glm-ocr
        for name in model_names:
            if "glm-ocr" in name:
                return "glm-ocr"
                
        # Fallback to llava
        for name in model_names:
            if "llava" in name:
                return "llava"
    except Exception:
        pass
    return None

def extract_question_from_image(image_path: str) -> dict:
    """
    Extracts question, options, correct answer, and explanation from a screenshot.
    Uses a robust Double-Pass Pipeline:
    - Pass 1: Multimodal vision model (prioritizing glm-ocr, fallback to llava) extracts the raw textual content.
    - Pass 2: High-accuracy model (qwen2.5:7b) parses, structures, validates, and builds
              the detailed seven-part explanation strictly adhering to the Question Generation Rulebook.
    """
    vision_model = get_available_vision_model()
    if not vision_model:
        print("  [!] Error: No vision model ('glm-ocr' or 'llava') is available in Ollama.")
        return None

    pass1_prompt = (
        "You are an expert OCR and text extractor assistant.\n"
        "Look at this screenshot and extract the multiple choice question exactly as written.\n"
        "Identify:\n"
        "- The main question prompt\n"
        "- Any code blocks or snippets\n"
        "- The options (A, B, C, D) with their contents\n"
        "- The correct answer (or identify which one is correct if indicated)\n"
        "- Any explanation or notes if visible\n\n"
        "Do not worry about JSON formatting or database schemas. Just output the extracted details in clear, structured Markdown."
    )

    try:
        print(f"  -> Pass 1: Running local vision OCR...")
        response_pass1 = ollama.chat(
            model=vision_model,
            messages=[{
                'role': 'user',
                'content': pass1_prompt,
                'images': [image_path]
            }],
            options={"temperature": 0.1}
        )
        raw_ocr_text = response_pass1.get("message", {}).get("content", "").strip()
        
        if not raw_ocr_text:
            print("  [!] Pass 1 returned empty text.")
            return None
            
        print(f"  -> Pass 2: Structuring and validating question against the Rulebook...")
        
        pass2_prompt = (
            "You are CertCoach, an expert MongoDB Certification Instructor.\n"
            "You will take the raw OCR text extracted from an exam screenshot and format it into a "
            "perfect multiple-choice question matching the official syllabus and strict quality guidelines.\n\n"
            f"RAW EXTRACTED OCR TEXT:\n"
            f"```\n{raw_ocr_text}\n```\n\n"
            "STRICT QUALITY & PEDAGOGICAL RULES:\n"
            "1. Enforce exactly 4 options: A, B, C, D. If the raw text lacks 4 options, construct plausible distractors.\n"
            "2. Identify the single correct option based on standard MongoDB functionality.\n"
            "3. Map the question to one of these exact syllabus topics:\n"
            "   - MongoDB Overview & The Document Model\n"
            "   - CRUD Operations - Create\n"
            "   - CRUD Operations - Read\n"
            "   - CRUD Operations - Update\n"
            "   - CRUD Operations - Delete\n"
            "   - Query Operators & MQL\n"
            "   - Querying Arrays & Embedded Documents\n"
            "   - Aggregation Framework\n"
            "   - Indexes & Performance\n"
            "   - Data Modeling\n"
            "   - MongoDB Drivers & PyMongo\n"
            "   - Tools, Tooling & Atlas Search\n"
            "4. Construct a high-fidelity explanation strictly in the following 7-part structure:\n"
            "   - ### 1. Correct Answer: [Letter and exact syntax]\n"
            "   - ### 2. Why Correct: [Detailed developer rationale]\n"
            "   - ### 3. Why Other Options Are Wrong: [Teardown of each incorrect option]\n"
            "   - ### 4. Exam Trap: [Common student misconception warning]\n"
            "   - ### 5. Memory Hook: [Short conceptual mnemonic or rule]\n"
            "   - ### 6. Follow-Up Practice Recommendation: [Doc citation suggestion]\n"
            "   - ### 7. Syntax Example: [Code block of syntax example, or 'Not required for this concept.']\n\n"
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
            "  \"correct_answer\": \"Option text or code matching the correct choice exactly\",\n"
            "  \"trap_analysis\": \"The detailed seven-part explanation template here\"\n"
            "}"
        )
        
        response_pass2 = ollama.chat(
            model='qwen2.5:7b',
            messages=[{
                'role': 'user',
                'content': pass2_prompt
            }],
            options={"temperature": 0.1}
        )
        content = response_pass2.get("message", {}).get("content", "").strip()
        
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
        print("\n[!] No local vision model ('glm-ocr' or 'llava') is loaded in Ollama.")
        print("Please run 'ollama pull glm-ocr' or 'ollama pull llava' in your terminal and verify it via 'ollama list' before running extraction.\n")
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
                "processed_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
                "error": "Failed to parse model output"
            }
            save_manifest(manifest)
            continue
            
        # Structure question matching standard Ultimate Schema
        mcq_data["topic"] = normalize_topic_name(
            mcq_data.get("topic", "MongoDB Overview & The Document Model")
        )
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
                    "processed_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
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
                "processed_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
                "question_id": q_id
            }
            save_manifest(manifest)
            
        except Exception as e:
            print(f"Error saving question from {img_name}: {e}")
            manifest[img_name] = {
                "status": "failed",
                "processed_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
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
