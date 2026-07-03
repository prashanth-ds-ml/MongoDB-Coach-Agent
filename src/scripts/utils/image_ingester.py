import os
import sys
import json
import base64
import requests
import time
from pathlib import Path

from dotenv import load_dotenv

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
IMAGE_DIR = os.path.join(PROJECT_ROOT, "data", "pics_qa")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "data", "extracted_questions.json")
OLLAMA_URL = "https://ollama.com/api/generate"
VISION_MODEL = "qwen3-vl:235b-instruct"

load_dotenv()
load_dotenv(os.path.expanduser("~/.certcoach/.env"))
API_KEY = os.getenv("ZHIPU_API_KEY", "")

SCHEMA_TEMPLATE = """
{
  "metadata": {
    "topic": "Identify the topic from the image (e.g. CRUD Operations, Indexes, Aggregation)",
    "difficulty": "Medium"
  },
  "context": {
    "scenario_description": "Any introductory context text provided before the question (e.g., 'United Airlines is...'). If none, leave blank.",
    "database_info": "Any mention of collections or databases in the prompt."
  },
  "question_text": "The exact question text asked in the image.",
  "options": [
    {
      "option_letter": "A", 
      "code_snippet": "The text or code for option A.",
      "is_correct": false,
      "feedback": "The explanation text given directly beneath this option in the screenshot. If no explanation is visible, infer why it might be wrong/right."
    }
  ]
}
"""

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def extract_question_from_image(image_path):
    print(f"👁️ Extracting data from: {os.path.basename(image_path)}", flush=True)
    base64_img = encode_image(image_path)
    
    prompt = f"""
    You are an expert OCR and MongoDB Certification analyzer.
    I am providing you with a screenshot of an official MongoDB learning path test question.
    
    Please extract ALL the text from this image and format it EXACTLY into this JSON schema:
    {SCHEMA_TEMPLATE}
    
    CRITICAL INSTRUCTIONS:
    1. Extract the text perfectly without typos.
    2. Ensure every single option (A, B, C, D) is captured in the "options" array.
    3. The screenshots often contain feedback text beneath EACH option (e.g., "Correct! The insertOne() method..."). Make sure you capture this text and put it into the "feedback" field for that specific option.
    4. Determine "is_correct" based on the feedback text in the image (e.g., if it says "Correct!", set it to true).
    """

    payload = {
        "model": VISION_MODEL,
        "prompt": prompt,
        "images": [base64_img],
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.0
        }
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(OLLAMA_URL, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            result = response.json()
            return json.loads(result.get("response", "{}"))
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}", flush=True)
            return None
    except Exception as e:
        print(f"❌ Exception during extraction: {e}", flush=True)
        return None

def main():
    print(f"🚀 Starting Bulk Image Ingestion using {VISION_MODEL}...")

    if not API_KEY:
        print("❌ ZHIPU_API_KEY is not set. Add it to ~/.certcoach/.env or a local .env file.")
        return

    if not os.path.exists(IMAGE_DIR):
        print(f"❌ Image directory not found: {IMAGE_DIR}")
        return
        
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"📸 Found {len(image_files)} images to process.")
    
    extracted_data = []
    
    # Load existing if we are resuming
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r") as f:
                extracted_data = json.load(f)
            print(f"📂 Loaded {len(extracted_data)} existing extractions. Resuming...")
        except Exception:
            pass

    processed_files = {item.get("source_file") for item in extracted_data}
    
    for idx, img_file in enumerate(image_files):
        if img_file in processed_files:
            continue
            
        img_path = os.path.join(IMAGE_DIR, img_file)
        start_time = time.time()
        
        data = extract_question_from_image(img_path)
        
        if data:
            data["source_file"] = img_file  # track source
            extracted_data.append(data)
            
            # Save incrementally
            with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
                json.dump(extracted_data, f, indent=4)
                
            elapsed = time.time() - start_time
            print(f"✅ Success! Extracted in {elapsed:.1f}s. Saved to JSON.")
        else:
            print(f"⚠️ Failed to extract {img_file}.")
            
        # Optional: Add a small delay so we don't melt the local GPU
        time.sleep(1)

    print(f"\n🎉 Extraction Complete! Total questions saved: {len(extracted_data)}")

if __name__ == "__main__":
    main()
