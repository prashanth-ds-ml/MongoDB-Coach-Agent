# Agent Context

Last verified: 2026-07-06

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

## Live Snapshot (2026-07-06, verified against the live DB, not inferred)

- `certcoach_db.questions`: 379 total. Provenance: 2 confirmed, 2 sourced, 375 suspect, 0 draft. The user confirmed 2 questions (both Topic 1 BSON Data Types, Easy) via `certcoach-review-questions` between sessions; 2 remain `sourced` awaiting review (Topic 10 Embedding vs Referencing Easy, Topic 11 PyMongo purpose Easy). **Practice is still not usable** -- 2 confirmed items for one concept is far short of the `3 Easy + 2 Medium` readiness gate for even that one concept.
- Suspect backlog breakdown (`certcoach-analyze-backlog`): 353 have a real regeneration lead, 23 have `topic_id: None` and no lead at all, 0 duplicates. 26 were screenshot-sourced; 1 recovered to `sourced`, 25 confirmed unrecoverable.
- New read-only report, `certcoach-map-questions-to-docs` (`src/certcoach/jobs/map_questions_to_docs.py`): for every question, resolves syllabus topic/concept (stored value if present, else the same keyword inference `certcoach-map-questions` uses) and the official doc(s) that concept maps to (same scoring as [[study_order_map|Study Order Map]]), then flags citation drift against what's currently stored. Live results: 356/379 questions had stored topic/concept, 23 were inference-only; 238 questions resolve to a concept-exact doc, 118 fall back to topic-level docs (no dedicated doc exists), 23 stay fully unresolved; 333/379 questions carry a citation that doesn't match any resolved official doc (expected -- legacy `citation_source` values are titles/URLs, not filenames). Full per-question CSV was written to a scratch path, not committed; regenerate with `--out <path>` when needed. This did not write to the database (explicit user choice).
- The doc-to-question generation loop (pull doc -> generate MCQ -> citation check -> self-consistency check -> `sourced`) is proven working end-to-end on real data. Four real bugs were found and fixed doing so -- see Decision Log 2026-07-06: deficit calculator ignoring the provenance gate, citation checker rejecting quotes over markdown backticks, self-consistency model (`deepseek-r1:8b` -> `qwen2.5-coder:7b`) that never finished reasoning, and doc-scoring unable to match `$`-operator concepts to their own docs.
- [[study_order_map|Study Order Map]]: all 58 syllabus concepts mapped to their official doc(s) in canonical study order -- read this before generating for a new concept.
- All 249 unit tests pass.
- **The entire provenance/trust implementation plus three sessions of fixes/tools on top of it are uncommitted in the working tree as of 2026-07-06.** Do not assume git history reflects current code; check `git status`/`git diff HEAD` first.

## Immediate Continuation

1. User runs `certcoach-review-questions` themselves to confirm the 2 remaining `sourced` questions.
2. Decide on the 25 unrecoverable screenshot questions and the 23 `topic_id: None` suspect records (purge vs. hold for review) -- the new doc-mapping report gives all 23 a best-effort topic/concept placement and doc lead if regeneration is preferred over purge.
3. Once a few questions are confirmed, run an actual practice session to verify the learner-facing loop, not just the data layer.
4. Ask before committing -- three sessions of uncommitted, tested work now sit in the working tree.
5. Resume the still-open Phase 4 lesson/population thread only after the provenance gate has enough confirmed inventory to matter.

## Commands

```powershell
.\.venv\Scripts\python.exe -m certcoach.jobs.analyze_backlog
.\.venv\Scripts\python.exe -m certcoach.jobs.map_questions_to_docs --out <path.csv>
.\.venv\Scripts\python.exe -m certcoach.jobs.reocr_pics_qa
.\.venv\Scripts\python.exe -m certcoach.jobs.recover_screenshot_citations
.\.venv\Scripts\python.exe -m certcoach.jobs.purge_screenshot_backlog
.\.venv\Scripts\python.exe -m certcoach.jobs.review_questions
.\.venv\Scripts\python.exe -m pytest tests\unit -q
```

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
