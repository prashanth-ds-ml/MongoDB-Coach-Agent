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
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from certcoach.core import database, planner
from certcoach.core.question_targets import DEFAULT_TOTAL_BANK_TARGET, QuestionTarget, build_weighted_targets

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
- Avoid duplicates, near-duplicates, cosmetic rewrites of existing questions, and repeated scenarios for the same topic/concept/difficulty.
""".strip()

EXPLANATION_SECTION_MIN_LENGTHS = {
    "### 1. Correct Answer": 30,
    "### 2. Why Correct": 90,
    "### 3. Why Other Options Are Wrong": 140,
    "### 4. Exam Trap": 60,
    "### 5. Memory Hook": 80,
    "### 6. Follow-Up Practice Recommendation": 120,
    "### 7. Syntax Example": 20,
}

EXPLANATION_SECTION_MIN_BULLETS = {
    "### 6. Follow-Up Practice Recommendation": 3,
}

EASY_EXPLANATION_SECTION_MIN_LENGTHS = {
    "### 1. Correct Answer": 24,
    "### 2. Why Correct": 70,
    "### 3. Why Other Options Are Wrong": 110,
    "### 4. Exam Trap": 45,
    "### 5. Memory Hook": 45,
    "### 6. Follow-Up Practice Recommendation": 80,
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
    question: str = Field(description="The multiple choice question.")
    options: list[str] = Field(description="Exactly four options.")
    correct_answer: str = Field(description="The exact correct option text or letter.")
    feedbacks: list[str] = Field(description="Exactly four feedback strings, one per option.")
    trap_analysis: str = Field(description="The main exam trap.")
    six_part_explanation: str = Field(description="Six-part explanation markdown.")
    citation_source: str = Field(description="Official source filename or section.")


def _load_env() -> tuple[str, str]:
    load_dotenv()
    env_path = os.path.join(database.GLOBAL_CONFIG_DIR, ".env")
    load_dotenv(env_path)
    return (
        os.getenv("MODEL", "qwen2.5-coder:7b"),
        os.getenv("LOCAL_LLM_URL", "http://localhost:11434"),
    )


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
            {"model": model, "prompt": "", "stream": False, "keep_alive": "30m", "options": {"num_ctx": 8192}},
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


def _question_count(target: QuestionTarget) -> int:
    return database.questions_col.count_documents({
        "metadata.topic": target.bank_topic,
        "metadata.concept": target.concept,
        "metadata.difficulty": target.difficulty,
    })


def _topic_matches(target: QuestionTarget, topic_filter: str | None) -> bool:
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


def audit_weighted_deficits(
    total_bank_target: int = DEFAULT_TOTAL_BANK_TARGET,
    topic_filter: str | None = None,
) -> list[tuple[QuestionTarget, int]]:
    targets = build_weighted_targets(planner.load_syllabus(), total_bank_target=total_bank_target)
    deficits = []
    for target in targets:
        if not _topic_matches(target, topic_filter):
            continue
        current = _question_count(target)
        missing = max(0, target.target_count - current)
        if missing:
            deficits.append((target, missing))
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
    return sum(1 for line in section.splitlines() if line.strip().startswith(("-", "*")))


def _count_code_fences(section: str) -> int:
    return section.count("```")


def _question_needs_syntax_example(question: dict) -> bool:
    metadata = question.get("metadata", {}) or {}
    topic_id = metadata.get("topic_id")
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


def make_question_id(target: QuestionTarget, question_number: int, fingerprint: str) -> str:
    difficulty = _slug(target.difficulty, 8)
    concept = _slug(target.concept, 32)
    return f"certcoach-t{target.topic_id:02d}-{concept}-{difficulty}-{question_number:03d}-{fingerprint[:8]}"


def is_duplicate_question(question: dict, target: QuestionTarget) -> tuple[bool, str]:
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


def validate_question_quality(question: dict) -> tuple[bool, list[str]]:
    issues = []
    options = question.get("options", [])
    explanation = str(question.get("explanation", "") or "")
    needs_syntax_example = _question_needs_syntax_example(question)
    difficulty = _difficulty_key(question)
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
    if len(explanation.strip()) < 800:
        issues.append("seven-part explanation is too short")
    if len({str(option.get("code_snippet", "")).strip().lower() for option in options}) != len(options):
        issues.append("duplicate option text")
    return not issues, issues


def print_question_template(question: dict) -> None:
    meta = question.get("metadata", {})
    console.print(f"\n[bold green]Inserted {question.get('_id')}[/bold green]")
    console.print(f"[cyan]Topic:[/cyan] {meta.get('topic')} | [cyan]Concept:[/cyan] {meta.get('concept')} | [cyan]Difficulty:[/cyan] {meta.get('difficulty')}")
    console.print(f"[bold]Question:[/bold] {question.get('question_text', '')}")
    for option in question.get("options", []):
        tags = []
        if option.get("is_correct"):
            tags.append("correct")
        if option.get("is_trap"):
            tags.append("trap")
        suffix = f" [{' / '.join(tags)}]" if tags else ""
        console.print(f"  {option.get('option_letter')}. {option.get('code_snippet', '')}{suffix}")
    console.print("[bold]Seven-Part Explanation:[/bold]")
    console.print(question.get("explanation", ""))


def existing_question_samples(target: QuestionTarget, limit: int = 8) -> list[str]:
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


def generate_weighted_question(target: QuestionTarget, context_text: str, avoid_questions: list[str] | None = None) -> dict | None:
    model, local_llm_url = _load_env()
    is_pymongo = "pymongo" in target.topic.lower() or "driver" in target.topic.lower()
    syntax_rule = (
        "Use PyMongo snake_case where the question is driver-specific, and contrast with mongosh only when useful."
        if is_pymongo
        else "Use strictly mongosh camelCase syntax. Do not use PyMongo snake_case in non-driver topics."
    )
    avoid_block = ""
    if avoid_questions:
        avoid_lines = "\n".join(f"- {text[:240]}" for text in avoid_questions[:12])
        avoid_block = f"""
Existing questions to avoid for this exact topic/concept/difficulty:
{avoid_lines}

You must create a genuinely different scenario, ask for a different decision point, and avoid reusing the same wording.
Do not reuse the same code shape, error condition, or return-value framing from these examples.
"""

    prompt = f"""You are CertCoach, an expert MongoDB Associate Python Developer exam question writer.

Generate exactly one weighted exam MCQ.

Topic: {target.topic}
Question bank key: {target.bank_topic}
Concept: {target.concept}
Difficulty: {target.difficulty}
Exam weight: {target.exam_weight:.2%}
Concept share within topic: {target.concept_weight:.2%}

Syntax rule:
{syntax_rule}

Question design:
- Build a fresh scenario, not a paraphrase of the documentation.
- Focus on one narrow decision point tied to the target concept.
- Make the four options similar enough to be believable, but only one should be correct.
- Prefer realistic MongoDB work: schema choice, query behavior, cursor behavior, driver behavior, Atlas workflow, or index tradeoff.
- The correct answer must be obvious to a careful reader of the source context, but not to someone relying on memory alone.

Official documentation context:
{context_text[:7000]}

{avoid_block}

Rules:
- Produce exactly 4 options with exactly 1 correct answer.
- Include at least one subtle exam-trap distractor.
- Make the difficulty match the requested level.
- Do not invent unsupported MongoDB behavior.
- Do not create a cosmetic rewrite of a common MongoDB docs example; create a fresh scenario grounded in the context.
- The six_part_explanation must contain these headings:
  ### 1. Correct Answer
  ### 2. Why Correct
  ### 3. Why Other Options Are Wrong
  ### 4. Exam Trap
  ### 5. Memory Hook
  ### 6. Follow-Up Practice Recommendation
  ### 7. Syntax Example
- Section 5 should be a compact mnemonic or memory hook with one or two concrete rules.
- Section 6 must be 3 to 5 bullet points, each bullet being a compact but specific action item or recall point.
- Section 7 should follow this rule: if the concept is syntax-heavy, include one short fenced code example plus 2 brief bullets explaining it; if not, write exactly "Not required for this concept."
- Each section must be detailed enough for a beginner to learn from the answer review.
- Section 3 must explicitly explain why each distractor is wrong.
- Explain every relevant syntax token, operator, method argument, return value, and casing trap.
- Use a short analogy in either Why Correct or Memory Hook when it helps anchor the concept.
{QUALITY_RULES}
"""
    try:
        llm = ChatOllama(model=model, base_url=local_llm_url, temperature=0.25, timeout=120.0, num_ctx=8192)
        mcq = llm.with_structured_output(SeedMCQ).invoke(prompt)
    except Exception as exc:
        print(f"  [!] Generation failed for {target.concept} ({target.difficulty}): {exc}")
        return None

    if not mcq or len(mcq.options) != 4:
        return None
    while len(mcq.feedbacks) < 4:
        mcq.feedbacks.append("Review the official MongoDB documentation for this concept.")
    mcq.feedbacks = mcq.feedbacks[:4]

    correct_answer = _resolve_correct_answer(mcq)
    if not correct_answer:
        return None

    correct_idx = mcq.options.index(correct_answer)
    trap_idx = 1 if correct_idx != 1 else 0
    fingerprint = question_fingerprint(target.bank_topic, target.concept, mcq.question)
    question_number = _next_question_number(target)
    q_id = make_question_id(target, question_number, fingerprint)

    return {
        "_id": q_id,
        "metadata": {
            "topic": target.bank_topic,
            "syllabus_topic": target.topic,
            "topic_id": target.topic_id,
            "concept": target.concept,
            "difficulty": target.difficulty,
            "question_number": question_number,
            "question_fingerprint": fingerprint,
            "exam_weight": target.exam_weight,
            "concept_weight": target.concept_weight,
            "generation_source": "nightly_weighted_seed",
            "citation_source": mcq.citation_source,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
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
                "feedback": mcq.feedbacks[idx],
            }
            for idx, option in enumerate(mcq.options)
        ],
        "explanation": mcq.six_part_explanation,
        "trap_analysis": mcq.trap_analysis,
        "citation_source": mcq.citation_source,
        "global_metrics": {
            "times_seen": 0,
            "times_correct": 0,
            "times_incorrect": 0,
            "average_time_seconds": 0.0,
        },
    }


def run_weighted_seed(
    total_bank_target: int = DEFAULT_TOTAL_BANK_TARGET,
    max_questions: int | None = None,
    dry_run: bool = False,
    topic_filter: str | None = None,
    max_attempts_per_slot: int = 5,
) -> int:
    database.check_connection()
    model, local_llm_url = _load_env()
    syllabus_by_id = {item["id"]: item for item in planner.load_syllabus()}
    deficits = audit_weighted_deficits(total_bank_target=total_bank_target, topic_filter=topic_filter)
    deficits.sort(key=lambda item: (item[0].exam_weight, item[1]), reverse=True)

    total_missing = sum(missing for _, missing in deficits)
    print(f"\nCertCoach Weighted Nightly Seeder")
    print(f"Target bank size: {total_bank_target}")
    if topic_filter:
        print(f"Topic filter: {topic_filter}")
    print(f"Missing weighted slots: {total_missing}\n")

    if dry_run:
        for target, missing in deficits[:50]:
            print(f"- Topic {target.topic_id} | {target.concept} | {target.difficulty}: missing {missing}")
        return 0

    inserted = 0
    failures = 0
    total_to_attempt = min(total_missing, max_questions) if max_questions is not None else total_missing

    clear_ollama_memory(local_llm_url)
    preload_ollama_model(model, local_llm_url)
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=34),
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
                context_text = planner.load_md_context(topic_item.get("md_files", []))
                if not context_text:
                    console.print(f"  [yellow][skip][/yellow] No docs for Topic {target.topic_id}: {target.topic}")
                    continue

                generated_for_target = 0
                while generated_for_target < missing:
                    if max_questions is not None and inserted >= max_questions:
                        console.print(f"\nReached max_questions={max_questions}. Inserted {inserted}.")
                        return inserted

                    label = f"T{target.topic_id} {target.concept} ({target.difficulty})"
                    progress.update(task_id, description=f"Seeding: {label[:52]}")
                    attempts = 0
                    slot_filled = False
                    avoid_questions = existing_question_samples(target)
                    while attempts < max_attempts_per_slot and not slot_filled:
                        attempts += 1
                        question = generate_weighted_question(target, context_text, avoid_questions)
                        if not question:
                            failures += 1
                            console.print(f"[yellow]Generation retry:[/yellow] empty/invalid response for {label} ({attempts}/{max_attempts_per_slot})")
                            continue

                        is_valid, quality_issues = validate_question_quality(question)
                        if not is_valid:
                            failures += 1
                            console.print(f"[yellow]Quality retry:[/yellow] {question.get('_id')} - {'; '.join(quality_issues)} ({attempts}/{max_attempts_per_slot})")
                            avoid_questions.append(question.get("question_text", ""))
                            continue

                        is_dup, reason = is_duplicate_question(question, target)
                        if is_dup:
                            console.print(f"[yellow]Duplicate retry:[/yellow] {reason} ({attempts}/{max_attempts_per_slot})")
                            avoid_questions.append(question.get("question_text", ""))
                            continue

                        database.questions_col.insert_one(question)
                        inserted += 1
                        generated_for_target += 1
                        progress.advance(task_id)
                        print_question_template(question)
                        slot_filled = True

                    if not slot_filled:
                        failures += 1
                        generated_for_target += 1
                        progress.advance(task_id)
                        console.print(f"[red]Slot failed:[/red] {label} after {max_attempts_per_slot} attempts")
    finally:
        unload_ollama_model(model, local_llm_url)

    print(f"\nWeighted seeding complete. Inserted {inserted} questions. Failed/skipped quality generations: {failures}.")
    return inserted


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Populate CertCoach questions by exam/topic/concept weight.")
    parser.add_argument("--target", type=int, default=DEFAULT_TOTAL_BANK_TARGET, help="Total weighted question-bank target.")
    parser.add_argument(
        "--topic",
        default=None,
        help="Populate one topic only. Accepts syllabus id, topic name, or question-bank topic key.",
    )
    parser.add_argument("--max-questions", type=int, default=None, help="Cap generated questions for this run.")
    parser.add_argument("--max-attempts", type=int, default=5, help="Retry attempts per missing slot when the model returns duplicates or low-quality output.")
    parser.add_argument("--dry-run", action="store_true", help="Print deficits without generating questions.")
    args = parser.parse_args(argv)

    inserted = run_weighted_seed(args.target, args.max_questions, args.dry_run, args.topic, args.max_attempts)
    return 0 if args.dry_run or inserted >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
