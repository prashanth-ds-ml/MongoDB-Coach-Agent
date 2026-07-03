import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from rich.console import Console
from rich.progress import (
    MofNCompleteColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from certcoach.core import database, planner
from certcoach.core.config import (
    get_local_llm_url,
    get_ollama_timeout,
    get_population_model,
    get_population_model_chain,
    get_population_num_ctx,
    get_population_easy_target,
    get_population_medium_target,
    get_population_source_chars,
)
from certcoach.core.content_contract import (
    contract_metadata,
    has_invented_topic1_type,
    is_contract_active,
    is_topic1_concept_only,
)
from certcoach.core.question_targets import QuestionTarget, build_weighted_targets
from certcoach.core.model_runner import get_model_runner
from certcoach.core.judge_questions import judge_question

class StyleTarget:
    def __init__(self, topic_id, topic, bank_topic, concept, difficulty, style_type, target_count, exam_weight, concept_weight):
        self.topic_id = topic_id
        self.topic = topic
        self.bank_topic = bank_topic
        self.concept = concept
        self.difficulty = difficulty
        self.style_type = style_type
        self.target_count = target_count
        self.exam_weight = exam_weight
        self.concept_weight = concept_weight

console = Console()
LETTERS = ["A", "B", "C", "D"]
SEVEN_PART_HEADINGS = [
    "### 1. Correct Answer",
    "### 2. Why Correct",
    "### 3. Why Other Options Are Wrong",
    "### 4. Exam Trap",
    "### 5. Memory Hook",
    "### 6. Follow-Up Practice Recommendation",
    "### 7. Syntax Example",
]
QUALITY_RULES = """
Quality rules:
- The question must test one clearly named syllabus concept, not a vague general MongoDB fact.
- The stem must be a fresh, concrete scenario. Do not reword an existing question or lift a documentation sentence verbatim.
- Every retry must change the decision point, not just the wording or answer option order.
- The correct answer must be fully supported by the supplied documentation context.
- There must be exactly four answer options and exactly one correct option.
- Distractors must be plausible exam traps, not joke answers, placeholders, or obvious nonsense.
- For syntax questions, distractors should vary one meaningful detail: casing, operator placement, argument shape, cursor method order, projection inclusion/exclusion, or PyMongo vs mongosh syntax.
- The explanation must use the seven required headings and teach the beginner why the correct answer works and why every distractor fails.
- Each explanation section must be substantive. A heading without useful content is a failure.
- If a syntax example is not required, Section 7 must explicitly say so.
- For Topic 1 and other concept-only topics, use only official BSON/document vocabulary. Do not invent type names such as subdocumentArray, documentArray, embeddedDocument, or subdocument.
- For Topic 1 prompts, prefer asking about BSON types, document shape, arrays, embedded documents, or _id behavior. Do not frame the question around a made-up BSON type.
- Avoid duplicates, near-duplicates, cosmetic rewrites of existing questions, and repeated scenarios for the same topic/concept/difficulty.
""".strip()

POPULATION_RULES = """
Population rules:
- Produce a lean MCQ shell only.
- Do not write the seven-part explanation in this response.
- Ask one narrow question with exactly four short options and exactly one correct answer.
- Prefer `correct_option_letter` when it is simpler, but `correct_answer` as exact option text is also acceptable.
- Include `citation_source` as one official filename or section from the provided docs.
- If you include `trap_analysis`, keep it short and concrete.
- Keep the output tightly grounded in the provided documentation context.
""".strip()

EXPLANATION_SECTION_MIN_LENGTHS = {
    "### 1. Correct Answer": 20,
    "### 2. Why Correct": 65,
    "### 3. Why Other Options Are Wrong": 100,
    "### 4. Exam Trap": 45,
    "### 5. Memory Hook": 40,
    "### 6. Follow-Up Practice Recommendation": 80,
    "### 7. Syntax Example": 20,
}

EXPLANATION_SECTION_MIN_BULLETS = {
    "### 6. Follow-Up Practice Recommendation": 2,
}

EASY_EXPLANATION_SECTION_MIN_LENGTHS = {
    "### 1. Correct Answer": 15,
    "### 2. Why Correct": 50,
    "### 3. Why Other Options Are Wrong": 75,
    "### 4. Exam Trap": 30,
    "### 5. Memory Hook": 30,
    "### 6. Follow-Up Practice Recommendation": 60,
}

EASY_EXPLANATION_SECTION_MIN_BULLETS = {
    "### 6. Follow-Up Practice Recommendation": 2,
}

SYNTAX_HEAVY_TOPIC_IDS = {2, 3, 4, 5, 6, 7, 8, 9, 11, 12}
SYNTAX_EXAMPLE_HINTS = (
    "insertone", "insertmany", "find(", "findone", "updateone", "updatemany", "deleteone", "deletemany",
    "projection", "cursor", "sort", "limit", "skip", "aggregate", "lookup", "unwind", "group", "match",
    "elemMatch", "dot notation", "mongoclient", "pymongo", "explain", "index", "atlas search", "search",
    "connection string", "uri"
)


class SeedMCQ(BaseModel):
    question: str = Field(default="", description="The multiple choice question.")
    options: list[str] = Field(default_factory=list, description="Exactly four options.")
    correct_answer: str = Field(default="", description="The exact correct option text or a single letter A/B/C/D.")
    feedbacks: list[str] = Field(default_factory=list, description="Exactly four feedback strings, one per option.")
    trap_analysis: str = Field(default="", description="The main exam trap.")
    explanation_correct_answer: str = Field(default="", description="What is the correct answer and a brief statement of it.")
    explanation_why_correct: str = Field(default="", description="Detailed explanation of why the correct option is correct.")
    explanation_why_wrong: str = Field(default="", description="Detailed explanation of why each of the other three options is incorrect, explaining the flaw in each option.")
    explanation_exam_trap: str = Field(default="", description="Description of the exam trap or common misconception related to this concept.")
    explanation_memory_hook: str = Field(default="", description="A compact mnemonic or memory hook with one or two concrete rules to remember.")
    explanation_practice_recommendations: list[str] = Field(default_factory=list, description="A list of 3 to 5 compact but specific action items or recall points for practice.")
    explanation_syntax_example: str = Field(default="", description="A markdown string containing a fenced code block of a syntax example if the concept is syntax-heavy, or exactly 'Not required for this concept.' if not syntax-heavy.")
    citation_source: str = Field(default="", description="Official source filename or section.")


def _load_env() -> tuple[str, str]:
    return get_population_model(), get_local_llm_url()


def _ollama_json_request(local_llm_url: str, path: str, payload: dict | None = None, timeout: float = 10.0) -> dict:
    url = f"{local_llm_url.rstrip('/')}{path}"
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="GET" if payload is None else "POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8")
    return json.loads(body) if body else {}


def clear_ollama_memory(local_llm_url: str, model: str | None = None) -> None:
    """Unload active Ollama models so long runs start with a clean VRAM/RAM state."""
    console.print("[cyan]Memory:[/cyan] checking loaded Ollama models")
    try:
        loaded = _ollama_json_request(local_llm_url, "/api/ps", timeout=4.0).get("models", [])
    except Exception as exc:
        console.print(f"[yellow]Memory:[/yellow] could not inspect Ollama models ({exc})")
        return

    names = [item.get("name") or item.get("model") for item in loaded]
    names = [name for name in names if name and (model is None or name == model)]
    if not names:
        console.print("[green]Memory:[/green] no matching loaded models found")
        return

    for name in names:
        try:
            _ollama_json_request(local_llm_url, "/api/generate", {"model": name, "prompt": "", "keep_alive": 0}, timeout=8.0)
            console.print(f"[green]Memory:[/green] unloaded {name}")
        except Exception as exc:
            console.print(f"[yellow]Memory:[/yellow] could not unload {name} ({exc})")


def preload_ollama_model(model: str, local_llm_url: str) -> None:
    """Load the configured model before the progress loop so first-item latency is explicit."""
    console.print(f"[cyan]Model:[/cyan] preloading {model}")
    try:
        _ollama_json_request(
            local_llm_url,
            "/api/generate",
            {"model": model, "prompt": "", "stream": False, "keep_alive": "30m", "options": {"num_ctx": 4096}},
            timeout=180.0,
        )
        console.print(f"[green]Model:[/green] {model} loaded")
    except Exception as exc:
        console.print(f"[yellow]Model:[/yellow] preload failed; generation will try to load on demand ({exc})")


def unload_ollama_model(model: str, local_llm_url: str) -> None:
    try:
        _ollama_json_request(local_llm_url, "/api/generate", {"model": model, "prompt": "", "keep_alive": 0}, timeout=8.0)
        console.print(f"[green]Memory:[/green] unloaded {model}")
    except Exception as exc:
        console.print(f"[yellow]Memory:[/yellow] could not unload {model} ({exc})")


def _question_count(target: StyleTarget | QuestionTarget) -> int:
    return database.questions_col.count_documents({
        "metadata.topic": target.bank_topic,
        "metadata.concept": target.concept,
        "metadata.difficulty": target.difficulty,
    })


def _topic_matches(target: StyleTarget | QuestionTarget, topic_filter: str | None) -> bool:
    if not topic_filter:
        return True
    filt = topic_filter.strip().lower()
    if not filt:
        return True
    if filt.isdigit() and target.topic_id == int(filt):
        return True
    return (
        filt == target.topic.lower()
        or filt == target.bank_topic.lower()
        or filt in target.topic.lower()
        or filt in target.bank_topic.lower()
    )


def _allocate_style_counts(total: int, weights: dict[str, float]) -> dict[str, int]:
    if total <= 0:
        return {k: 0 for k in weights}
    import math
    raw = {k: total * v for k, v in weights.items()}
    counts = {k: int(math.floor(v)) for k, v in raw.items()}
    remaining = total - sum(counts.values())
    for key, _ in sorted(raw.items(), key=lambda item: item[1] - math.floor(item[1]), reverse=True)[:remaining]:
        counts[key] += 1
    return counts


def _get_db_style_counts(topic_id: int, concept: str, difficulty: str) -> dict[str, int]:
    cursor = database.questions_col.find({
        "metadata.topic_id": topic_id,
        "metadata.concept": concept,
        "metadata.difficulty": difficulty,
    }, {"metadata": 1})
    
    counts = {"Type A": 0, "Type B": 0, "Type C": 0, "Type D": 0}
    for q in cursor:
        if not is_contract_active(q):
            continue
        meta = q.get("metadata", {}) or {}
        style = meta.get("question_style_type")
        if not style:
            style_name = meta.get("question_style", "")
            if "Syntax" in style_name:
                style = "Type A"
            elif "Output" in style_name:
                style = "Type C"
            elif "Troubleshooting" in style_name or "Error" in style_name:
                style = "Type D"
            else:
                style = "Type B"
        if style in counts:
            counts[style] += 1
        else:
            counts["Type B"] += 1
    return counts


def audit_weighted_deficits(
    total_bank_target: int | None = None,
    topic_filter: str | None = None,
    concept_filter: str | None = None,
    target_easy: int | None = None,
    target_medium: int | None = None,
    extra_easy: int = 0,
    extra_medium: int = 0,
) -> list[tuple[StyleTarget, int]]:
    targets = build_weighted_targets(
        planner.load_syllabus(),
        total_bank_target=total_bank_target,
        extra_easy=extra_easy,
        extra_medium=extra_medium,
    )
    deficits = []
    population_targets = {
        "Easy": max(3, target_easy if target_easy is not None else get_population_easy_target()),
        "Medium": max(2, target_medium if target_medium is not None else get_population_medium_target()),
    }
    
    for target in targets:
        if not _topic_matches(target, topic_filter):
            continue
        if concept_filter and target.concept.casefold() != concept_filter.strip().casefold():
            continue
            
        # Get active counts in database for each style under this (topic, concept, difficulty)
        db_counts = _get_db_style_counts(target.topic_id, target.concept, target.difficulty)
        
        current_total = sum(db_counts.values())
        requested_extra = extra_easy if target.difficulty == "Easy" else extra_medium
        requested_count = max(population_targets[target.difficulty], current_total) + requested_extra

        # Distribute the requested count into style guidance.
        if target.topic_id in {2, 3, 4, 5, 6, 7, 8, 9, 11, 12}:
            weights = {"Type A": 0.35, "Type B": 0.25, "Type C": 0.20, "Type D": 0.20}
        else:
            weights = {"Type B": 0.70, "Type D": 0.30}
            
        style_targets = _allocate_style_counts(requested_count, weights)

        remaining_missing = max(0, requested_count - current_total)
        style_order = sorted(
            style_targets,
            key=lambda style: style_targets[style] - db_counts.get(style, 0),
            reverse=True,
        )
        for style_type in style_order:
            if remaining_missing <= 0:
                break
            target_style_count = style_targets[style_type]
            style_gap = max(0, target_style_count - db_counts.get(style_type, 0))
            missing = min(style_gap, remaining_missing)
            if missing > 0:
                style_target = StyleTarget(
                    topic_id=target.topic_id,
                    topic=target.topic,
                    bank_topic=target.bank_topic,
                    concept=target.concept,
                    difficulty=target.difficulty,
                    style_type=style_type,
                    target_count=target_style_count,
                    exam_weight=target.exam_weight,
                    concept_weight=target.concept_weight
                )
                deficits.append((style_target, missing))
                remaining_missing -= missing
                
    return deficits


def _resolve_correct_answer(mcq: SeedMCQ) -> str | None:
    answer = (mcq.correct_answer or "").strip()
    if answer.upper() in ("A", "B", "C", "D"):
        idx = ["A", "B", "C", "D"].index(answer.upper())
        if idx < len(mcq.options):
            return mcq.options[idx]
    if answer in mcq.options:
        return answer
    for option in mcq.options:
        if option.strip().startswith(answer):
            return option
    return None


def _slug(text: str, max_len: int = 36) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return (slug or "general")[:max_len].strip("-")


def normalize_question_for_duplicate_check(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"\(select (one|all that apply)\)", " ", text)
    text = re.sub(r"[^a-z0-9_$]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def question_fingerprint(topic: str, concept: str, question_text: str) -> str:
    normalized = normalize_question_for_duplicate_check(question_text)
    basis = f"{_slug(topic, 48)}|{_slug(concept, 48)}|{normalized}"
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def _token_similarity(left: str, right: str) -> float:
    left_tokens = set(normalize_question_for_duplicate_check(left).split())
    right_tokens = set(normalize_question_for_duplicate_check(right).split())
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def _parse_six_part_explanation(explanation: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_heading: str | None = None
    for raw_line in explanation.splitlines():
        stripped = raw_line.strip()
        if stripped in SEVEN_PART_HEADINGS:
            current_heading = stripped
            sections[current_heading] = ""
            continue
        if current_heading:
            sections[current_heading] = f"{sections[current_heading]}{raw_line.rstrip()}\n"
    return {heading: sections.get(heading, "").strip() for heading in SEVEN_PART_HEADINGS}


def _count_bullet_lines(section: str) -> int:
    return sum(1 for line in section.splitlines() if line.strip().startswith(("-", "*")) or re.match(r"^\d+\.", line.strip()))


def _count_code_fences(section: str) -> int:
    return section.count("```")


def _question_needs_syntax_example(question: dict) -> bool:
    metadata = question.get("metadata", {}) or {}
    # If the style choice was Type B (Theory/Concept), it doesn't need a syntax example
    if metadata.get("question_style_type") == "Type B":
        return False
        
    topic_id = metadata.get("topic_id")
    concept = str(metadata.get("concept", "")).strip().lower()
    if topic_id == 4 and concept in {"$set", "$push", "$inc", "$unset", "upsert", "findandmodify"}:
        return False
    if isinstance(topic_id, int) and topic_id in SYNTAX_HEAVY_TOPIC_IDS:
        return True

    haystack = " ".join(
        str(part or "")
        for part in (
            metadata.get("topic"),
            metadata.get("syllabus_topic"),
            metadata.get("concept"),
            question.get("question_text"),
            " ".join(str(option.get("code_snippet", "")) for option in question.get("options", []) or []),
        )
    ).lower()
    return any(hint in haystack for hint in SYNTAX_EXAMPLE_HINTS)


def _difficulty_key(question: dict) -> str:
    difficulty = str(question.get("metadata", {}).get("difficulty", "") or "").strip().lower()
    if difficulty in {"easy", "medium", "hard"}:
        return difficulty
    return "medium"


def _next_question_number(target: QuestionTarget) -> int:
    query = {
        "metadata.topic": target.bank_topic,
        "metadata.concept": target.concept,
        "metadata.difficulty": target.difficulty,
    }
    return database.questions_col.count_documents(query) + 1


def make_question_id(target: StyleTarget | QuestionTarget, question_number: int, fingerprint: str) -> str:
    difficulty = _slug(target.difficulty, 8)
    concept = _slug(target.concept, 32)
    return f"certcoach-t{target.topic_id:02d}-{concept}-{difficulty}-{question_number:03d}-{fingerprint[:8]}"


def is_duplicate_question(question: dict, target: StyleTarget | QuestionTarget) -> tuple[bool, str]:
    fingerprint = question.get("metadata", {}).get("question_fingerprint", "")
    if database.questions_col.find_one({"_id": question.get("_id")}):
        return True, "stable id already exists"
    if fingerprint and database.questions_col.find_one({"metadata.question_fingerprint": fingerprint}):
        return True, "question fingerprint already exists"
    if database.questions_col.find_one({"question_text": question.get("question_text", "")}):
        return True, "exact question text already exists"

    nearby = database.questions_col.find({
        "metadata.topic": target.bank_topic,
        "metadata.concept": target.concept,
        "metadata.difficulty": target.difficulty,
    })
    for existing in nearby:
        if _token_similarity(existing.get("question_text", ""), question.get("question_text", "")) >= 0.92:
            return True, f"near-duplicate of {existing.get('_id')}"
    return False, ""


def validate_question_quality(question: dict, require_explanation: bool = True) -> tuple[bool, list[str]]:
    issues = []
    options = question.get("options", [])
    explanation = str(question.get("explanation", "") or "")
    needs_syntax_example = _question_needs_syntax_example(question)
    difficulty = _difficulty_key(question)
    metadata = question.get("metadata", {}) or {}
    topic_id = metadata.get("topic_id")
    topic_text = " ".join(
        str(part or "")
        for part in (
            metadata.get("topic"),
            metadata.get("syllabus_topic"),
            metadata.get("concept"),
            question.get("question_text"),
            " ".join(str(option.get("code_snippet", "")) for option in options),
        )
    ).lower()
    if not str(question.get("question_text", "")).strip():
        issues.append("missing question text")
    if len(options) != 4:
        issues.append("does not have exactly four options")
    if any(not str(option.get("code_snippet", "")).strip() for option in options):
        issues.append("contains blank option text")
    if sum(1 for option in options if option.get("is_correct")) != 1:
        issues.append("does not have exactly one correct option")
    if any("placeholder" in str(option.get("code_snippet", "")).lower() for option in options):
        issues.append("contains placeholder option text")
    if is_topic1_concept_only(metadata, topic_text):
        if any(has_invented_topic1_type(str(option.get("code_snippet", ""))) for option in options):
            issues.append("contains invented BSON type names")
        if has_invented_topic1_type(str(question.get("question_text", ""))):
            issues.append("question text contains invented BSON type names")
    if topic_id == 4 and str(metadata.get("concept", "")).strip().lower() == "replaceone()":
        leak_terms = (
            "update_one",
            "update_many",
            "find_one_and_update",
            "find_and_modify",
            "upsert",
            "$set",
            "$inc",
            "$push",
            "$unset",
            "$rename",
        )
        leaked = [term for term in leak_terms if term in topic_text]
        if leaked:
            issues.append("replaceOne() question leaks future-scope terms: " + ", ".join(sorted(set(leaked))))
    if topic_id == 4 and str(metadata.get("concept", "")).strip().lower() == "updateone()":
        question_text = str(question.get("question_text", "")).lower()
        correct_options = [
            str(option.get("code_snippet", "")).lower()
            for option in options
            if option.get("is_correct")
        ]
        replacement_terms = (
            "replace the entire",
            "replace an entire",
            "replace the whole",
            "replace_one",
            "replaceone(",
            "entire document",
            "entire content",
            "full document",
            "replacement document",
        )
        leaked = [term for term in replacement_terms if term in question_text]
        if leaked:
            issues.append("updateOne() question drifts into replaceOne() semantics: " + ", ".join(sorted(set(leaked))))
        if any("replace_one" in option or "replaceone(" in option for option in correct_options):
            issues.append("updateOne() question marks replaceOne() syntax as correct")
    if topic_id == 4 and str(metadata.get("concept", "")).strip().lower() == "updatemany()":
        question_text = str(question.get("question_text", "")).lower()
        correct_options = [
            str(option.get("code_snippet", "")).lower()
            for option in options
            if option.get("is_correct")
        ]
        replacement_terms = (
            "replace the entire",
            "replace an entire",
            "replace the whole",
            "replace_one",
            "replaceone(",
            "replacement document",
            "full document",
            "single matching document",
        )
        leaked = [term for term in replacement_terms if term in question_text]
        if leaked:
            issues.append("updateMany() question drifts into replacement semantics: " + ", ".join(sorted(set(leaked))))
        if any("replace_one" in option or "replaceone(" in option for option in correct_options):
            issues.append("updateMany() question marks replaceOne() syntax as correct")
    if topic_id == 4 and str(metadata.get("concept", "")).strip().lower() == "$set":
        question_text = str(question.get("question_text", "")).lower()
        leak_terms = (
            "$inc",
            "$push",
            "$unset",
            "upsert",
            "findandmodify",
            "find_one_and_update",
            "replace_one",
            "replaceone(",
        )
        leaked = [term for term in leak_terms if term in question_text]
        if leaked:
            issues.append("$set question drifts into another Topic 4 update concept: " + ", ".join(sorted(set(leaked))))
    if topic_id == 4 and str(metadata.get("concept", "")).strip().lower() == "$push":
        question_text = str(question.get("question_text", "")).lower()
        leak_terms = ("$set", "$inc", "$unset", "upsert", "findandmodify", "replace_one", "replaceone(")
        leaked = [term for term in leak_terms if term in question_text]
        if leaked:
            issues.append("$push question drifts into another Topic 4 update concept: " + ", ".join(sorted(set(leaked))))
    if topic_id == 4 and str(metadata.get("concept", "")).strip().lower() == "$inc":
        question_text = str(question.get("question_text", "")).lower()
        leak_terms = ("$set", "$push", "$unset", "upsert", "findandmodify", "replace_one", "replaceone(")
        leaked = [term for term in leak_terms if term in question_text]
        if leaked:
            issues.append("$inc question drifts into another Topic 4 update concept: " + ", ".join(sorted(set(leaked))))
    if topic_id == 4 and str(metadata.get("concept", "")).strip().lower() == "$unset":
        question_text = str(question.get("question_text", "")).lower()
        leak_terms = ("$set", "$push", "$inc", "upsert", "findandmodify", "replace_one", "replaceone(")
        leaked = [term for term in leak_terms if term in question_text]
        if leaked:
            issues.append("$unset question drifts into another Topic 4 update concept: " + ", ".join(sorted(set(leaked))))
    if topic_id == 4 and str(metadata.get("concept", "")).strip().lower() == "upsert":
        question_text = str(question.get("question_text", "")).lower()
        leak_terms = ("$set", "$push", "$inc", "$unset", "findandmodify", "replace_one", "replaceone(")
        leaked = [term for term in leak_terms if term in question_text]
        if leaked:
            issues.append("upsert question drifts into another Topic 4 update concept: " + ", ".join(sorted(set(leaked))))
    if topic_id == 4 and str(metadata.get("concept", "")).strip().lower() == "findandmodify":
        question_text = str(question.get("question_text", "")).lower()
        leak_terms = ("$set", "$push", "$inc", "$unset", "upsert", "replace_one", "replaceone(")
        leaked = [term for term in leak_terms if term in question_text]
        if leaked:
            issues.append("findAndModify question drifts into another Topic 4 update concept: " + ", ".join(sorted(set(leaked))))
    if topic_id == 2 and str(metadata.get("concept", "")).strip().lower() == "_id and objectid":
        question_text = str(question.get("question_text", "")).lower()
        option_text = " ".join(str(option.get("code_snippet", "")) for option in options).lower()
        if "_id" not in question_text and "objectid" not in question_text and "_id" not in option_text and "objectid" not in option_text:
            issues.append("question text for _id and ObjectId must explicitly reference _id or ObjectId")
    if topic_id == 3 and str(metadata.get("concept", "")).strip().lower() == "find()":
        leak_terms = (
            "single document",
            "python dictionary",
            "projection",
            "include 'title'",
            "excluding '_id'",
        )
        leaked = [term for term in leak_terms if term in topic_text]
        if leaked:
            issues.append("find() question leaks later-scope terms: " + ", ".join(sorted(set(leaked))))
    if require_explanation:
        sections = _parse_six_part_explanation(explanation)
        missing_headings = [heading for heading, content in sections.items() if not content]
        if not needs_syntax_example:
            missing_headings = [heading for heading in missing_headings if heading != "### 7. Syntax Example"]
        if missing_headings:
            issues.append("missing seven-part headings or content: " + ", ".join(missing_headings))
        min_lengths = EASY_EXPLANATION_SECTION_MIN_LENGTHS if difficulty == "easy" else EXPLANATION_SECTION_MIN_LENGTHS
        short_sections = [
            heading
            for heading, min_length in min_lengths.items()
            if len(sections.get(heading, "")) < min_length
        ]
        if not needs_syntax_example:
            short_sections = [heading for heading in short_sections if heading != "### 7. Syntax Example"]
        if short_sections:
            issues.append("seven-part explanation sections are too short: " + ", ".join(short_sections))
        min_bullets = EASY_EXPLANATION_SECTION_MIN_BULLETS if difficulty == "easy" else EXPLANATION_SECTION_MIN_BULLETS
        short_bullet_sections = [
            heading
            for heading, min_bullet_count in min_bullets.items()
            if _count_bullet_lines(sections.get(heading, "")) < min_bullet_count
        ]
        if short_bullet_sections:
            issues.append("seven-part explanation sections need more bullets: " + ", ".join(short_bullet_sections))
        syntax_section = sections.get("### 7. Syntax Example", "")
        if needs_syntax_example:
            if "```" not in syntax_section:
                issues.append("missing syntax example code block for a syntax-heavy concept")
            if _count_code_fences(syntax_section) < 1:
                issues.append("syntax example needs a fenced code block")
            if len(syntax_section.strip()) < 80:
                issues.append("syntax example is too short")
        elif syntax_section.strip() and not any(
            marker in syntax_section.strip().lower()
            for marker in ("not required", "not needed", "optional", "no syntax example")
        ):
            issues.append("syntax example should explicitly say it is not required for this concept")
        if len(explanation.strip()) < 550:
            issues.append("seven-part explanation is too short")
    if len({str(option.get("code_snippet", "")).strip().lower() for option in options}) != len(options):
        issues.append("duplicate option text")
        
    # Check casing validation rules using the shared lexical guard
    meta = question.get("metadata", {}) or {}
    topic_name = meta.get("topic") or meta.get("syllabus_topic") or ""
    syntax_ok, syntax_msg = planner.validate_lexical_syntax_guard(
        topic_name,
        question.get("question_text", ""),
        options
    )
    if not syntax_ok:
        issues.append(f"Casing validation failed: {syntax_msg}")
        
    return not issues, issues


def print_question_template(question: dict) -> None:
    meta = question.get("metadata", {})
    console.print(f"\n[bold green]Inserted {question.get('_id')}[/bold green]")
    console.print(
        f"[cyan]Topic:[/cyan] {(meta.get('topic') or '').encode('ascii', 'replace').decode('ascii')} | "
        f"[cyan]Concept:[/cyan] {(meta.get('concept') or '').encode('ascii', 'replace').decode('ascii')} | "
        f"[cyan]Difficulty:[/cyan] {(meta.get('difficulty') or '').encode('ascii', 'replace').decode('ascii')}"
    )
    console.print(f"[bold]Question:[/bold] {(question.get('question_text', '') or '').encode('ascii', 'replace').decode('ascii')}")
    for option in question.get("options", []):
        tags = []
        if option.get("is_correct"):
            tags.append("correct")
        if option.get("is_trap"):
            tags.append("trap")
        suffix = f" [{' / '.join(tags)}]" if tags else ""
        console.print(f"  {(option.get('option_letter') or '').encode('ascii', 'replace').decode('ascii')}. {(option.get('code_snippet', '') or '').encode('ascii', 'replace').decode('ascii')}{suffix}")
    console.print("[bold]Seven-Part Explanation:[/bold]")
    console.print((question.get("explanation", "") or "").encode("ascii", "replace").decode("ascii"))


def existing_question_samples(target: StyleTarget | QuestionTarget, limit: int = 8) -> list[str]:
    cursor = database.questions_col.find(
        {
            "metadata.topic": target.bank_topic,
            "metadata.concept": target.concept,
            "metadata.difficulty": target.difficulty,
        },
        {"question_text": 1},
    ).limit(limit)
    return [
        str(item.get("question_text", "") or "").strip()
        for item in cursor
        if str(item.get("question_text", "") or "").strip()
    ]


def _concept_variation_guidance(target: StyleTarget | QuestionTarget, avoid_questions: list[str] | None = None) -> str:
    avoid_text = " ".join(avoid_questions or []).lower()
    concept = str(target.concept or "").strip().lower()
    topic_id = int(target.topic_id or 0)

    if topic_id == 4 and concept == "replaceone()":
        return (
            "Variation requirement for replaceOne(): do NOT mention later CRUD concepts or update operators in the stem or options. "
            "Avoid terms like update_one, update_many, $set, $inc, $push, $unset, upsert, findAndModify, or any other later-scope method/operator names. "
            "Build distractors from unrelated earlier-scope methods such as insert_one or find_one, or from wrong argument order, wrong replacement shape, or wrong filter placement."
        )
    if topic_id == 4 and concept == "updateone()":
        return (
            "Variation requirement for updateOne(): keep the concept on updating a single matching document with update operators such as $set, $inc, $push, or $unset. "
            "Do NOT ask about replacing an entire document, replacement documents, or replace_one()/replaceOne() as the correct answer. "
            "Prefer scenarios about operator choice, matchedCount vs modifiedCount, single-document scope, or valid update document syntax."
        )
    if topic_id == 4 and concept == "updatemany()":
        return (
            "Variation requirement for updateMany(): keep the concept on updating multiple matching documents with update operators such as $set, $inc, $push, or $unset. "
            "Do NOT ask about replacing an entire document, single-document-only behavior, or replace_one()/replaceOne() as the correct answer. "
            "Prefer scenarios about broad filters, multiple matched documents, operator choice, or how updateMany differs from updateOne."
        )
    if topic_id == 4 and concept == "$set":
        return (
            "Variation requirement for $set: keep the concept on assigning or overwriting a field value in a partial update. "
            "Do NOT ask the same 'update one field' syntax question again. "
            "Choose a different decision point such as malformed nested $set usage, why the update document must contain an operator, "
            "the difference between $set and replacement semantics, or a scenario that changes a non-string field while leaving the rest of the document untouched. "
            "Do NOT ask about increments, array appends, field removal, upserts, or replacement-document semantics. "
            "If you mention method names in code, use mongosh camelCase such as updateOne and replaceOne, not snake_case."
            " Include a fenced syntax example section that shows the exact $set update document."
        )
    if topic_id == 4 and concept == "$push":
        return (
            "Variation requirement for $push: keep the concept on appending values to arrays. "
            "Do NOT ask about $set, $inc, $unset, upsert, or full-document replacement. "
            "Prefer scenarios about adding one item to an array, using $each, or choosing array append over assignment."
            " If you include a method name in code, use mongosh camelCase such as updateOne, not update_one."
        )
    if topic_id == 4 and concept == "$inc":
        return (
            "Variation requirement for $inc: keep the concept on incrementing or decrementing numeric fields. "
            "Do NOT ask about $set, $push, $unset, upsert, or full-document replacement. "
            "Prefer scenarios that involve arithmetic changes to counters, quantities, or scores. "
            "If you mention a method name in code, use mongosh camelCase such as updateOne, not update_one."
        )
    if topic_id == 4 and concept == "$unset":
        return (
            "Variation requirement for $unset: keep the concept on removing fields from documents. "
            "Do NOT ask about assignment, incrementing, array appends, upsert, or full-document replacement. "
            "Prefer scenarios where a field should be deleted while the rest of the document remains."
        )
    if topic_id == 4 and concept == "upsert":
        return (
            "Variation requirement for upsert: keep the concept on inserting a new document when no match is found, or updating the matched document when one exists. "
            "Do NOT ask about field-level operators as the main concept. "
            "Prefer scenarios centered on the no-match insert behavior, matched-document update behavior, or the result object."
        )
    if topic_id == 4 and concept == "findandmodify":
        return (
            "Variation requirement for findAndModify: keep the concept on atomic find-and-update behavior and the returned document semantics. "
            "Do NOT ask about simple field assignment, array appends, increments, upserts, or replacement-document syntax as the main answer. "
            "Prefer scenarios about returning the pre-modified or post-modified document and atomic single-document updates."
        )

    if topic_id == 2:
        if concept == "insertmany()":
            return (
                "Variation requirement for insertMany(): do NOT ask the return-type / insertedIds question again. "
                "Choose a different decision point such as ordered vs unordered behavior, array-vs-object syntax, "
                "duplicate-key handling, or the difference between insertMany() and insertOne(). "
                "Prefer a fresh scenario that uses a new document shape, a new error condition, or a new option flag."
            )
        if concept == "insertone()":
            return (
                "Variation requirement for insertOne(): do NOT ask the same single-document syntax question again. "
                "Choose a different decision point such as explicit _id handling, return-value semantics, collection path placement, "
                "or a mongosh-vs-PyMongo syntax contrast. "
                "Prefer a fresh scenario that changes the context, not just the wording."
            )
        if concept == "_id and objectid":
            return (
                "Variation requirement for _id and ObjectId: do NOT ask another generic 'what is _id' question. "
                "Choose a different decision point such as automatic ObjectId generation, custom _id values, querying by _id, "
                "or why ObjectId is used as a unique identifier. "
                "Prefer a fresh scenario with a different data shape or insert/query action."
            )
    if topic_id == 3:
        if concept == "find()":
            return (
                "Variation requirement for find(): do NOT ask about find_one(), single-document return values, Python dictionaries, or projections. "
                "Keep the concept on find() returning a cursor / iterable result set, basic filter usage, and retrieving multiple documents. "
                "Prefer scenarios about many matching documents, cursor behavior, or choosing find() over single-document methods."
            )
        if concept == "sort/limit/skip":
            return (
                "Variation requirement for sort/limit/skip: do NOT keep asking generic limit-only questions. "
                "Prefer fresh scenarios about sort direction, chaining order, skip for pagination offsets, or combined sort().skip().limit() behavior. "
                "Ensure the concept coverage includes all three methods rather than repeating limit() syntax."
            )

    if "return" in avoid_text and "insertmany" in concept:
        return "Return-value questions are already overused here. Ask a different insertMany() decision point."
    if "syntax" in avoid_text and "insertone" in concept:
        return "Syntax questions are already overused here. Ask a different insertOne() decision point."

    return ""


def generate_weighted_question(
    target: StyleTarget | QuestionTarget,
    context_text: str,
    avoid_questions: list[str] | None = None,
    citation_source: str = "",
) -> dict | None:
    import random
    is_pymongo = "pymongo" in target.topic.lower() or "driver" in target.topic.lower()
    syntax_rule = (
        "Use PyMongo snake_case where the question is driver-specific, and contrast with mongosh only when useful."
        if is_pymongo
        else "Use strictly mongosh camelCase syntax. Do not use PyMongo snake_case in non-driver topics."
    )
    
    # Retrieve style choice directly from the target
    style_choice = getattr(target, "style_type", None)
    if not style_choice:
        if target.topic_id in {2, 3, 4, 5, 6, 7, 8, 9, 11, 12}:
            style_choice = random.choices(
                ["Type A", "Type B", "Type C", "Type D"],
                weights=[0.35, 0.25, 0.20, 0.20],
                k=1
            )[0]
        else:
            style_choice = "Type B"

    if style_choice == "Type A":
        style_name = "Syntax Selection & Trap Spotting"
        style_prompt = """
Style Target: Type A - Syntax Selection & Trap Spotting
- Design a question where the student is given a coding scenario and must select the syntactically correct query, command, or method call.
- The options should look extremely similar to test precise knowledge of syntax rules (e.g., camelCase vs. snake_case, correct/incorrect quoting of dot-notation paths like {"address.city": "val"} vs. {address.city: "val"}, or correct/incorrect bracket placement like [] vs {} for array queries).
- Only one option must be syntactically valid and correct.
"""
    elif style_choice == "Type C":
        style_name = "Predicting Query Output"
        style_prompt = """
Style Target: Type C - Predicting Query Output
- Design a question where a small JSON dataset (or document structure) and a query or aggregation pipeline is presented in the question stem.
- The student must predict what the command outputs or how many documents are returned.
- Focus on Aggregation pipeline tracing (such as $unwind, $project, $lookup stages) or Array query behavior (such as $elemMatch vs implicit array matching).
"""
    elif style_choice == "Type D":
        style_name = "Troubleshooting, Errors & Performance"
        style_prompt = """
Style Target: Type D - Troubleshooting, Errors & Performance
- Design a question focused on error resolution, exception handling, or database performance.
- Focus on scenarios where a query throws an error (e.g., mixing field inclusion/exclusion in a projection, duplicate key write errors, transaction failures), how bulk write operations behave when `ordered` is true vs false, or analyzing simplified explain plan output (such as COLLSCAN vs IXSCAN or nReturned vs totalKeysExamined).
- The options should represent different resolutions, explanation of errors, or performance optimizations, with exactly one correct option.
"""
    else:
        style_name = "Theory, Constraints & Data Modeling"
        style_prompt = """
Style Target: Type B - Theory, Constraints & Data Modeling
- Design a conceptual, rule-based, or architectural question.
- Focus on MongoDB limitations (e.g., 16MB document size limit, BSON types), indexing rules (compound index prefixes, covered queries, multikey index limits), or modeling decisions (embedding vs. referencing trade-offs).
"""

    avoid_block = ""
    if avoid_questions:
        avoid_lines = "\n".join(f"- {text[:240]}" for text in avoid_questions[:12])
        avoid_block = f"""
Existing questions to avoid for this exact topic/concept/difficulty:
{avoid_lines}

You must create a genuinely different scenario, ask for a different decision point, and avoid reusing the same wording.
Do not reuse the same code shape, error condition, or return-value framing from these examples.
"""

    variation_block = _concept_variation_guidance(target, avoid_questions)
    if variation_block:
        variation_block = f"""
Variation guidance:
- {variation_block}
"""

    prompt = f"""You are CertCoach, an expert MongoDB Associate Python Developer exam question writer.

Generate exactly one weighted exam MCQ.

Topic: {target.topic}
Question bank key: {target.bank_topic}
Concept: {target.concept}
Difficulty: {target.difficulty}
Exam weight: {target.exam_weight:.2%}
Concept share within topic: {target.concept_weight:.2%}

Question Style:
{style_prompt}

Syntax rule:
{syntax_rule}

Question design:
- Build a fresh scenario, not a paraphrase of the documentation.
- Focus on one narrow decision point tied to the target concept.
- Make the four options similar enough to be believable, but only one should be correct.
- Prefer realistic MongoDB work: schema choice, query behavior, cursor behavior, driver behavior, Atlas workflow, or index tradeoff.
- The correct answer must be obvious to a careful reader of the source context, but not to someone relying on memory alone.

Official documentation context:
{context_text[:get_population_source_chars()]}

{avoid_block}
{variation_block}

Rules:
- Produce exactly 4 options with exactly 1 correct answer.
- The JSON object must use the field name `question`, not `question_text`.
- Prefer `correct_option_letter` with a single value A, B, C, or D if that is easier; `correct_answer` may also be the exact option text.
- Include at least one subtle exam-trap distractor.
- Make the difficulty match the requested level.
- Do not invent unsupported MongoDB behavior.
- Be strictly grounded in the provided documentation context. Do not test on concepts, APIs, commands, or drivers that are not explicitly documented in the provided source text.
- Do not jump ahead to advanced concepts (like indexing, aggregation, or PyMongo connection options) if the current topic/concept doesn't cover them. If the topic is Topic 1 (Overview & Document Model), keep the focus purely on BSON data types, fields, and collections.
- Do not create a cosmetic rewrite of a common MongoDB docs example; create a fresh scenario grounded in the context.
- Keep the output lean:
  - question: one sentence, under 70 words.
  - options: exactly four short strings, each under 35 words.
  - correct_answer or correct_option_letter: one clear answer marker.
  - citation_source: one official filename or section from the provided docs.
- Optional fields are allowed, but do not spend tokens on long explanations here.
- Do not include the seven-part explanation in this response; explanation repair will add it later.
- If you include trap_analysis, keep it short and concrete.
- Critical Output Format: You MUST output a single flat JSON object with exactly the keys defined in the schema. The "options" key MUST be a list of exactly 4 strings. Do NOT write your thought process or any other fields inside the "options" list.
- If you use a letter, set `correct_option_letter` to exactly one of A, B, C, or D. Do not invent any other answer marker.
{POPULATION_RULES}
"""
    
    # Use model_runner with quality gates
    model_runner = get_model_runner()
    
    # Extract source files from context for judge verification
    source_files = []
    if context_text:
        source_files = [f"context_{hash(context_text) % 10000}"]
    
    model_chain = get_population_model_chain()
    
    result = model_runner.generate_with_quality_gate(
        prompt=prompt,
        model_chain=model_chain,
        max_retries=2,
        source_files=source_files,
        context_text=context_text,
        response_kind="question_shell"
    )
    
    if not result["success"]:
        print(f"  [!] Quality gate failed for {target.concept} ({target.difficulty}): {result['quality_issues']}")
        return None
    
    mcq = SeedMCQ(**result["result"])
    if not mcq or len(mcq.options) != 4:
        return None

    correct_answer = _resolve_correct_answer(mcq)
    if not correct_answer:
        return None

    correct_idx = mcq.options.index(correct_answer)
    trap_idx = 1 if correct_idx != 1 else 0
    fingerprint = question_fingerprint(target.bank_topic, target.concept, mcq.question)
    question_number = _next_question_number(target)
    q_id = make_question_id(target, question_number, fingerprint)

    chosen_citation_source = (mcq.citation_source or citation_source or "").strip()
    return {
        "_id": q_id,
        "metadata": {
            "topic": target.bank_topic,
            "syllabus_topic": target.topic,
            "topic_id": target.topic_id,
            "concept": target.concept,
            "difficulty": target.difficulty,
            "question_style": style_name,
            "question_style_type": style_choice,
            "question_number": question_number,
            "question_fingerprint": fingerprint,
            "exam_weight": target.exam_weight,
            "concept_weight": target.concept_weight,
            "generation_source": "nightly_weighted_seed",
            "citation_source": chosen_citation_source,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            **contract_metadata("nightly_weighted_seed"),
        },
        "context": {
            "scenario_description": f"Weighted {target.difficulty.lower()} practice for {target.concept}.",
            "database_info": "",
        },
        "question_text": mcq.question,
        "options": [
            {
                "option_letter": LETTERS[idx],
                "code_snippet": option,
                "is_correct": idx == correct_idx,
                "is_trap": idx == trap_idx,
                "feedback": mcq.feedbacks[idx] if idx < len(mcq.feedbacks) else "",
            }
            for idx, option in enumerate(mcq.options)
        ],
        "explanation": "",
        "trap_analysis": mcq.trap_analysis,
        "citation_source": chosen_citation_source,
        "global_metrics": {
            "times_seen": 0,
            "times_correct": 0,
            "times_incorrect": 0,
            "average_time_seconds": 0.0,
        },
    }


def run_weighted_seed(
    total_bank_target: int | None = None,
    max_questions: int | None = None,
    dry_run: bool = False,
    topic_filter: str | None = None,
    concept_filter: str | None = None,
    max_attempts_per_slot: int = 5,
    extra_easy: int = 0,
    extra_medium: int = 0,
    target_easy: int | None = None,
    target_medium: int | None = None,
) -> int:
    database.check_connection()
    model, local_llm_url = _load_env()
    syllabus_by_id = {item["id"]: item for item in planner.load_syllabus()}
    deficits = audit_weighted_deficits(
        total_bank_target=total_bank_target,
        topic_filter=topic_filter,
        concept_filter=concept_filter,
        target_easy=target_easy,
        target_medium=target_medium,
        extra_easy=extra_easy,
        extra_medium=extra_medium,
    )
    concept_order = {
        (item["id"], concept): concept_index
        for item in planner.load_syllabus()
        for concept_index, concept in enumerate(item.get("subtopics", []))
    }
    difficulty_order = {"Easy": 0, "Medium": 1}
    deficits.sort(key=lambda item: (
        item[0].topic_id,
        concept_order.get((item[0].topic_id, item[0].concept), 10_000),
        difficulty_order.get(item[0].difficulty, 10),
        item[0].style_type,
    ))

    total_missing = sum(missing for _, missing in deficits)
    print(f"\nCertCoach Weighted Nightly Seeder")
    effective_easy_target = max(3, target_easy if target_easy is not None else get_population_easy_target())
    effective_medium_target = max(2, target_medium if target_medium is not None else get_population_medium_target())
    print("Study-ready threshold: 3 Easy + 2 Medium per concept")
    print(f"Population inventory target: {effective_easy_target} Easy + {effective_medium_target} Medium per concept")
    if extra_easy or extra_medium:
        print(f"Explicit extras requested per concept: +{extra_easy} Easy, +{extra_medium} Medium")
    if topic_filter:
        print(f"Topic filter: {topic_filter}")
    if concept_filter:
        print(f"Concept filter: {concept_filter}")
    print(f"Requested generation slots: {total_missing}\n")

    if dry_run:
        for target, missing in deficits[:50]:
            print(f"- Topic {target.topic_id} | {target.concept} | {target.difficulty} ({target.style_type}): missing {missing}")
        return 0

    inserted = 0
    failures = 0
    attempted_slots = 0
    total_to_attempt = min(total_missing, max_questions) if max_questions is not None else total_missing

    progress = Progress(
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
    )

    try:
        with progress:
            task_id = progress.add_task("Seeding weighted questions", total=total_to_attempt)
            for target, missing in deficits:
                topic_item = syllabus_by_id[target.topic_id]
                md_files = topic_item.get("md_files", [])
                context_text = planner.load_md_context(md_files, prioritize_concept=target.concept)
                weak_focus_context = planner.load_topic_benchmark_focus(target.topic_id, target.concept)
                if isinstance(weak_focus_context, str) and weak_focus_context.strip():
                    context_text = "\n\n---\n\n".join(
                        part for part in (weak_focus_context, context_text)
                        if isinstance(part, str) and part.strip()
                    )
                if not context_text:
                    progress.console.print(f"  [yellow][skip][/yellow] No docs for Topic {target.topic_id}: {target.topic}")
                    continue

                prioritized = planner.prioritize_md_files(md_files, target.concept)
                progress.console.print(f"\n[cyan][Target Info][/cyan] Topic {target.topic_id} ({target.topic}) | Concept: [bold]{target.concept}[/bold] | Difficulty: {target.difficulty} | Style: [bold]{target.style_type}[/bold]")
                progress.console.print(f"  - Mapped md files: {md_files}")
                progress.console.print(f"  - Prioritized context file: [bold green]{prioritized[0] if prioritized else 'None'}[/bold green]")
                progress.console.print(f"  - Injected Context Length: {len(context_text)} characters")

                generated_for_target = 0
                while generated_for_target < missing:
                    if max_questions is not None and attempted_slots >= max_questions:
                        progress.console.print(
                            f"\nReached max_questions={max_questions}. "
                            f"Attempted {attempted_slots} slots and inserted {inserted}."
                        )
                        return inserted

                    attempted_slots += 1
                    label = f"T{target.topic_id} {target.concept} ({target.difficulty} - {target.style_type})"
                    progress.update(task_id, description=f"Seeding: {label[:52]}")
                    attempts = 0
                    slot_filled = False
                    avoid_questions = existing_question_samples(target)
                    while attempts < max_attempts_per_slot and not slot_filled:
                        attempts += 1
                        primary_source = prioritized[0] if prioritized else (md_files[0] if md_files else "")
                        question = generate_weighted_question(target, context_text, avoid_questions, primary_source)
                        if not question:
                            failures += 1
                            progress.console.print(f"[yellow]Generation retry:[/yellow] empty/invalid response for {label} ({attempts}/{max_attempts_per_slot})")
                            continue

                        is_valid, quality_issues = validate_question_quality(question, require_explanation=False)
                        if not is_valid:
                            failures += 1
                            progress.console.print(f"[yellow]Quality retry:[/yellow] {question.get('_id')} - {'; '.join(quality_issues)} ({attempts}/{max_attempts_per_slot})")
                            avoid_questions.append(question.get("question_text", ""))
                            continue

                        is_dup, reason = is_duplicate_question(question, target)
                        if is_dup:
                            progress.console.print(f"[yellow]Duplicate retry:[/yellow] {reason} ({attempts}/{max_attempts_per_slot})")
                            avoid_questions.append(question.get("question_text", ""))
                            continue

                        question["metadata"]["content_contract_status"] = "needs_explanation_repair"
                        database.questions_col.insert_one(question)
                        try:
                            from certcoach.jobs.repair_explanations import apply_repair, generate_repair

                            repair_candidate = database.questions_col.find_one({"_id": question["_id"]}) or question
                            repair = generate_repair(repair_candidate)
                            if repair:
                                apply_repair(repair_candidate, repair)
                                repaired_question = database.questions_col.find_one({"_id": question["_id"]}) or repair_candidate
                                inserted += 1
                                generated_for_target += 1
                                progress.advance(task_id)
                                print_question_template(repaired_question)
                                slot_filled = True
                            else:
                                progress.console.print(f"[yellow]Repair pending:[/yellow] inserted shell for {label} but explanation repair failed")
                                failures += 1
                                generated_for_target += 1
                                progress.advance(task_id)
                                slot_filled = True
                        except Exception as exc:
                            progress.console.print(f"[yellow]Repair handoff failed:[/yellow] {exc}")
                            failures += 1
                            generated_for_target += 1
                            progress.advance(task_id)
                            slot_filled = True

                    if not slot_filled:
                        failures += 1
                        generated_for_target += 1
                        progress.advance(task_id)
                        progress.console.print(f"[red]Slot failed:[/red] {label} after {max_attempts_per_slot} attempts")
    finally:
        # Model unloading is now handled by model_runner internally
        pass

    print(f"\nWeighted seeding complete. Inserted {inserted} questions. Failed/skipped quality generations: {failures}.")
    return inserted


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Populate concepts toward configured inventory targets, with optional explicit extras.")
    parser.add_argument(
        "--topic",
        default=None,
        help="Populate one topic only. Accepts syllabus id, topic name, or question-bank topic key.",
    )
    parser.add_argument("--concept", default=None, help="Populate only this exact syllabus concept.")
    parser.add_argument("--max-questions", type=int, default=None, help="Cap generated questions for this run.")
    parser.add_argument("--extra-easy", type=int, default=0, help="Explicit additional Easy questions requested per selected concept.")
    parser.add_argument("--extra-medium", type=int, default=0, help="Explicit additional Medium questions requested per selected concept.")
    parser.add_argument("--target-easy", type=int, default=None, help="Override the configured Easy inventory target.")
    parser.add_argument("--target-medium", type=int, default=None, help="Override the configured Medium inventory target.")
    parser.add_argument("--max-attempts", type=int, default=5, help="Retry attempts per missing slot when the model returns duplicates or low-quality output.")
    parser.add_argument("--dry-run", action="store_true", help="Print deficits without generating questions.")
    args = parser.parse_args(argv)

    inserted = run_weighted_seed(
        None,
        args.max_questions,
        args.dry_run,
        args.topic,
        args.concept,
        args.max_attempts,
        args.extra_easy,
        args.extra_medium,
        args.target_easy,
        args.target_medium,
    )
    return 0 if args.dry_run or inserted >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
