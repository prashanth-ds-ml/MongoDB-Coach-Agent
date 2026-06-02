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

print("=== Audit of Topic 1 Questions in MongoDB ===")
# List topics matching or subtopics
all_qs = list(questions_col.find({}))
print(f"Total questions in database: {len(all_qs)}")

t1_topics = ["MongoDB Overview & The Document Model", "BSON Data Types", "Document structure", "Collections vs Tables", "General"]
t1_counts = {t: {"Easy": 0, "Medium": 0, "Hard": 0} for t in t1_topics}

for q in all_qs:
    topic = q.get("metadata", {}).get("topic", "")
    diff = q.get("metadata", {}).get("difficulty", "")
    if topic in t1_counts:
        if diff in t1_counts[topic]:
            t1_counts[topic][diff] += 1

for t, diffs in t1_counts.items():
    print(f"Topic/Key: {t:<40} | Easy: {diffs['Easy']} | Medium: {diffs['Medium']} | Hard: {diffs['Hard']}")

# Look at one BSON Data Types question's explanation to check template compliance
bson_q = questions_col.find_one({"metadata.topic": "BSON Data Types"})
if bson_q:
    print("\n--- Example BSON Data Types Question ---")
    print(f"Question: {bson_q.get('question_text')}")
    print(f"Explanation: {bson_q.get('explanation')}")
    print(f"Trap Analysis: {bson_q.get('trap_analysis')}")
else:
    print("\nNo BSON Data Types question found in the database.")
