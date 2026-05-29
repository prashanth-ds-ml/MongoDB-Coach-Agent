import os
import random
import uuid
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")
load_dotenv(ENV_PATH)

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    print("\n[!] Welcome to CertCoach! Let's set up your environment.")
    MONGO_URI = input("Enter your MongoDB Connection URI: ").strip()
    os.makedirs(GLOBAL_CONFIG_DIR, exist_ok=True)
    with open(ENV_PATH, "a") as f:
        f.write(f"\nMONGO_URI={MONGO_URI}\n")
    print(f"Saved configuration to {ENV_PATH}\n")

client = MongoClient(MONGO_URI)
db = client["certcoach_db"]

questions_col = db["questions"]
profiles_col = db["user_profiles"]
attempts_col = db["user_attempts"]


# --- QUESTION BANK ---

def get_random_questions(topic=None, limit=10, subtopic_keywords=None):
    """
    Fetch questions filtered by topic, then narrowed by subtopic keywords.
    """
    query = {}
    if topic:
        query["metadata.topic"] = {"$regex": f"^{topic}$", "$options": "i"}

    questions = list(questions_col.find(query))
    
    # 2. Narrow by subtopic keywords if provided
    if subtopic_keywords:
        keywords_lower = [kw.lower() for kw in subtopic_keywords]

        def _matches(q):
            haystack = (
                q.get("question_text", "") + " " +
                " ".join(opt.get("code_snippet", "") for opt in q.get("options", []))
            ).lower()
            return any(kw in haystack for kw in keywords_lower)

        keyword_filtered = [q for q in questions if _matches(q)]

        # Only use keyword-filtered set if it has enough questions
        if len(keyword_filtered) >= min(3, limit):
            questions = keyword_filtered

    random.shuffle(questions)
    return questions[:limit]


def get_all_topics():
    """Returns a list of all distinct topics available in the question bank."""
    return sorted(questions_col.distinct("metadata.topic"))

def get_questions_count():
    return questions_col.count_documents({})

def save_generated_question(mcq_data: dict):
    """Saves a newly LLM-generated question into the standard Ultimate Schema."""
    q_id = str(uuid.uuid4())
    rich_question = {
        "_id": q_id,
        "metadata": {
            "topic": mcq_data.get("topic", "General"),
            "difficulty": mcq_data.get("difficulty", "Medium"),
            "citation_source": mcq_data.get("citation_source", ""),
            "created_at": datetime.utcnow().isoformat()
        },
        "context": {
            "scenario_description": mcq_data.get("scenario", ""),
            "database_info": ""
        },
        "question_text": mcq_data.get("question", ""),
        "options": [],
        "global_metrics": {
            "total_attempts": 0,
            "correct_attempts": 0
        }
    }
    
    letters = ['A', 'B', 'C', 'D']
    for idx, opt_text in enumerate(mcq_data.get("options", [])):
        is_correct = (opt_text.strip() == mcq_data.get("correct_answer", "").strip())
        is_trap = False
        trap_analysis = mcq_data.get("trap_analysis", "")
        feedback = mcq_data.get("explanation", "")
        
        if not is_correct and trap_analysis and letters[idx] in trap_analysis:
            is_trap = True
            feedback = trap_analysis
            
        rich_question["options"].append({
            "option_letter": letters[idx],
            "code_snippet": opt_text,
            "is_correct": is_correct,
            "is_trap": is_trap,
            "feedback": feedback
        })

    questions_col.insert_one(rich_question)
    return q_id

# --- USER PROGRESS & ANALYTICS ---

def save_attempt(user_id: str, question_id: str, topic: str, user_selected_letter: str, is_correct: bool, confidence: str):
    """Save an individual question attempt to MongoDB."""
    attempt = {
        "user_id": user_id,
        "question_id": question_id,
        "topic": topic,
        "user_selected_letter": user_selected_letter,
        "is_correct": is_correct,
        "confidence_level": confidence,
        "timestamp": datetime.utcnow().isoformat()
    }
    attempts_col.insert_one(attempt)

def get_user_attempts(user_id: str):
    """Retrieve all attempts for a user."""
    return list(attempts_col.find({"user_id": user_id}))

def get_analytics(user_id: str):
    """Calculate mastery manually from MongoDB data."""
    user_attempts = list(attempts_col.find({"user_id": user_id}))
    
    total = len(user_attempts)
    correct = sum(1 for a in user_attempts if a.get("is_correct"))
    
    topic_map = {}
    for a in user_attempts:
        t = a.get("topic", "Unknown")
        if t not in topic_map:
            topic_map[t] = {"attempts": 0, "correct": 0}
        topic_map[t]["attempts"] += 1
        if a.get("is_correct"):
            topic_map[t]["correct"] += 1
            
    topic_stats = []
    for t, data in topic_map.items():
        topic_stats.append({
            "topic": t,
            "attempts": data["attempts"],
            "correct": data["correct"]
        })
        
    return {
        "total_attempts": total,
        "correct_attempts": correct,
        "topic_stats": sorted(topic_stats, key=lambda x: x["correct"], reverse=True)
    }

# --- USER PROFILE & COACH PLANNER ---

def get_user_profile(user_id: str):
    profile = profiles_col.find_one({"_id": user_id})
    if not profile:
        profile = {
            "_id": user_id,
            "exam_date": None,
            "experience_level": None,
            "streak_days": 0,
            "last_login_date": None,
            "study_preference": {"hours_per_week": 10},
            "progress": {"completed_topics": [], "current_agenda": []},
            "created_at": datetime.utcnow().isoformat()
        }
        profiles_col.insert_one(profile)
    return profile

def update_user_profile(user_id: str, updates: dict):
    # Ensure profile exists
    get_user_profile(user_id)
    
    # We can use $set to update nested fields if we format them correctly,
    # but for simplicity let's just fetch, merge, and replace to match previous behavior,
    # or just use $set for top level. The previous code did simple recursive update.
    
    profile = profiles_col.find_one({"_id": user_id})
    for k, v in updates.items():
        if isinstance(v, dict) and k in profile and isinstance(profile[k], dict):
            profile[k].update(v)
        else:
            profile[k] = v
            
    profiles_col.replace_one({"_id": user_id}, profile)

def update_streak(user_id: str):
    from datetime import timedelta
    profile = get_user_profile(user_id)
    today_date = datetime.utcnow().date()
    
    last_login_str = profile.get("last_login_date")
    if last_login_str:
        try:
            last_login = datetime.fromisoformat(last_login_str).date()
        except Exception:
            last_login = None
    else:
        last_login = None

    current_streak = profile.get("streak_days", 0)

    if last_login == today_date:
        pass # Already counted today
    elif last_login == today_date - timedelta(days=1):
        current_streak += 1
    else:
        current_streak = 1

    update_user_profile(user_id, {
        "streak_days": current_streak,
        "last_login_date": today_date.isoformat()
    })
