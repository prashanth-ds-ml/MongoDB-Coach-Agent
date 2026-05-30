import os
import json
import random
import datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(_HERE, "../data"))

SYLLABUS_FILE = os.path.join(DATA_DIR, "syllabus.json")
RAW_MD_DIR = os.path.join(DATA_DIR, "raw_markdowns")

MOCK_EXAM_UNLOCK_THRESHOLD = 0.70  # 70% topics mastered required

from certcoach.core import database


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def load_syllabus() -> list:
    with open(SYLLABUS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_md_context(md_files: list) -> str:
    """Load markdown file content as context for the LLM."""
    texts = []
    CLEANED_MD_DIR = os.path.join(DATA_DIR, "cleaned_markdowns")
    RAW_MD_DIR_DYNAMIC = os.path.join(DATA_DIR, "raw_markdowns")
    for fname in md_files:
        clean_path = os.path.join(CLEANED_MD_DIR, fname)
        raw_path = os.path.join(RAW_MD_DIR_DYNAMIC, fname)
        
        if os.path.exists(clean_path):
            with open(clean_path, "r", encoding="utf-8") as f:
                texts.append(f.read())
        elif os.path.exists(raw_path):
            with open(raw_path, "r", encoding="utf-8") as f:
                texts.append(f.read())
    return "\n\n---\n\n".join(texts)


def has_topic_documentation(topic_item: dict) -> bool:
    """Check if a topic has any reference documentation files available on disk."""
    md_files = topic_item.get("md_files", [])
    if not md_files:
        return False
    CLEANED_MD_DIR = os.path.join(DATA_DIR, "cleaned_markdowns")
    RAW_MD_DIR_DYNAMIC = os.path.join(DATA_DIR, "raw_markdowns")
    for fname in md_files:
        clean_path = os.path.join(CLEANED_MD_DIR, fname)
        raw_path = os.path.join(RAW_MD_DIR_DYNAMIC, fname)
        if os.path.exists(clean_path) or os.path.exists(raw_path):
            return True
    return False


def calculate_days_left(exam_date_str: str) -> int:
    if not exam_date_str:
        return 30
    try:
        exam_date = datetime.datetime.fromisoformat(exam_date_str)
        delta = exam_date - datetime.datetime.utcnow()
        return max(0, delta.days)
    except Exception:
        return 30


# ---------------------------------------------------------------------------
# CALENDAR PLANNER
# ---------------------------------------------------------------------------

def generate_study_calendar(days: int, experience_level: str = None, diagnostic_mastered_topics: list = None) -> list:
    """
    Spread the syllabus topics across the available days.
    Last 20% of days = mock exam / revision buffer.
    Returns a list of dicts: {date, day_num, phase, topic_id, topic, md_files, subtopics}
    """
    syllabus = load_syllabus()
    
    if diagnostic_mastered_topics:
        active_syllabus = [t for t in syllabus if t["topic"] not in diagnostic_mastered_topics]
    else:
        active_syllabus = syllabus

    total_topics = len(active_syllabus)
    if total_topics == 0:
        total_topics = 1 # Avoid division by zero
        active_syllabus = syllabus[:1]

    study_days = max(1, round(days * 0.80))   # First 80% for learning
    buffer_days = days - study_days            # Last 20% for revision & mocks

    # How many days per topic?
    days_per_topic = max(1, study_days // total_topics)

    calendar = []
    today = datetime.date.today()
    day_cursor = 0

    for topic_item in active_syllabus:
        for d in range(days_per_topic):
            date = today + datetime.timedelta(days=day_cursor)
            calendar.append({
                "day_num": day_cursor + 1,
                "date": date.strftime("%a %d %b"),
                "date_iso": date.isoformat(),
                "phase": "Study",
                "topic_id": topic_item["id"],
                "topic": topic_item["topic"],
                "subtopics": topic_item["subtopics"],
                "md_files": topic_item.get("md_files", []),
                "exam_weight": topic_item.get("exam_weight", "Medium"),
            })
            day_cursor += 1

            # Stop if we've used all study days
            if day_cursor >= study_days:
                break
        if day_cursor >= study_days:
            break

    # Revision + mock buffer
    for d in range(buffer_days):
        date = today + datetime.timedelta(days=day_cursor)
        calendar.append({
            "day_num": day_cursor + 1,
            "date": date.strftime("%a %d %b"),
            "date_iso": date.isoformat(),
            "phase": "Mock & Revision",
            "topic_id": None,
            "topic": "Full Mock Exam / Weak Topic Revision",
            "subtopics": [],
            "md_files": [],
            "exam_weight": "High",
        })
        day_cursor += 1

    return calendar


def get_today_calendar_item(calendar: list) -> dict | None:
    """Return the calendar entry for today."""
    today_iso = datetime.date.today().isoformat()
    for item in calendar:
        if item["date_iso"] == today_iso:
            return item
    # Fallback: return the first uncompleted study day
    for item in calendar:
        if item["phase"] == "Study":
            return item
    return None


# ---------------------------------------------------------------------------
# SYLLABUS STATUS
# ---------------------------------------------------------------------------

def get_syllabus_status(user_id: str) -> dict:
    syllabus = load_syllabus()
    analytics = database.get_analytics(user_id)
    profile = database.get_user_profile(user_id)
    completed = set(profile.get("progress", {}).get("completed_topics", []))

    topic_perf = {ts["topic"]: ts for ts in analytics.get("topic_stats", [])}

    total_topics = len(syllabus)
    mastered_count = 0
    next_topic = None
    skipped_unmapped_topics = []
    gap_topics = []
    status_list = []

    for item in syllabus:
        syllabus_topic = item["topic"]
        bank_keys = item.get("bank_topic_keys", [])

        total_attempts = 0
        correct_attempts = 0
        for key in bank_keys:
            perf = topic_perf.get(key, {})
            total_attempts += perf.get("attempts", 0)
            correct_attempts += perf.get("correct", 0)

        accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
        is_mastered = syllabus_topic in completed or (total_attempts >= 3 and accuracy >= 80)

        has_questions = item.get("in_question_bank", False)
        if not has_questions:
            gap_topics.append(syllabus_topic)

        if is_mastered:
            mastered_count += 1
        else:
            if has_topic_documentation(item):
                if next_topic is None:
                    next_topic = item
            else:
                skipped_unmapped_topics.append({
                    "id": item["id"],
                    "topic": syllabus_topic
                })

        status_list.append({
            "id": item["id"],
            "topic": syllabus_topic,
            "exam_weight": item.get("exam_weight", "Medium"),
            "subtopics": item.get("subtopics", []),
            "question_keywords": item.get("question_keywords", []),
            "md_files": item.get("md_files", []),
            "bank_keys": bank_keys,
            "has_questions": has_questions,
            "attempts": total_attempts,
            "accuracy": round(accuracy, 1),
            "is_mastered": is_mastered,
        })

    mastery_percent = (mastered_count / total_topics) * 100 if total_topics > 0 else 0
    mock_exam_unlocked = mastery_percent >= (MOCK_EXAM_UNLOCK_THRESHOLD * 100)

    return {
        "total_topics": total_topics,
        "mastered_count": mastered_count,
        "mastery_percent": round(mastery_percent, 1),
        "mock_exam_unlocked": mock_exam_unlocked,
        "unlock_threshold_percent": int(MOCK_EXAM_UNLOCK_THRESHOLD * 100),
        "next_topic": next_topic,
        "skipped_unmapped_topics": skipped_unmapped_topics,
        "gap_topics": gap_topics,
        "status_list": status_list,
    }


def get_due_review_topics(user_id: str) -> list:
    user_attempts = database.get_user_attempts(user_id)
    
    last_attempts = {}
    for a in user_attempts:
        t = a.get("topic")
        try:
            dt = datetime.datetime.fromisoformat(a.get("timestamp"))
        except Exception:
            dt = datetime.datetime.utcnow()
        if t not in last_attempts or dt > last_attempts[t]["dt"]:
            last_attempts[t] = {
                "dt": dt,
                "is_correct": a.get("is_correct"),
                "confidence": a.get("confidence_level", "Medium")
            }
            
    due_topics = []
    now = datetime.datetime.utcnow()
    for t, data in last_attempts.items():
        if not data["is_correct"] or data["confidence"] == "Low":
            interval = 1
        elif data["confidence"] == "Medium":
            interval = 2
        else: # High
            interval = 3
            
        next_review = data["dt"] + datetime.timedelta(days=interval)
        if now >= next_review:
            due_topics.append(t)
            
    return due_topics


def generate_daily_agenda(user_id: str) -> list:
    status = get_syllabus_status(user_id)
    due_reviews = get_due_review_topics(user_id)
    agenda = []

    # 1. Anki Spaced Repetition Review
    for item in status["status_list"]:
        # If it's in the due reviews list OR (accuracy < 60% and attempted)
        is_due = any(k in due_reviews for k in item["bank_keys"])
        is_weak = not item["is_mastered"] and item["attempts"] > 0 and item["accuracy"] < 60
        if (is_due or is_weak) and has_topic_documentation(item):
            agenda.append({
                "type": "Review",
                "topic": item["topic"],
                "bank_keys": item["bank_keys"],
                "subtopics": item["subtopics"],
                "question_keywords": item.get("question_keywords", []),
                "md_files": item["md_files"],
                "desc": f"🔄 Spaced Repetition Due (Accuracy {item['accuracy']}%)",
            })
            break  # Only one review per day for pacing

    # 2. Next uncompleted topic from syllabus
    if status["next_topic"]:
        nt = status["next_topic"]
        if not any(a["topic"] == nt["topic"] for a in agenda):
            agenda.append({
                "type": "Learn",
                "topic": nt["topic"],
                "bank_keys": nt.get("bank_topic_keys", [nt["topic"]]),
                "subtopics": nt.get("subtopics", []),
                "question_keywords": nt.get("question_keywords", []),
                "md_files": nt.get("md_files", []),
                "desc": f"📘 Topic #{nt['id']} in official syllabus",
            })

    # 3. Domain Boss Fight (if mastered % 3 == 0)
    mastered_count = status["mastered_count"]
    profile = database.get_user_profile(user_id)
    beaten_bosses = profile.get("progress", {}).get("beaten_bosses", [])
    
    if mastered_count > 0 and mastered_count % 3 == 0:
        boss_level = mastered_count // 3
        if boss_level not in beaten_bosses:
            agenda.append({
                "type": "BossFight",
                "topic": f"Domain Boss Fight: Level {boss_level}",
                "boss_level": boss_level,
                "desc": "👾 Defeat the Boss to proceed to the next domain! (10 timed questions)",
            })
            # Prevent learning next topic until boss is defeated
            agenda = [a for a in agenda if a["type"] != "Learn"]

    return agenda


def mark_topic_complete(user_id: str, topic: str):
    profile = database.get_user_profile(user_id)
    progress = profile.get("progress", {})
    completed = progress.get("completed_topics", [])
    if topic not in completed:
        completed.append(topic)
        progress["completed_topics"] = completed
        database.update_user_profile(user_id, {"progress": progress})

def mark_boss_complete(user_id: str, boss_level: int):
    profile = database.get_user_profile(user_id)
    progress = profile.get("progress", {})
    beaten_bosses = progress.get("beaten_bosses", [])
    if boss_level not in beaten_bosses:
        beaten_bosses.append(boss_level)
        progress["beaten_bosses"] = beaten_bosses
        database.update_user_profile(user_id, {"progress": progress})


def audit_documentation_files() -> dict:
    """
    Cross-checks the syllabus.json against raw_markdowns/ files.
    Returns a structured audit dict:
    {
        "total_topics": int,
        "complete_topics": list of dicts,  # all md_files are present
        "incomplete_topics": list of dicts,  # some md_files are missing
        "empty_topics": list of dicts       # md_files is empty
    }
    """
    syllabus = load_syllabus()
    raw_dir = os.path.join(DATA_DIR, "raw_markdowns")
    
    complete = []
    incomplete = []
    empty = []
    
    for item in syllabus:
        topic_name = item["topic"]
        md_files = item.get("md_files", [])
        
        if not md_files:
            empty.append({
                "id": item["id"],
                "topic": topic_name,
                "subtopics": item.get("subtopics", [])
            })
            continue
            
        present_files = []
        missing_files = []
        
        for fname in md_files:
            fpath = os.path.join(raw_dir, fname)
            if os.path.exists(fpath):
                present_files.append(fname)
            else:
                missing_files.append(fname)
                
        details = {
            "id": item["id"],
            "topic": topic_name,
            "subtopics": item.get("subtopics", []),
            "present": present_files,
            "missing": missing_files
        }
        
        if missing_files:
            incomplete.append(details)
        else:
            complete.append(details)
            
    return {
        "total_topics": len(syllabus),
        "complete": complete,
        "incomplete": incomplete,
        "empty": empty
    }
