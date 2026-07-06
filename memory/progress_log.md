# Progress Log

Append-only record of implementation progress with timestamps.

## 2026-06-03T00:00:00+05:30
- Aligned the coach persona with a bounded state machine: Teach -> Check -> Practice -> Review.
- Updated the CLI lesson flow so follow-up Q&A stays inside the current concept.
- Added project memory files for flow design, decisions, and progress tracking.
- Updated the README to reflect seven-part repairs and concept-scoped teaching.
- Tightened micro-challenges so they stay inside the current concept and do not pull in later-topic methods.
- Removed generated profile snapshot files and documented the canonical project layout.

## 2026-06-15T00:00:00+05:30
- Completed study-runtime and question-bank lifecycle stabilization.
- Added verified question backups, deterministic migration, explanation repair, comparison reporting, and a bounded overnight runner.
- Enforced canonical syllabus topic and concept ordering for repair and population.
- Separated the `3 Easy + 2 Medium` readiness gate from configurable default population inventory targets of `5 Easy + 5 Medium`.
- Verified 121 unit tests and prepared the Phase 4 checkpoint for publication.

## 2026-06-17T00:00:00+05:30
- Refreshed the quality-gated model runner to support separate population and repair response contracts.
- Normalized judge validation so population questions can use string options plus `correct_answer`.
- Switched the active chain to local-first ordering with OpenRouter and Cloudflare as fallback.
- Removed Unicode-sensitive progress glyphs from overnight repair/population output to keep Windows runs stable.
- Brought the maintained unit suite to 123 passing tests.
- Added model chain config (`get_population_model_chain()`, `get_repair_model_chain()`, judge config) with local `gemma4:12b` first pass, OpenRouter and Cloudflare Workers AI fallback.
- Implemented the quality pipeline: deterministic checks -> duplicate (stem hash) check -> LLM judge (RAG-grounded) -> retry -> fallback, logged as JSONL to `logs/model_quality.jsonl` per attempt, with a 3-failure/5-minute circuit breaker per model.
- Added `source_files` metadata on generated questions for judge verification, and the `yixin0829/mongodb-dev-cert-prep` exam-fidelity benchmark (22 CRUD objectives, PyMongo examples).
- Core quality modules landed: `model_runner.py` (quality gates, circuit breaker, multi-provider) and `judge_questions.py` (RAG judge with source verification).

## 2026-07-03T00:00:00+05:30
- Phase 4 bank-maintenance loop reached Topic 4: `replaceOne()` fully populated (6E/5M); `updateOne()`, `updateMany()`, `$set`, `$push`, `$inc` all study-ready (3E/2M each); ordered target advanced to `$unset`. Topic 3 closed from the selector's perspective (all six concepts study-ready). Topic 2 concepts split into `insertOne()`, `insertMany()`, `_id and ObjectId`, backlog cleared.
- Bank-wide quarantine triage: 121 records canonically mapped and pending repair, 28 held for manual classification, 16 labeled `keep_aside_misc`; 3 blank/off-domain hard-delete candidates removed. Classification never activates a record on its own.
- `next_phase4_topic` now treats `quarantine_pending` as an incomplete concept; the overnight runner triages quarantined records for the selected topic/concept before repair/population, using a scope-audit -> repair -> populate -> recheck loop, local-model-only for long runs.
- Stored lesson prebuild reached 100%: all 58 syllabus concepts have validated, exam-audited lesson artifacts in `certcoach_db.lesson_artifacts`. 39 are also exported as markdown under `memory/lessons/` (Topics 3-10); Topics 1-2 remain Mongo-only; Topics 11-12 local exports pending via `scripts/enhance_all_lessons.py`. The builder sanitizes out-of-scope transactions, sharding config, BSON method leaks, and JS cursor helpers (`.forEach`) before saving.
- Added bulk lesson-enhancement infrastructure (`scripts/enhance_all_lessons.py`): runs all 58 concepts in canonical order, skips already-generated files, feeds real exam question stems into the prompt, 10s delay between calls, supports the NVIDIA API (`NVIDIA_API_KEY`) with fallback to `openrouter:openrouter/free`.
- Topic 1 (`BSON Data Types`, `Document structure`, `Collections vs Tables`) complete under the stricter no-future-topic lesson rule; validator now hard-fails on future-topic methods, query language, projection, dot notation, Atlas/platform references, and misc concept leakage.
- Regression coverage added for: report-selector backlog-scope fix, scope-audit future-scope quarantine routing, Topic 2 stem guard, Topic 3 `findOne()`/`countDocuments()` repair checklist, stricter Topic 1 lesson validator, lesson-repair prompt path, and missing/leaky-section lesson fallback. Maintained unit suite: 165 passing.
- Repo audit pass: fixed a hardcoded Zhipu API key in `src/scripts/utils/image_ingester.py` (now reads `ZHIPU_API_KEY`), untracked `user_profiles.json`/`user_attempts.json`/`pics_qa/`/`scratch/` from git (were tracked despite matching `.gitignore` rules added after the fact), regenerated `requirements.txt` in UTF-8 to mirror `pyproject.toml` instead of a 140-package `pip freeze` dump, fixed a stale `mongodbcret`-path reference in `scripts/extract_pdf.py`, and added `[tool.pytest.ini_options] testpaths = ["tests/unit"]` so bare `pytest` no longer risks collecting `scratch/test_zhipu_vision.py`.

## 2026-07-04 (approximate; reconstructed 2026-07-05, never logged when it happened)
- A provenance/trust system was implemented on top of the existing content-contract lifecycle: every question now carries `provenance.state` in `draft -> sourced -> confirmed/suspect`, and `database.is_practice_ready()` requires both `is_contract_active()` and `is_confirmed()`. See [[decision_log|Decision Log]] 2026-07-04 for the full backfilled decision record.
- Added: deterministic citation verification (`database.verify_citation`), a self-consistency check separate from fact-checking (`nightly_seed_questions.run_self_consistency_check`), a one-at-a-time human review screen (`certcoach-review-questions`), multi-response ("select all that apply") question support end-to-end, domain-weighted mock selection matching real exam weights, wrong-attempt remediation (citation + domain-matched flashcards, stateless), domain/concept accuracy dashboards, a flashcard browser in the CLI, and a screenshot-sourced-question cleanup pipeline (`reocr_pics_qa` -> `recover_screenshot_citations` -> `purge_screenshot_backlog`, plus `analyze_backlog`/`backfill_provenance`).
- `backfill_provenance` and `backfill_provenance --suspect-uncited` were run against the live `certcoach_db`, backed up first (`backups/questions-20260704T*`). This is why the bank went from ~516 total records (per the 2026-07-03 snapshot) to 377, with 376 landing in `suspect` because their citation quote was empty by construction (legacy generation never recorded a verbatim quote, only a filename/title/URL hint).
- None of this was committed to git or recorded in `memory/agent_context.md` / `memory/session_handoff.md` at the time -- it sat undiscovered in the working tree until the next session started and found the memory docs badly out of sync with `git status` and the live DB.

## 2026-07-05
- Reconstructed the undocumented provenance system above from the working-tree diff and live DB state; updated `agent_context.md`, `session_handoff.md`, and `decision_log.md` to reflect it.
- Ran `reocr_pics_qa` to completion: 69/69 `pics_qa/` screenshots transcribed with `glm-ocr:latest` (66 new, 3 already done, 0 failures).
- Fixed `analyze_backlog.py`'s `_has_real_doc_lead()`: it only matched `citation_source` against a literal filename in `cleaned_markdowns/`, but legacy questions store `citation_source` as a title or URL, never a real filename, so it always returned `False` for the legacy backlog. Added a topic-level fallback; updated 3 tests that encoded the old behavior, added 1 new test. 239/239 tests pass.
- Re-ran `analyze_backlog`: of 376 suspect questions, 353 have a real regeneration lead (topic has official docs), 23 (`topic_id: None`) have none, 0 are duplicates.
- Ran `recover_screenshot_citations` against the true screenshot-sourced count (26, not the ~333 assumed in the job docstrings -- most suspect records are legacy-generated, not screenshot-sourced): 1 recovered to `sourced`, 25 confirmed unrecoverable.
- Live bank state at session end: 377 total, 0 confirmed, 1 sourced, 375 suspect. Practice/mocks have zero usable inventory until questions are confirmed via the review screen. All provenance-system code remains uncommitted.

## 2026-07-06
- Removed `scratch/` (24 unreferenced debug scripts) and dropped a drafted-then-abandoned `inspect_doc.py` after redirecting toward the simplest working loop: doc -> generate -> verify -> review -> practice.
- Proved that loop end-to-end on real data (Topic 1 BSON Data Types), fixing 4 real bugs surfaced in the process: a deficit calculator blind to the provenance gate, a citation checker that rejected verbatim quotes over markdown backticks, a self-consistency model (`deepseek-r1:8b`) that reasoned for 14,000+ characters without ever answering (replaced with `qwen2.5-coder:7b`, benchmarked against 4 alternatives first), and a doc-scoring function that couldn't match bare `$`-operator concepts to their own reference docs.
- Improved `review_questions.py`: full seven-part explanation now renders (was truncated at 800 chars), source filename is a clickable local-file link, and the redundant/buggy "Source excerpt" preview was removed.
- Built [[study_order_map|Study Order Map]]: all 58 syllabus concepts mapped to their official doc(s) in canonical order, using the corrected doc-scoring logic. See [[decision_log|Decision Log]] 2026-07-06 for full reasoning on every fix.
- Unit suite: 241 passing. Everything from this session and the prior undocumented one remains uncommitted.

## 2026-07-06 (continued, session 2)
- Session started by re-verifying live state rather than trusting the prior handoff: working tree was unchanged, but the live DB had moved -- the user confirmed 2 of the 4 `sourced` questions independently via `certcoach-review-questions`, and total question count ticked up from 377 to 379.
- Built `certcoach-map-questions-to-docs` (`src/certcoach/jobs/map_questions_to_docs.py`), a read-only report mapping every question to its syllabus topic/concept and official doc(s), reusing `map_questions.find_best_concept()` for topic-id-less records and the same doc-scoring logic behind [[study_order_map|Study Order Map]]. Added entry point + 8 unit tests. Explicitly no DB writes, per the user's choice among three offered options -- see [[decision_log|Decision Log]] 2026-07-06.
- Live results: 356/379 questions had stored topic/concept, 23 orphaned records were placed via inference; 238 resolve to a concept-exact doc, 118 fall back to topic-level docs, 23 have no topic to resolve against; 333/379 have citation drift (recorded citation isn't a real official doc filename). Full per-question CSV written to a scratch path, not committed.
- Unit suite: 249 passing. Nothing from any of the three accumulated sessions is committed yet.
