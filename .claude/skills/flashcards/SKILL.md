---
name: flashcards
description: Author atomic, doc-grounded flashcards for a syllabus topic/concept, validate them, and merge into all three bundled copies of flashcards.json.
---

# Flashcards

Authors new flashcards directly (no local Ollama call) for one syllabus topic, following the
standard in `memory/content_authoring_guidelines.md`. Read that file first -- it has the schema,
the quality bar, and why flashcards are atomic/concept-level now instead of one long note per
exam objective.

## Argument

`$ARGUMENTS` is a topic reference: a `topic_id` integer (e.g. `2`), a topic name substring, or
`next` to pick the first topic in canonical syllabus order that has zero flashcards for any of
its concepts. If empty, treat it as `next`.

## Steps

1. **Resolve the target topic.** Read `src/certcoach/data/syllabus.json` (or call
   `certcoach.core.planner.load_syllabus()`). Find the matching topic item -- note its `id`,
   `topic`, `subtopics` (the concepts), and `md_files`.
2. **Check current coverage.** Read `data/flashcards.json` and see which of this topic's
   concepts already have cards (`topic_id` + `concept` fields). If the topic already has cards
   and you're regenerating, you'll pass `--remove-topic-id` when merging (step 5); if it has
   none yet, you won't.
3. **Resolve and read the official doc(s) for each concept**, one concept at a time -- use
   `certcoach.core.planner.resolve_concept_docs(md_files, concept)` to find which file(s) apply
   (a concept can map to more than one, or share a doc with a sibling concept), then read the
   resolved file(s) directly from `src/certcoach/data/cleaned_markdowns/`. Do not paraphrase from
   memory -- read the actual file every time, docs change.
4. **Author atomic cards.** For each concept, write however many distinct, testable, atomic
   facts the doc actually supports (the Topic 1 pilot averaged ~5-7 per concept for a
   medium-to-rich doc; a thin doc might only support 2-3 -- don't pad with restated filler to hit
   a number). Follow the schema and quality bar in `memory/content_authoring_guidelines.md`
   exactly. Card `id` convention: `fc-t{topic_id:02d}-{concept-slug}-{n}` (see existing Topic 1
   cards for the exact slugging style). `subheading` is the closest original numbered exam
   objective for that domain (check the old numbering pattern still visible in
   `memory/MongoDB_Exam_Blueprint.md`'s domain list, or just continue the existing `1.1`/`1.2`/`1.3`
   -style sequence within the topic if no original mapping is obvious) -- shared across every
   card under one concept, not unique per card.
5. **Write the new cards to a JSON file** in the scratchpad directory (a plain JSON array of
   card dicts), then validate and merge:
   ```
   python -m certcoach.jobs.flashcard_tools <scratch_file.json> --validate-only
   ```
   Fix anything flagged, then actually merge:
   ```
   python -m certcoach.jobs.flashcard_tools <scratch_file.json> [--remove-topic-id <id>]
   ```
   This writes to all three bundled copies (`data/`, `mobile/assets/`, `web-flashcards/src/`)
   atomically -- either all three update or none do.
6. **Verify sync** (`sha256sum` all three files, confirm they match) and **report a summary**:
   topic, concepts covered, card count per concept, and anything the doc didn't support well
   enough to write a good card about.

## Do not

- Do not write cards longer than the schema's length guidance -- these are recall aids, not
  study articles.
- Do not invent facts the doc doesn't support, even to hit a round card count.
- Do not rename or drop the fields `mobile/` and `web-flashcards/` already read (`category`,
  `question`, `answer`, `title`, `subheading`) -- see the guidelines doc.
- Do not merge without running `--validate-only` first if you're at all unsure about length or
  formatting.
