"""Markdown header-delimited chunking shared by doc inspection (fact yield
estimation) and the CLI's per-section lesson display. Kept dependency-light
(only langchain_text_splitters) so the CLI's startup path doesn't have to
pull in the generation/database stack just to split a doc into sections."""
from __future__ import annotations

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

CHUNK_HEADERS = [("#", "H1"), ("##", "H2"), ("###", "H3"), ("####", "H4")]
MIN_CHUNK_CHARS = 40

# Coarser split for the CLI's per-section lesson display and its coverage
# reporting (one natural topic per screen, e.g. "ObjectId", "Date", without
# fragmenting a section's own sub-examples into separate clicks). Used with
# group_toward_target=True (below) -- confirmed against the real corpus (64
# unique resolved docs): grouping consecutive small headers toward a 2800-char
# target gives a median of 3 sections/doc for the typical doc-length band
# (p25-p75 is ~4.4K-13.4K chars), matching the "3-4 parts" a learner actually
# wants per doc. A pure fixed-cap split-only approach (the old design) instead
# scales section count with how many small headers a doc happens to have --
# a doc with five ~1-3K sections produced 5+ sections even though none were
# individually oversized. Genuinely long docs (13K-81K chars, ~14 of 64) still
# scale up proportionally rather than being forced into 4 oversized chunks --
# an 81K-char doc split into 4 parts would mean ~20K chars per screen, which
# isn't bite-sized by any definition. Shared here (not just in cli.py) so the
# syllabus-status coverage line computes the same section count the learner
# actually sees.
LESSON_SECTION_HEADERS = [("#", "H1"), ("##", "H2")]
LESSON_SECTION_MAX_CHARS = 2800

# How far a group is allowed to overshoot the target before it's closed off
# (avoids stopping a group short by one small trailing header just because
# the running total nudged past the exact target) and how far a single
# section must exceed the target before it's forcibly sub-split (avoids
# sub-splitting a section that's only slightly, harmlessly over target).
_GROUP_OVERSHOOT_FACTOR = 1.15
_SPLIT_OVERSHOOT_FACTOR = 1.6


def chunk_doc_text(
    text: str,
    max_chunk_chars: int,
    headers: list[tuple[str, str]] | None = None,
    group_toward_target: bool = False,
) -> list[dict]:
    """Splits one doc's text into header-delimited sections (tagged with their
    header path, e.g. "BSON Types > ObjectId") instead of one flat blob. Any
    section still too large for one model call falls back to a secondary
    recursive character split. Sections under MIN_CHUNK_CHARS (nav cruft,
    a bare "> Source: ..." metadata line before the first header) are dropped
    -- they're not worth a model call.

    headers defaults to CHUNK_HEADERS (H1-H4, fine-grained -- used for
    fact-extraction yield estimation). Callers wanting coarser, more
    natural reading-sized sections (e.g. the CLI's lesson display) can pass
    a shallower list like H1+H2 only.

    group_toward_target=False (default) preserves the original one-chunk-per-
    header behavior (only ever splits a section further, never merges) --
    left untouched so the fact-extraction/yield-estimation pipeline in
    inspect_doc.py, which was tuned and verified against this exact behavior,
    is unaffected. Pass True to instead greedily group consecutive small
    header sections toward max_chunk_chars before starting a new chunk --
    this is what makes the CLI's lesson display land near "3-4 sections" for
    a typical doc instead of one chunk per header regardless of size."""
    active_headers = headers or CHUNK_HEADERS
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=active_headers, strip_headers=False)
    header_chunks = header_splitter.split_text(text)
    header_keys = [key for _, key in active_headers]

    parts: list[tuple[str, str]] = []
    for doc in header_chunks:
        content = doc.page_content.strip()
        if len(content) < MIN_CHUNK_CHARS:
            continue
        label = " > ".join(
            doc.metadata[key] for key in header_keys if key in doc.metadata
        ) or "(untitled section)"
        parts.append((label, content))

    if not group_toward_target:
        chunks: list[dict] = []
        for label, content in parts:
            if len(content) <= max_chunk_chars:
                chunks.append({"label": label, "text": content})
                continue
            sub_splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk_chars, chunk_overlap=200)
            for i, sub_text in enumerate(sub_splitter.split_text(content), start=1):
                if len(sub_text.strip()) < MIN_CHUNK_CHARS:
                    continue
                chunks.append({"label": f"{label} (part {i})", "text": sub_text})
        return chunks

    groups: list[tuple[str, str]] = []
    cur_label: str | None = None
    cur_text = ""
    cur_has_real_label = False
    for label, content in parts:
        candidate = f"{cur_text}\n\n{content}" if cur_text else content
        # A group still holding only a leading metadata stub (no real header
        # label yet) must never be closed off on its own -- otherwise a large
        # first real section could push straight past the overshoot check
        # before the stub ever gets a chance to merge into it, and the stub
        # would show up as its own near-empty screen.
        if cur_text and cur_has_real_label and len(candidate) > max_chunk_chars * _GROUP_OVERSHOOT_FACTOR:
            groups.append((cur_label, cur_text))
            cur_label, cur_text = label, content
            cur_has_real_label = label != "(untitled section)"
        else:
            if not cur_has_real_label and label != "(untitled section)":
                cur_label = label
                cur_has_real_label = True
            elif cur_label is None:
                cur_label = label
            cur_text = candidate
    if cur_text:
        groups.append((cur_label, cur_text))

    chunks = []
    for label, content in groups:
        if len(content) <= max_chunk_chars * _SPLIT_OVERSHOOT_FACTOR:
            chunks.append({"label": label, "text": content})
            continue
        sub_splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk_chars, chunk_overlap=200)
        for i, sub_text in enumerate(sub_splitter.split_text(content), start=1):
            if len(sub_text.strip()) < MIN_CHUNK_CHARS:
                continue
            chunks.append({"label": f"{label} (part {i})", "text": sub_text})
    return chunks
