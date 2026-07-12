import os
import json
import re
import datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(_HERE, "../data"))
REPO_ROOT = os.path.abspath(os.path.join(_HERE, "../../../"))
MEMORY_DIR = os.path.join(REPO_ROOT, "memory")

SYLLABUS_FILE = os.path.join(DATA_DIR, "syllabus.json")

MOCK_EXAM_UNLOCK_THRESHOLD = 0.70  # 70% topics mastered required
PRACTICE_QUESTION_COUNT = 5
PRACTICE_EASY_COUNT = 3
PRACTICE_MEDIUM_COUNT = 2

from certcoach.core import database


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def load_syllabus() -> list:
    with open(SYLLABUS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def score_md_file_for_concept(filename: str, concept: str) -> int:
    if not concept:
        return 0
    # Split camelCase word boundaries (e.g. "insertOne" -> "insert One")
    # before tokenizing -- official doc filenames are snake_case, so a
    # CamelCase concept name like "insertOne()"/"findOne()"/"updateMany()"
    # previously fused into one token ("insertone") that could never
    # substring-match a real filename, silently forcing every such concept
    # into the arbitrary first-2-files fallback in resolve_concept_docs.
    camel_split_concept = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", concept)
    # Strip "$" so a bare operator concept like "$set" tokenizes to "set" --
    # official doc filenames never include the literal dollar sign (e.g.
    # ..._operator_update_set__....md), so leaving it in the token silently
    # blocked every purely-operator-named concept from matching its own
    # dedicated reference doc.
    tokens = [
        t.lower()
        for t in camel_split_concept.replace("()", " ").replace("/", " ").replace("-", " ").replace("$", " ").split()
        if len(t) > 2
    ]
    filename_lower = filename.lower()
    score = 0
    for token in tokens:
        if token in filename_lower:
            score += 10
        if "bson" in token and "bson" in filename_lower:
            score += 5
        if "crud" in token and "crud" in filename_lower:
            score += 5
    return score


def prioritize_md_files(md_files: list[str], concept: str) -> list[str]:
    if not concept:
        return md_files
    return sorted(md_files, key=lambda filename: score_md_file_for_concept(filename, concept), reverse=True)


def resolve_concept_docs(md_files: list[str], concept: str, max_files: int = 3) -> list[str]:
    """Doc-relevance filter shared by lesson delivery, question generation, and
    the dry-run preview job. A flat `score > 0` threshold let a single generic
    token (e.g. "data" in "BSON Data Types") falsely match unrelated topic-level
    docs whose filenames merely happen to contain that word (`..._data_modeling_
    introduction`, `..._databases_and_collections`) alongside the real match.
    Requiring each candidate to reach at least half the top score for this
    concept filters those out while still keeping every doc in a genuinely-tied
    multi-doc concept (e.g. sort/limit/skip's three cursor docs, which all score
    equally and would otherwise be wrongly narrowed by an absolute cutoff).
    """
    if not concept:
        return md_files[:max_files]
    scored = [(filename, score_md_file_for_concept(filename, concept)) for filename in md_files]
    max_score = max((score for _, score in scored), default=0)
    if max_score <= 0:
        return md_files[:2][:max_files]
    threshold = max_score * 0.5
    relevant = [
        filename for filename, score in sorted(scored, key=lambda pair: pair[1], reverse=True)
        if score >= threshold
    ]
    return relevant[:max_files]


def load_md_context(md_files: list, prioritize_concept: str = None) -> str:
    """Load markdown file content as context for the LLM."""
    if prioritize_concept:
        md_files = resolve_concept_docs(md_files, prioritize_concept)

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


def resolve_topic_id(topic_name: str) -> int | None:
    if not topic_name:
        return None
    normalized = topic_name.strip().lower()
    for item in load_syllabus():
        if item.get("topic", "").strip().lower() == normalized:
            return item.get("id")
    return None


def load_topic_benchmark_context(topic_id: int | None = None, concept: str = "") -> str:
    """Load the topic benchmark record for prompt grounding."""
    if topic_id is None:
        return ""

    benchmark_file = os.path.join(MEMORY_DIR, f"topic_{int(topic_id):02d}_benchmark.md")
    if not os.path.exists(benchmark_file):
        return ""

    with open(benchmark_file, "r", encoding="utf-8") as f:
        benchmark_text = f.read().strip()

    if not benchmark_text:
        return ""

    header = f"Benchmark context for Topic {int(topic_id)}"
    if concept:
        header += f" / {concept}"

    return f"{header}:\n```\n{benchmark_text[:12000]}\n```"


def load_topic_benchmark_focus(topic_id: int | None = None, concept: str = "") -> str:
    """Load only the weak-focus portion of a topic benchmark record."""
    if topic_id is None:
        return ""

    benchmark_file = os.path.join(MEMORY_DIR, f"topic_{int(topic_id):02d}_benchmark.md")
    if not os.path.exists(benchmark_file):
        return ""

    with open(benchmark_file, "r", encoding="utf-8") as f:
        benchmark_text = f.read().splitlines()

    if not benchmark_text:
        return ""

    started = False
    focus_lines: list[str] = []
    for line in benchmark_text:
        if line.strip() == "- `weak_focus`:":
            started = True
            continue
        if started:
            if line.startswith("- `") or line.startswith("## "):
                break
            if line.strip():
                focus_lines.append(line.strip())

    if not focus_lines:
        return ""

    header = f"Benchmark weak focus for Topic {int(topic_id)}"
    if concept:
        header += f" / {concept}"

    return "\n".join([header + ":", *focus_lines])


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
        delta = exam_date - datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
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


# ---------------------------------------------------------------------------
# SYLLABUS STATUS
# ---------------------------------------------------------------------------

def get_syllabus_status(user_id: str) -> dict:
    syllabus = load_syllabus()
    analytics = database.get_analytics(user_id)
    profile = database.get_user_profile(user_id)
    completed = set(profile.get("progress", {}).get("completed_topics", []))
    completed_subtopics_map = profile.get("progress", {}).get("completed_subtopics", {})

    topic_perf = {ts["topic"]: ts for ts in analytics.get("topic_stats", [])}

    total_topics = len(syllabus)
    mastered_count = 0
    next_topic = None
    skipped_unmapped_topics = []
    gap_topics = []
    insufficient_concepts = []
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
        subtopics = item.get("subtopics", [])
        completed_subtopics = completed_subtopics_map.get(syllabus_topic, [])
        uncompleted_subtopics = [s for s in subtopics if s not in completed_subtopics]
        readiness_concepts = (
            uncompleted_subtopics
            if subtopics
            else ([] if syllabus_topic in completed else [syllabus_topic])
        )
        concept_difficulty_counts = {
            concept: database.get_active_question_counts_by_difficulty(topic_id=item["id"], concepts=[concept])
            for concept in readiness_concepts
        }
        concept_question_counts = {
            concept: sum(counts.values())
            for concept, counts in concept_difficulty_counts.items()
        }
        ready_subtopics = [
            concept for concept in readiness_concepts
            if concept_difficulty_counts.get(concept, {}).get("Easy", 0) >= PRACTICE_EASY_COUNT
            and concept_difficulty_counts.get(concept, {}).get("Medium", 0) >= PRACTICE_MEDIUM_COUNT
        ]
        insufficient_subtopics = [
            concept for concept in readiness_concepts
            if concept not in ready_subtopics
        ]
        insufficient_concepts.extend(
            {
                "topic_id": item["id"],
                "topic": syllabus_topic,
                "concept": concept,
                "active_questions": concept_question_counts.get(concept, 0),
                "required_questions": PRACTICE_QUESTION_COUNT,
                "easy_questions": concept_difficulty_counts.get(concept, {}).get("Easy", 0),
                "required_easy": PRACTICE_EASY_COUNT,
                "medium_questions": concept_difficulty_counts.get(concept, {}).get("Medium", 0),
                "required_medium": PRACTICE_MEDIUM_COUNT,
            }
            for concept in insufficient_subtopics
        )
        concept_coverage = (len(completed_subtopics) / len(subtopics) * 100) if subtopics else 100
        # Do not let quiz analytics skip syllabus concepts. Analytics informs readiness;
        # mastery requires explicit coverage of every mapped concept.
        is_mastered = (
            (bool(subtopics) and not uncompleted_subtopics)
            or (not subtopics and syllabus_topic in completed)
        )

        has_questions = bool(ready_subtopics)
        if not has_questions:
            gap_topics.append(syllabus_topic)

        if is_mastered:
            mastered_count += 1
        else:
            # Lesson/Q&A eligibility is doc coverage only -- question-bank readiness
            # (ready_subtopics) gates practice separately inside run_practice_questions,
            # so a concept with no confirmed questions yet must still be teachable today.
            if has_topic_documentation(item) and readiness_concepts:
                if next_topic is None:
                    next_topic = {**item, "next_ready_subtopic": readiness_concepts[0]}
            else:
                if not has_topic_documentation(item):
                    skipped_unmapped_topics.append({
                        "id": item["id"],
                        "topic": syllabus_topic
                    })

        status_list.append({
            "id": item["id"],
            "topic": syllabus_topic,
            "exam_weight": item.get("exam_weight", "Medium"),
            "subtopics": item.get("subtopics", []),
            "completed_subtopics": completed_subtopics,
            "uncompleted_subtopics": uncompleted_subtopics,
            "ready_subtopics": ready_subtopics,
            "insufficient_subtopics": insufficient_subtopics,
            "concept_question_counts": concept_question_counts,
            "concept_difficulty_counts": concept_difficulty_counts,
            "concept_coverage": round(concept_coverage, 1),
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
        "insufficient_concepts": insufficient_concepts,
        "status_list": status_list,
    }


def calculate_readiness_metrics(user_id: str) -> dict:
    """Estimates Current Readiness, Expected Readiness, and Pass Probability."""
    status = get_syllabus_status(user_id)
    mastery_percent = status.get("mastery_percent", 0.0) if hasattr(status, "get") else 0.0
    if not isinstance(mastery_percent, (int, float)):
        mastery_percent = 0.0
    
    analytics = database.get_analytics(user_id)
    total_attempts = analytics.get("total_attempts", 0) if hasattr(analytics, "get") else 0
    if not isinstance(total_attempts, (int, float)):
        total_attempts = 0
    correct_attempts = analytics.get("correct_attempts", 0) if hasattr(analytics, "get") else 0
    if not isinstance(correct_attempts, (int, float)):
        correct_attempts = 0
    overall_accuracy = (correct_attempts / max(1, total_attempts)) * 100
    
    dampener = min(1.0, total_attempts / 30.0)
    current_readiness = ((mastery_percent * 0.6) + (overall_accuracy * 0.4)) * dampener
    target_readiness = 80.0
    
    # Expected Readiness based on calendar days passed
    profile = database.get_user_profile(user_id)
    calendar = profile.get("study_calendar", []) if hasattr(profile, "get") else []
    total_days = len(calendar) if calendar else 30
    days_left = calculate_days_left(profile.get("exam_date") if hasattr(profile, "get") else None)
    days_passed = max(0, total_days - days_left)
    
    expected_readiness = (days_passed / max(1, total_days)) * target_readiness
    expected_readiness = min(target_readiness, max(0.0, expected_readiness))
    
    # Pass probability bounded [0, 99]%
    ratio = current_readiness / max(1.0, target_readiness)
    pass_probability = ratio * ratio * 100
    if current_readiness >= 85.0:
        pass_probability = min(99.0, max(90.0, pass_probability))
    else:
        pass_probability = min(99.0, max(0.0, pass_probability * 0.8))
        
    return {
        "current_readiness": round(current_readiness, 1),
        "expected_readiness": round(expected_readiness, 1),
        "target_readiness": target_readiness,
        "pass_probability": round(pass_probability, 1),
        # Same threshold the dampener above saturates at -- below it, these
        # numbers are still mostly noise, not a real prediction, and the
        # display should say so rather than presenting a bare percentage.
        "low_data": total_attempts < 30,
    }


def get_study_plan_recommendation(user_id: str) -> dict:
    """Adapts coaching strategy based on progress vs study calendar pacing."""
    metrics = calculate_readiness_metrics(user_id)
    current = metrics.get("current_readiness", 0.0) if hasattr(metrics, "get") else 0.0
    expected = metrics.get("expected_readiness", 0.0) if hasattr(metrics, "get") else 0.0
    
    profile = database.get_user_profile(user_id)
    days_left = calculate_days_left(profile.get("exam_date") if hasattr(profile, "get") else None)
    calendar = profile.get("study_calendar", []) if hasattr(profile, "get") else []
    total_days = len(calendar) if calendar else 30
    days_passed = max(0, total_days - days_left)
    
    sessions = database.get_study_sessions(user_id)
    total_sessions_logged = len(sessions)
    
    # Estimate missed study sessions
    missed_sessions_count = max(0, days_passed - total_sessions_logged)
    
    status = "On Track"
    recommendation = "Maintain your current daily pacing. You are on track to pass."
    
    if days_left <= 5 and current < 50.0:
        status = "Behind Schedule"
        recommendation = f"Current Readiness: {current:.0f}%, Days Remaining: {days_left}. Based on your current performance, writing the exam is not recommended. Suggested postponement: 7-10 days."
    elif missed_sessions_count >= 3 or current < expected - 10.0:
        status = "Behind Schedule"
        recommendation = f"You missed {missed_sessions_count} study sessions. Current readiness is below target. Recommendation: Increase study time."
    elif current >= expected + 5.0 and days_left >= 2:
        status = "Ahead of Schedule"
        recommendation = f"You are progressing faster than expected. Estimated completion: {days_left} days. Recommendation: Reserve final 2 days for revision and mock exams."
        
    return {
        "status": status,
        "recommendation": recommendation,
        "missed_sessions": missed_sessions_count
    }


def get_due_review_topics(user_id: str) -> list:
    user_attempts = database.get_user_attempts(user_id)
    
    last_attempts = {}
    for a in user_attempts:
        t = a.get("topic")
        try:
            dt = datetime.datetime.fromisoformat(a.get("timestamp"))
        except Exception:
            dt = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        if t not in last_attempts or dt > last_attempts[t]["dt"]:
            last_attempts[t] = {
                "dt": dt,
                "is_correct": a.get("is_correct"),
                "confidence": a.get("confidence_level", "Medium")
            }
            
    due_topics = []
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
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
    
    # Spaced-repetition due reviews are locked until the user masters at least 1 topic
    if status["mastered_count"] >= 1:
        due_reviews = get_due_review_topics(user_id)
    else:
        due_reviews = []
    
    # Check Exam Day Mode (Readiness >= 85%)
    readiness_data = calculate_readiness_metrics(user_id)
    exam_day_mode = readiness_data["current_readiness"] >= 85.0
    
    agenda = []

    # 1. Anki Spaced Repetition Review (Locked until at least 1 topic mastered)
    if status["mastered_count"] >= 1:
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

    # 2. Daily Track (Learn vs revision Mock based on Exam Day Mode)
    if not exam_day_mode:
        if status["next_topic"]:
            nt = status["next_topic"]
            if not any(a["topic"] == nt["topic"] for a in agenda):
                profile = database.get_user_profile(user_id)
                completed_subtopics = profile.get("progress", {}).get("completed_subtopics", {}).get(nt["topic"], [])
                uncompleted_subtopics = [s for s in nt.get("subtopics", []) if s not in completed_subtopics]
                
                active_subtopic = nt.get("next_ready_subtopic")
                if not active_subtopic:
                    ready_subtopics = nt.get("ready_subtopics", [])
                    active_subtopic = ready_subtopics[0] if ready_subtopics else None
                if not active_subtopic:
                    return agenda
                
                agenda.append({
                    "type": "Learn",
                    "topic": nt["topic"],
                    "active_subtopic": active_subtopic,
                    "bank_keys": nt.get("bank_topic_keys", [nt["topic"]]),
                    "subtopics": [active_subtopic],
                    "question_keywords": nt.get("question_keywords", []),
                    "md_files": nt.get("md_files", []),
                    "desc": f"📘 Topic #{nt['id']} | Concept: {active_subtopic}",
                })

    else:
        # Exam Day Mode: avoid new topics, focus entirely on mixed mocks/revision
        agenda.append({
            "type": "Review",
            "topic": "Mixed Mock Exam / Weak Area Revision",
            "bank_keys": list(set(k for item in status["status_list"] for k in item["bank_keys"])),
            "subtopics": [],
            "question_keywords": [],
            "md_files": [],
            "desc": "🏆 Exam Day Mode Revision: Mixed Mock Exam & Weak Domain Recall"
        })

    # 3. Domain Boss Fight (if mastered % 3 == 0)
    if not exam_day_mode:
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

def mark_subtopic_complete(user_id: str, topic_name: str, subtopic: str):
    profile = database.get_user_profile(user_id)
    progress = profile.get("progress", {})
    completed_subtopics = progress.get("completed_subtopics", {})
    
    if topic_name not in completed_subtopics:
        completed_subtopics[topic_name] = []
        
    if subtopic not in completed_subtopics[topic_name]:
        completed_subtopics[topic_name].append(subtopic)
        progress["completed_subtopics"] = completed_subtopics
        database.update_user_profile(user_id, {"progress": progress})
        
    # Check if all subtopics for this topic are completed
    syllabus = load_syllabus()
    topic_item = next((item for item in syllabus if item["topic"] == topic_name), None)
    if topic_item:
        subtopics = topic_item.get("subtopics", [])
        completed_for_topic = completed_subtopics.get(topic_name, [])
        if all(sub in completed_for_topic for sub in subtopics):
            mark_topic_complete(user_id, topic_name)


def mark_boss_complete(user_id: str, boss_level: int):
    profile = database.get_user_profile(user_id)
    progress = profile.get("progress", {})
    beaten_bosses = progress.get("beaten_bosses", [])
    if boss_level not in beaten_bosses:
        beaten_bosses.append(boss_level)
        progress["beaten_bosses"] = beaten_bosses
        database.update_user_profile(user_id, {"progress": progress})


def normalize_lesson_chunk_counts(value) -> dict:
    """Backward-compatible read of a stored lesson-chunk-completion entry.
    Older data (written before this feature tracked correct/total
    separately) stored a bare int count; current data stores
    {"completed", "correct"}. Never crash on whichever shape is on disk."""
    if isinstance(value, dict):
        return {"completed": value.get("completed", 0), "correct": value.get("correct", 0)}
    if isinstance(value, int):
        return {"completed": value, "correct": 0}
    return {"completed": 0, "correct": 0}


def mark_lesson_chunk_complete(user_id: str, topic_name: str, concept: str, all_correct: bool) -> dict:
    """Increments the per-topic/concept bite-sized lesson check-in counters
    and returns the new {"completed": n, "correct": n} totals -- "correct"
    tracks whether every question in that check-in was answered right, so
    the running total reflects "how often did this land," not just "how
    many times did you click through." Counts check-ins completed, not
    unique sections -- re-reading a concept increments further rather than
    staying capped at its section count (accepted simplification while the
    check-in feature is still pilot-scoped to one concept)."""
    profile = database.get_user_profile(user_id)
    progress = profile.get("progress", {})
    completed_lesson_chunks = progress.get("completed_lesson_chunks", {})
    topic_counts = completed_lesson_chunks.get(topic_name, {})
    concept_counts = normalize_lesson_chunk_counts(topic_counts.get(concept))
    concept_counts["completed"] += 1
    if all_correct:
        concept_counts["correct"] += 1
    topic_counts[concept] = concept_counts
    completed_lesson_chunks[topic_name] = topic_counts
    progress["completed_lesson_chunks"] = completed_lesson_chunks
    database.update_user_profile(user_id, {"progress": progress})
    return concept_counts


def mark_concept_lesson_seen(user_id: str, topic_id: int, concept: str) -> None:
    """Records that a concept's lesson content has been shown to the learner
    -- independent of both the lesson-check-in pilot gate and the post-lesson
    MCQ score gate (mark_subtopic_complete only fires on a >=4/5 score, which
    can't happen for a concept with no confirmed questions yet). This is the
    signal flashcard review keys off: a card only enters rotation once its
    concept has actually been read, regardless of whether scored practice
    exists for it. Keyed by topic_id (not topic name) because flashcards are
    tagged by topic_id -- avoids an extra name<->id lookup at read time."""
    if topic_id is None:
        return
    profile = database.get_user_profile(user_id)
    progress = profile.get("progress", {})
    lessons_seen = progress.get("lessons_seen", {})
    topic_key = str(topic_id)
    seen_concepts = lessons_seen.get(topic_key, [])
    if concept not in seen_concepts:
        seen_concepts.append(concept)
        lessons_seen[topic_key] = seen_concepts
        progress["lessons_seen"] = lessons_seen
        database.update_user_profile(user_id, {"progress": progress})


# Lightweight SM-2-style intervals (days), not full FSRS -- proportionate to
# a single learner reviewing a few hundred cards, not a multi-user product
# needing per-card difficulty/stability curves. A wrong answer always resets
# to the 1-day bucket; a right answer grows the interval, capped at 60 days
# so a card never drifts out of reach before the exam.
_FLASHCARD_EASE_FACTOR = 2.3
_FLASHCARD_MAX_INTERVAL_DAYS = 60


def compute_next_review(streak: int, interval_days: int, is_correct: bool) -> dict:
    """Pure scheduling step -- no I/O, no timestamps -- so the interval math
    is testable without mocking the clock. Callers attach next_due_at."""
    if not is_correct:
        return {"streak": 0, "interval_days": 1}
    new_streak = streak + 1
    if new_streak == 1:
        new_interval = 1
    elif new_streak == 2:
        new_interval = 3
    else:
        new_interval = min(round(interval_days * _FLASHCARD_EASE_FACTOR), _FLASHCARD_MAX_INTERVAL_DAYS)
    return {"streak": new_streak, "interval_days": new_interval}


def record_flashcard_review(user_id: str, card_id: str, is_correct: bool) -> dict:
    """Read-modify-write against progress.flashcard_review_state[card_id],
    same convention as mark_lesson_chunk_complete. Returns the new state
    (including next_due_at) so the caller can confirm the new interval
    without a second profile read."""
    profile = database.get_user_profile(user_id)
    progress = profile.get("progress", {})
    review_state = progress.get("flashcard_review_state", {})
    prior = review_state.get(card_id, {"streak": 0, "interval_days": 0})

    new_state = compute_next_review(prior.get("streak", 0), prior.get("interval_days", 0), is_correct)
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    new_state["last_reviewed_at"] = now.isoformat()
    new_state["next_due_at"] = (now + datetime.timedelta(days=new_state["interval_days"])).isoformat()

    review_state[card_id] = new_state
    progress["flashcard_review_state"] = review_state
    database.update_user_profile(user_id, {"progress": progress})
    return new_state


def get_due_flashcards(user_id: str) -> list[dict]:
    """Cards eligible for review right now: the concept must have actually
    been taught (see mark_concept_lesson_seen) and the card must either have
    no review history yet (never reviewed = immediately due) or have passed
    its next_due_at. Never-reviewed cards sort first (introduce new material
    before drilling older ones), then soonest-due first."""
    profile = database.get_user_profile(user_id)
    progress = profile.get("progress", {})
    lessons_seen = progress.get("lessons_seen", {})
    review_state = progress.get("flashcard_review_state", {})
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

    due = []
    for card in database.load_flashcards():
        seen_concepts = lessons_seen.get(str(card.get("topic_id")), [])
        if card.get("concept") not in seen_concepts:
            continue
        state = review_state.get(card["id"])
        if state is None:
            due.append({**card, "review_state": None})
            continue
        try:
            next_due_at = datetime.datetime.fromisoformat(state["next_due_at"])
        except Exception:
            due.append({**card, "review_state": state})
            continue
        if now >= next_due_at:
            due.append({**card, "review_state": state})

    due.sort(key=lambda c: (
        c["review_state"] is not None,
        c["review_state"]["next_due_at"] if c["review_state"] else "",
    ))
    return due


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


def validate_lexical_syntax_guard(topic: str, question: str, options: list) -> tuple[bool, str]:
    """
    Verifies casing rules:
    - Standard topics must strictly use mongosh camelCase (insertOne, findOne, etc.) 
      and avoid PyMongo snake_case driver methods in code blocks or options.
    - Python/Driver topics should compare or use PyMongo snake_case in code blocks or options.
    """
    import re
    topic_lower = topic.lower()
    is_driver = "pymongo" in topic_lower or "driver" in topic_lower or "topic 11" in topic_lower
    
    pymongo_methods = [
        "insert_one", "insert_many", "find_one", "update_one", "update_many", 
        "delete_one", "delete_many", "replace_one"
    ]
    
    # Extract option texts to handle both dictionary shapes and raw strings
    option_texts = []
    for opt in options:
        if isinstance(opt, dict):
            option_texts.append(opt.get("code_snippet", ""))
        else:
            option_texts.append(str(opt))
            
    # Extract only code sections from the question stem
    # Includes inline code (backticks) and code blocks (triple backticks)
    code_blocks = re.findall(r'```(?:[a-zA-Z0-9]+)?\n(.*?)\n```', question, re.DOTALL)
    inline_codes = re.findall(r'`([^`]+)`', question)
    question_code = " ".join(code_blocks + inline_codes)
    
    # Combined code text
    code_text = (question_code + " " + " ".join(option_texts)).lower()
    question_lower = question.lower()
    driver_context = is_driver or "pymongo" in question_lower or "pymongo" in code_text

    if not driver_context:
        for m in pymongo_methods:
            # Match method call syntax like .insert_one or insert_one as a full word
            pattern = rf"\.?\b{re.escape(m)}\b"
            if re.search(pattern, code_text):
                return False, f"Standard topic contains PyMongo snake_case method in code: '{m}'. Standard topics must use mongosh camelCase (e.g. '{m.replace('_', '')[0].lower() + m.replace('_', '')[1:]}')."
    else:
        has_pymongo = any(re.search(rf"\.?\b{re.escape(m)}\b", code_text) for m in pymongo_methods)
        pymongo_conn_keywords = ["mongoclient", "uri", "pool", "timeout", "tls", "host", "port", "pymongo"]
        # Search connection keywords in both the extracted code blocks and the plain question text
        has_conn_keywords = any(k in code_text for k in pymongo_conn_keywords) or any(k in question_lower for k in pymongo_conn_keywords)
        
        # Check if code exists in options or question code blocks
        code_markers = [".", "()", "[", "]", "{", "}", "import ", "def ", " = ", "_id"]
        has_code = any(any(m in opt for m in code_markers) for opt in option_texts) or any(m in question_code for m in code_markers)
        
        if has_code and not has_pymongo and not has_conn_keywords:
            return False, "Driver topic lacks PyMongo snake_case driver syntax (e.g., insert_one, find_one) or connection keywords (e.g., MongoClient, URI) in code segments."
            
    return True, "Passed syntax guard."
