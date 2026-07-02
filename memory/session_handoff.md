# Session Handoff

Last updated: 2026-07-02

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

## Completed This Session

1. **Implemented `model_runner.py`** — `generate_with_quality_gate()`, `call_model()` (Ollama/Cloudflare/OpenRouter), `deterministic_checks()`, `check_duplicate()` (stem hash), `log_attempt()` JSONL, `ModelCircuitBreaker` class.
2. **Implemented `judge_questions.py`** — RAG-grounded judge with source file verification, context grounding, explanation structure validation, Topic 1 invented-type guard.
3. **Wired quality gates into `nightly_seed_questions.py` and `repair_explanations.py`** — Replaced direct LLM calls with `model_runner.generate_with_quality_gate()`.
4. **Added `source_files` tracking to `database.save_generated_question()`** — Metadata field for judge verification.
5. **Configured local-first model chains** — Ollama `gemma4:12b` is prepended automatically, then OpenRouter `gpt-oss-120b`/`20b`, then Cloudflare fallback.
6. **Patched HTTP providers** — Direct HTTP calls for OpenRouter/Cloudflare, normalized chat outputs to text before JSON parsing.
7. **Added regression coverage** — Verified OpenRouter path succeeds with mocked HTTP response.
8. **Split population and repair contracts** — Population now validates string options plus `correct_answer`; repair validates the seven-part explanation schema.
9. **Built the combined benchmark layer** — Added schema, ordered index, and topic records for all 12 syllabus topics.
10. **Integrated weak-focus priority** — Lesson, population, and repair prompts now see weak-focus benchmark text before the full benchmark record and official docs.
11. **Split population into shell + immediate repair** — Population now uses `response_kind="question_shell"`, validates only the MCQ shell, inserts a repair-pending shell, and hands it to `repair_explanations` in the same pass.
12. **Verified Topic 1 progress** — Two new `Collections vs Tables` records were inserted and repaired successfully; the remaining Topic 1 backlog was reclassified into explanation repair versus question regeneration.
13. **Normalized repaired shells** — Existing `Collections vs Tables` shells were updated to `generated` after the `apply_repair()` metadata fix, bringing Topic 1 to 17/17 active.
14. **Restored Topic 1 ordering** — `next_phase4_topic` now uses the stored repair backlog, so Topic 1 `BSON Data Types` is once again the next ordered concept ahead of Topic 2.
15. **Separated repair from regeneration** — `migrate_question()` now returns `repair` for explanation-only fixes and `regenerate` for structurally bad or Topic 1-rescued records, with a new `needs_question_regeneration` status.
16. **Advanced Topic 4 `replaceOne()` readiness** — Repaired and promoted one quarantined Medium record after replacing ambiguous/future-scope distractors and rewriting its seven-part explanation. The concept is now study-ready at `5 Easy + 2 Medium`.
17. **Verified the current implementation** — Ollama JSON-mode focused tests passed (`6 passed`), and the full unit suite passed (`142 passed`, one existing deprecation warning).
18. **Added controlled quarantine triage** — `triage_quarantined_questions` weights the stem and correct answer over distractors, records evidence/confidence, remaps only high-confidence records, and leaves every classified record quarantined until separate review.
19. **Applied bank-wide triage after backup** — Backup `questions-20260620T173713Z` contains 516 records with SHA-256 `612f2d7f607f77d7d544b85d35a9851eac8418f0315d9a14f5da6b4bdd2e3a07`.
20. **Promoted the first reviewed quarantine** — Record `1044291f-4aa4-4bf8-8d60-619a0580d062` was semantically remapped from `BSON Data Types` to Topic 1 `Document structure`, passed validation, had no exact duplicate, and was activated.
21. **Verified quarantine changes** — Full unit suite passes (`147 passed`, one existing deprecation warning).

## Next Action

Session closed after documenting the current state.
Resume at Topic 4 `$unset` if work continues.

## Recent Note

- Topic 2 concept buckets are now separated into `insertOne()`, `insertMany()`, and `_id and ObjectId`.
- Quarantined records were triaged conservatively: only blank/off-domain records were hard-deleted, while MongoDB concepts with missing scope stay in the remap/repair pipeline.
- Repair-pending and quarantined backlog should be sorted by exact topic/concept before any delete, remap, repair, or rerun decision.
- The selector now points to Topic 2 `_id and ObjectId`, and the generator has a variation brief for `insertMany()` while the validator guards against malformed `_id and ObjectId` stems.
- Scope leaks are being quarantined rather than left as learner-facing content.
- The population shell contract is stable; the scope-audit loop is now part of the standard runner path.
- Topic 3 `findOne()` and `countDocuments()` repair checklist regressions are pinned, and the runner changes now favor local-only generation for long overnight loops.
- Resume point is now Topic 4 `$inc`, which reached readiness during this session; continue with the next ordered concept on the following run.
- The study-pattern guardrail note is now linked from Memory Home and should be used as the reference for lesson and micro-challenge formatting.
- Stored-lesson runtime is now read-first: if a validated concept lesson exists in `lesson_artifacts`, the CLI uses it; otherwise it falls back to live generation.
- The registered durable lesson loop is now: `build source bundle -> generate lesson -> validate -> repair or fill missing sections -> validate -> store -> audit active concept questions -> remap/quarantine out-of-scope items -> recheck readiness -> move to next concept`.
- Topic 1 no longer has a lesson-prebuild blocker. The next lesson target is Topic 2 `insertOne()`.

## Known Blockers

- 50 concepts not study-ready (need Phase 4 batches)
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
