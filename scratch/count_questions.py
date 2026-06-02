import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["certcoach_db"]
questions_col = db["questions"]

all_qs = list(questions_col.find({}))
print(f"Total questions in bank: {len(all_qs)}")

counts = {}
for q in all_qs:
    topic = q.get("metadata", {}).get("topic", "General")
    diff = q.get("metadata", {}).get("difficulty", "Medium")
    if topic not in counts:
        counts[topic] = {"Easy": 0, "Medium": 0, "Hard": 0}
    counts[topic][diff] = counts[topic].get(diff, 0) + 1

print("\nCounts by Topic and Difficulty:")
for topic, diffs in counts.items():
    print(f"Topic: {topic} | Easy: {diffs.get('Easy', 0)} | Medium: {diffs.get('Medium', 0)} | Hard: {diffs.get('Hard', 0)}")
