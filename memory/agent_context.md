# Agent Context

Last verified: 2026-07-08 (session 14, closed cleanly -- see Immediate Continuation)

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
- Wrong-attempt remediation is a stateless lookup only (the missed question's own citation + a few domain-matched flashcards) -- no new explanation generation, nothing saved, no spaced-repetition scheduling engine exists or is planned.
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

## Live Snapshot (2026-07-08 session 14, verified against the live DB, not inferred)

- **Pivot in effect since session 11**: Claude authors MCQs and flashcards directly (no local Ollama generation call) -- both still funnel through the identical citation-verify/self-consistency/confirm pipeline every other question does. Local Ollama's only remaining jobs are the self-consistency check and, later, the adaptive coach.
- `certcoach_db.questions`, Topic 1 BSON Data Types: 1 `confirmed` Easy, 18 `sourced`, 2 `draft`, 34 `suspect` (all of the original 30 legacy suspects now individually reviewed and annotated -- see [[decision_log|Decision Log]] session 13). Comfortably past the 16-slot weighted target (7 Easy + 9 Medium) with real candidate surplus, pending human confirm via `certcoach-review-questions`. **Practice is still not usable** -- nothing beyond the original 1 is confirmed yet.
- **Flashcards**: atomic, concept-level cards now exist for Topics 1-3 (BSON Data Types/Document structure/Collections vs Tables, CRUD-Create, CRUD-Read -- 67 cards total across `data/`, `mobile/assets/`, `web-flashcards/src/`, all byte-identical). Topics 4-12 still have zero cards.
- **Real, unfixed gap found twice now**: `planner.resolve_concept_docs()`'s fallback (when every candidate doc scores 0) is `md_files[:2]` -- an arbitrary "first N files in syllabus order" pick, not a relevance judgment. Confirmed concretely for Topic 2 (`insertOne()`, `insertMany()`, `_id and ObjectId`) and Topic 3 (`findOne()`, `Projections`, `countDocuments()`) -- any CamelCase-with-`()` concept name tokenizes to a fused string (`"insertone"`, `"findone"`) that never matches a real filename. Worked around by hand in both flashcard sessions; will very likely hit Topic 4 (`replaceOne()`, `updateOne()`, `updateMany()`, `findAndModify`) too. Worth fixing in `score_md_file_for_concept`'s tokenizer at that point rather than continuing to route around it per topic.
- **`/mcqs` skill rules updated based on live use** (session 13): Phase A's audit step now has four outcomes (Keep/Improve/Move/Discard, not three) -- explicitly don't discard-and-stop when a concept is short of target, don't silently skip the `suspect` legacy backlog, back up before any delete. See `.claude/skills/mcqs/SKILL.md` step 4 for the exact mechanics; `feedback_mcq_audit_bias.md` (personal memory, not this vault) has the "why."
- Topic 10 "Embedding vs Referencing" now has 5 `suspect` records (2 original unexplained ones from session 7, still uninvestigated, plus 3 moved there this session from a BSON Data Types mistag) -- still nothing confirmed for that concept, still worth investigating the original 2 before trusting the bank's overall state.

## Immediate Continuation

**Session 14 closed cleanly (not a mid-flow pause) after the user asked to update docs and close out.**
Full detail is in [[session_handoff|Session Handoff]]'s Completed/Next Action lists -- summary:

1. Ask before committing -- sessions 5 through 14 are all still uncommitted and stacked (provenance/trust pipeline groundwork, the full CLI bug-fix pass, the root audit + persona grounding fixes, CLI review parity, `antigravity_cli`/`src/scripts`/`review-web` removals, and all of sessions 12-14's flashcard/MCQ content work). No test run needed for sessions 12-14 specifically (data-only, no source changed).
2. Run `certcoach-review-questions` to confirm/reject the ~20 BSON Data Types candidates from session 13 -- zero human review has touched that output yet.
3. Continue `/flashcards` topic-by-topic (Topic 4 next) and `/mcqs` concept-by-concept, applying the now-documented legacy-pool review pattern each time.
4. Investigate the 2 original unexplained Topic 10/11 confirmed/sourced questions from session 7 -- still open, read-only, safe to do first.
5. Run `certcoach-map-questions-to-docs --write` live (confirm with the user immediately before, it's a real DB write) to backfill the 23 orphan questions -- still not done.
6. Once a few questions are confirmed, run an actual practice session to verify the learner-facing loop, not just the data layer.
7. Do not start the adaptive-coach/spaced-revision work (journey steps 10-11) until the user reports 3 topics/concepts mastered.

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
