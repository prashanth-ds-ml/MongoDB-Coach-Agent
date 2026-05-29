import os
import json
import uuid
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in environment variables. Please check your .env file.")

LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")
MODEL = "qwen3.5:latest"

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SYLLABUS_FILE = os.path.join(PROJECT_ROOT, "data", "syllabus.json")
QUESTIONS_FILE = os.path.join(PROJECT_ROOT, "data", "extracted_questions.json")
TAGGED_QUESTIONS_FILE = os.path.join(PROJECT_ROOT, "data", "extracted_questions_tagged.json")

def get_topic_keys():
    with open(SYLLABUS_FILE, "r", encoding="utf-8") as f:
        syllabus = json.load(f)
    
    keys = set()
    for item in syllabus:
        for key in item.get("bank_topic_keys", []):
            keys.add(key)
    return sorted(list(keys))

def query_ollama_for_tag(question_text, topics):
    prompt = f"""
You are an expert MongoDB Certification categorizer.
I will give you a certification question. You must categorize it into EXACTLY ONE of the following official topics:

{json.dumps(topics, indent=2)}

Question:
\"\"\"
{question_text}
\"\"\"

Reply with ONLY the exact name of the topic from the list. Do not include any other text, quotes, or explanations.
    """
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.0
        }
    }
    
    try:
        response = requests.post(f"{LOCAL_LLM_URL}/api/generate", json=payload, timeout=60)
        response.raise_for_status()
        result = response.json().get("response", "").strip().strip('\'"')
        
        # Fallback if the model outputs something weird
        best_match = None
        for t in topics:
            if t.lower() in result.lower():
                best_match = t
                break
                
        return best_match if best_match else result
    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return "Unknown Topic"

def main():
    print(f"Loading syllabus topics...")
    topics = get_topic_keys()
    print(f"Found {len(topics)} topic keys: {topics}")
    
    if not os.path.exists(QUESTIONS_FILE):
        print(f"Questions file not found: {QUESTIONS_FILE}")
        return
        
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    print(f"Found {len(questions)} questions. Starting tagging process with {MODEL}...")
    
    for i, q in enumerate(questions):
        print(f"Tagging {i+1}/{len(questions)}: {q['question_text'][:50]}...", end=" ")
        
        q_text = q.get("question_text", "")
        if not q_text and q.get("options"):
            q_text = "Context: " + str(q.get("context", {})) + "\nOptions: " + str(q.get("options"))
            
        topic = query_ollama_for_tag(q_text, topics)
        
        if "metadata" not in q:
            q["metadata"] = {}
            
        q["metadata"]["topic"] = topic
        print(f"-> {topic}")
        
    print("\nTagging complete. Saving tagged questions...")
    with open(TAGGED_QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=4)
        
    print(f"Connecting to MongoDB Atlas...")
    client = MongoClient(MONGO_URI)
    db = client["certcoach_db"]
    questions_col = db["questions"]
    
    print("Clearing existing questions in Atlas...")
    questions_col.delete_many({})
    
    for q in questions:
        if "_id" not in q or not q["_id"]:
            q["_id"] = str(uuid.uuid4())
            
    print(f"Inserting {len(questions)} questions into Atlas...")
    result = questions_col.insert_many(questions)
    print(f"Successfully inserted {len(result.inserted_ids)} questions.")
    
    questions_col.create_index("metadata.topic")
    print("Created index on metadata.topic")

if __name__ == "__main__":
    main()
