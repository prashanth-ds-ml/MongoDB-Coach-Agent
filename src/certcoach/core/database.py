import os
import sys
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

client = None
db = None
questions_col = None
profiles_col = None
attempts_col = None
study_sessions_col = None
draft_questions_col = None
connection_error = None

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["certcoach_db"]
    questions_col = db["questions"]
    profiles_col = db["user_profiles"]
    attempts_col = db["user_attempts"]
    study_sessions_col = db["user_study_sessions"]
    draft_questions_col = db["draft_questions"]
except Exception as e:
    connection_error = e

def check_connection():
    if connection_error is not None:
        print(f"\n⚠️  MongoDB Connection/Configuration Error: {connection_error}")
        print("Could not connect to MongoDB. This usually happens due to:")
        print("  1. Network or DNS resolution timeouts (especially with mongodb+srv:// Atlas URIs)")
        print("  2. Missing internet access or a local server downtime")
        print("  3. An incorrect connection string in your .env file")
        print(f"\nPlease verify your network/database connection or update your connection string at:\n  {ENV_PATH}\n")
        sys.exit(1)


# --- QUESTION BANK ---

def get_random_questions(topic=None, limit=10, subtopic_keywords=None, difficulty=None, strict_keywords=False):
    """
    Fetch questions filtered by topic, then narrowed by subtopic keywords and optionally difficulty.
    """
    query = {}
    if topic:
        query["metadata.topic"] = {"$regex": f"^{topic}$", "$options": "i"}
    if difficulty:
        query["metadata.difficulty"] = {"$regex": f"^{difficulty}$", "$options": "i"}

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

        if strict_keywords:
            questions = keyword_filtered
        else:
            # Only use keyword-filtered set if it has enough questions
            if len(keyword_filtered) >= min(3, limit):
                questions = keyword_filtered
            elif len(keyword_filtered) >= 1:
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


# --- STUDY SESSION TRACKING ---

def save_study_session(user_id: str, start_time: datetime, end_time: datetime, duration: float, topics_covered: list, questions_attempted: int, accuracy: float):
    """Log a complete study session into MongoDB."""
    session = {
        "user_id": user_id,
        "start_time": start_time.isoformat() if hasattr(start_time, "isoformat") else str(start_time),
        "end_time": end_time.isoformat() if hasattr(end_time, "isoformat") else str(end_time),
        "duration": duration,  # in minutes
        "topics_covered": topics_covered,
        "questions_attempted": questions_attempted,
        "accuracy": accuracy,
        "timestamp": datetime.utcnow().isoformat()
    }
    study_sessions_col.insert_one(session)


def get_study_sessions(user_id: str) -> list:
    """Retrieve all study sessions logged by a user."""
    return list(study_sessions_col.find({"user_id": user_id}))


# --- AI QUESTION GENERATION BANK MANAGEMENT ---

def save_draft_question(mcq_data: dict) -> str:
    """Saves a draft AI-generated question awaiting user validation."""
    q_id = str(uuid.uuid4())
    draft = {
        "_id": q_id,
        "topic": mcq_data.get("topic", "General"),
        "difficulty": mcq_data.get("difficulty", "Medium"),
        "scenario": mcq_data.get("scenario", ""),
        "question": mcq_data.get("question", ""),
        "options": mcq_data.get("options", []),
        "correct_answer": mcq_data.get("correct_answer", ""),
        "trap_analysis": mcq_data.get("trap_analysis", "No specific trap."),
        "explanation": mcq_data.get("explanation", ""),
        "citation_source": mcq_data.get("citation_source", ""),
        "created_at": datetime.utcnow().isoformat()
    }
    draft_questions_col.insert_one(draft)
    return q_id


def get_draft_questions() -> list:
    """Retrieve all pending draft questions."""
    return list(draft_questions_col.find({}))


def approve_draft_question(draft_id: str) -> bool:
    """Moves a draft question to the production bank after running duplicate check."""
    draft = draft_questions_col.find_one({"_id": draft_id})
    if not draft:
        return False

    # Duplicate check based on question text
    existing = questions_col.find_one({"question_text": draft["question"]})
    if existing:
        draft_questions_col.delete_one({"_id": draft_id})
        return False

    # Convert draft to standard Ultimate Schema
    rich_question = {
        "_id": draft["_id"],
        "metadata": {
            "topic": draft["topic"],
            "difficulty": draft["difficulty"],
            "citation_source": draft["citation_source"],
            "created_at": datetime.utcnow().isoformat()
        },
        "context": {
            "scenario_description": draft["scenario"],
            "database_info": ""
        },
        "question_text": draft["question"],
        "options": [],
        "global_metrics": {
            "total_attempts": 0,
            "correct_attempts": 0,
            "times_seen": 0,
            "times_correct": 0,
            "times_incorrect": 0,
            "average_time_seconds": 0.0
        }
    }

    letters = ['A', 'B', 'C', 'D']
    for idx, opt_text in enumerate(draft["options"]):
        is_correct = (opt_text.strip() == draft["correct_answer"].strip())
        is_trap = False
        trap_analysis = draft.get("trap_analysis", "")
        feedback = draft.get("explanation", "")

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
    draft_questions_col.delete_one({"_id": draft_id})
    return True


# --- QUESTION EXPOSURE & QUALITY TRACKING ---

def update_question_exposure(question_id: str, is_correct: bool, elapsed_seconds: float):
    """Increment seen/correct counts and calculate rolling response time averages."""
    q = questions_col.find_one({"_id": question_id})
    if not q:
        return

    metrics = q.get("global_metrics", {})
    times_seen = metrics.get("times_seen", 0) + 1
    times_correct = metrics.get("times_correct", 0) + (1 if is_correct else 0)
    times_incorrect = metrics.get("times_incorrect", 0) + (0 if is_correct else 1)

    prev_avg = metrics.get("average_time_seconds", 0.0)
    new_avg = prev_avg + (elapsed_seconds - prev_avg) / times_seen

    questions_col.update_one(
        {"_id": question_id},
        {"$set": {
            "global_metrics.total_attempts": times_seen,
            "global_metrics.correct_attempts": times_correct,
            "global_metrics.times_seen": times_seen,
            "global_metrics.times_correct": times_correct,
            "global_metrics.times_incorrect": times_incorrect,
            "global_metrics.average_time_seconds": new_avg
        }}
    )


def get_questions_quality_analytics() -> list:
    """Analyzes success rates and flags questions that are too easy or too hard."""
    all_qs = list(questions_col.find({}))
    results = []
    for q in all_qs:
        metrics = q.get("global_metrics", {})
        attempts = metrics.get("times_seen", 0)
        correct = metrics.get("times_correct", 0)
        avg_time = metrics.get("average_time_seconds", 0.0)

        success_rate = (correct / attempts * 100) if attempts > 0 else 100.0
        difficulty = "Medium"
        flag = "Balanced"
        if attempts >= 3:
            if success_rate >= 95.0:
                difficulty = "Easy"
                flag = "Likely Too Easy"
            elif success_rate <= 30.0:
                difficulty = "Hard"
                flag = "Needs Review (Very Hard)"

        results.append({
            "id": q["_id"],
            "question_text": q.get("question_text", "")[:60] + "...",
            "topic": q.get("metadata", {}).get("topic", "General"),
            "attempts": attempts,
            "success_rate": round(success_rate, 1),
            "average_time": round(avg_time, 1),
            "difficulty": difficulty,
            "flag": flag
        })
    return results


def save_active_exam(user_id: str, topic: str, questions: list, user_answers: list, flagged: list, elapsed: float):
    """Saves the current state of an in-progress timed exam for crash resilience and resumption."""
    clean_questions = []
    for q in questions:
        q_copy = dict(q)
        if "_id" in q_copy:
            q_copy["_id"] = str(q_copy["_id"])
        clean_questions.append(q_copy)
        
    db["active_exam_state"].replace_one(
        {"_id": user_id},
        {
            "_id": user_id,
            "topic": topic,
            "questions": clean_questions,
            "user_answers": user_answers,
            "flagged": flagged,
            "elapsed": elapsed,
            "timestamp": datetime.utcnow().isoformat()
        },
        upsert=True
    )


def get_active_exam(user_id: str) -> dict | None:
    """Retrieves any saved unfinished exam state."""
    return db["active_exam_state"].find_one({"_id": user_id})


def clear_active_exam(user_id: str):
    """Deletes any cached unfinished exam state upon finalization or deliberate quit."""
    db["active_exam_state"].delete_one({"_id": user_id})
