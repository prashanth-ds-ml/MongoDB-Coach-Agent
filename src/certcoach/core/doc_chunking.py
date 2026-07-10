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
# fragmenting a section's own sub-examples into separate clicks). The cap is
# a safety net for an oversized section, not the primary split signal --
# confirmed against the real corpus (64 unique resolved docs): median
# section length barely moves between cap=1500/1800/2200 (~1000-1060 chars
# either way, since headers already govern most splits), but cap=1200
# over-fragments (+76% total sections vs the old cap=3000 baseline) while
# 1800 caps the handful of genuinely large sections (ObjectId, decimal128,
# aggregation references) without inflating section count nearly as much
# (+32%). Shared here (not just in cli.py) so the syllabus-status coverage
# line computes the same section count the learner actually sees.
LESSON_SECTION_HEADERS = [("#", "H1"), ("##", "H2")]
LESSON_SECTION_MAX_CHARS = 1800


def chunk_doc_text(text: str, max_chunk_chars: int, headers: list[tuple[str, str]] | None = None) -> list[dict]:
    """Splits one doc's text into header-delimited sections (tagged with their
    header path, e.g. "BSON Types > ObjectId") instead of one flat blob. Any
    section still too large for one model call falls back to a secondary
    recursive character split. Sections under MIN_CHUNK_CHARS (nav cruft,
    a bare "> Source: ..." metadata line before the first header) are dropped
    -- they're not worth a model call.

    headers defaults to CHUNK_HEADERS (H1-H4, fine-grained -- used for
    fact-extraction yield estimation). Callers wanting coarser, more
    natural reading-sized sections (e.g. the CLI's lesson display) can pass
    a shallower list like H1+H2 only."""
    active_headers = headers or CHUNK_HEADERS
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=active_headers, strip_headers=False)
    header_chunks = header_splitter.split_text(text)
    header_keys = [key for _, key in active_headers]

    chunks: list[dict] = []
    for doc in header_chunks:
        content = doc.page_content.strip()
        if len(content) < MIN_CHUNK_CHARS:
            continue
        label = " > ".join(
            doc.metadata[key] for key in header_keys if key in doc.metadata
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
