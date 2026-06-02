import sys
import os

# Set PYTHONPATH to include src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from certcoach.core.database import MONGO_URI
from pymongo import MongoClient

def audit():
    client = MongoClient(MONGO_URI)
    db = client["certcoach_db"]
    q_col = db["questions"]
    
    total = q_col.count_documents({})
    print(f"Total questions in production: {total}")
    
    topics = [
        "BSON Data Types",
        "General",
        "CRUD Operations",
        "Query Operators",
        "Aggregation Framework",
        "Indexes & Performance",
        "Replication",
        "Sharding",
        "Security",
        "Administration",
        "Diagnostics",
        "Tools"
    ]
    
    for t in topics:
        c_easy = q_col.count_documents({"metadata.topic": t, "metadata.difficulty": "Easy"})
        c_medium = q_col.count_documents({"metadata.topic": t, "metadata.difficulty": "Medium"})
        c_hard = q_col.count_documents({"metadata.topic": t, "metadata.difficulty": "Hard"})
        c_tot = q_col.count_documents({"metadata.topic": t})
        print(f"  Topic: {t} | Total: {c_tot} (Easy: {c_easy}, Medium: {c_medium}, Hard: {c_hard})")

if __name__ == "__main__":
    audit()
