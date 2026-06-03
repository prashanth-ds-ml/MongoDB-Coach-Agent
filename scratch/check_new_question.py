import os
import dotenv
from pymongo import MongoClient

GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")
dotenv.load_dotenv(ENV_PATH)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["certcoach_db"]
questions_col = db["questions"]

print("=== Verification of Newly Generated Questions ===")
# Find a recently created question or one that has a long explanation
new_qs = list(questions_col.find({"metadata.topic": "BSON Data Types"}).sort("metadata.created_at", -1).limit(3))

for idx, q in enumerate(new_qs, 1):
    print(f"\nQuestion {idx}: {q.get('question_text')}")
    print(f"Concept: {q.get('metadata', {}).get('concept', 'N/A')}")
    print(f"Difficulty: {q.get('metadata', {}).get('difficulty')}")
    print(f"Explanation:\n{q.get('explanation')}")
    print("-" * 50)
