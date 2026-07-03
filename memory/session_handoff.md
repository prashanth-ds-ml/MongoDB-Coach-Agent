# Session Handoff

Last updated: 2026-07-03

Related: [[Memory Home]], [[agent_context|Agent Context]], [[next_steps|Next Steps]], [[canonical_state_flow|Canonical State Flow]], [[preparation_tool_gap_assessment|Preparation Tool Gap Assessment]]

## Current State

- Phase: Phase 4 live question-bank operations.
- Status: **Repair and population now run in a scope-audit -> repair -> populate -> recheck loop, and future-scope leaks are quarantined before learner-facing use.**
- Durable loop rule: continue the canonical syllabus order across sessions, one question at a time, and do not advance to the next topic/concept until the selector shows the current backlog is clear.
- Reporting rule: every session should begin by stating the active topic/concept and the current counts for repair pending, quarantined total, quarantined repairable, hard-delete candidates, and population missing Easy/Medium, scoped only to that active topic/concept.
- Quarantine triage: 3 hard-delete candidates were removed; MongoDB-aligned quarantined items were left for remap or repair.
- Operating rule: repair-pending and quarantined records are now handled by exact `topic_id + concept` in canonical order, using the same loop.
- Benchmark integration: official docs + reference repo remain combined into topic benchmark records, and weak-focus context is still injected ahead of full docs.
- Current ordered target: Topic 4 -> `$unset`.
- Current Topic 3 state: Topic 3 is closed from the selector perspective; all six concepts are study-ready and the selector has advanced to Topic 4.
- Current Topic 4 state: `replaceOne()`, `updateOne()`, `updateMany()`, `$set`, `$push`, and `$inc` are all study-ready and populated at `6 Easy + 5 Medium`, `3 Easy + 2 Medium`, `3 Easy + 2 Medium`, `3 Easy + 2 Medium`, `3 Easy + 2 Medium`, and `3 Easy + 2 Medium` respectively. The next ordered target is `$unset`.
- Current bank snapshot after the latest pass: Topic 4 `replaceOne()` has `6` active Easy, `5` active Medium, and `3` quarantined records. Topic 4 `updateOne()` has `3` active Easy, `2` active Medium. Topic 4 `updateMany()` has `3` active Easy, `2` active Medium. Topic 4 `$set` has `3` active Easy, `2` active Medium. Topic 4 `$push` has `3` active Easy, `2` active Medium. Topic 4 `$inc` has `3` active Easy, `2` active Medium, with `1` repair-pending record still awaiting cleanup.
- Bank-wide quarantine triage snapshot: 163 quarantined records remain. `120` are high-confidence canonical mappings pending repair, `27` need manual classification, and `16` are explicitly kept aside as misc. One reviewed record was remapped to Topic 1 `Document structure`, validated, duplicate-checked, and promoted.
- Loop update: `next_phase4_topic` now treats `quarantine_pending` as an incomplete concept, and the overnight runner now triages quarantined records for the selected topic/concept before running explanation repair and population.
- Current reporting template for the loop: `Topic X | Concept Y | repair pending N | quarantined total N | quarantined repairable N | hard-delete candidates N | population missing Easy N, Medium N`, where every count refers only to that topic/concept.
- Current Topic 4 execution note: the overnight runner now enforces a local-only model chain for long repair/population runs so it does not waste time on dead remote fallbacks.
- Learner-facing template note: the new `study_pattern_guardrails.md` file defines the micro-challenge as question-only and keeps lesson examples inside the active concept boundary.
- Lesson prebuild pipeline is now scaffolded: `certcoach-prebuild-lesson` stores concept-scoped lesson artifacts in MongoDB, `certcoach.core.lesson_bank` validates the six-section lesson contract, and the CLI now prefers validated stored lessons before live generation.
- First live lesson-prebuild target was Topic 1 `BSON Data Types`, following the canonical lesson order rather than the active Phase 4 question-bank selector.
- The `BSON Data Types` lesson loop is now complete end-to-end: the local Ollama pipeline produced a validated stored lesson after the fallback path filled missing lesson sections one-by-one.
- Lesson prebuild retry behavior now preserves the better draft when the corrective rewrite attempt degrades the lesson further, and the section-by-section fallback is the durable recovery path when the full lesson prompt is incomplete.
- The `BSON Data Types` practice audit is also complete: 12 mis-mapped active questions were remapped to nearby Topic 1 concepts and 11 bad or out-of-scope records were quarantined before the readiness recheck.
- Current `BSON Data Types` active inventory after cleanup: `9 Easy`, `11 Medium`, `0 Hard`. The concept remains comfortably above the required `3 Easy + 2 Medium` readiness gate with a cleaner lesson-aligned practice pool.
- Topic 1 `Document structure` now also passes the full lesson loop under the stricter no-future-topic rule. The lesson had initially leaked `findOne()`, `insertOne()`, dot notation, projection, and query language; the validator, section-regeneration path, and concept-specific scrub now remove those leaks before the lesson can become `validated`.
- Topic 1 `Document structure` practice cleanup remains in place and the current active inventory is `4 Easy`, `5 Medium`, `0 Hard`, with the concept still above the required readiness gate.
- Topic 1 `Collections vs Tables` has been re-run under the stricter Topic 1 validator and is now `validated` without `insertOne()` or CRUD/write-flow leakage. Its active practice pool remains comfortably above readiness at `12 Easy`, `10 Medium`, `3 Hard` after the earlier Atlas/platform leak quarantine.
- Topic 1 is now complete across all three concepts under the stricter lesson boundary: exact concept only, no future-topic methods, no misc filler, and concept-local practice cleanup where needed.
- Current Topic 2 state: `insertOne()`, `insertMany()`, and `_id and ObjectId` now have separated concept buckets; Topic 2 backlog is cleared, and the final generic CRUD stem was quarantined.
- Current Topic 2 execution: `scripts/run_phase4_overnight.ps1` now supports `-RepeatUntilClean` plus scope-audit routing so the same runner can keep draining each concept until the topic is clean or the max-cycle cap is reached.
- Current repair behavior: `question_bank_comparison_report` counts stored backlog by stable `topic_id + concept` scope, including legacy hard-difficulty records that were previously invisible to the selector; `migrate_question()` still distinguishes explanation repair from question regeneration, `next_phase4_topic` treats both as incomplete, and `validate_question_quality()` now rejects Topic 2 `_id and ObjectId` stems that do not explicitly mention `_id` or `ObjectId`.
- Focused verification: `tests/unit/test_question_bank_comparison_report.py`, `tests/unit/test_mark_scope_leaks.py`, and the new Topic 2 stem-guard regression in `tests/unit/test_nightly_seed_questions.py` passed after the selector and scope-audit fixes.
- Focused verification: the unit suite now includes stricter Topic 1 lesson-scope coverage in `tests/unit/test_lesson_bank.py`; `.\.venv\Scripts\python.exe -m pytest tests\unit -q` now passes with `164 passed`.

## Latest Decisions (2026-06-17)

1. **Model chain with quality gates** — Primary `gemma4:12b` (local Ollama), then OpenRouter and Cloudflare fallback via configured chain. No additional local models needed.
2. **Quality pipeline**: Deterministic checks -> Duplicate check -> LLM Judge (RAG-grounded) -> Retry with fix hint -> Fallback model -> Log everything.
3. **Structured logging** — JSONL per attempt to `logs/model_quality.jsonl` with verdict, flags, latency, tokens, model.
4. **Circuit breaker** — Per-model failure tracking prevents repeated calls to degraded models.
5. **Source tracking requirement** — Each generated question must store `source_files` metadata for RAG judge verification.
6. **Local-first fallback** — Ollama `gemma4:12b` is tried before OpenRouter `gpt-oss-120b`/`gpt-oss-20b` and Cloudflare `@cf/meta/llama-3.3-70b-instruct`.
7. **Direct HTTP adapters** — `model_runner.py` uses direct HTTP for OpenRouter and Cloudflare Workers AI, so missing optional LangChain provider packages no longer block repair/population runs.
8. **Population contract split** — Question generation uses string options plus `correct_answer`; repair generation uses the seven-part explanation schema.
9. **Shell-mode population** — Population now uses a lean `question_shell` contract, inserts the shell as `needs_explanation_repair`, then immediately hands it to the repair job so the stored record becomes active in the same pass when repair succeeds.
10. **Repair metadata fix** — `apply_repair()` now writes the content-contract metadata under `metadata.*`, so repaired shells correctly become active records.
11. **Scope-audit loop** — `mark_scope_leaks` now runs before and after repair/population, quarantining future-scope records instead of letting them leak into practice.
12. **Topic 2 stem guard** — `validate_question_quality()` now rejects `_id and ObjectId` questions that do not explicitly mention `_id` or `ObjectId`, and malformed stems are quarantined instead of staying learner-facing.
13. **Ollama JSON mode** — Local Ollama generation now requests `format="json"` through both the LangChain and direct HTTP adapters.

## Completed This Session (2026-07-03)

1. **Implemented `scripts/enhance_all_lessons.py`** — Bulk lesson enhancer that iterates all 58 syllabus concepts in canonical order, checks if a local markdown export already exists (skip-if-present), and calls `enhance_single_concept()` with a 10-second delay between API requests to avoid rate-limiting.
2. **Implemented `scripts/enhance_lesson_llm.py` NVIDIA/OpenRouter routing** — `get_model_runner()` now detects `NVIDIA_API_KEY` env var and routes to `nvidia:meta/llama-3.1-70b-instruct`; otherwise falls back to `openrouter:openrouter/free`.
3. **Fixed NVIDIA API key variable name in `.env`** — The repo-local `.env` previously stored the NVIDIA key under the raw name `nvidia`; both the enhancer and `model_runner.py` now accept either `NVIDIA_API_KEY` or `nvidia` for backward compat.
4. **Added skip-if-already-enhanced logic** — Script now checks `memory/lessons/topic_NN_<concept_snake>.md` on disk before calling the LLM, so partial runs resume cleanly without re-processing completed concepts.
5. **Produced 39 high-quality local lesson markdown files** covering Topics 3–10 (39 concepts) in `memory/lessons/`. Topics 1–2 lessons remain stored directly in MongoDB (`lesson_artifacts` collection) from the prior session.
6. **Topics fully enhanced this session:**
   - **Topic 3** (Read): `find()`, `findOne()`, `Projections`, `Cursors`, `sort/limit/skip`, `countDocuments()`
   - **Topic 4** (Update): `replaceOne()`, `updateOne()`, `updateMany()`, `$set`, `$push`, `$inc`, `$unset`, `upsert`, `findAndModify()`
   - **Topic 5** (Delete): `deleteOne()`, `deleteMany()`
   - **Topic 6** (Query Operators): Comparison (`$eq/$gt/$lt/$in/$nin`), Logical (`$and/$or/$not/$nor`), Element (`$exists/$type`), Atlas Search Query Basics
   - **Topic 7** (Arrays & Embedded): `$elemMatch`, Dot Notation, Array Size Queries
   - **Topic 8** (Aggregation): `$match`, `$group`, `$project`, `$sort`, `$limit`, `$lookup`, `$unwind`, `$addFields`, `$out`
   - **Topic 9** (Indexes): Single-Field, Compound, Multikey, `explain()`, `collscan vs ixscan`, Atlas Search Indexes
   - **Topic 10** (Data Modeling): `embedding vs referencing`

## Next Action

Continue with Topics 11 and 12 lesson enhancement (remaining concepts not yet in `memory/lessons/`). Then resume Phase 4 question-bank population starting at Topic 4 `$unset` (current selector target).

## Recent Note

## Recent Note

- **Bulk lesson enhancement complete for Topics 3–10**: 39 enhanced lesson markdown files are now in `memory/lessons/`. Topics 1–2 lessons are stored in MongoDB `lesson_artifacts` from the prior session.
- `scripts/enhance_all_lessons.py` now skips already-generated files; safe to re-run at any time to resume from where a rate-limited run stopped.
- NVIDIA API key env var is `NVIDIA_API_KEY` (canonical); the legacy bare `nvidia` var is still accepted in `model_runner.py` and `enhance_all_lessons.py` for backward compat.
- Topics 11 and 12 lesson markdown exports are the remaining gap; they can be enhanced in the next session using the same script.
- Phase 4 question-bank selector target remains `Topic 4 → $unset`. Resume there before advancing to later topics.
- Stored-lesson runtime is read-first: if a validated concept lesson exists in `lesson_artifacts`, the CLI uses it; otherwise it falls back to live generation.
- Lesson prebuild pipeline is 100% complete in MongoDB. The local `memory/lessons/` export is a convenience cache for agent context and offline review.

## Known Blockers

- 50 concepts not study-ready (need Phase 4 question-bank population)
- Plain `pytest` collects `scratch/test_zhipu_vision.py` (optional `zhipuai`)
- Phase 5 full study-flow and mixed-mock smoke tests remain manual

## Commands

```powershell
# Preview next concept
.\.venv\Scripts\python.exe -m certcoach.jobs.next_phase4_topic

# Run overnight batch (current)
.\scripts\run_phase4_overnight.ps1 -RepairBatchSize 25 -PopulationBatchSize 25

# Run unit tests
.\.venv\Scripts\python.exe -m pytest tests\unit -q
```
