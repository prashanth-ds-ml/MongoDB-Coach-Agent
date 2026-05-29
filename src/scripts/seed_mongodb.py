import os
import json
import uuid
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from dotenv import load_dotenv

def seed_database():
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        print("Error: MONGO_URI not found in environment variables.")
        return

    print("Connecting to MongoDB...")
    client = MongoClient(mongo_uri)
    db = client["certcoach_db"]
    questions_col = db["questions"]

    # Load extracted questions
    data_path = os.path.join(os.path.dirname(__file__), "../../data/extracted_questions.json")
    if not os.path.exists(data_path):
        print(f"Error: Could not find {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        raw_questions = json.load(f)

    print(f"Loaded {len(raw_questions)} questions from extracted_questions.json.")

    # Create unique index on question_text to prevent duplicates (ignore if it fails due to existing dupes)
    try:
        questions_col.create_index("question_text", unique=True)
    except Exception as e:
        print(f"Warning: Could not create unique index: {e}")

    success_count = 0
    duplicate_count = 0
    skipped_count = 0

    for q in raw_questions:
        if not q.get("question_text", "").strip():
            skipped_count += 1
            continue
            
        # Give it a unique _id if it doesn't have one
        if "_id" not in q:
            q["_id"] = str(uuid.uuid4())
            
        # Ensure it has the structure expected by the app
        if "global_metrics" not in q:
            q["global_metrics"] = {
                "total_attempts": 0,
                "correct_attempts": 0
            }

        # Handle nested fields safely
        if "metadata" not in q:
            q["metadata"] = {"topic": "General", "difficulty": "Medium"}

        try:
            questions_col.insert_one(q)
            success_count += 1
        except Exception as e:
            # Handle duplicate key error (code 11000)
            if hasattr(e, "code") and e.code == 11000 or "duplicate key error" in str(e):
                duplicate_count += 1
            else:
                print(f"Error inserting question: {e}")

    print("\n--- Seeding Complete ---")
    print(f"Successfully inserted: {success_count}")
    print(f"Skipped (duplicates):  {duplicate_count}")
    print(f"Skipped (empty text):  {skipped_count}")
    print(f"Total in collection:   {questions_col.count_documents({})}")

if __name__ == "__main__":
    seed_database()
