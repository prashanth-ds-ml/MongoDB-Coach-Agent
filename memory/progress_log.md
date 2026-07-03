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
