"""Re-OCR the pics_qa/ screenshots and save the raw transcript this time.

The original extraction pipeline (image_extractor.py) ran a vision-model OCR
pass over each screenshot but only kept the final structured MCQ -- the raw
transcript was discarded, which is exactly why none of the 333 questions
built from these screenshots ever had a real citation quote (see
analyze_backlog.py). This script re-runs OCR only, and persists the
transcript as a .md file under data/pics_qa_transcripts/, so
database.verify_citation() can check a quote against it the same way it
checks quotes against the official docs.

These screenshots are the user's own MongoDB University course material --
a legitimate but separate source category from the official reference docs.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

import ollama
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn

console = Console()

_HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.abspath(os.path.join(_HERE, "..", "data", "pics_qa"))
TRANSCRIPT_DIR = os.path.abspath(os.path.join(_HERE, "..", "data", "pics_qa_transcripts"))

OCR_PROMPT = (
    "You are an expert OCR assistant. Transcribe ALL visible text in this screenshot "
    "exactly as written -- the question prompt, every option, any code blocks, and any "
    "visible explanation or notes. Do not summarize, do not skip anything, do not add "
    "commentary of your own. Output plain text only."
)


def get_available_vision_model() -> str | None:
    try:
        models = getattr(ollama.list(), "models", [])
        names = [getattr(m, "model", "") for m in models]
    except Exception:
        return None
    for name in names:
        if "glm-ocr" in name:
            return name
    for name in names:
        if "llava" in name or "vl" in name.lower():
            return name
    return None


def transcript_filename(image_name: str) -> str:
    stem = re.sub(r"[^a-zA-Z0-9]+", "-", os.path.splitext(image_name)[0]).strip("-")
    return f"{stem}.md"


def collapse_repetition(text: str, probe_len: int = 120) -> str:
    """glm-ocr can degenerate into repeating the same block over and over
    instead of stopping (confirmed live: one screenshot produced a clean
    ~340-char transcript on its first cycle, then repeated it ~40 times into
    a 14KB file). If the opening `probe_len` characters recur later in the
    text, cut everything from that second occurrence onward."""
    if len(text) <= probe_len:
        return text
    probe = text[:probe_len]
    second_occurrence = text.find(probe, probe_len)
    if second_occurrence == -1:
        return text
    return text[:second_occurrence].rstrip()


def ocr_image(image_path: str, vision_model: str) -> str | None:
    response = ollama.chat(
        model=vision_model,
        messages=[{"role": "user", "content": OCR_PROMPT, "images": [image_path]}],
        options={"temperature": 0.1},
    )
    text = response.get("message", {}).get("content", "").strip()
    if not text:
        return None
    return collapse_repetition(text) or None


def run_reocr(limit: int | None = None, force: bool = False) -> dict:
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    vision_model = get_available_vision_model()
    if not vision_model:
        console.print("[red]No vision model (glm-ocr/llava/vl) available in Ollama.[/red]")
        return {"processed": 0, "skipped": 0, "failed": 0}

    console.print(f"[cyan]Using vision model:[/cyan] {vision_model}")

    if not os.path.exists(IMAGE_DIR):
        console.print(f"[red]Image directory not found: {IMAGE_DIR}[/red]")
        return {"processed": 0, "skipped": 0, "failed": 0}

    images = sorted(f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg")))
    if limit is not None:
        images = images[:limit]

    processed, skipped, failed = 0, 0, 0
    progress = Progress(
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=34),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    )
    with progress:
        task_id = progress.add_task("Re-OCRing screenshots", total=len(images))
        for image_name in images:
            transcript_path = os.path.join(TRANSCRIPT_DIR, transcript_filename(image_name))
            if os.path.exists(transcript_path) and not force:
                skipped += 1
                progress.advance(task_id)
                continue

            image_path = os.path.join(IMAGE_DIR, image_name)
            try:
                text = ocr_image(image_path, vision_model)
            except Exception as exc:
                console.print(f"[yellow]OCR failed for {image_name}: {exc}[/yellow]")
                failed += 1
                progress.advance(task_id)
                continue

            if not text:
                console.print(f"[yellow]OCR returned empty text for {image_name}[/yellow]")
                failed += 1
                progress.advance(task_id)
                continue

            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(f"<!-- source screenshot: {image_name} -->\n\n{text}\n")
            processed += 1
            progress.advance(task_id)

    console.print(f"\nProcessed: {processed}  Skipped (already had transcript): {skipped}  Failed: {failed}")
    return {"processed": processed, "skipped": skipped, "failed": failed}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Re-OCR pics_qa screenshots and save raw transcripts.")
    parser.add_argument("--limit", type=int, default=None, help="Only process the first N images (for a test batch).")
    parser.add_argument("--force", action="store_true", help="Re-OCR even if a transcript already exists.")
    args = parser.parse_args(argv)

    run_reocr(limit=args.limit, force=args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
