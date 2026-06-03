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
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from certcoach.core import database
from certcoach.jobs.nightly_seed_questions import (
    QUALITY_RULES,
    SEVEN_PART_HEADINGS,
    _question_needs_syntax_example,
    _load_env,
    clear_ollama_memory,
    preload_ollama_model,
    validate_question_quality,
    unload_ollama_model,
)

console = Console()
REPAIR_ATTEMPTS = 3


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
    if not topic_filter:
        return True
    filt = topic_filter.strip().lower()
    if not filt:
        return True
    meta = q.get("metadata", {})
    haystack = " ".join([
        str(meta.get("topic", "")),
        str(meta.get("syllabus_topic", "")),
        str(meta.get("concept", "")),
        str(meta.get("topic_id", "")),
    ]).lower()
    return filt in haystack


def is_structurally_repairable(q: dict) -> tuple[bool, str]:
    options = q.get("options", [])
    if not q.get("question_text"):
        return False, "missing question_text"
    if len(options) != 4:
        return False, "does not have exactly 4 options"
    if sum(1 for opt in options if opt.get("is_correct")) != 1:
        return False, "does not have exactly one correct option"
    return True, "repairable"


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


def generate_repair(q: dict) -> RepairedExplanation | None:
    model, local_llm_url = _load_env()
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
- `explanation_memory_hook`: a compact mnemonic or memory hook with one or two concrete rules.
- `explanation_practice_recommendations`: a list of 3 to 5 compact but specific action items or recall points for practice. Do NOT add markdown hyphen prefixes (e.g. - ) inside the list items themselves; the system will format them.
- `explanation_syntax_example`: a markdown string containing a fenced code block of a syntax example if the concept is syntax-heavy, or exactly 'Not required for this concept.' if not syntax-heavy.

Make it beginner-friendly but technically precise. Explain syntax tokens, method names, operators, return values, casing traps, and why each distractor is wrong.
Syntax example rule:
- If this question needs syntax, include a short fenced code example and 2 brief bullets explaining it.
- If syntax is not needed, write exactly: Not required for this concept.
Current need for syntax example: {"yes" if needs_syntax_example else "no"}
{QUALITY_RULES}
"""
    for attempt in range(1, REPAIR_ATTEMPTS + 1):
        try:
            timeout_val = float(os.getenv("OLLAMA_TIMEOUT", "300.0"))
            llm = ChatOllama(
                model=model,
                base_url=local_llm_url,
                temperature=0.25,
                timeout=timeout_val,
                num_ctx=8192,
                format="json",
            )
            repaired_raw = llm.with_structured_output(RepairedExplanationSchema).invoke(prompt)
        except Exception as exc:
            print(f"  [!] Repair generation failed: {exc}")
            return None

        if not repaired_raw or len(repaired_raw.feedbacks) != 4:
            continue

        rec_bullets = "\n".join(
            f"- {rec.strip()}" for rec in repaired_raw.explanation_practice_recommendations
        )
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
{repaired_raw.explanation_syntax_example.strip()}
""".strip()

        repaired = RepairedExplanation(
            explanation=explanation_markdown,
            feedbacks=repaired_raw.feedbacks,
            trap_analysis=repaired_raw.trap_analysis,
        )

        issues = _repair_quality_issues(q, repaired)
        if not issues:
            return repaired

        print(f"  [!] Repair quality retry: {'; '.join(issues)} ({attempt}/{REPAIR_ATTEMPTS})")

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
            }
        },
    )


def run_repair(max_questions: int | None = None, topic_filter: str | None = None, dry_run: bool = False) -> dict:
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
    if dry_run:
        console.print("Mode: [bold yellow]dry-run[/bold yellow]")
    console.print()

    for item in audit["issues"]:
        q = _find_question(item["id"])
        if not q:
            failed.append((item["id"], "question not found"))
            continue
        if not _topic_matches(q, topic_filter):
            continue

        ok, reason = is_structurally_repairable(q)
        if not ok:
            skipped.append((item["id"], reason))
            continue
        candidate_items.append((item, q))

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
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=34),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
    )

    clear_ollama_memory(local_llm_url)
    preload_ollama_model(model, local_llm_url)
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
                console.print(f"[bold]Question:[/bold] {q.get('question_text', '')}")
                console.print("[bold]Seven-Part Explanation:[/bold]")
                console.print(repair.explanation)
                time.sleep(0.2)
    finally:
        unload_ollama_model(model, local_llm_url)

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
    parser.add_argument("--max-questions", type=int, default=None, help="Cap repaired questions for this run.")
    parser.add_argument("--dry-run", action="store_true", help="Show repairable questions without calling the model.")
    args = parser.parse_args(argv)

    run_repair(args.max_questions, args.topic, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
