import os
import sys
import random
import uuid
import hashlib
import hmac
import secrets
from datetime import datetime, timezone
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
users_col = None
error_book_col = None
connection_error = None

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["certcoach_db"]
    questions_col = db["questions"]
    profiles_col = db["user_profiles"]
    attempts_col = db["user_attempts"]
    study_sessions_col = db["user_study_sessions"]
    draft_questions_col = db["draft_questions"]
    users_col = db["users"]
    error_book_col = db["user_error_book"]
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
    try:
        client.admin.command("ping")
    except Exception as e:
        print(f"\n⚠️  MongoDB Connection Error: {e}")
        print("Could not ping MongoDB. Verify your network/database connection or update your connection string.")
        sys.exit(1)


# --- AUTHENTICATION ---

def _hash_password(password: str, salt_hex: str | None = None) -> dict:
    salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 210_000)
    return {
        "algorithm": "pbkdf2_sha256",
        "iterations": 210_000,
        "salt": salt.hex(),
        "hash": digest.hex(),
    }


def _verify_password(password: str, password_hash: dict) -> bool:
    if not password_hash or password_hash.get("algorithm") != "pbkdf2_sha256":
        return False
    iterations = int(password_hash.get("iterations", 210_000))
    salt = bytes.fromhex(password_hash["salt"])
    expected = password_hash["hash"]
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations).hex()
    return hmac.compare_digest(digest, expected)


def create_user(email: str, password: str, display_name: str = "") -> tuple[bool, str | dict]:
    email_norm = email.strip().lower()
    if users_col.find_one({"email": email_norm}):
        return False, "An account with that email already exists."

    user = {
        "_id": str(uuid.uuid4()),
        "email": email_norm,
        "display_name": display_name.strip() or email_norm.split("@")[0],
        "password_hash": _hash_password(password),
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
        "last_login_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
    }
    users_col.insert_one(user)
    public_user = {k: v for k, v in user.items() if k != "password_hash"}
    return True, public_user


def authenticate_user(email: str, password: str) -> tuple[bool, str | dict]:
    email_norm = email.strip().lower()
    user = users_col.find_one({"email": email_norm})
    if not user or not _verify_password(password, user.get("password_hash", {})):
        return False, "Invalid email or password."

    users_col.update_one({"_id": user["_id"]}, {"$set": {"last_login_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()}})
    public_user = {k: v for k, v in user.items() if k != "password_hash"}
    return True, public_user


# --- QUESTION BANK ---

def get_random_questions(topic=None, limit=10, subtopic_keywords=None, difficulty=None, strict_keywords=False, topic_id=None, concepts=None):
    """
    Fetch questions filtered by topic/topic_id, then narrowed by concepts and subtopic keywords.
    """
    query = {}
    if topic_id is not None:
        query["metadata.topic_id"] = int(topic_id)
    elif topic:
        query["metadata.topic"] = {"$regex": f"^{topic}$", "$options": "i"}
        
    if difficulty:
        query["metadata.difficulty"] = {"$regex": f"^{difficulty}$", "$options": "i"}

    # 1. First attempt: Direct concept matching on metadata.concept
    matched_questions = []
    if concepts:
        concept_query = dict(query)
        # Match any of the concepts in a case-insensitive manner or direct mapping
        concept_query["metadata.concept"] = {"$in": concepts}
        matched_questions = list(questions_col.find(concept_query))
        
    if len(matched_questions) >= limit:
        random.shuffle(matched_questions)
        return matched_questions[:limit]
        
    # 2. Second attempt: Fall back to keyword/substring matching across all questions of the topic
    all_topic_qs = list(questions_col.find(query))
    
    # Gather search keywords
    search_keywords = []
    if subtopic_keywords:
        search_keywords.extend(subtopic_keywords)
    if concepts:
        search_keywords.extend(concepts)
        
    if search_keywords:
        keywords_lower = [kw.lower() for kw in search_keywords]
        
        def _matches(q):
            # Check if this question is already in matched_questions to avoid duplicates
            if q["_id"] in {mq["_id"] for mq in matched_questions}:
                return False
            haystack = (
                q.get("question_text", "") + " " +
                q.get("metadata", {}).get("concept", "") + " " +
                q.get("metadata", {}).get("syllabus_topic", "") + " " +
                " ".join(opt.get("code_snippet", "") for opt in q.get("options", []))
            ).lower()
            return any(kw in haystack for kw in keywords_lower)

        keyword_filtered = [q for q in all_topic_qs if _matches(q)]
        
        # Combine direct concept matches and keyword filtered matches
        combined = matched_questions + keyword_filtered
    else:
        # Exclude already matched ones from the fallback general pool
        matched_ids = {mq["_id"] for mq in matched_questions}
        fallback = [q for q in all_topic_qs if q["_id"] not in matched_ids]
        combined = matched_questions + fallback
        
    random.shuffle(combined)
    return combined[:limit]


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
            "created_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
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

def classify_mistake_trap(topic: str, question_text: str, correct_snippet: str, selected_snippet: str) -> str:
    """Heuristic to classify why a student fell for a trap."""
    topic_lower = topic.lower()
    q_lower = question_text.lower()
    c_lower = (correct_snippet or "").lower()
    s_lower = (selected_snippet or "").lower()
    
    # 1. Casing trap: e.g. insert_one vs insertOne
    if ("_" in c_lower and "_" not in s_lower) or ("_" not in c_lower and "_" in s_lower):
        return "Lexical Casing Trap"
        
    # 2. Array/Embedded elements: e.g. $elemMatch, dot notation
    if "array" in topic_lower or "$elemmatch" in q_lower or "$elemmatch" in c_lower or "$elemmatch" in s_lower:
        return "Array Matching Semantics"
        
    # 3. Cursor execution order: sort, limit, skip
    if any(k in q_lower or k in c_lower or k in s_lower for k in ["sort", "limit", "skip", "cursor"]):
        return "Cursor Method Sequencing"
        
    # 4. Data Modeling choice: embedded vs referenced
    if "modeling" in topic_lower or "relationship" in topic_lower or "embed" in q_lower or "reference" in q_lower:
        return "Data Modeling Choice"
        
    # 5. Query Operator Logic: $and vs $or vs implicit AND
    if any(op in q_lower or op in c_lower or op in s_lower for op in ["$and", "$or", "$nor", "$not", "$exists", "$type"]):
        return "MQL Operator Logic"
        
    return "Syntax / Conceptual Nuance"


def log_mistake(user_id: str, question_id: str, topic: str, concept: str, selected_option: str, correct_option: str, trap_type: str):
    """Log or increment a mistake in the user's error book."""
    existing = error_book_col.find_one({"user_id": user_id, "question_id": question_id, "reviewed": False})
    if existing:
        error_book_col.update_one(
            {"_id": existing["_id"]},
            {
                "$inc": {"fail_count": 1},
                "$set": {
                    "last_failed_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
                    "selected_option": selected_option,
                    "correct_option": correct_option,
                    "trap_type": trap_type
                }
            }
        )
    else:
        error_book_col.insert_one({
            "user_id": user_id,
            "question_id": question_id,
            "topic": topic,
            "concept": concept,
            "selected_option": selected_option,
            "correct_option": correct_option,
            "trap_type": trap_type,
            "fail_count": 1,
            "created_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
            "last_failed_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
            "reviewed": False
        })


def resolve_mistake(user_id: str, question_id: str):
    """Mark a mistake as resolved/reviewed when answered correctly."""
    error_book_col.update_many(
        {"user_id": user_id, "question_id": question_id, "reviewed": False},
        {"$set": {"reviewed": True, "resolved_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()}}
    )


def get_error_book(user_id: str, limit: int = 50) -> list:
    """Retrieve unresolved/active mistakes for a user, sorted by failure frequency."""
    return list(
        error_book_col.find({"user_id": user_id, "reviewed": False})
        .sort([("fail_count", -1), ("last_failed_at", -1)])
        .limit(limit)
    )


def save_attempt(user_id: str, question_id: str, topic: str, user_selected_letter: str, is_correct: bool, confidence: str):
    """Save an individual question attempt to MongoDB and manage error book entries."""
    attempt = {
        "user_id": user_id,
        "question_id": question_id,
        "topic": topic,
        "user_selected_letter": user_selected_letter,
        "is_correct": is_correct,
        "confidence_level": confidence,
        "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
    }
    attempts_col.insert_one(attempt)
    
    if is_correct:
        resolve_mistake(user_id, question_id)
    else:
        # Fetch question details to run heuristic classification
        try:
            q_doc = questions_col.find_one({"_id": question_id})
            if q_doc:
                question_text = q_doc.get("question_text", "")
                concept = q_doc.get("metadata", {}).get("concept", "")
                
                correct_snippet = ""
                selected_snippet = ""
                for opt in q_doc.get("options", []):
                    if opt.get("is_correct"):
                        correct_snippet = opt.get("code_snippet", "")
                    if opt.get("option_letter") == user_selected_letter:
                        selected_snippet = opt.get("code_snippet", "")
                
                trap_type = classify_mistake_trap(topic, question_text, correct_snippet, selected_snippet)
                log_mistake(
                    user_id=user_id,
                    question_id=question_id,
                    topic=topic,
                    concept=concept,
                    selected_option=user_selected_letter,
                    correct_option=correct_snippet,
                    trap_type=trap_type
                )
        except Exception:
            # Fallback if lookup fails
            log_mistake(
                user_id=user_id,
                question_id=question_id,
                topic=topic,
                concept="Unclassified",
                selected_option=user_selected_letter,
                correct_option="Unknown",
                trap_type="Unclassified"
            )

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
            "progress": {"completed_topics": [], "current_agenda": [], "streak_freezes": 0},
            "created_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
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
    today_date = datetime.now(timezone.utc).date()
    
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
    elif last_login == today_date - timedelta(days=2) and profile.get("progress", {}).get("streak_freezes", 0) > 0:
        # Streak freeze active! Decrement freeze balance and preserve current streak
        progress = profile.get("progress", {})
        progress["streak_freezes"] = progress.get("streak_freezes", 0) - 1
        update_user_profile(user_id, {"progress": progress})
        from rich.console import Console
        console = Console()
        console.print("\n[bold yellow]❄️ Streak Freeze Active! Your streak has been preserved.[/bold yellow]")
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
        "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
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
        "created_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
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
            "created_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
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


SEVEN_PART_EXPLANATION_MARKERS = [
    "correct answer",
    "why correct",
    "why other options are wrong",
    "exam trap",
    "memory hook",
    "follow-up practice recommendation",
    "syntax example",
]


def audit_question_explanations(min_explanation_chars: int = 500) -> dict:
    """Audit whether question-bank items have detailed seven-part explanations."""
    all_qs = list(questions_col.find({}))
    issues = []
    compliant = 0

    for q in all_qs:
        explanation_parts = [
            str(q.get("explanation", "") or ""),
            str(q.get("trap_analysis", "") or ""),
            str(q.get("citation_source", "") or ""),
        ]
        for opt in q.get("options", []):
            explanation_parts.append(str(opt.get("feedback", "") or ""))
        explanation_text = "\n".join(explanation_parts)
        lowered = explanation_text.lower()

        missing_markers = [marker for marker in SEVEN_PART_EXPLANATION_MARKERS if marker not in lowered]
        option_feedback_missing = [
            opt.get("option_letter", "?")
            for opt in q.get("options", [])
            if not str(opt.get("feedback", "") or "").strip()
        ]

        q_issues = []
        if missing_markers:
            q_issues.append("missing sections: " + ", ".join(missing_markers))
        if len(explanation_text.strip()) < min_explanation_chars:
            q_issues.append(f"explanation too short (< {min_explanation_chars} chars)")
        if len(q.get("options", [])) != 4:
            q_issues.append("does not have exactly 4 options")
        if option_feedback_missing:
            q_issues.append("missing option feedback: " + ", ".join(option_feedback_missing))

        if q_issues:
            issues.append({
                "id": str(q.get("_id", "")),
                "topic": q.get("metadata", {}).get("topic", "General"),
                "concept": q.get("metadata", {}).get("concept", ""),
                "difficulty": q.get("metadata", {}).get("difficulty", ""),
                "question_text": str(q.get("question_text", ""))[:90],
                "issues": q_issues,
            })
        else:
            compliant += 1

    total = len(all_qs)
    compliance_percent = (compliant / total * 100) if total else 100.0
    return {
        "total_questions": total,
        "compliant_questions": compliant,
        "non_compliant_questions": len(issues),
        "compliance_percent": round(compliance_percent, 1),
        "issues": issues,
    }


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
            "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
        },
        upsert=True
    )


def get_active_exam(user_id: str) -> dict | None:
    """Retrieves any saved unfinished exam state."""
    return db["active_exam_state"].find_one({"_id": user_id})


def clear_active_exam(user_id: str):
    """Deletes any cached unfinished exam state upon finalization or deliberate quit."""
    db["active_exam_state"].delete_one({"_id": user_id})


def award_streak_freeze(user_id: str) -> bool:
    """Awards a streak freeze token, capped at a maximum of 3 active tokens."""
    profile = get_user_profile(user_id)
    progress = profile.get("progress", {})
    current_freezes = progress.get("streak_freezes", 0)
    if current_freezes < 3:
        progress["streak_freezes"] = current_freezes + 1
        update_user_profile(user_id, {"progress": progress})
        return True
    return False


def update_database_connection(new_uri: str) -> bool:
    """Rewrites the .env files, closes the active client, and re-establishes the connection."""
    global client, db, questions_col, profiles_col, attempts_col, study_sessions_col, draft_questions_col, users_col, error_book_col, MONGO_URI, connection_error
    
    os.environ["MONGO_URI"] = new_uri
    MONGO_URI = new_uri
    
    # Update global config and local .env files
    env_paths = [ENV_PATH, os.path.join(os.getcwd(), ".env")]
    for path in env_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                replaced = False
                new_lines = []
                for line in lines:
                    if line.strip().startswith("MONGO_URI="):
                        new_lines.append(f"MONGO_URI={new_uri}\n")
                        replaced = True
                    else:
                        new_lines.append(line)
                if not replaced:
                    if new_lines and not new_lines[-1].endswith("\n"):
                        new_lines.append("\n")
                    new_lines.append(f"MONGO_URI={new_uri}\n")
                with open(path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
            except Exception as e:
                print(f"[!] Error writing to {path}: {e}")
                
    # Close old client
    if client is not None:
        try:
            client.close()
        except Exception:
            pass
            
    # Try connecting
    try:
        new_client = MongoClient(new_uri, serverSelectionTimeoutMS=5000)
        new_client.admin.command("ping")
        client = new_client
        db = client["certcoach_db"]
        questions_col = db["questions"]
        profiles_col = db["user_profiles"]
        attempts_col = db["user_attempts"]
        study_sessions_col = db["user_study_sessions"]
        draft_questions_col = db["draft_questions"]
        users_col = db["users"]
        error_book_col = db["user_error_book"]
        connection_error = None
        return True
    except Exception as e:
        connection_error = e
        return False
