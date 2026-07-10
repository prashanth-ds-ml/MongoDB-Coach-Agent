"""Combined doc-study + dry-run yield preview for one syllabus concept.

Journey: load a concept's official doc(s) as study material, then estimate
how many citable questions the same text can likely sustain -- section by
section, before spending any generation budget on `certcoach-seed-nightly`.
Reuses the same doc-resolution path (`planner.resolve_concept_docs`) and the
same citation gate (`database.verify_citation`) the real generation pipeline
already applies, so the yield estimate reflects the standard a generated
question must clear later -- not a separate, looser heuristic.

Docs are scanned one markdown section (header-delimited chunk) at a time
instead of one flat, character-truncated blob -- a single POPULATION_SOURCE_CHARS
cutoff can never be right for a corpus ranging from ~600 to ~122,000 characters,
and a header-aware split keeps each model call looking at a coherent section
(e.g. "ObjectId", "Date") instead of an arbitrary mid-table/mid-sentence cutoff.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from certcoach.core import database, planner
from certcoach.core.config import get_population_model, get_population_source_chars
from certcoach.core.model_runner import get_model_runner
from certcoach.core.question_targets import MIN_CONCEPT_TARGETS, weighted_target_for_concept
from certcoach.jobs.nightly_seed_questions import style_weights_for_topic

CHUNK_HEADERS = [("#", "H1"), ("##", "H2"), ("###", "H3"), ("####", "H4")]
MIN_CHUNK_CHARS = 40

console = Console()

CANDIDATE_FACTS_PROMPT = """You are reviewing official MongoDB documentation to find distinct, testable facts suitable for exam-style multiple choice questions on the concept "{concept}".

Read the documentation context below and list each distinct testable fact you find that is grounded in this text.

For each fact, provide:
- quote: a 10-30 word passage copied VERBATIM, character-for-character, from the context below that states this fact. Never paraphrase or invent a quote.
- suggested_difficulty: "Easy" or "Medium"
- suggested_response_type: "single" or "multiple"
- suggested_style_type: the exam-style taxonomy type this fact best supports a question for -- exactly one of:
  - "Type A": Syntax Selection & Trap Spotting (the fact is about correct syntax, method calls, or query/command form)
  - "Type B": Theory, Constraints & Data Modeling (the fact is a rule, limitation, or architectural/modeling concept)
  - "Type C": Predicting Query Output (the fact is about what a query, aggregation stage, or operation returns/produces)
  - "Type D": Troubleshooting, Errors & Performance (the fact is about errors, exceptions, or performance characteristics)
- rationale: one short sentence on why this fact is testable.

Documentation context:
\"\"\"
{context}
\"\"\"

Respond with a JSON object exactly formatted as:
{{"facts": [{{"quote": "...", "suggested_difficulty": "Easy", "suggested_response_type": "single", "suggested_style_type": "Type B", "rationale": "..."}}]}}
"""


def load_topic_item(topic_id: int) -> dict:
    syllabus_by_id = {item["id"]: item for item in planner.load_syllabus()}
    topic_item = syllabus_by_id.get(topic_id)
    if topic_item is None:
        raise ValueError(f"No syllabus topic with id {topic_id}")
    return topic_item


def resolve_concept_docs(topic_item: dict, concept: str) -> list[str]:
    """Thin wrapper returning the filenames themselves (not joined text) so
    each source doc can be shown as its own study panel."""
    return planner.resolve_concept_docs(topic_item.get("md_files", []), concept)


def extract_candidate_facts(context_text: str, concept: str, max_chars: int) -> list[dict]:
    truncated = context_text[:max_chars]
    if not truncated.strip():
        return []
    prompt = CANDIDATE_FACTS_PROMPT.format(concept=concept, context=truncated)
    runner = get_model_runner()
    model_config = {"provider": "ollama", "model": get_population_model()}
    response = runner._call_model(model_config, prompt, temperature=0.2, num_ctx=4096)
    if not response:
        return []
    match = re.search(r"\{.*\}", response, re.DOTALL)
    if not match:
        return []
    try:
        parsed = json.loads(match.group(0))
    except Exception:
        return []
    facts = parsed.get("facts") if isinstance(parsed, dict) else None
    return facts if isinstance(facts, list) else []


def chunk_doc_text(text: str, max_chunk_chars: int) -> list[dict]:
    """Splits one doc's text into header-delimited sections (tagged with their
    header path, e.g. "BSON Types > ObjectId") instead of one flat blob. Any
    section still too large for one model call falls back to a secondary
    recursive character split. Sections under MIN_CHUNK_CHARS (nav cruft,
    a bare "> Source: ..." metadata line before the first header) are dropped
    -- they're not worth a model call."""
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=CHUNK_HEADERS, strip_headers=False)
    header_chunks = header_splitter.split_text(text)

    chunks: list[dict] = []
    for doc in header_chunks:
        content = doc.page_content.strip()
        if len(content) < MIN_CHUNK_CHARS:
            continue
        label = " > ".join(
            doc.metadata[key] for key in ("H1", "H2", "H3", "H4") if key in doc.metadata
        ) or "(untitled section)"

        if len(content) <= max_chunk_chars:
            chunks.append({"label": label, "text": content})
            continue

        sub_splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk_chars, chunk_overlap=200)
        for i, sub_text in enumerate(sub_splitter.split_text(content), start=1):
            if len(sub_text.strip()) < MIN_CHUNK_CHARS:
                continue
            chunks.append({"label": f"{label} (part {i})", "text": sub_text})

    return chunks


def verify_candidate(resolved_files: list[str], quote: str) -> tuple[bool, str]:
    """Reuses the real pipeline's own citation gate (`database.verify_citation`)
    against each resolved doc in turn, instead of a bespoke quote-matching
    check, so a candidate only counts if it would also pass generation."""
    if not quote:
        return False, ""
    for doc_file in resolved_files:
        synthetic_question = {"provenance": {"citation": {"doc_file": doc_file, "quote": quote}}}
        verified, _ = database.verify_citation(synthetic_question)
        if verified:
            return True, doc_file
    return False, ""


def inspect_concept(
    topic_id: int,
    concept: str,
    max_chars: int,
    progress_callback=None,
) -> dict:
    """Scans every resolved doc section by section (see chunk_doc_text) rather
    than one flat, character-truncated blob, so the yield estimate reflects
    what the whole doc can sustain, not just whatever fits before an arbitrary
    cutoff. progress_callback(index, total, label), if given, fires after each
    chunk is scanned -- multi-chunk docs mean multiple model calls, so callers
    driving a CLI should surface progress rather than appear to hang."""
    topic_item = load_topic_item(topic_id)
    resolved_files = resolve_concept_docs(topic_item, concept)
    allowed_style_types = set(style_weights_for_topic(topic_id).keys())

    all_chunks: list[dict] = []
    for doc_file in resolved_files:
        doc_text = planner.load_md_context([doc_file])
        for chunk in chunk_doc_text(doc_text, max_chars):
            all_chunks.append({**chunk, "doc_file": doc_file})

    chunk_results: list[dict] = []
    verified: list[dict] = []
    dropped: list[dict] = []
    for index, chunk in enumerate(all_chunks, start=1):
        candidates = extract_candidate_facts(chunk["text"], concept, max_chars)
        chunk_verified: list[dict] = []
        chunk_dropped: list[dict] = []
        for candidate in candidates:
            quote = str(candidate.get("quote", "")).strip()
            ok, matched_file = verify_candidate([chunk["doc_file"]], quote)
            if ok:
                enriched = {**candidate, "matched_doc_file": matched_file}
                # Inspection reports what's achievable, it doesn't decide final
                # style -- a suggestion outside this topic's allowed taxonomy
                # (or missing/malformed) is cleared, not guessed, so downstream
                # reporting and selection can rely on "valid Type or None".
                if enriched.get("suggested_style_type") not in allowed_style_types:
                    enriched["suggested_style_type"] = None
                chunk_verified.append(enriched)
                verified.append(enriched)
            else:
                chunk_dropped.append(candidate)
                dropped.append(candidate)

        chunk_results.append({
            "label": chunk["label"],
            "doc_file": chunk["doc_file"],
            "text": chunk["text"],
            "verified": chunk_verified,
            "dropped": chunk_dropped,
        })
        if progress_callback:
            progress_callback(index, len(all_chunks), chunk["label"])

    syllabus = planner.load_syllabus()
    weighted_target = weighted_target_for_concept(syllabus, topic_id, concept)

    return {
        "topic_id": topic_id,
        "concept": concept,
        "resolved_files": resolved_files,
        "chunks": chunk_results,
        "verified": verified,
        "dropped": dropped,
        "weighted_target": weighted_target,
    }


def print_study_material(resolved_files: list[str], concept: str) -> None:
    if not resolved_files:
        console.print(f"[yellow]No official doc resolved for concept '{concept}'.[/yellow]")
        return
    for filename in resolved_files:
        text = planner.load_md_context([filename])
        console.print(Panel(
            Markdown(text, code_theme="monokai"),
            title=f"Study Material: {concept} ({filename})",
            border_style="cyan",
        ))


def print_chunk_yield_report(result: dict) -> None:
    """Shows which sections of the doc were actually productive, e.g. "ObjectId
    -> 2 verified" vs "BSON with MongoDB Drivers -> 0 verified" -- tells you
    which sections are worth real generation budget instead of just a single
    aggregate count with no sense of where it came from."""
    chunks = result.get("chunks") or []
    if not chunks:
        return

    table = Table(title=f"Per-section yield: Topic {result['topic_id']} -> {result['concept']}")
    table.add_column("Section")
    table.add_column("Doc")
    table.add_column("Found", justify="right")
    table.add_column("Verified", justify="right")
    table.add_column("Dropped", justify="right")
    for chunk in chunks:
        found = len(chunk["verified"]) + len(chunk["dropped"])
        table.add_row(
            chunk["label"], chunk["doc_file"],
            str(found), str(len(chunk["verified"])), str(len(chunk["dropped"])),
        )
    console.print(table)


def print_yield_report(result: dict) -> None:
    total = len(result["verified"]) + len(result["dropped"])
    table = Table(title=f"Dry-run yield: Topic {result['topic_id']} -> {result['concept']}")
    table.add_column("Metric")
    table.add_column("Count", justify="right")
    table.add_row("Candidate facts found", str(total))
    table.add_row("Verified (citable)", str(len(result["verified"])))
    table.add_row("Dropped (quote not verbatim)", str(len(result["dropped"])))
    console.print(table)

    if not result["verified"]:
        console.print("[yellow]No verifiable candidate facts -- this doc may not sustain generation for this concept yet.[/yellow]")
        return

    breakdown = Table(title="Verified facts by difficulty / response type")
    breakdown.add_column("Difficulty")
    breakdown.add_column("Response type")
    breakdown.add_column("Count", justify="right")
    counts: dict[tuple[str, str], int] = {}
    for fact in result["verified"]:
        key = (fact.get("suggested_difficulty", "?"), fact.get("suggested_response_type", "?"))
        counts[key] = counts.get(key, 0) + 1
    for (difficulty, response_type), count in sorted(counts.items()):
        breakdown.add_row(difficulty, response_type, str(count))
    console.print(breakdown)


def print_taxonomy_yield_report(result: dict, topic_id: int) -> None:
    """Shows verified-fact yield by exam-style taxonomy type (Type A-D), so
    the reviewer can see e.g. "4 Type-A-worthy facts, 2 Type-C" before
    spending any generation budget -- restricted to the types this topic
    actually allows (style_weights_for_topic), with an "unclassified" row for
    facts the model couldn't confidently place (see inspect_concept, which
    clears out-of-scope suggestions rather than guessing)."""
    allowed_style_types = list(style_weights_for_topic(topic_id).keys())
    counts: dict[str, int] = {style: 0 for style in allowed_style_types}
    unclassified = 0
    for fact in result["verified"]:
        style = fact.get("suggested_style_type")
        if style in counts:
            counts[style] += 1
        else:
            unclassified += 1

    table = Table(title=f"Verified facts by exam-style taxonomy: Topic {result['topic_id']} -> {result['concept']}")
    table.add_column("Style type")
    table.add_column("Count", justify="right")
    for style in allowed_style_types:
        table.add_row(style, str(counts[style]))
    if unclassified:
        table.add_row("[dim]unclassified[/dim]", str(unclassified))
    console.print()
    console.print(table)


def print_target_coverage(result: dict) -> None:
    """Compares this doc's verified yield against the concept's real
    exam-weighted population target (question_targets.weighted_target_for_concept)
    -- the same target certcoach-seed-nightly works toward -- so a shortfall here
    is a signal the concept needs a broader corpus or another generation pass,
    not just a raw candidate-fact count with nothing to measure it against."""
    target = result.get("weighted_target") or {}
    verified_counts: dict[str, int] = {}
    for fact in result["verified"]:
        difficulty = fact.get("suggested_difficulty", "?")
        verified_counts[difficulty] = verified_counts.get(difficulty, 0) + 1

    table = Table(title=f"Coverage vs. exam-weighted target: Topic {result['topic_id']} -> {result['concept']}")
    table.add_column("Difficulty")
    table.add_column("Target", justify="right")
    table.add_column("This doc verifies", justify="right")
    table.add_column("Shortfall", justify="right")

    total_target = 0
    total_verified = 0
    for difficulty in ("Easy", "Medium"):
        target_count = target.get(difficulty, MIN_CONCEPT_TARGETS.get(difficulty, 0))
        verified_count = verified_counts.get(difficulty, 0)
        shortfall = max(0, target_count - verified_count)
        total_target += target_count
        total_verified += verified_count
        table.add_row(
            difficulty, str(target_count), str(verified_count),
            "[green]met[/green]" if shortfall == 0 else str(shortfall),
        )
    console.print()
    console.print(table)

    if total_verified >= total_target:
        console.print(f"[green]This doc alone can likely sustain the full weighted target ({total_target} questions).[/green]")
    else:
        remaining = total_target - total_verified
        console.print(
            f"[yellow]This doc alone covers {total_verified}/{total_target} of the weighted target -- "
            f"{remaining} more will need another doc, a broader corpus pass, or additional generation retries.[/yellow]"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Load a concept's official doc as study material, then dry-run how many "
                     "citable questions it can likely yield before generating anything."
    )
    parser.add_argument("--topic", type=int, required=True, help="Syllabus topic id.")
    parser.add_argument("--concept", required=True, help="Exact syllabus concept name.")
    parser.add_argument("--max-chars", type=int, default=None, help="Override population source-char cap.")
    args = parser.parse_args(argv)

    max_chars = args.max_chars if args.max_chars is not None else get_population_source_chars()

    def report_progress(index: int, total: int, label: str) -> None:
        console.print(f"  [dim]Scanning section {index}/{total}: {label}[/dim]")

    try:
        result = inspect_concept(args.topic, args.concept, max_chars, progress_callback=report_progress)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    print_study_material(result["resolved_files"], args.concept)
    console.print()
    print_chunk_yield_report(result)
    console.print()
    print_yield_report(result)
    print_taxonomy_yield_report(result, args.topic)
    print_target_coverage(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
