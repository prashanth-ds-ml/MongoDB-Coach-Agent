# Agent Context

Last verified: 2026-07-14 (session 16, closed cleanly -- see Immediate Continuation)

## Mission

CertCoach prepares the learner for the MongoDB Associate Python Developer certification through concept-scoped lessons, validated retrieval practice, persisted progress, and mixed mocks.

## Current Phase

Provenance/trust rollout. A `draft -> sourced -> confirmed/suspect` state now gates every question independently of the older content-contract lifecycle (`active`/`repair_pending`/`quarantined`/`legacy`). Both gates must pass before a question reaches a learner. This phase was implemented and partially run against the live bank in the prior working session, but was never committed to git or documented in memory until 2026-07-05 -- treat any pre-2026-07-05 snapshot in this file's history as superseded.

## Required Product Path

```text
daily agenda -> concept lesson -> scoped Q&A -> five-question practice
-> answer review -> persisted progress -> mixed mock
```

## Non-Negotiable Rules

- `is_practice_ready(question)` = `is_contract_active(question)` AND `is_confirmed(question)`. Neither check alone is sufficient; a question needs both a well-formed contract and a human-confirmed provenance state to ever reach practice, mocks, or remediation.
- `provenance.state` transitions: `draft` (unverified) -> `sourced` (deterministic citation check + self-consistency check both passed) -> `confirmed` (human approved via `certcoach-review-questions`, one question at a time -- never a batch table) or `suspect` (flagged wrong, quarantined the same way `draft` is).
- Citation verification is deterministic only (`database.verify_citation`): a stored quote must appear verbatim (whitespace-normalized) in the named source file under `cleaned_markdowns/` or `pics_qa_transcripts/`. No LLM is ever used to judge factual truth.
- The self-consistency check (separate model, `get_self_consistency_model()`) only judges internal coherence (does the explanation support the marked answer, are options distinct) -- it is never a MongoDB fact-checker and must not be described as one.
- Mock exams (`Full Mock`, `Timed Mock Exam`) draw only from `confirmed` inventory, apportioned by real exam domain weights (`database.EXAM_DOMAIN_WEIGHTS`), with a per-concept round-robin cap and an explicit shortfall report -- never silent padding. The session-scoped Mini-Mock is exempt.
- Population targets are floored at `3 Easy + 2 Medium` per concept (fixed -- mirrors the five-question practice-session composition in `cli.py`) but scale upward from there by each concept's real exam-blueprint weight (`question_targets.build_weighted_targets`/`topic_exam_weight_map`, cascaded from the same `EXAM_DOMAIN_WEIGHTS` the mock uses), not a flat identical target for every concept. `--target-easy`/`--target-medium` on `certcoach-seed-nightly` still overrides flatly when explicitly passed. Generation that can't reach a concept's target after retries is reported as an explicit shortfall, never padded.
- Wrong-attempt remediation is a stateless lookup only (the missed question's own citation + a few domain-matched flashcards) -- no new explanation generation, nothing saved.
- Flashcard spaced review (session 15, supersedes the earlier "no scheduling engine" rule): `planner.mark_concept_lesson_seen` fires when a concept's lesson is shown, independent of the MCQ-score gate -- this is what puts a concept's flashcards into rotation, not topic mastery. `compute_next_review`/`record_flashcard_review`/`get_due_flashcards` run a lightweight SM-2-style schedule (not full FSRS). `CoachPersona.evaluate_flashcard_recall` grades a *typed* answer via the local Ollama model, defaulting to incorrect on any parse failure rather than silently crediting an ungraded answer. See [[project_adaptive_coach_deferred]] (personal memory) for why the old "wait for 3 topics mastered" gate was dropped.
- Lesson-panel chunking (`run_teach_session`) calls `chunk_doc_text(..., group_toward_target=True)` -- greedily groups small header-sections toward `LESSON_SECTION_MAX_CHARS` (2800) instead of one chunk per header. `inspect_doc.py`'s fact-extraction dry-run still uses the old split-only default (`group_toward_target=False`) and is unaffected.
- Legacy, repair-pending, and quarantined content-contract records still cannot enter learner-facing practice; provenance is an additional, stricter gate on top, not a replacement.
- Long repair/population runs use `scripts/run_phase4_overnight.ps1`.
- Optional UI, analytics, gamification, simulator, and general platform work are deferred until after the exam.
- The daily agenda's `"Learn"` item (concept lesson + scoped Q&A) is gated only on doc coverage + an uncompleted concept, never on question-bank readiness (`planner.get_syllabus_status`'s `next_topic` uses `readiness_concepts`, not `ready_subtopics`). Only the five-question practice step at the end of `run_teach_session` gates on the 3E+2M floor -- a concept with zero confirmed questions is still teachable today.
- The concept lesson panel in `run_teach_session` shows the resolved official doc's text verbatim (`planner.load_md_context`), one doc at a time -- it is never an AI paraphrase. `lesson_bank.get_validated_lesson()`/`coach.explain_topic()`/the 6-section lesson template are no longer used in this flow (still exist for `certcoach-prebuild-lesson`, untouched).
- Doc-relevance resolution (which official doc(s) back a concept, for lesson display, question generation, and dry-run preview alike) goes through one shared function, `planner.resolve_concept_docs()` -- a candidate doc must score at least half the concept's top score, not just `> 0`, to exclude generic-token false positives (e.g. "data" in "BSON Data Types" wrongly matching unrelated topic-level docs). Do not reintroduce a separate ad hoc `prioritize_md_files` + `score > 0` filter at a new call site; use the shared function.
- `certcoach-preview-concept`'s dry-run yield report compares a doc's verified yield against the concept's real exam-weighted target (`question_targets.weighted_target_for_concept`), not just a raw candidate count.
- `POPULATION_SOURCE_CHARS` (doc text visible to both generation and dry-run) is 8000, not 1600 -- do not lower it without re-checking corpus doc-size distribution (median ~5,728 chars, p90 37,594, max 121,920).
- `certcoach-preview-concept`'s dry-run scans a doc section-by-section (`inspect_doc.chunk_doc_text`, markdown-header split), not one flat truncated blob -- this lifted BSON Data Types' verified yield from 3 to 66 (see decision log). Real generation (`nightly_seed_questions.py`) does not use chunk-aware scanning yet.
- `certcoach-generate-from-doc` (`src/certcoach/jobs/generate_from_doc.py`) generates questions from one concept's chunked+verified doc facts via local Ollama, independent of the exam-weighted quantity target. **Deprioritized since the session-11 pivot to Claude-authored content** (not deleted -- kept as a fallback/comparison path). See Decision Log sessions 7/11 for the full mechanics and live-verification history.
- `ingest_authored_content.ingest_authored_question()` runs a directly-authored (Claude- or human-written) MCQ through the identical trust pipeline `generate_from_doc.py`/`nightly_seed_questions.py` use -- duplicate check, quality gate, citation verify, self-consistency. Never writes `confirmed`. This is the mechanism both the `/mcqs` and (via `flashcard_tools.py`'s simpler validate/merge) `/flashcards` skills use.

## Live Snapshot (2026-07-12 session 15, verified against the live DB, not inferred)

- **Practice-ready inventory is thin and concentrated**: only 9 of 355 questions are `provenance.state == confirmed` (is_practice_ready), covering just 2 of 12 topics (MongoDB Overview & Document Model: 8, MongoDB Drivers & PyMongo: 1). Every High-weight topic (CRUD x4, Query Operators, Arrays, Aggregation, Indexes) has zero. 321 of 330 `suspect` questions share one root cause -- legacy content with no citation on record -- needing full re-authoring, not a fix. No automated content-generation job exists; the queue only grows when `/mcqs`/`certcoach-seed-nightly` is run manually.
- **Flashcards**: 67 cards, same 3-of-12-topics shape as the MCQ gap (Document Model, CRUD-Create, CRUD-Read). Topics 4-12 have zero.
- **Adaptive coach gate superseded** (see the Non-Negotiable Rules entry above): flashcard-based SM-2-lite spaced review now tracks from day one instead of waiting for 3 topics mastered, since mastery itself depends on the same scarce MCQ inventory above.
- **Real, unfixed gap, found three times now**: `planner.resolve_concept_docs()`'s zero-score fallback is `md_files[:2]` (arbitrary first-N pick). Any CamelCase-with-`()` concept name tokenizes to a fused string that never matches a real filename. Will very likely hit Topic 4 (`replaceOne()`, `updateOne()`, `updateMany()`, `findAndModify`) next -- worth fixing in `score_md_file_for_concept`'s tokenizer at that point.
- Topic 10 "Embedding vs Referencing" still has 5 `suspect` records (2 unexplained since session 7) -- still uninvestigated.

## Immediate Continuation

**Session 15's full work (chunking redesign, pattern rollup, flashcard-tracking build) is committed and pushed** (`2c2f2b0`, confirmed 0 ahead/0 behind `origin/codex/publish-bank-loop`) -- this file previously said it was "the next commit to land"; that was stale and is now corrected. **Session 16 added a standalone `certcoach-notes` companion tool + "My Notes" viewer, and fixed a review-queue back-button UX gap** (commit `9a3b551`, not yet pushed). Full detail in [[session_handoff|Session Handoff]]'s Completed/Next Action -- summary:

1. Run `certcoach-review-questions` to confirm the queued BSON Data Types candidates -- highest-leverage action to move practice-readiness off 2/12 topics.
2. Continue `/flashcards` (Topic 4 next) and `/mcqs` -- both now also feed the flashcard review queue.
3. Investigate Topic 10's 2 unexplained records from session 7 -- still open, read-only.
4. Investigate 13 unexplained modified `cleaned_markdowns/*.md` files sitting uncommitted in the working tree since before session 16 (not this session's work) -- decide commit/discard/re-run.
5. Push session 16's commit (`9a3b551`) once asked.
6. Run `certcoach-map-questions-to-docs --write` live (confirm first, real DB write) to backfill 23 orphan questions -- unchanged since session 7.

## Commands

```powershell
.\.venv\Scripts\python.exe -m certcoach.jobs.analyze_backlog
.\.venv\Scripts\python.exe -m certcoach.jobs.map_questions_to_docs --out <path.csv>
.\.venv\Scripts\python.exe -m certcoach.jobs.reocr_pics_qa
.\.venv\Scripts\python.exe -m certcoach.jobs.recover_screenshot_citations
.\.venv\Scripts\python.exe -m certcoach.jobs.purge_screenshot_backlog
.\.venv\Scripts\python.exe -m certcoach.jobs.review_questions
.\.venv\Scripts\certcoach-preview-concept.exe --topic <id> --concept "<name>"  # combined study + dry-run
.\.venv\Scripts\python.exe -m pytest tests\unit -q
```

`review-web/` (Docket) was retired in session 11 -- `certcoach-review-questions` (CLI) has full parity. Don't reference or rebuild it without checking the decision log first.

## Deep References

- Release blockers: [[preparation_tool_gap_assessment|Preparation Tool Gap Assessment]]
- Current execution order: [[next_steps|Next Steps]]
- Product behavior: [[coach_flow_spec|Coach Flow Spec]]
- Decisions: [[decision_log|Decision Log]]
- Exam scope: [[project_exam_scope|Project Exam Scope]]
- Latest checkpoint: [[session_handoff|Session Handoff]]
- Doc study order: [[study_order_map|Study Order Map]]

## Resume Point

- Verify this file against `git status`/`git log` and a live DB provenance count before trusting it -- it was badly stale once already.
- Don't run destructive jobs without confirmation; in-place `provenance` updates are lower-risk.
- Note the DB moves between sessions even when git doesn't -- the user runs `certcoach-review-questions` independently, so always re-check live provenance counts at session start rather than trusting the last snapshot.
