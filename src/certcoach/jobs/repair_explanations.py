import argparse
import os
import sys
import time
from datetime import datetime, timezone

from bson import ObjectId
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

from certcoach.core.config import get_ollama_timeout

from certcoach.core import database, planner
from certcoach.core.bank_state import matches_concept_filter, matches_topic_filter
from certcoach.core.config import (
    get_local_llm_url,
    get_ollama_timeout,
    get_repair_model,
    get_repair_model_chain,
    get_repair_num_ctx,
)
from certcoach.core.content_contract import contract_metadata
from certcoach.core.model_runner import get_model_runner
from certcoach.core.judge_questions import judge_explanation_repair
from certcoach.jobs.nightly_seed_questions import (
    QUALITY_RULES,
    SEVEN_PART_HEADINGS,
    _question_needs_syntax_example,
    validate_question_quality,
)

console = Console()
REPAIR_ATTEMPTS = 3
REPAIR_PENDING_STATUS = "needs_explanation_repair"


def _ascii_safe(text: str) -> str:
    return (text or "").encode("ascii", "replace").decode("ascii")


def _load_env() -> tuple[str, str]:
    return get_repair_model(), get_local_llm_url()


class RepairedExplanationSchema(BaseModel):
    feedbacks: list[str] = Field(description="Exactly four detailed feedback strings matching options A, B, C, D in order.")
    trap_analysis: str = Field(description="Detailed exam trap explanation.")
    explanation_correct_answer: str = Field(description="What is the correct answer and a brief statement of it.")
    explanation_why_correct: str = Field(description="Detailed explanation of why the correct option is correct.")
    explanation_why_wrong: str = Field(description="Detailed explanation of why each of the other three options is incorrect, explaining the flaw in each option.")
    explanation_exam_trap: str = Field(description="Description of the exam trap or common misconception related to this concept.")
    explanation_memory_hook: str = Field(description="A compact mnemonic or memory hook with one or two concrete rules to remember.")
    explanation_practice_recommendations: list[str] = Field(description="A list of 3 to 5 compact but specific action items or recall points for practice.")
    explanation_syntax_example: str = Field(description="A markdown string containing a fenced code block of a syntax example if the concept is syntax-heavy, or exactly 'Not required for this concept.' if not syntax-heavy.")


class RepairedExplanation(BaseModel):
    explanation: str = Field(description="Detailed seven-part explanation markdown.")
    feedbacks: list[str] = Field(description="Exactly four detailed feedback strings, one per option.")
    trap_analysis: str = Field(description="Detailed exam trap explanation.")


def _find_question(question_id: str) -> dict | None:
    q = database.questions_col.find_one({"_id": question_id})
    if q:
        return q
    try:
        return database.questions_col.find_one({"_id": ObjectId(question_id)})
    except Exception:
        return None


def _topic_matches(q: dict, topic_filter: str | None) -> bool:
    return matches_topic_filter(q, topic_filter)


def _concept_matches(q: dict, concept_filter: str | None) -> bool:
    return matches_concept_filter(q, concept_filter)


def _syllabus_order_key(q: dict, syllabus: list[dict]) -> tuple[int, int, str]:
    metadata = q.get("metadata", {}) or {}
    topic_id = metadata.get("topic_id")
    concept = str(metadata.get("concept", ""))
    for topic_index, topic_item in enumerate(syllabus):
        if topic_item["id"] != topic_id:
            continue
        concepts = topic_item.get("subtopics", [])
        concept_index = concepts.index(concept) if concept in concepts else len(concepts)
        return topic_index, concept_index, str(q.get("_id", ""))
    return len(syllabus), 0, str(q.get("_id", ""))


def is_structurally_repairable(q: dict) -> tuple[bool, str]:
    options = q.get("options", [])
    if not q.get("question_text"):
        return False, "missing question_text"
    if len(options) != 4:
        return False, "does not have exactly 4 options"
    if sum(1 for opt in options if opt.get("is_correct")) != 1:
        return False, "does not have exactly one correct option"
    return True, "repairable"


def is_marked_for_explanation_repair(q: dict) -> bool:
    status = str(q.get("metadata", {}).get("content_contract_status", "")).strip().lower()
    return status == REPAIR_PENDING_STATUS


def _repair_quality_issues(q: dict, repaired: RepairedExplanation) -> list[str]:
    candidate = dict(q)
    candidate["explanation"] = repaired.explanation
    candidate["trap_analysis"] = repaired.trap_analysis
    candidate["options"] = [
        {**dict(opt), "feedback": repaired.feedbacks[idx]}
        for idx, opt in enumerate(q.get("options", []))
    ]
    ok, issues = validate_question_quality(candidate)
    return [] if ok else issues


def _normalize_practice_recommendations(q: dict, recs: list[str]) -> list[str]:
    concept = str(q.get("metadata", {}).get("concept", "")).strip()
    topic = str(q.get("metadata", {}).get("topic", "")).strip()
    defaults = [
        f"Compare how {concept or 'this concept'} behaves in the exact scenario shown in the question.",
        f"Memorize the return type, syntax shape, and common exam trap for {concept or 'this concept'}.",
        f"Practice explaining why the wrong options fail for {concept or topic or 'this topic'} without using vague wording.",
    ]
    cleaned = [str(item).strip() for item in recs if str(item).strip()]
    if len(cleaned) >= 3:
        return cleaned[:3]
    for item in defaults:
        if len(cleaned) >= 3:
            break
        if item not in cleaned:
            cleaned.append(item)
    while len(cleaned) < 3:
        cleaned.append(defaults[len(cleaned)])
    return cleaned[:3]


def _synthesize_syntax_example(q: dict) -> str:
    concept = str(q.get("metadata", {}).get("concept", "")).strip().lower()

    if "replaceone" in concept or "replace_one" in concept:
        return """```python
collection.replace_one({'status': 'inactive'}, {'status': 'active', 'type': 'admin'})

# 1. The first argument is the filter used to find the document.
# 2. The second argument is a plain replacement document with no $ operators.
```"""

    if "updateone" in concept or "updatemany" in concept:
        return """```python
collection.update_one({'status': 'inactive'}, {'$set': {'status': 'active'}})

# 1. The first argument is the filter used to find matching documents.
# 2. The second argument uses an update operator such as $set instead of a raw replacement document.
```"""

    if "insertmany" in concept:
        return """```python
collection.insert_many([
    {'name': 'Ada'},
    {'name': 'Grace'}
])

# 1. The method takes an iterable of documents, not a single document.
# 2. Each item in the array is inserted as its own MongoDB document.
```"""

    if "insertone" in concept:
        return """```python
collection.insert_one({'name': 'Ada', 'role': 'engineer'})

# 1. The method inserts exactly one document.
# 2. The argument is a single plain document, not a list of documents.
```"""

    if "findone" in concept:
        return """```python
collection.find_one({'status': 'active'})

# 1. The method returns one document or None.
# 2. The filter is the same shape as a find query, but the result is a single document.
```"""

    if "find()" in concept or concept == "find" or concept == "find_one":
        return """```python
cursor = collection.find({'status': 'active'})

# 1. find() returns a cursor, so you iterate over the results.
# 2. The filter can match many documents, not just one.
```"""

    return """```python
# Use the exact method and document shape shown in the question.
collection.method_name({...})

# 1. Match the syntax in the prompt.
# 2. Keep the operator and argument shape aligned with the concept.
```"""


def _normalize_syntax_example(q: dict, syntax_example: str, needs_syntax_example: bool) -> str:
    if not needs_syntax_example:
        return syntax_example.strip() if syntax_example.strip() else "Not required for this concept."

    value = syntax_example.strip()
    if "```" in value and len(value) >= 80:
        return value

    return _synthesize_syntax_example(q)


def generate_repair(q: dict) -> RepairedExplanation | None:
    meta = q.get("metadata", {})
    needs_syntax_example = _question_needs_syntax_example(q)
    options_text = []
    for opt in q.get("options", []):
        correctness = "CORRECT" if opt.get("is_correct") else "WRONG"
        options_text.append(
            f"{opt.get('option_letter', '?')}) {opt.get('code_snippet', '')}\n"
            f"Marked: {correctness}\n"
            f"Current feedback: {opt.get('feedback', '')}"
        )

    syntax_instruction = (
        "- This concept is syntax-heavy, so `explanation_syntax_example` MUST be a short fenced code block with 2 brief bullets explaining the exact syntax being tested.\n"
        "- Do not output 'Not required for this concept.' for syntax-heavy concepts.\n"
        "- Keep the example aligned to the same method or operator used in the question.\n"
        if needs_syntax_example
        else "- This concept is conceptual, so `explanation_syntax_example` should be exactly 'Not required for this concept.'\n"
    )

    concept_name = str(meta.get("concept", "") or "").lower()
    if needs_syntax_example and "insertmany" in concept_name:
        syntax_instruction += (
            "- For insertMany(), show a short mongosh example that includes the array of documents and, if relevant, the options object.\n"
            "- End the section with exactly 2 short bullets that explain the array argument and the key option being tested.\n"
        )
    elif needs_syntax_example and "insertone" in concept_name:
        syntax_instruction += (
            "- For insertOne(), show a short mongosh example that inserts one document into a named collection.\n"
            "- End the section with exactly 2 short bullets that explain the single-document argument and the collection path.\n"
        )
    elif needs_syntax_example and ("find()" in concept_name or "findone" in concept_name or "find_" in concept_name):
        syntax_instruction += (
            "- For find()/find_one() concepts, show a short PyMongo example that contrasts the cursor returned by find() with the single-document result returned by find_one().\n"
            "- End the section with exactly 2 short bullets that explain cursor vs document return behavior and the query filter shape.\n"
        )
        syntax_instruction += (
            "- For the memory hook, use this exact contrast or a very close paraphrase: 'Find is for a crowd; find_one is for one.' Include two explicit rules: find() returns a cursor for many documents, and find_one() returns a single document.\n"
            "- For the exam trap, explicitly contrast cursor vs single-document return behavior and say that the trap is confusing one-document retrieval with many-document retrieval or assuming both methods return the same type.\n"
            "- For the practice recommendations, include exactly 3 items and make one of them compare cursor iteration versus direct document access.\n"
            "- Do not leave the memory hook, exam trap, or practice recommendations generic or empty; they must directly contrast cursor vs single-document behavior.\n"
        )

    prompt = f"""You are CertCoach, an expert MongoDB Associate Python Developer exam editor.

Repair the explanation quality for this existing question. Do NOT change the question text, option text, correct answer, or option letters.

Topic: {meta.get('topic', 'General')}
Syllabus topic: {meta.get('syllabus_topic', '')}
Concept: {meta.get('concept', '')}
Difficulty: {meta.get('difficulty', '')}

Question:
{q.get('question_text', '')}

Options:
{chr(10).join(options_text)}

Current explanation:
{q.get('explanation', '')}

Current trap analysis:
{q.get('trap_analysis', '')}

Return detailed explanation and feedback fields matching the schema:
- `feedbacks`: exactly four detailed feedback strings matching options A, B, C, D in order.
- `trap_analysis`: detailed exam-trap analysis.
- `explanation_correct_answer`: brief statement of the correct option and why.
- `explanation_why_correct`: detailed explanation of why the correct option is correct.
- `explanation_why_wrong`: detailed explanation of why each of the other three options is incorrect, explaining the flaw in each option.
- `explanation_exam_trap`: description of the exam trap or common misconception related to this concept.
- `explanation_memory_hook`: a compact mnemonic or memory hook with at least two concrete rules. Make it long enough to survive validation and useful enough to remember under exam pressure.
- `explanation_practice_recommendations`: a list of exactly 3 compact but specific action items or recall points for practice. Each item should be a full sentence with enough detail to stand alone. Do NOT add markdown hyphen prefixes (e.g. - ) inside the list items themselves; the system will format them.
- `explanation_syntax_example`: a markdown string containing a fenced code block of a syntax example if the concept is syntax-heavy, or exactly 'Not required for this concept.' if not syntax-heavy.

Make it beginner-friendly but technically precise. Explain syntax tokens, method names, operators, return values, casing traps, and why each distractor is wrong.
For the memory hook, prefer a two-part rule of thumb that names the BSON type or concept and the most common exam trap.
For Topic 3 find()/find_one(), make the memory hook explicit: compare cursor vs single-document behavior and mention that `find()` is for many while `find_one()` is for one.
For Topic 3 find()/find_one(), use the exact memory-hook wording above if needed; do not invent a totally new hook if the prompt already supplies one.
For the practice recommendations, avoid one-word reminders; each recommendation should tell the learner exactly what to compare, memorize, or practice.
Do not omit any required field, even if the answer seems obvious. Every JSON key must have a non-empty, substantive value.
For Topic 3 find()/find_one() repairs, treat the following as mandatory:
- The memory hook must explicitly contrast cursor vs single-document behavior.
- The exam trap must explicitly mention that the common mistake is confusing a cursor-returning method with a single-document method.
- The practice recommendations must contain exactly 3 items.
- If the explanation is syntax-heavy, the syntax example must show the same method used in the question.
If any required field feels uncertain, restate the concept from the supplied documentation instead of omitting the field.
Syntax example rule:
- If this question needs syntax, include a short fenced code example and 2 brief bullets explaining it.
- If syntax is not needed, write exactly: Not required for this concept.
Current need for syntax example: {"yes" if needs_syntax_example else "no"}
{syntax_instruction}
Response contract:
- Return exactly one flat JSON object.
- Do not wrap the JSON in markdown fences.
- Do not add commentary, preambles, or trailing text.
- Include exactly these keys: feedbacks, trap_analysis, explanation_correct_answer, explanation_why_correct, explanation_why_wrong, explanation_exam_trap, explanation_memory_hook, explanation_practice_recommendations, explanation_syntax_example.
- feedbacks must be a list of exactly 4 strings in A/B/C/D order.
- explanation_practice_recommendations must be a list of exactly 3 strings.
- explanation_syntax_example must be plain text with no heading markers.
{QUALITY_RULES}
"""
    
    # Use model_runner with quality gates
    model_runner = get_model_runner()
    
    # Extract source files from existing question for judge verification
    source_files = []
    citation_source = meta.get("citation_source", "")
    if citation_source:
        source_files = [citation_source]
    
    # Extract context text from existing question for judge verification
    context_text = q.get("context", {}).get("scenario_description", "")
    topic_id = meta.get("topic_id") or planner.resolve_topic_id(meta.get("syllabus_topic") or meta.get("topic") or "")
    weak_focus_context = planner.load_topic_benchmark_focus(topic_id, meta.get("concept", ""))
    benchmark_context = planner.load_topic_benchmark_context(topic_id, meta.get("concept", ""))
    if isinstance(weak_focus_context, str) and weak_focus_context.strip():
        context_text = "\n\n---\n\n".join(
            part for part in (weak_focus_context, context_text, benchmark_context)
            if isinstance(part, str) and part.strip()
        )

    model_chain = get_repair_model_chain()
    
    result = model_runner.generate_with_quality_gate(
        prompt=prompt,
        model_chain=model_chain,
        max_retries=REPAIR_ATTEMPTS - 1,
        source_files=source_files,
        context_text=context_text,
        response_kind="repair"
    )
    
    if not result["success"]:
        print(f"  [!] Repair quality gate failed: {result['quality_issues']}")
        return None
    
    repaired_raw = RepairedExplanationSchema(**result["result"])
    if not repaired_raw or len(repaired_raw.feedbacks) != 4:
        return None

    recs = _normalize_practice_recommendations(q, repaired_raw.explanation_practice_recommendations)
    syntax_example = _normalize_syntax_example(
        q,
        repaired_raw.explanation_syntax_example,
        needs_syntax_example,
    )
    rec_bullets = "\n".join(f"- {rec.strip()}" for rec in recs)
    explanation_markdown = f"""
### 1. Correct Answer
{repaired_raw.explanation_correct_answer.strip()}

### 2. Why Correct
{repaired_raw.explanation_why_correct.strip()}

### 3. Why Other Options Are Wrong
{repaired_raw.explanation_why_wrong.strip()}

### 4. Exam Trap
{repaired_raw.explanation_exam_trap.strip()}

### 5. Memory Hook
{repaired_raw.explanation_memory_hook.strip()}

### 6. Follow-Up Practice Recommendation
{rec_bullets}

### 7. Syntax Example
{syntax_example}
""".strip()

    repaired = RepairedExplanation(
        explanation=explanation_markdown,
        feedbacks=repaired_raw.feedbacks,
        trap_analysis=repaired_raw.trap_analysis,
    )

    issues = _repair_quality_issues(q, repaired)
    if not issues:
        return repaired

    print(f"  [!] Repair quality retry: {'; '.join(issues)} (attempt {REPAIR_ATTEMPTS})")

    return None


def apply_repair(q: dict, repaired: RepairedExplanation) -> None:
    options = []
    for idx, opt in enumerate(q.get("options", [])):
        updated = dict(opt)
        updated["feedback"] = repaired.feedbacks[idx]
        options.append(updated)

    database.questions_col.update_one(
        {"_id": q["_id"]},
        {
            "$set": {
                "explanation": repaired.explanation,
                "trap_analysis": repaired.trap_analysis,
                "options": options,
                "metadata.explanation_repair_source": "certcoach_repair_explanations",
                "metadata.explanation_repaired_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
                "metadata.content_contract_version": contract_metadata("repair_explanations")["content_contract_version"],
                "metadata.content_contract_status": contract_metadata("repair_explanations")["content_contract_status"],
                "metadata.content_contract_source": contract_metadata("repair_explanations")["content_contract_source"],
            }
        },
    )


def run_repair(
    max_questions: int | None = None,
    topic_filter: str | None = None,
    dry_run: bool = False,
    concept_filter: str | None = None,
) -> dict:
    database.check_connection()
    model, local_llm_url = _load_env()
    audit = database.audit_question_explanations()
    candidate_items = []
    skipped = []
    failed = []

    console.print("\n[bold cyan]CertCoach 7-Part Explanation Repair[/bold cyan]")
    console.print(f"Total questions: [bold]{audit['total_questions']}[/bold]")
    console.print(f"Already compliant: [bold green]{audit['compliant_questions']}[/bold green]")
    console.print(f"Needs review: [bold red]{audit['non_compliant_questions']}[/bold red]")
    console.print(f"Compliance: [bold yellow]{audit['compliance_percent']}%[/bold yellow]")
    if topic_filter:
        console.print(f"Topic filter: [bold]{topic_filter}[/bold]")
    if concept_filter:
        console.print(f"Concept filter: [bold]{concept_filter}[/bold]")
    if dry_run:
        console.print("Mode: [bold yellow]dry-run[/bold yellow]")
    console.print()

    repair_query: dict[str, object] = {
        "metadata.content_contract_status": REPAIR_PENDING_STATUS,
    }
    candidate_questions = list(database.questions_col.find(repair_query))

    for q in candidate_questions:
        if not _topic_matches(q, topic_filter):
            continue
        if not _concept_matches(q, concept_filter):
            continue
        if not is_marked_for_explanation_repair(q):
            skipped.append((str(q.get("_id", "")), "not marked needs_explanation_repair"))
            continue

        ok, reason = is_structurally_repairable(q)
        if not ok:
            skipped.append((str(q.get("_id", "")), reason))
            continue
        candidate_items.append(({"id": q.get("_id")}, q))

    candidate_items.sort(key=lambda item: _syllabus_order_key(item[1], planner.load_syllabus()))
    if max_questions is not None:
        candidate_items = candidate_items[:max_questions]

    total_candidates = len(candidate_items)
    console.print(f"Repairable questions selected: [bold cyan]{total_candidates}[/bold cyan]")
    console.print(f"Skipped structural/manual questions: [bold yellow]{len(skipped)}[/bold yellow]")
    if max_questions is not None:
        console.print(f"Batch cap: [bold]{max_questions}[/bold]")
    console.print()

    if dry_run:
        for idx, (_, q) in enumerate(candidate_items[:25], 1):
            meta = q.get("metadata", {})
            label = f"{meta.get('topic', 'General')} | {meta.get('concept', '') or '-'} | {q.get('question_text', '')[:90]}"
            console.print(f"[cyan]{idx:02d}.[/cyan] {label}")
        if total_candidates > 25:
            console.print(f"[dim]Showing first 25 of {total_candidates} repairable questions.[/dim]")
        result = {"repaired": 0, "repairable": total_candidates, "skipped": skipped, "failed": failed}
        console.print(f"\n[bold yellow]Dry run complete.[/bold yellow] Repairable: {total_candidates}, skipped/manual: {len(skipped)}, failed lookup: {len(failed)}")
        return result

    repaired = 0
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
            task_id = progress.add_task("Repairing explanations", total=total_candidates)
            for _, q in candidate_items:
                meta = q.get("metadata", {})
                label = f"{meta.get('topic', 'General')} | {meta.get('concept', '') or '-'}"
                progress.update(task_id, description=f"Repairing: {label[:48]}")

                repair = generate_repair(q)
                if not repair:
                    failed.append((str(q.get("_id", "")), "generation failed"))
                    progress.advance(task_id)
                    continue

                # Construct temporary repaired question dict for quality validation
                repaired_q = dict(q)
                repaired_q["explanation"] = repair.explanation
                repaired_q["trap_analysis"] = repair.trap_analysis
                options = []
                for idx, opt in enumerate(q.get("options", [])):
                    updated = dict(opt)
                    updated["feedback"] = repair.feedbacks[idx]
                    options.append(updated)
                repaired_q["options"] = options

                is_valid, quality_issues = validate_question_quality(repaired_q)
                if not is_valid:
                    failed.append((str(q.get("_id", "")), f"quality check failed: {'; '.join(quality_issues)}"))
                    progress.advance(task_id)
                    continue

                apply_repair(q, repair)
                repaired += 1
                progress.advance(task_id)
                console.print(f"\n[bold green]Repaired {q.get('_id')}[/bold green]")
                console.print(f"[bold]Question:[/bold] {_ascii_safe(q.get('question_text', ''))}")
                console.print("[bold]Seven-Part Explanation:[/bold]")
                console.print(_ascii_safe(repair.explanation))
                time.sleep(0.2)
    finally:
        # Model unloading is now handled by model_runner internally
        pass

    result = {"repaired": repaired, "repairable": total_candidates, "skipped": skipped, "failed": failed}
    console.print(
        f"\n[bold green]Repair complete.[/bold green] "
        f"Repaired: [bold green]{repaired}[/bold green], "
        f"skipped/manual: [bold yellow]{len(skipped)}[/bold yellow], "
        f"failed: [bold red]{len(failed)}[/bold red]"
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Repair existing question explanations into the CertCoach seven-part template.")
    parser.add_argument("--topic", default=None, help="Repair only questions matching topic id/name/bank/concept text.")
    parser.add_argument("--concept", default=None, help="Repair only questions mapped to this exact syllabus concept.")
    parser.add_argument("--max-questions", type=int, default=None, help="Cap repaired questions for this run.")
    parser.add_argument("--dry-run", action="store_true", help="Show repairable questions without calling the model.")
    args = parser.parse_args(argv)

    run_repair(args.max_questions, args.topic, args.dry_run, args.concept)
    return 0


if __name__ == "__main__":
    sys.exit(main())
