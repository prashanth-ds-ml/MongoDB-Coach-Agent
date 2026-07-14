# Session Handoff

Last updated: 2026-07-14 (session 16, closed cleanly)

Related: [[Memory Home]], [[agent_context|Agent Context]], [[next_steps|Next Steps]], [[decision_log|Decision Log]], [[study_order_map|Study Order Map]]

## Current State

- Phase: pivot to Claude-authored content (decided session 11) is actively running for MCQs/flashcards. As of session 15, adaptive/spaced review no longer waits on a mastery gate -- flashcard-based tracking (see below) runs from day one. See [[agent_context|Agent Context]]'s Live Snapshot for full current numbers.
- **Committed and pushed through `2c2f2b0`** on `origin/codex/publish-bank-loop` (`prashanth-ds-ml/MongoDB-Coach-Agent`, confirmed 0 ahead/0 behind) -- this includes sessions 5-15 in full (session 15 part 2's chunking redesign/pattern-rollup/flashcard-tracking work, previously logged below as "the next commit to land," was already committed and pushed by the time session 16 started -- that line was stale and is now corrected).
- **Session 16 committed locally but not pushed**: `9a3b551` (quick-notes companion tool + review-queue back-option fix, 6 files). Ask before pushing.
- **Uncommitted in the working tree, not this session's work, origin unknown**: 13 `cleaned_markdowns/*.md` files (topics 1/6/7/8/9/10/11) show real content diffs (e.g. previously-missing example blocks being added back) -- left alone this session per explicit user choice ("commit quick-notes only"). Investigate and decide (commit/discard/re-run source) before they're mistaken for session 16's work.
- Live DB provenance counts move independently of git between sessions (the user runs `certcoach-review-questions` on their own) -- always re-check live counts at session start via `database.get_provenance_counts`/the `gap_report.py`-style script pattern used in sessions 12-14, rather than trusting the last snapshot here.
- **Historical detail below this point (sessions 5-14) is append-only and kept for record -- do not treat old DB counts, commit hashes, or "live right now" numbers in those entries as current, including their repeated "nothing committed" claims.** Session 16 is the active thread; see [[agent_context|Agent Context]] for what's actually true today.

## Completed This Session (2026-07-05)

1. **Reconstructed the undocumented provenance system** by reading `git diff HEAD` across `database.py`, `content_contract.py`, `cli.py`, `judge_questions.py`, `nightly_seed_questions.py`, `config.py`, and all six new `jobs/` scripts, then verified against the live DB rather than trusting docstrings alone.
2. **Ran `certcoach-reocr-pics-qa`** to completion: 69/69 screenshots transcribed (66 newly OCR'd with `glm-ocr:latest`, 3 already done, 0 failures) into `src/certcoach/data/pics_qa_transcripts/`.
3. **Found and fixed a real bug in `analyze_backlog.py`**: `_has_real_doc_lead()` only matched a question's `citation_source` against a literal filename in `cleaned_markdowns/`, but every legacy question stores `citation_source` as a human-readable title (e.g. `"Find One Document"`) or a mongodb.com URL, never the corpus's real filenames -- so the check always returned `False` for the legacy backlog regardless of whether real docs existed. Added a topic-level fallback (`_topic_has_cleaned_markdowns`) that checks whether any `topic_{NN}_*` file exists for the question's `topic_id`. Updated 3 existing unit tests in `tests/unit/test_analyze_backlog.py` that had encoded the old, narrower behavior, and added one new test for the corrected behavior. All 239 tests still pass.
4. **Re-ran `certcoach-analyze-backlog`** with the fix: of 376 suspect questions, 353 now correctly show a real regeneration lead (topic has official docs), 23 (`topic_id: None`) have no lead at all, 0 are duplicates. Before the fix, the script reported 0 `has_doc_lead` and would have wrongly signaled that all 376 (minus 26 screenshot ones) were safe to delete.
5. **Ran `certcoach-recover-screenshot-citations`** against the true screenshot-sourced count (26 records, not the ~333 the docstrings assumed -- most suspect questions are legacy-generated, not screenshot-sourced). Result: 1 recovered to `sourced`, 25 confirmed unrecoverable (no supporting quote findable in the transcript), consistent with the known original-extraction-rewrote-content problem documented in `purge_screenshot_backlog.py`.

## Completed This Session (2026-07-06)

1. **Deleted `scratch/`** (24 unreferenced, already-gitignored debug scripts, including the known pytest hazard file) after confirming nothing imports it.
2. **Drafted then dropped `inspect_doc.py`** (a per-doc question-yield estimator) after the user redirected toward the simplest working loop; removed the file, its test, and its entry point rather than leave dead scaffolding.
3. **Fixed `nightly_seed_questions._get_db_style_counts()`** to gate on `database.is_practice_ready()` instead of `is_contract_active()` alone -- the deficit calculator was blind to the provenance gate and reported 0 generation slots needed for concepts that are actually 100% unconfirmed.
4. **Proved the full doc-to-question loop live** on Topic 1 → BSON Data Types: correct doc pulled, MCQ generated with a style tag and citation, seven-part explanation attached.
5. **Fixed `database.verify_citation()`** to strip markdown emphasis punctuation before comparing quote to source -- a genuinely verbatim quote was being rejected only because the doc wrapped the same words in backticks.
6. **Benchmarked 5 local Ollama models** for the self-consistency check and switched the default from `deepseek-r1:8b` (produced 14,000+ characters of reasoning and still timed out) to `qwen2.5-coder:7b` (fast and correct on the genuinely-good test case). Noted but deferred: none of the 5 models reliably caught a deliberately-broken test case, a separate prompt-design weakness.
7. **Reprocessed the 2 live test questions** through the fixed pipeline -- both now `sourced`.
8. **Improved `review_questions.py`**: full seven-part explanation now renders as Markdown (was silently truncated at 800 characters, cutting off the last 4 of 7 sections); source filename is now a clickable `file://` link (Windows Terminal renders this as clickable; older console hosts won't); removed the "Source excerpt" preview entirely (redundant now that the file is one click away, and its own quote-matching logic didn't share the markdown fix in #5).
9. **Fixed `planner.score_md_file_for_concept()`** to strip `$` from concept tokens -- bare-operator concepts (`$set`, `$elemMatch`, `$match`, etc.) were scoring 0 against their own dedicated reference docs because filenames never contain a literal `$`. Improved doc resolution for Topics 4, 7, and 8.
10. **Built and saved [[study_order_map|Study Order Map]]**: all 58 syllabus concepts mapped to their official doc(s) in canonical study order, generated after the fix above.

## Completed This Session (2026-07-06, continued)

1. **Verified live state instead of trusting the last snapshot**: found the working tree byte-identical to the prior handoff, but the live DB had moved -- the user confirmed 2 of the 4 `sourced` questions independently via `certcoach-review-questions` between sessions, and 2 new suspect records had appeared. Corrected a mid-investigation false alarm: an initial query used top-level `topic_id`/`concept` fields, which don't exist on question documents (they live under `metadata.*`), and wrongly suggested 375/379 suspect records had no topic at all; re-querying the correct field path confirmed the real count matches the known 23.
2. **Built `certcoach-map-questions-to-docs`** (`src/certcoach/jobs/map_questions_to_docs.py`), a read-only report requested by the user to map every question to its syllabus topic/concept and official doc(s), explicitly scoped to no DB writes (user's choice among three offered options). Reuses `find_best_concept()` from the existing `map_questions.py` job for topic-id-less records and the same `planner.score_md_file_for_concept()`/`prioritize_md_files()` scoring that built [[study_order_map|Study Order Map]]. Added entry point `certcoach-map-questions-to-docs` (`pyproject.toml`) and 8 unit tests (`tests/unit/test_map_questions_to_docs.py`).
3. **Ran it against the live bank**: 356/379 questions had stored topic/concept; the 23 orphaned records were placed via inference (none stayed fully unmapped). 238 questions resolve to a concept-exact official doc, 118 fall back to topic-level docs (genuine corpus gaps, same pattern as `study_order_map.md`), 23 have no topic to resolve a doc against at all. 333/379 questions carry a citation value that isn't one of the resolved official docs -- expected, since legacy `citation_source` is a human-readable title or URL, never a real filename. Full per-question detail written to a scratch CSV (not committed, regenerate with `--out <path>` when needed).
4. Reinstalled the package (`pip install -e .`) to register the new entry point; full suite verified at 249/249 passing.

## Completed This Session (2026-07-06, session 3)

1. **Committed** the 3-sessions-deep provenance/trust rollout (`730d8e7`) and a separate unrelated flashcards.json sync (`f350d2a`); deleted a stray garbled debug file that had no reference anywhere.
2. **Wiped learner history** (`user_attempts`, `user_study_sessions`, `user_profiles`, `lesson_artifacts`) at the user's explicit request, backed up first, to give a genuinely fresh start.
3. **Reset Topic 1 BSON Data Types to true zero**, including deleting its 2 already-confirmed questions per the user's explicit "discard and redo" choice, backed up first.
4. **Purged the 25 confirmed-unrecoverable screenshot suspects**; kept the 23 orphan suspects as regeneration signal rather than purging them.
5. **Built the exam-weighted population target system**: `question_targets.topic_exam_weight_map()` cascades the real `EXAM_DOMAIN_WEIGHTS` down through topic and concept (replacing the flat 5E/5M-for-everyone default); `nightly_seed_questions.audit_weighted_deficits` now consumes it for the default path; added a shortfall report; updated `AGENTS.md`/`agent_context.md`'s documented rule. 255/255 tests pass. **This code (question_targets.py, nightly_seed_questions.py, database.py, AGENTS.md, agent_context.md, 2 test files) is not committed.**
6. Dry-ran the new weighted targets against Topic 1 BSON Data Types (confirmed correct: 16 slots, 7 Easy + 9 Medium) but stopped before any live generation -- no questions generated yet this session.

## Completed This Session (2026-07-06, session 4)

1. **Committed the exam-weighted population target work** from session 3 (`805f5e9`), after re-verifying 255/255 tests passed and confirming the working tree matched the handoff exactly.
2. **Ran the first live weighted seed batch**: `certcoach-seed-nightly --topic 1 --concept "BSON Data Types" --max-questions 3`. Inserted 3 questions -- 1 reached `sourced`, 2 landed in `draft` because the model's quoted excerpt paraphrased the source doc by one word each time (dropped/added "alias"); the citation gate correctly rejected both. This is the pipeline working as designed, not a bug.

## Completed This Session (2026-07-07, session 5)

1. **Found the working tree mid-build on a browser review UI** ("Docket") with no memory record of it: `database.py` already had `get_provenance_counts`/`get_citation_excerpt` and concept-scoped `get_questions_for_review`/`count_questions_for_review` (all tested, 6 passing tests), `pyproject.toml` already declared `certcoach-review-web = "certcoach.web.review_api:run"` plus `fastapi`/`uvicorn` deps -- but `src/certcoach/web/` didn't exist. Asked the user how to proceed (build it / commit DB groundwork only / drop it); user chose **build it**.
2. **Built `src/certcoach/web/review_api.py`**: FastAPI app serving the same one-question-at-a-time confirm/suspect decision as `certcoach-review-questions`, in a browser. `GET /api/counts`, `GET /api/queue` (topic_id/concept-scoped), `POST /api/questions/{id}/confirm`, `POST /api/questions/{id}/suspect`, `GET /` (self-contained HTML/vanilla-JS page: stat pills, question card, citation excerpt shown in its source paragraph context, Confirm/Suspect/Skip actions). No ObjectId handling needed -- `_id` is a plain UUID string.
3. **Installed `fastapi`, `uvicorn`, `httpx`** into `.venv` (httpx is test-only, for `TestClient`) and reinstalled the package to register the `certcoach-review-web` entry point.
4. **Added `tests/unit/test_review_api.py`** (9 tests: counts/queue serialization, confirm/suspect success + 404, reason forwarding, index page). Full suite: 270 passing.
5. **Live-smoke-tested**: started `certcoach-review-web`, hit `/api/counts`, `/api/queue`, `/` against the real `certcoach_db` -- correctly showed Topic 1 BSON Data Types' actual state (1 sourced/verified, 2 draft/unverified, citation excerpt correctly locating each quote in its source paragraph).
6. **User tested it live in a browser and hit "confirm is blocked"** on the first queued question. Not a bug -- that question's citation genuinely fails the deterministic check (AI-quoted excerpt doesn't match the source doc verbatim), so Confirm is correctly disabled, same gate the CLI enforces. Fixed the real gap: the web UI silently grayed out the button with no explanation, unlike the CLI's yellow warning text. Added an amber "Citation check failed -- Confirm is unavailable..." banner (same wording as the CLI) plus a disabled-button tooltip. Re-verified 9/9 `test_review_api.py` passing; server re-tested serving the fix.
7. Stopped the dev server before closing the session. **Nothing from this session is committed.**

## Completed This Session (2026-07-07, session 6)

1. **Audited the user's full 12-step study-loop journey** (load doc -> dry-run yield -> generate -> review with citations in a React tool -> confirm -> build bank -> mocks -> track attempts -> adaptive coach -> spaced-revision notes -> flashcards) against the actual repo. Steps 1, 3, 5, 7, 8, 9 already existed and work. Step 2 (per-doc dry-run) had been built once and deleted, never committed. Step 4 wanted React but Docket's frontend was inline vanilla JS. Steps 10-11 (adaptive coach, spaced-revision notes) had been deliberately cut in an earlier session to a stateless lookup, documented in `database.py`'s "spec point 10" comment and this file's own "no spaced-repetition scheduling engine exists or is planned" line.
2. **User decided**: defer steps 10-11 until 3 topics/concepts are mastered (saved to personal memory `project_adaptive_coach_deferred`, not this vault); combine steps 1+2 into one command instead of two; rebuild the review tool in React.
3. **Built `certcoach-preview-concept`** (`src/certcoach/jobs/inspect_doc.py`, entry point added to `pyproject.toml`) -- `--topic --concept`, resolves the concept's doc(s) via `planner.load_md_context`/`prioritize_md_files` (same mechanism `nightly_seed_questions.py` uses), prints each as a study panel, then asks the population model to enumerate candidate testable facts and verifies each one's quote via `database.verify_citation` (the same citation gate real generation must clear), reporting yield/dropped counts and a difficulty/response-type breakdown. Recovered the original (never-committed) `inspect_doc.py`'s heuristic from a stale `.pyc` bytecode cache via disassembly, then re-scoped it from a bare `--doc filename` to topic/concept, which is what made it fit the existing pipeline this time. 9 new tests (`tests/unit/test_inspect_doc.py`). Live-smoke-tested against Topic 1 BSON Data Types on the real DB/docs: 5 candidate facts, 3 verified (2 Easy/single, 1 Medium/multiple), 2 correctly dropped.
4. **Rebuilt Docket's frontend in React** (`review-web/`, React 19 + Vite 8, matching `web-flashcards/`'s tooling exactly -- this is the repo's first React app that actually talks to a backend over HTTP, unlike `web-flashcards` which only reads a static bundled JSON). Components: `api.js` (fetch wrapper), `StatPills.jsx`, `CitationPanel.jsx` (side-by-side citation excerpt with highlighted match + the amber "Confirm is unavailable" banner, reproducing session 5's real fix verbatim), `QuestionCard.jsx` (two-column layout, Confirm/Suspect/Skip), `App.jsx` (flat, `useState`-driven, no router/state library). `review_api.py` backend changed to pure JSON (dropped `_INDEX_HTML`, `GET /` now returns service info) plus `CORSMiddleware` for the Vite dev origin (`DOCKET_CORS_ORIGINS` env-overridable). Updated `test_review_api.py`'s one HTML-content assertion, added a CORS-header test. `npm run build` and `npm run lint` (oxlint) both clean.
5. **Live-verified end-to-end against the real DB**: started both `certcoach-review-web` (8765) and `npm run dev` (5173) as background processes; confirmed `/api/counts` and `/api/queue` return correctly shaped real data through CORS, including an actual `citation_verified: false` record (Topic 1, BSON Data Types, the "number" alias question) -- exactly the regression case the amber-banner fix guards against.
6. Full suite: **280/280 tests pass**. Reinstalled the package (`pip install -e .`) to register the new `certcoach-preview-concept` entry point.
7. **Nothing from this session is committed**, and it stacks on top of session 5's still-uncommitted Docket backend work.
8. **Built and saved a learner-journey diagram** (`memory/diagrams/learner_journey.html`, linked from `Memory Home.md`) mapping the 12-step journey against build status: build loop (steps 1-6, all built), practice loop (steps 7-8, built), gated adaptive layer (steps 9-11, deliberately deferred).
9. **Audited the live interactive CLI (`certcoach`) against that diagram** and found a real problem, not just a gap: `Study Settings & Extras -> f) AI Question Bank Management Wizard` (`cli.py`) was reachable and looked functional, but `quiz_generator.generate_quiz_for_topic()` depends on a `chroma_db` vector store that doesn't exist in this repo -- every generation attempt threw, was caught, and silently fell back to the same hardcoded mock question every time, regardless of topic. It also never captured a real citation quote (so it could never pass `verify_citation`/reach `confirmed` -- not a safety hole, but dead scaffolding) and wrote through an unrelated `draft_questions_col`/`approve_draft_question` path.
10. **User chose removal.** Deleted `run_ai_question_wizard()` and its `validate_lexical_syntax_guard` wrapper; replaced the menu entry with `run_question_bank_reports()`, keeping the two legitimate reports (Quality Analytics, Seven-Part Explanation Coverage Audit) that used to share the function. Updated `test_cli.py` (renamed the wizard test to target the new function/choice numbering; repointed the syntax-guard test to `planner.validate_lexical_syntax_guard` directly). Full suite: **280/280 still pass** (test count unchanged -- 1:1 replacement).
11. Noted but did not act on: `database.save_draft_question`/`approve_draft_question`/`get_draft_questions`/`draft_questions_col` and `core/quiz_generator.py` are now fully orphaned (no callers left anywhere in `src/certcoach`) -- a further cleanup the user hasn't asked for yet.
12. **User asked for that follow-up cleanup too.** Removed `save_draft_question`, `get_draft_questions`, `approve_draft_question`, and the `draft_questions_col` global (both places it was assigned: module load and `update_database_connection`) from `database.py`; deleted `src/certcoach/core/quiz_generator.py` and `src/certcoach/core/retriever.py` (`CertCoachRetriever`) entirely -- confirmed via repo-wide grep that nothing in `src/certcoach` or `tests/` referenced any of these; the only remaining hits are a separate, previously-reviewed legacy copy under `src/scripts/core/`, left untouched (out of scope, already covered by the 2026-07-06 `src/scripts/` retention decision). Full suite: **280/280 still pass**, unchanged (no test ever touched these symbols).
13. Session closed. Full state as of now:
    - **Uncommitted, tested, live-verified, ready to review**: session 5's Docket backend (`src/certcoach/web/`, provenance-review DB helpers in `database.py`), session 6's `certcoach-preview-concept` (`inspect_doc.py` + test), the React `review-web/` rewrite, the CLI wizard removal + `run_question_bank_reports()` replacement, and this orphaned-code cleanup.
    - **Saved to the repo**: `memory/diagrams/learner_journey.html` (the journey diagram, linked from `Memory Home.md`).
    - **Saved to personal memory** (not this vault): the adaptive-coach/spaced-revision deferral, gated on 3 topics mastered.
    - Nothing pushed or committed this session -- ask before either.

## Completed This Session (2026-07-07, session 7)

1. **Fixed a real product-path bug the user hit live**: accepted the 12-day plan, chose "Start Today's Study Agenda," and got "all 58 concepts blocked" -- including concept #1, which the user wanted to study *today*. Root cause: `planner.get_syllabus_status()`'s `next_topic` selection required `ready_subtopics` (the 3E+2M question-readiness filter) before a `"Learn"` agenda item could ever be emitted, even though the lesson/Q&A pipeline (`lesson_bank.py`, `certcoach-prebuild-lesson`) has zero dependency on question count. Changed the condition to `readiness_concepts` (doc coverage + an uncompleted concept) so lesson delivery is decoupled from practice readiness; practice itself is untouched and still correctly blocks at the 3E+2M floor with a clear "not ready yet" message. Updated the one test that encoded the old coupling. 280/280 passing after this fix.
2. **Replaced the AI-paraphrased lesson with the raw official doc, verbatim** (`run_teach_session`, `cli.py`), per the user's explicit call after seeing the AI-authored "Core Concept" panel live. Removed the `lesson_bank.get_validated_lesson()`/`coach.explain_topic()` call path and the weak-focus/benchmark context merge that existed only to feed it; the panel is now just `planner.load_md_context([filename])`'s output. The 6-section lesson template (Level Breakdown, Exam Radar, Micro-Challenge, etc.) is no longer shown in this flow -- accepted tradeoff, not an oversight. Follow-up Q&A (`coach.handle_followup`) untouched.
3. **Docs now shown one at a time**, not concatenated -- each resolved file gets its own panel + a "next doc" prompt, per the user's stated preference to read every official doc for thorough understanding, just not merged into one wall of text.
4. **Found and fixed a real doc-relevance bug** while investigating why the BSON Data Types panel merged 3 docs: `score_md_file_for_concept`'s flat `score > 0` threshold let the generic token "data" (from "BSON Data Types") falsely match two unrelated topic-level docs (`core_data_modeling_introduction`, `core_databases_and_collections`) purely because "data" is a substring of their filenames (score 10 each, vs. the real match's score 25). Added `planner.resolve_concept_docs()` (relative threshold: a candidate must score >= 50% of the concept's top score) and switched all 5 duplicated call sites (`load_md_context`, `lesson_bank.py`, `nightly_seed_questions.py`, `map_questions_to_docs.py`, `inspect_doc.py`) to use it. Verified safe against a real multi-doc concept (`sort/limit/skip`'s three cursor docs, tied at score 10 each -- all kept). This means live generation (`nightly_seed_questions.py` cites through the same `load_md_context` path) was almost certainly pulling citation context from irrelevant docs for any concept whose name shares a common word with another doc's filename.
5. **Added exam-weighted target comparison to `certcoach-preview-concept`'s dry-run**, per the user wanting to see doc yield "with respect to the weightages": `question_targets.weighted_target_for_concept()` + `default_total_bank_target()` (the latter promoted out of `nightly_seed_questions._default_total_bank_target`, now shared) feed a new "Coverage vs. exam-weighted target" table in `inspect_doc.py`.
6. **Raised `POPULATION_SOURCE_CHARS` 1600 -> 8000** (`.env.example` updated too) after finding the cap applied identically to both the dry-run *and* real generation (`nightly_seed_questions.py:987`), leaving the median corpus doc (~5,728 chars) only ~28% visible and the BSON Data Types doc (23,941 chars) only ~7% visible -- confirmed live: candidate facts found rose 5 -> 8. Verified (citable) count stayed flat at 3 though -- the added candidates mostly failed the verbatim-quote check, meaning quote-paraphrase compliance is now the dominant yield ceiling, not doc visibility. User explicitly deferred fixing that for a later session.
7. **Rebuilt the dry-run to chunk each doc by markdown header instead of one flat truncated blob**, per the user's own brainstormed idea (`langchain_text_splitters.MarkdownHeaderTextSplitter`, already a transitive dependency via `langchain_ollama` -- no new package needed). `chunk_doc_text()` splits on `#`/`##`/`###`/`####`, tags each chunk with its header path (e.g. "BSON Types > ObjectId") and source doc file, drops sub-40-char stub chunks, and falls back to `RecursiveCharacterTextSplitter` for any section still too large for one model call. `inspect_concept()` now scans every chunk individually (fact-extraction + per-chunk citation verification against that chunk's own source file, tighter than checking against every resolved file), and a new "Per-section yield" table shows exactly which sections are productive.
   - **Live result, BSON Data Types (15 sections scanned)**: verified (citable) candidates went from 3 (flat 8000-char truncation) to **66** (chunked scan) -- 73 found, 66 verified (90% pass rate, vs. 37.5% flat). Fully covers the 16-slot weighted target (7 Easy + 9 Medium) with large surplus -- `print_target_coverage` now reports both difficulties "met". This proves the concept was never corpus-limited; flat truncation (at either 1600 or 8000 chars) simply never showed the model most of the doc's 15 sections.
   - Scoped to the dry-run only this session at first -- but see #8 below, the user then redirected to build real generation off this chunked scan directly.
8. **Built `certcoach-generate-from-doc`** (`src/certcoach/jobs/generate_from_doc.py`), per the user's explicit redirect: "leave weightage aware question generation... focus on getting quality questions based on exam type taxonomy... for the single doc learner just read." Reuses `inspect_doc.inspect_concept()`'s chunked dry-run to get verified facts per doc section, selects one fact per section (coverage of everything the learner read) capped at `--max-questions` (default 8), assigns each an exam-style taxonomy type (Type A Syntax/Trap, Type B Theory/Constraints, Type C Predicting Output, Type D Troubleshooting/Performance -- the same weights `nightly_seed_questions.py` already uses per topic) via weighted random choice, then runs each through the real generation + quality-gate + duplicate-check + explanation-repair + citation-verification + self-consistency pipeline -- reusing `nightly_seed_questions.py`'s `StyleTarget`/`generate_weighted_question`/`validate_question_quality`/`is_duplicate_question`/`run_generation_pipeline_checks` directly rather than reimplementing them (provenance-critical logic, not orchestration). Added a `generation_source` param to `generate_weighted_question` (default unchanged) so these questions are labeled `"doc_chunk_seed"`, not mislabeled `"nightly_weighted_seed"`. **User's stated end-goal: retire `nightly_seed_questions.py` entirely once this proves out** -- the import coupling to it is a known, temporary tradeoff.
9. **Broke and fixed the editable install mid-session**: `pip install -e .` (to register the new entry point) uninstalled the existing registration, then failed to complete because the user's own running `certcoach` CLI session (PID still alive) had `certcoach.exe` locked -- `import certcoach` broke entirely for a few minutes. Restored by manually writing a `.pth` file (`.venv/Lib/site-packages/certcoach-editable.pth` -> `src/`) so imports/pytest work again; the console-script `.exe` wrappers (including the new `certcoach-generate-from-doc`) are still not regenerated -- run `pip install -e .` properly once the user's `certcoach` session is closed. Until then, use `python -m certcoach.jobs.generate_from_doc` instead of the bare command.
10. All 300 unit tests pass (11 new for `generate_from_doc.py`'s selection/taxonomy/orchestration logic, plus the earlier chunking-related additions) -- one of these (`assign_style_types`'s taxonomy coverage) was initially written as a 20-draw probabilistic assertion and flaked on a later run; rewrote it to mock `random.choices` for deterministic coverage instead of relying on statistical likelihood.
11. **Ran `generate_from_doc.py` live against BSON Data Types (`--max-questions 5`), then stopped it early at the user's explicit request** ("pause the process") after 4 of 5 targets had been attempted. Real result, verified against the live DB: 1 question reached `sourced` (Binary Data section, `certcoach-t01-bson-data-types-easy-005-0c9c3c96`), 2 landed at `draft` (ObjectId and the top BSON Types section -- citation/self-consistency correctly caught something on each, not a bug), 1 was left mid-pipeline with `content_contract_status: needs_explanation_repair` and no `provenance` field yet (`certcoach-t01-bson-data-types-easy-007-95198767`, String section -- inserted but interrupted before `repair_explanations` ran when the process was stopped; recoverable via `certcoach-repair-explanations`, not corrupted, invisible to any learner surface since it has no provenance state). The Timestamps section (5th target) was never attempted. This is enough real evidence that the full pipeline -- selection, generation, quality gate, dedup, insert, repair, citation check, self-consistency, provenance -- works end-to-end, not just in unit tests.
12. Updated `agent_context.md` and `decision_log.md` with this session's rules/decisions. Nothing from sessions 5-7 is committed -- ask before committing, per every prior handoff's standing note.

## Completed This Session (2026-07-07, session 8)

1. **Locked the learner-facing journey spec** ([[coach_flow_spec|Coach Flow Spec]], v2.0) at the
   user's explicit request, before resuming any feature work. Rewrote it from v1.0's abstract
   mode boundaries into a concrete, code-verified stage-by-stage flow (Stage 0 daily-agenda
   selection through Stage 6 Free Chat), with an exact gate-number table (3E+2M practice unlock,
   >=4/5 mastery, >=3 topics for Mini-Mock, 70% for Full/Timed Mock) and an explicit "out of
   scope" section for the deferred adaptive layer. Scoped to the learner-facing journey only,
   not the separate content-build/maintainer loop (dry-run -> generate -> Docket review ->
   confirm) that sessions 5-7's uncommitted work mostly touched. See Decision Log 2026-07-07
   session 8 for the full reasoning.
2. Documentation-only session -- no source files changed, no tests run. Everything from
   sessions 5-7 (Docket backend, `generate_from_doc.py`, `review-web/`, CLI cleanup, the
   lesson-gate/doc-source/`resolve_concept_docs`/weighted-target/chunking fixes) is still
   uncommitted, exactly as left. Still ask before committing.

## Completed This Session (2026-07-07, session 9)

1. **Closed the two gaps identified right after session 8's spec lock**, per the user's explicit
   walk-through of the full content lifecycle and a direct ask to "fix this flow, fix the gaps,
   remove all the dead code and other irrelevant code."
2. **Taxonomy-aware inspection**: `inspect_doc.CANDIDATE_FACTS_PROMPT` now asks for a
   `suggested_style_type` (Type A-D) per candidate fact, validated in `inspect_concept()` against
   `nightly_seed_questions.style_weights_for_topic(topic_id)`'s allowed set (out-of-scope
   suggestions cleared to `None`, never guessed). New `print_taxonomy_yield_report()` shows
   verified-fact counts per allowed Type plus an "unclassified" row. Promoted the previously
   3x-duplicated taxonomy weight table into one canonical `style_weights_for_topic()` in
   `nightly_seed_questions.py`.
3. **Content-aware generation**: `generate_from_doc.select_generation_targets()` now carries each
   fact's `suggested_style_type` through; `assign_style_types()` uses it directly when valid for
   the topic, falling back to weighted-random only when missing/invalid. Each target is tagged
   `style_source` ("content"/"fallback") and `print_summary()` reports the split.
4. **Orphan backfill**: `certcoach-map-questions-to-docs --write` persists
   `metadata.topic_id`/`metadata.concept` only onto documents currently missing them, reusing the
   existing `resolve_topic_and_concept()` heuristic -- never overwrites an already-tagged
   document, never touches `provenance.state`. Defaults to a dry-run count when `--write` is
   omitted. **Not yet run live against the real DB** -- next session should run it (with the
   user's go-ahead immediately before, since it's a real write) to actually clear the 23 orphans.
5. **Legacy reference panel**: `database.get_legacy_reference_questions()`, `GET /api/legacy`
   (`review_api.py`), and `LegacyPanel.jsx` (`review-web/`) show old-bank `suspect` questions for
   the same concept alongside the fresh review queue -- read-only, no confirm/suspect action.
   `npm run lint`/`npm run build` both clean.
6. **Removed a batch of confirmed zero-caller dead code** (see Decision Log session 9 for the
   full list) and deleted the orphaned `src/certcoach/jobs/lesson_aligned_practice_builder.py`
   outright. Left `nightly_seed_questions.py`'s own orchestration (`run_weighted_seed`/`main`)
   untouched -- still the live `certcoach-seed-nightly` entry point.
7. **Bumped [[coach_flow_spec|Coach Flow Spec]] to v2.1**, adding a Content Lifecycle section
   documenting this closed loop.
8. All 311 unit tests pass (7 new for the taxonomy-aware inspect/generate paths, 3 new for the
   orphan backfill, 2 new for the legacy-reference route). Full-package import smoke test run
   after dead-code removal. Nothing pushed or committed this session -- ask before either.

## Completed This Session (2026-07-07, session 10)

1. **Ran a deep audit of `src/certcoach/cli.py`** (menus, options, interactions) at the user's
   request, saved to [[cli_audit_2026-07-07|CLI Behavior Audit]] (linked from Memory Home), then
   fixed all 19 findings plus one additional issue found while planning the fix
   (`main_menu()`'s exit handling was inconsistent because the installed console-script entry
   point bypasses the `if __name__` graceful-exit wrapper entirely -- see the audit doc and
   Decision Log session 10 for the full mechanics).
2. Highlights: centralized `main_menu()`'s exit handling into one `try/finally`; added a
   `confirm()` wrapper (Ctrl+C = decline) and replaced all 8 raw `Confirm.ask` sites; made
   mock-exam resume discard the whole saved session on any length mismatch instead of partially
   restoring it; made the mock shortfall report actually stay on screen; split
   `run_practice_questions`'s shortfall gate by `is_mock` and fixed the non-mock branch to check
   the real fixed composition instead of the caller's `num`; fixed onboarding's save-before-confirm
   bug and same-day exam-date boundary bug; fixed `ask()` to honor "back" in Rich's `choices`
   list (root cause of several menus silently rejecting "back"); made the exam Summary Grid
   timer-aware; fixed a stale hardcoded mock-pacing message and four hardcoded "70%"
   mastery-threshold strings.
3. Two pre-existing unit tests (`test_run_practice_questions_allows_option_b_answer`,
   `test_run_practice_questions_next_prompt_q_exits`) were unknowingly relying on the old,
   looser shortfall gate -- updated their fixtures to a real 3E+2M composition rather than
   weakening the new, correct gate. All 311 tests pass. Nothing committed this session -- ask
   before committing (this stacks on everything from sessions 5-9, still uncommitted).

## Completed This Session (2026-07-08, session 11)

1. **Ran a full root-level senior-review audit** (AI Engineer / QA / CLI-UX / MongoDB /
   Architect angles) at the user's request, delivered as an artifact (10 sections: Summary,
   Keep, Improve, Remove, AI Coaching, MongoDB, CLI/UX, Tests, Questions, Roadmap).
2. **Grounded `handle_followup`** (`core/persona.py`) in the same `md_context` `explain_topic`
   already resolves, and copied over `explain_topic`'s "never invent, say so if not covered"
   guardrail language. `handle_free_chat` and `evaluate_scenario`/`generate_scenario` were left
   unchanged -- the latter is still the single highest hallucination-risk surface per the audit,
   just not tackled this session.
3. **Brought `certcoach-review-questions` (CLI) to feature parity with Docket (`review-web/`)**:
   added `--concept` filtering, switched citation display to `database.get_citation_excerpt`'s
   in-context highlighted view, added a read-only legacy-reference panel. All three gaps closed
   by wiring existing `database.py` functions into the CLI tool rather than new backend work.
   Docket has since been retired entirely (see item 9 below) now that the CLI has parity.
4. **Removed `src/antigravity_cli/`, `src/scripts/`, `workflows/`, `.clinerules`**, the `ag`
   entry point + now-unused `pyyaml` dependency from `pyproject.toml`, and the 3 test files that
   only tested `src/scripts` (`test_indexer.py`, `test_map_mongodb_docs_to_syllabus.py`,
   `test_mongodb_docs_md_scraper.py`) -- a whole second, unmaintained ingestion pipeline the
   maintainers had already flagged as undecided. Done in two steps (auto-mode safety guard
   required separate confirmation for `workflows`/`.clinerules`/the 3 tests, since they weren't
   named in the first request even though they were direct casualties of it).
5. **Corrected a misread from the audit discussion**: CertCoach is single-machine only (not
   multi-device), so the `update_user_profile`/`update_streak` fetch-merge-`replace_one` race
   stays a "fix eventually" item, not an elevated priority. Not touched this session.
6. 304/304 tests pass (12 fewer than session 10's 316 -- the 3 removed test files accounted for
   the difference, confirmed by count). `import certcoach.cli` verified clean after removals.
7. **Closed the audit's top hallucination-risk finding**: `generate_scenario`/`evaluate_scenario`
   (`core/persona.py`) had zero doc grounding and zero MongoDB-correctness guardrails -- the
   Scenario Simulator invented both the scenario and the judgment of the student's real answer
   purely from the model's own knowledge. Fixed by having `run_scenario_simulator` (`cli.py`)
   resolve a concrete subtopic + official doc within the chosen topic (mirroring
   `run_teach_session`'s per-subtopic doc resolution) and pass it through as `md_context` to both
   functions, which now carry the same "ground in reference material, don't invent, say so if
   unsure" language as `explain_topic`/`handle_followup`. Refactored both from inline-prompt
   methods into free `build_scenario_prompt`/`build_scenario_evaluation_prompt` functions
   (matching `build_followup_prompt`'s existing pattern) so the prompt content is unit-testable.
   4 new tests added. 308/308 tests pass.
8. Nothing committed this session -- ask before committing (stacks on sessions 5-10).
9. **Retired `review-web/` (Docket) entirely.** Deleted `review-web/`, `src/certcoach/web/`
   (the FastAPI backend), and `tests/unit/test_review_api.py`. Removed the `certcoach-review-web`
   entry point and the now-unused `fastapi`/`uvicorn` dependencies from `pyproject.toml`. Rewrote
   `requirements.txt` in plain UTF-8 (it had drifted to UTF-16 from an old accidental `pip
   freeze`) and dropped the now-dead `pyyaml` line left over from the `antigravity_cli` removal.
   Fixed a stale docstring in `cli.py` (`run_question_bank_reports`) that still named
   `certcoach-review-web` as a sibling tool. 296/296 tests pass (12 fewer -- `test_review_api.py`
   accounted for the difference). Neither `review-web/` nor `src/certcoach/web/` were ever
   git-tracked, so nothing was lost.
10. **Fixed the interrupted `pip install -e .` from session 7, properly this time.** Re-ran it
    now that nothing holds `certcoach.exe` locked -- completed cleanly. Also found and removed
    two stale artifacts left by the original interrupted attempt: a corrupted
    `~ertcoach-0.1.0.dist-info` directory (leading `~`, from an interrupted uninstall) that was
    causing a spurious "Ignoring invalid distribution -ertcoach" warning on every pip operation,
    and the now-redundant manual `certcoach-editable.pth` workaround file. Re-ran the install
    once more afterward to confirm the warning is gone. All `certcoach-*.exe` console scripts
    (18 total) now exist in `.venv/Scripts/`, including `certcoach-generate-from-doc` as a bare
    command for the first time.
11. **Stopped here on the user's explicit request** ("stop and update all the docs so that we
    will continue later") before running the remaining live-operation items below or committing
    anything. Nothing was left half-finished -- everything attempted up to the stop is complete
    and verified.
12. **Strategic pivot, decided by the user right after the pause**: Claude authors MCQs (single
    and multi-select) and flashcards directly from here on, instead of relying on local Ollama
    generation, to speed up exam prep. Local Ollama stays exactly where it already is (the
    self-consistency check) and will additionally power the future adaptive coach once real
    attempt-history tracking exists. The existing citation-verify/self-consistency/confirm
    pipeline is unchanged -- Claude-authored drafts go through the identical gates.
13. **Audited flashcard + MCQ content quality** (user's explicit request, before generating
    anything new). Findings: `data/flashcards.json` (43 cards, in sync across `data/`,
    `mobile/assets/`, `web-flashcards/src/`) had 27/43 cards (63%) with real defects -- unclosed
    code fences, literal mid-sentence truncation, and scraped-source artifacts ("Full Practice
    Set link below", stray section headers) -- a bulk import never cleaned up. Live DB check of
    the 4 currently-reachable MCQs (2 confirmed, 2 sourced): 3 solid, 1 (Topic 10 "Embedding vs
    Referencing", `sourced`) is a stray off-topic legacy item with a 0-character explanation --
    this explains the session-7 "Topic 10/11 mystery" (see Next Action below). A sample of the
    351 inert `suspect` legacy questions looked like decent raw material, not individually bad.
14. **Redesigned and rebuilt flashcards** from one long-form note per broad exam objective to
    atomic, concept-level Q&A cards (matching MCQ/syllabus granularity) -- the old shape was
    reference material, not something recallable in a few seconds. Shipped a 17-card pilot
    covering all of Topic 1 (BSON Data Types x7, Document structure x6, Collections vs Tables
    x4), replacing `fc_1_1`/`fc_1_2`, grounded directly in the 3 official Topic 1 docs. Schema
    keeps every field the frontends already read (`id`, `category`, `domain_weight_pct`,
    `subheading`, `title`, `question`, `answer`) and adds `topic_id`/`concept`/`source_doc` for
    future concept-level remediation matching. Re-ran the truncation/artifact scanner afterward:
    0 of the 17 new cards flagged; the 26 still-flagged cards are exactly the pre-existing ones
    outside Topic 1. All 3 copies re-verified byte-identical.
15. **Removed all remaining old-format flashcards** (topics 2-6, 41 cards) per the user's
    explicit "remove all the old cards" instruction -- flashcards.json now holds only the 17
    Topic 1 atomic cards until replacements are authored via the new workflow (item 16 below).
16. **Built the `/flashcards` and `/mcqs` project skills** (`.claude/skills/{flashcards,mcqs}/SKILL.md`)
    plus a shared `memory/content_authoring_guidelines.md` reference doc both point at (quality
    bar, schema, taxonomy definitions, the exact syntax-example/casing gate rules). Also built
    the reusable tooling both skills depend on:
    - `src/certcoach/jobs/flashcard_tools.py` (`certcoach-flashcard-tools`) -- `validate_cards`/
      `merge_cards`, extracted from the ad hoc Topic 1 pilot script into a tested (11 tests),
      reusable module. Merges write all three bundled copies atomically or none.
    - `src/certcoach/jobs/ingest_authored_content.py` (`certcoach-ingest-authored`) -- takes a
      directly-authored MCQ and runs it through the *exact* existing trust pipeline (duplicate
      check, quality gate, citation-verify, self-consistency), reusing `nightly_seed_questions.py`'s
      functions directly rather than reimplementing them. Never writes `confirmed`. 12 tests.
    - Caught and fixed one real quality-gate bug while building this: the Syntax Example section
      must say exactly "not required for this concept" for non-syntax-heavy style types (e.g.
      Type B) -- a real code example there instead *fails* validation. Found by testing against
      the real (unmocked) `validate_question_quality`, not by trusting the assembly logic.
    - Also caught and fixed a test-isolation bug: several new tests patched the wrong module
      (the function's definition site instead of where `ingest_authored_content` imported it),
      which silently hit the live, reachable MongoDB instance when run alone and only failed as
      part of the full suite. Fixed per "patch where it's used, not where it's defined."
17. All 317 tests pass (full suite, and each new test file confirmed to pass standalone too --
    not just as part of the suite). Nothing committed this session -- ask before committing.

## Completed This Session (2026-07-08, session 12)

1. **Ran `/flashcards` for Topic 2 (CRUD Operations - Create)**, the next topic in canonical
   order with zero cards (Topics 2-6 were wiped in session 11). Authored 15 atomic cards --
   `insertOne()` x6, `insertMany()` x6, `_id and ObjectId` x3 -- grounded in
   `topic_02_CRUD_Create_L1_01.md`/`_L1_02.md` (the mongosh reference docs) and the PyMongo
   insert-guide doc, `category: "CRUD Operations"` / `domain_weight_pct: 51` per
   `question_targets.EXAM_DOMAIN_WEIGHTS`. `_id and ObjectId` only got 3 cards -- most of that
   concept's substance (auto-ObjectId-on-missing-`_id`, `_id` type restrictions, ordering
   guarantees) is already covered by Topic 1's BSON/Document cards, so only genuinely new,
   CRUD-Create-scoped facts were added rather than restating them.
2. **Found (not fixed) a real gap in `planner.resolve_concept_docs()`**: its fallback when every
   candidate doc scores 0 is `md_files[:2]` -- an arbitrary "first 2 files in syllabus.json order"
   pick, not a relevance judgment. This bit Topic 2: `score_md_file_for_concept()` tokenizes
   `"insertOne()"` to `"insertone"` (one fused token), which is never a substring of any filename
   (`..._crud_insert__...`, `..._insert_documents__...`), so all 4 of Topic 2's docs scored 0 for
   all 3 concepts and the resolver would have silently returned just the two generically-named
   `CRUD_Create_L1_01/02.md` lesson files for every concept, skipping the actual official
   PyMongo/manual docs entirely. Worked around it this session by reading and manually selecting
   from all 4 docs instead of trusting the resolver output. Root cause is the same class of bug as
   the session-7 `resolve_concept_docs` fix (concept-name tokenization not matching filenames) but
   on the *fallback* path rather than the scoring path -- likely affects other CamelCase-with-`()`
   concepts (e.g. `findOne()`, `updateMany()`) the same way. Not fixed -- flagging for a future
   session since it's a shared function with 5 call sites (lesson display, generation, dry-run,
   map-questions-to-docs, and now the flashcard/mcq authoring workflow).
3. **Validated and merged** via `flashcard_tools` (`--validate-only` then real merge): 17 -> 32
   cards across all three bundled copies, re-verified byte-identical (`sha256sum`).
4. Nothing else touched this session -- no code changes, no tests run (static JSON content only).

## Completed This Session (2026-07-08, session 13)

1. **Ran `/mcqs` for Topic 1, BSON Data Types** -- the first Claude-authored MCQ pass since the
   session-11 pivot, and the natural first real target since it already had 1 confirmed question
   toward its 16-slot weighted target (7 Easy + 9 Medium). Audited all 35 non-confirmed questions
   tagged to the concept (3 draft, 1 sourced, 1 left with no provenance from an interrupted
   session-7 run, 30 legacy suspect): kept the 1 solid sourced question as-is; discarded 2 drafts
   that turned out redundant with an already-**confirmed** question (same "$type `number` alias"
   fact, both also had broken citations); improved 2 more by rewriting and superseding via
   `mark_question_suspect` (one had failed self-consistency because its explanation implied but
   never stated the correct option letter; one was left with a genuinely empty explanation from an
   interrupted generation run). Authored 16 new questions total (across two rounds -- see item 2)
   covering previously-untested facts from the official BSON types doc: type-alias table lookups,
   two genuine multi-select questions (deprecated types with a real "JavaScript vs.
   JavaScript-with-scope" trap; ObjectId's 3-byte-component structure), `$isNumber`, ObjectId's
   big-endian exception, `decimal128` precision/use-case/Python-support-gap, Timestamp-vs-Date,
   Date's signed range, binary subtype 9 (vector data), and `ObjectId.getTimestamp()`. All ran
   through the full existing pipeline (`ingest_authored_content.py`): duplicate check, quality
   gate, citation verify, self-consistency (local Ollama, `qwen2.5-coder:7b`) -- nothing is ever
   auto-confirmed.
2. **User feedback mid-session, now saved to personal memory
   ([[feedback_mcq_audit_bias]]/`feedback_mcq_audit_bias.md`, not this vault)**: the first-round
   audit was too quick to discard-and-stop instead of discard-and-replace, even though the concept
   was still short of target. Went back and authored 4 more genuinely distinct questions (Python's
   decimal128 support gap, `ObjectId.getTimestamp()`, binary subtype 9/vector data, and the
   "integer replaces the timestamp" ObjectId-constructor trap) to actually fill the freed-up
   headroom rather than leaving it empty. Net result across both rounds: 20 authored, 0 skipped as
   duplicate, 17 reached `sourced`, 3 landed at `draft` (2 from known local self-consistency
   model limitations on subtler/multi-select checks -- not flaws in the questions themselves; 1
   from the model producing no parseable verdict at all). Live DB now: BSON Data Types has 1
   confirmed + 15 sourced + 2 draft + 34 suspect (30 original legacy + 4 newly discarded this
   session) -- 16 non-suspect candidates now queued against the 16-slot weighted target, up from 2
   at session start.
3. **Went back and actually reviewed all 30 pre-existing legacy `suspect` records** for this
   concept, per the same user feedback -- rather than leaving them as a blanket "not reviewed."
   Findings, by category: 3 were vacuous auto-generated filler ("always refer to official specs",
   no real fact tested); ~13 were off-topic drift into Topic 10's embedding/referencing territory
   (cited from the data-modeling-introduction doc, not a BSON Data Types doc) or internally
   redundant with each other (the same "array can hold documents" fact repeated ~8 times); 2 were
   factually wrong (claimed nested arrays aren't valid BSON, which is false); ~9 were duplicates of
   facts already covered by this session's new pool (`$type` number alias, the `long` alias,
   decimal128 precision); 2 were concept-mismatched (ID slug and source doc say Document
   structure, not BSON Data Types). **3 were genuinely salvageable** and got rewritten with fresh
   citations and superseded: "Float" is not a real BSON type (Double is) -- new
   `easy-014-53f7aa70`; the Object BSON type (what developers call an "embedded document") -- new
   `easy-015-c9aea4f3`; why `_id`/ObjectId acts as the primary key -- new `easy-016-055fd722`
   (also merges two near-duplicate legacy versions of that fact). All 30 legacy records now carry
   a specific, categorized `suspect_reason` instead of the generic "no verbatim citation quote on
   record" placeholder every one of them had before. All 3 new questions reached `sourced`
   cleanly. Live DB now: BSON Data Types has 1 confirmed + 18 sourced + 2 draft + 34 suspect (30
   legacy, now all annotated, + 4 discarded this session) -- comfortably past the 16-slot weighted
   target with genuine surplus, consistent with the "more non-duplicate content is fine" feedback.
4. **User pushed further** ("if useful for future topics/concepts, move them; delete duplicates;
   salvage what we can; if factually wrong but correctable with docs, fix them") -- went back
   through the 30-record annotation from item 3 and actually acted on it instead of leaving
   everything sitting in `suspect`:
   - **Corrected the factually-wrong claim** (2 legacy records asserted a BSON array can't contain
     another array/document as an element -- false; nested arrays and arrays-of-documents are
     explicitly documented) with one new question grounded in
     `topic_01_docs_manual_core_data_modeling_introduction__c1bfc595e5.md` -> `easy-017-3f698bdd`.
     That same doc's "arrays of documents" fact also let this one question supersede 6 more
     internally-redundant "array can hold X" legacy duplicates in one shot, instead of needing a
     separate rewrite for each.
   - **Salvaged and correctly re-homed** a schema-flexibility fact (2 legacy records, mistagged
     under BSON Data Types) as a new question under the concept it actually belongs to,
     **Collections vs Tables** -> `certcoach-t01-collections-vs-tables-easy-002-ccf1db42` -- the
     first non-suspect question that concept has ever had.
   - **Moved 3 records to Topic 10** (`metadata.topic_id`/`concept` updated to
     `"Embedding vs Referencing"`) that were genuinely about data-modeling relationships, not BSON
     typing -- left `suspect` with an updated reason since they still need a proper citation
     rewrite, but now a future Topic 10 `/mcqs` pass will actually find them instead of them being
     silently stranded under the wrong concept forever.
   - **Backed up then deleted 25 records** that were pure zero-salvage duplicates or vacuous
     auto-generated filler (backup: `backups/bson-data-types-legacy-cleanup-20260708/questions.json`,
     28 records including the 3 moved ones, before any changes).
   - Net result: BSON Data Types' suspect count dropped from 34 -> 6 (the few remaining are
     genuine "superseded-by-X" references or one too-vague-to-salvage item, kept for audit trail,
     not clutter). 2 more new questions reached `sourced` cleanly.
5. No source code changed this session -- data-only, no test run needed.
6. **Codified session 13's MCQ-audit feedback directly into the skill** (not just personal
   memory): `.claude/skills/mcqs/SKILL.md` step 4 now has four outcomes (Keep/Improve/Move/Discard,
   up from three), explicit "don't discard-and-stop when the concept is short of target" and
   "don't silently skip the `suspect` legacy backlog" rules, and a backup-before-delete
   requirement. Personal memory (`feedback_mcq_audit_bias.md`) updated to point back at the skill
   as the source of truth for mechanics.

## Completed This Session (2026-07-08, session 14)

1. **Ran `/flashcards` for Topic 3 (CRUD Operations - Read)** -- the next topic in canonical order
   with zero cards. Confirmed the `resolve_concept_docs` fallback bug flagged in session 12 hits
   again here: `findOne()`, `Projections`, and `countDocuments()` all tokenize to fused CamelCase
   strings that never match any filename, so the resolver silently fell back to an arbitrary
   "first 2 files" pick for all three. Worked around it by reading all 11 of Topic 3's docs
   directly and hand-assigning the real sources per concept (e.g. `findOne()`'s actual content
   lives in the PyMongo `find`/`find_one` guide, not the fallback's generic picks) -- same pattern
   as session 12's Topic 2 workaround. Still not fixed at the code level.
2. **Authored 35 atomic cards** across all 6 Topic 3 concepts: `find()` x7, `findOne()` x5,
   `Projections` x6, `Cursors` x5, `sort/limit/skip` x8 (the richest concept -- 3 dedicated mongosh
   reference docs), `countDocuments()` x4. Grounded in the PyMongo query/find/project/count/cursors
   guides plus the mongosh `find()`/`cursor.limit()`/`cursor.skip()`/`cursor.sort()` reference docs.
   Deliberately kept `find()` facts (cursor semantics, type bracketing, dot notation) separate
   from `findOne()` facts (return-value shape, natural-order default, the ObjectId-from-URL
   gotcha) to avoid overlap between the two sibling concepts.
3. **Validated and merged**: 32 -> 67 cards across all three bundled copies, re-verified
   byte-identical (`sha256sum`). No source code changed -- data-only session.

## Completed This Session (2026-07-09 to 2026-07-12, session 15)

See [[decision_log|Decision Log]]'s two 2026-07-09/2026-07-12 entries for full reasoning; summary:

**Part 1 (commits `f4eb3c3`..`47038f6`, committed and pushed to `prashanth-ds-ml`):**
1. Built the ephemeral review-quiz mode (`run_review_quiz`) over the still-unconfirmed backlog.
2. Full CLI command-handling sweep after a live `/exit` failure -- widened `EXIT_COMMANDS`/
   `BACK_COMMANDS`/`PRACTICE_COMMANDS`/`CONTINUE_COMMANDS`, fixed ~10 related issues.
3. Chunked the lesson panel by markdown header instead of one flat blob; fixed the long-flagged
   CamelCase tokenizer bug in `score_md_file_for_concept`; fixed a real content-loss bug in
   `topic_06_Query_Operators_L5_01.md` (missing `$nor`/`$not`/`$or`).
4. Added ephemeral, non-punitive per-section comprehension check-ins, pilot-scoped to
   "Document structure"; fixed a local-model JSON-truncation reliability issue along the way
   (`_close_unbalanced_json`, 0/5 -> 5/5 live success rate).
5. Fixed an invalid Rich color (`"gold"` -> `"gold1"`) and prompt-dimming inconsistencies found
   via a full color/box-style audit.
6. Committed sessions 5-14's entire stacked backlog as 5 logically-grouped commits, then pushed
   to `prashanth-ds-ml/MongoDB-Coach-Agent` (had to `gh auth switch` first -- wrong account active).

**Part 2 (uncommitted as of this handoff -- next commit to land):**
1. **Redesigned lesson chunking**: `chunk_doc_text` now greedily groups small header-sections
   toward a 2800-char target (`group_toward_target=True`) instead of only ever splitting large
   ones -- median section count per doc dropped from ~7-9 to 3, verified against the real corpus
   and live on the exact doc the user flagged (9-10 sections -> 4). Old split-only behavior kept as
   the default so `inspect_doc.py`'s fact-extraction pipeline is unaffected.
2. **Mistake pattern rollup**: `database.get_trap_pattern_report()` groups existing error-book
   trap classifications by frequency, surfaced as a "Pattern Summary" panel in the Error Book
   screen. Also fixed one styling inconsistency: the Error Book's explanation panel was missing
   `code_theme="monokai"`.
3. **Ran a repo-wide "ready to stop touching and study" audit.** Code came back clean (376/376
   tests, no dead code, all entry points valid, no secrets). Real finding: only 9/355 questions
   are `provenance.state == confirmed`, covering just 2/12 topics -- every High-weight topic has
   zero practice-ready MCQs, and 321/330 `suspect` questions share one root cause (no citation on
   legacy records) that needs full re-authoring, not a fix. No automated content-generation job
   exists anywhere -- confirmed via GitHub Actions/session scheduler/Windows Task Scheduler checks.
4. **Superseded the "wait for 3 topics mastered" adaptive-coach gate.** Built flashcard-based
   spaced review tracking from day one: `mark_concept_lesson_seen` (fires when a lesson is shown,
   independent of the MCQ-score gate), SM-2-lite scheduling (`compute_next_review`/
   `record_flashcard_review`/`get_due_flashcards`), and Ollama-graded typed recall
   (`evaluate_flashcard_recall`) -- wired into a new Library menu option, "Review Due Flashcards."
   Flashcard content coverage is currently the same 3-of-12-topics gap as the MCQ bank (67 cards) --
   tracking is built to let content catch up topic-by-topic, per the user's explicit choice.
5. 395/395 tests pass (19 new). Verified live against a disposable scratch profile and the real
   local Ollama model (3/3 recall-grading cases correct on first attempt).

## Completed This Session (2026-07-14, session 16)

1. **Built the standalone quick-notes companion tool**, per the user's exploratory ask about a
   second-terminal notes tab for building a personal cheat sheet. Counter-proposed a manually-opened
   command instead of an auto-spawned terminal (Windows terminal-spawning is fragile); user agreed
   ("yes, build it that way"). Shipped: `certcoach-notes` (`src/certcoach/jobs/quick_notes.py`,
   entry point registered in `pyproject.toml`) for freeform, timestamped note capture in a second
   terminal; `database.add_quick_note`/`get_quick_notes` + a new `quick_notes_col` collection
   (wired in all 3 required places -- module declaration, initial connection,
   `update_database_connection`); a read-only `show_quick_notes()` viewer wired into
   `run_library_submenu()` as option `j` ("My Notes"), Back shifted to `k`. Distinct from the
   existing per-question `add_question_review_note` (content-improvement signal) and the
   pre-authored `show_exam_traps()` cheat sheet.
2. **Fixed a real UX gap in the Review Pending Questions menu**: the user reported "no option to go
   back" -- not a functional bug (`ask()` already accepted the typed word "back"), but the hint was
   easy to miss, buried as inline text at the end of a long prompt rather than a visible option like
   the rest of the app's lettered/numbered menus. Added an explicit `0. Back` line matching the
   existing 1-N numbered-list convention; `0` now works alongside "back".
3. Added tests for both (`test_add_quick_note_*`, `test_get_quick_notes_*` in
   `test_content_contract_provenance.py`; `test_show_quick_notes_*`,
   `test_show_review_queue_menu_zero_exits_without_reviewing` in `test_cli.py`). 411/411 tests pass.
   Ran `pip install -e .` to register the `certcoach-notes` console-script entry point (had to wait
   for a locked `certcoach.exe` from the user's own running session to close first).
4. **Corrected a stale claim found while closing the session**: `git log`/branch-tracking showed
   session 15 part 2's work (commit `2c2f2b0`) was already committed *and* pushed to
   `origin/codex/publish-bank-loop`, despite this file previously saying it was still "the next
   commit to land." Fixed in the Current State section above.
5. **Committed session 16's own work** (`9a3b551`, 6 files) after the user chose "commit quick-notes
   only" when asked how to handle the working tree's mixed state -- explicitly left 13 unrelated,
   pre-existing modified `cleaned_markdowns/*.md` files (topics 1/6/7/8/9/10/11, real content diffs,
   origin unknown from this session's context) untouched rather than guess at bundling or discarding
   them. Not pushed -- ask before pushing.

## Next Action

**Content pipeline (active thread):**
1. Run `certcoach-review-questions` to confirm/reject the queued BSON Data Types candidates --
   still the single highest-leverage action to move practice-readiness off 2/12 topics.
2. Continue `/flashcards` topic-by-topic (Topic 4 next) and `/mcqs` concept-by-concept -- both are
   now doing double duty: MCQ bank growth *and* feeding the new flashcard spaced-review queue.
   The `resolve_concept_docs` fallback gap (flagged sessions 12/14, still unfixed) will very likely
   hit Topic 4 (`replaceOne()`, `updateOne()`, `updateMany()`, `findAndModify`) a third time.
3. Mark the stray Topic 10 "Embedding vs Referencing" `sourced` question suspect (flagged since
   session 11) -- still open, still safe to do first, read-only.

**Housekeeping:**
4. Investigate the 13 unexplained modified `cleaned_markdowns/*.md` files (topics 1/6/7/8/9/10/11)
   sitting in the working tree since before session 16 -- decide whether to commit, discard, or
   re-run whatever produced them. See Current State above.
5. Push session 16's commit (`9a3b551`) once the user asks.
6. `memory/agent_context.md` is still over its ~800-word budget -- flagged every session since 14,
   still not addressed with a dedicated trim pass.
7. Run `certcoach-map-questions-to-docs --write` live (confirm with the user first, real DB write)
   to backfill the 23 orphan questions -- unchanged, still pending since session 7.

## Known Blockers

- **MCQ practice inventory**: only 9 of 355 questions are `confirmed`/practice-ready, covering just
  2 of 12 topics (MongoDB Overview & Document Model, 1 driver question). Every High-weight topic
  (CRUD x4, Query Operators, Arrays, Aggregation, Indexes) has zero. Root cause: 321/330 `suspect`
  questions are legacy content with no citation on record -- needs re-authoring, not a fix. No
  automated generation job exists; the queue only grows when `/mcqs`/`certcoach-seed-nightly` is
  run manually and someone reviews via `certcoach-review-questions`.
- **Flashcard inventory**: same shape of gap, one level behind -- 67 cards across only 3 of 12
  topics (Document Model, CRUD Create, CRUD Read). The new spaced-review tracking is built and
  live but has nothing to schedule outside those 3 topics until `/flashcards` catches up.
- The self-consistency check still can't reliably catch every subtle issue (confirmed again in
  session 13) -- deferred, not blocking; affected questions land safely in `draft` for human review.
- Phase 5 full study-flow and mixed-mock smoke tests remain manual and are blocked on meaningful
  `confirmed` inventory.

## Commands

```powershell
# Provenance/trust pipeline
.\.venv\Scripts\python.exe -m certcoach.jobs.analyze_backlog
.\.venv\Scripts\python.exe -m certcoach.jobs.map_questions_to_docs --out <path.csv>
.\.venv\Scripts\python.exe -m certcoach.jobs.map_questions_to_docs --write  # backfill orphan topic_id/concept (real DB write)
.\.venv\Scripts\python.exe -m certcoach.jobs.backfill_provenance --dry-run
.\.venv\Scripts\python.exe -m certcoach.jobs.reocr_pics_qa
.\.venv\Scripts\python.exe -m certcoach.jobs.recover_screenshot_citations
.\.venv\Scripts\python.exe -m certcoach.jobs.purge_screenshot_backlog
.\.venv\Scripts\python.exe -m certcoach.jobs.review_questions
.\.venv\Scripts\certcoach-review-web.exe  # browser UI ("Docket"), http://127.0.0.1:8765 by default

# Per-concept seeding loop (now exam-weighted by default)
.\.venv\Scripts\python.exe -m certcoach.jobs.nightly_seed_questions --topic 1 --concept "BSON Data Types"

# Preview next Phase 4 concept (secondary thread)
.\.venv\Scripts\python.exe -m certcoach.jobs.next_phase4_topic

# Run unit tests
.\.venv\Scripts\python.exe -m pytest tests\unit -q
```
