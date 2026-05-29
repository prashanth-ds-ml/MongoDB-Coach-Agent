import os
import json
import uuid
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in environment variables. Please check your .env file.")

client = MongoClient(MONGO_URI)
db = client["certcoach_db"]
questions_col = db["questions"]

# Path to the extracted questions
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
QUESTIONS_FILE = os.path.join(PROJECT_ROOT, "data", "extracted_questions.json")

def seed_db():
    print(f"Connecting to MongoDB Atlas at {MONGO_URI.split('@')[1]}...")
    if not os.path.exists(QUESTIONS_FILE):
        print(f"File not found: {QUESTIONS_FILE}")
        return

    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)

    if not questions:
        print("No questions found in JSON.")
        return

    print(f"Found {len(questions)} questions in JSON. Clearing existing questions in Atlas...")
    questions_col.delete_many({})

    # Ensure all have an _id that MongoDB accepts
    for q in questions:
        if "_id" not in q or not q["_id"]:
            q["_id"] = str(uuid.uuid4())

    print(f"Inserting {len(questions)} questions into Atlas...")
    result = questions_col.insert_many(questions)
    
    print(f"Successfully inserted {len(result.inserted_ids)} questions.")
    
    # Optional: Create an index on topic for faster retrieval
    questions_col.create_index("metadata.topic")
    print("Created index on metadata.topic")

if __name__ == "__main__":
    seed_db()
