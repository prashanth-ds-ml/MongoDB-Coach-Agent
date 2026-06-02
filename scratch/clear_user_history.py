import os
import sys
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# 1. Load Environment Variables from Global Config
GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")
load_dotenv(ENV_PATH)

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    print("Error: MONGO_URI not found in environment or global .env file.")
    sys.exit(1)

# 2. Database Connection
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["certcoach_db"]
    profiles_col = db["user_profiles"]
    attempts_col = db["user_attempts"]
    study_sessions_col = db["user_study_sessions"]
    
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)

USER_ID = "local_user_1"

# 3. Delete Profile
profile_delete_res = profiles_col.delete_one({"_id": USER_ID})
print(f"Deleted user profile for '{USER_ID}': {profile_delete_res.deleted_count} document(s).")

# 4. Delete Attempts
attempts_delete_res = attempts_col.delete_many({"user_id": USER_ID})
print(f"Deleted attempts for '{USER_ID}': {attempts_delete_res.deleted_count} document(s).")

# 5. Delete Study Sessions
sessions_delete_res = study_sessions_col.delete_many({"user_id": USER_ID})
print(f"Deleted study sessions for '{USER_ID}': {sessions_delete_res.deleted_count} document(s).")

# 6. Recreate Local Files
_HERE = os.path.dirname(os.path.abspath(__file__))
# Let's target the exact workspace path to be absolutely sure
DATA_DIR = os.path.abspath(os.path.join(_HERE, "../src/certcoach/data"))
CHAT_LOGS_DIR = os.path.join(DATA_DIR, "chat_logs")
BRAIN_FILE = os.path.join(CHAT_LOGS_DIR, "MongoDB_Brain.md")
HISTORY_FILE = os.path.join(CHAT_LOGS_DIR, "active_history.json")

print(f"Targeting local logs directory: {CHAT_LOGS_DIR}")

if os.path.exists(HISTORY_FILE):
    try:
        os.remove(HISTORY_FILE)
        print("Deleted active_history.json successfully.")
    except Exception as e:
        print(f"Error deleting active_history.json: {e}")

try:
    os.makedirs(CHAT_LOGS_DIR, exist_ok=True)
    with open(BRAIN_FILE, "w", encoding="utf-8") as f:
        f.write("# 🧠 MongoDB Brain\n\n")
        f.write("This document contains your entire conversation history with CertCoach. "
                "Use it to review past explanations, questions, and insights.\n\n---\n")
    print("Reset MongoDB_Brain.md successfully.")
except Exception as e:
    print(f"Error resetting MongoDB_Brain.md: {e}")

print("\nAll user history cleared. Preparation is now fresh and ready for onboarding.")
