"""Recover citations for suspect questions originally built from pics_qa
screenshots, now that reocr_pics_qa.py has saved their raw transcripts.

For each such question, a model is asked to find a short verbatim passage in
the transcript that supports the question's marked answer -- never to
paraphrase or invent one. The candidate quote then goes through the exact
same gate as freshly generated questions (nightly_seed_questions.
run_generation_pipeline_checks): a deterministic citation check, then a
self-consistency check. Only a pass on both reaches provenance.state=
'sourced'. A failure leaves the existing `suspect` record untouched -- this
never downgrades or overwrites a record it couldn't improve.
"""
from __future__ import annotations

import argparse
import os
import sys

from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn

from certcoach.core import database
from certcoach.core.config import get_local_llm_url, get_population_model
from certcoach.jobs.nightly_seed_questions import _ollama_json_request, run_generation_pipeline_checks
from certcoach.jobs.reocr_pics_qa import TRANSCRIPT_DIR, transcript_filename

console = Console()


def _citation_source_of(question: dict) -> str:
    return str(question.get("metadata", {}).get("citation_source", "") or question.get("citation_source", ""))


def load_transcript_text(image_name: str) -> str | None:
    path = os.path.join(TRANSCRIPT_DIR, transcript_filename(image_name))
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return f.read()


def find_supporting_quote(question: dict, transcript_text: str, local_llm_url: str, model: str) -> str | None:
    correct = next(
        (opt.get("code_snippet", "") for opt in question.get("options", []) if opt.get("is_correct")),
        "",
    )
    prompt = f"""You are given the raw OCR transcript of a screenshot and an existing multiple-choice question built from it.

Transcript:
{transcript_text[:4000]}

Question: {question.get('question_text', '')}
Correct answer: {correct}

Find a short passage (10 to 30 words) copied VERBATIM, character-for-character, from the transcript above that supports the correct answer. Copy it exactly as it appears, including any OCR artifacts -- do not paraphrase or clean it up. If no such passage exists anywhere in the transcript, respond with exactly: NONE

Respond with ONLY the quote (or NONE) and nothing else.
"""
    try:
        response = _ollama_json_request(
            local_llm_url,
            "/api/generate",
            {"model": model, "prompt": prompt, "stream": False},
            timeout=120.0,
        )
    except Exception:
        return None
    text = response.get("response", "").strip().strip('"')
    if not text or text.strip().upper() == "NONE":
        return None
    return text


def run_recovery(limit: int | None = None, topic_id: int | None = None) -> dict:
    database.check_connection()
    local_llm_url = get_local_llm_url()
    model = get_population_model()

    query = {"provenance.state": "suspect"}
    if topic_id is not None:
        query["metadata.topic_id"] = int(topic_id)
    candidates = [
        q for q in database.questions_col.find(query)
        if _citation_source_of(q).startswith("pics_qa/")
    ]
    if limit is not None:
        candidates = candidates[:limit]

    stats = {"sourced": 0, "still_suspect": 0, "no_transcript": 0}
    progress = Progress(
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=34),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    )
    with progress:
        task_id = progress.add_task("Recovering citations", total=len(candidates))
        for question in candidates:
            image_name = _citation_source_of(question).split("/", 1)[-1]
            transcript_text = load_transcript_text(image_name)
            if not transcript_text:
                stats["no_transcript"] += 1
                progress.advance(task_id)
                continue

            quote = find_supporting_quote(question, transcript_text, local_llm_url, model)
            if not quote:
                stats["still_suspect"] += 1
                progress.console.print(f"  {question['_id']}: no supporting quote found, left as suspect")
                progress.advance(task_id)
                continue

            provenance = run_generation_pipeline_checks(
                question,
                citation_doc_file=transcript_filename(image_name),
                citation_quote=quote,
                local_llm_url=local_llm_url,
                generation_model=f"ollama:{model}",
            )

            if provenance["state"] == "sourced":
                database.questions_col.update_one({"_id": question["_id"]}, {"$set": {"provenance": provenance}})
                stats["sourced"] += 1
            else:
                stats["still_suspect"] += 1
            progress.console.print(f"  {question['_id']}: {provenance['state']} -- {provenance['pipeline_note']}")
            progress.advance(task_id)

    console.print(
        f"\nSourced: {stats['sourced']}  Still suspect (unchanged): {stats['still_suspect']}  "
        f"No transcript yet: {stats['no_transcript']}"
    )
    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Recover citations for screenshot-sourced suspect questions.")
    parser.add_argument("--limit", type=int, default=None, help="Only attempt the first N candidates (for a test batch).")
    parser.add_argument("--topic", type=int, default=None, help="Restrict to one topic_id.")
    args = parser.parse_args(argv)
    run_recovery(limit=args.limit, topic_id=args.topic)
    return 0


if __name__ == "__main__":
    sys.exit(main())
