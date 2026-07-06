# Next Steps: Study-Readiness Build Order

Related: [[Memory Home]], [[active_context|Active Context]], [[decision_log|Decision Log]], [[preparation_tool_gap_assessment|Preparation Tool Gap Assessment]]

The project is not frozen yet. Complete and review one phase at a time. Do not run live-bank repair, migration, or population early.

---

## Current Phase (as of 2026-07-05): Provenance/Trust Rollout

This supersedes the Phase 4 narrative below as the active work, though Phase 4's content-contract lifecycle rules still apply underneath it. See [[agent_context|Agent Context]] and [[session_handoff|Session Handoff]] for full current state; see [[decision_log|Decision Log]] 2026-07-04/2026-07-05/2026-07-06 for the design decisions. Short version: every question now needs `provenance.state == "confirmed"` (human-reviewed) in addition to the old content-contract `active` status before it reaches practice/mocks. The live bank currently has only 2 confirmed questions (one concept). Immediate order: resolve the screenshot/legacy suspect backlog (`analyze_backlog`, `certcoach-map-questions-to-docs` for topic/doc/citation-drift triage, `recover_screenshot_citations`, `purge_screenshot_backlog`), then keep confirming inventory via `certcoach-review-questions`, then resume Phase 4 population/lessons below.

## Historical Phase 4 Narrative (superseded by the provenance gate above, kept for context)

Completed daytime operations:

- Created and verified a pre-migration backup of 351 records.
- Applied deterministic migration: 69 active, 216 pending explanation repair, and 66 quarantined.
- Created and verified a post-migration backup of 351 records.
- Prepared and validated `scripts/run_phase4_overnight.ps1`.
- Restricted explanation repair to records explicitly marked `needs_explanation_repair`.
- Made the overnight runner automatically select the first concept with pending repairs or inventory below the configured target, in canonical syllabus order.
- Aligned repair and population filters with exact canonical topic IDs so Topic 1 cannot touch or count Topics 10-12.
- **Implemented quality gates**: `model_runner.py` + `judge_questions.py` with local-first multi-provider fallback (local Ollama, OpenRouter gpt-oss-120b/20b, Cloudflare Llama 3.3 70B).
- **Wired quality gates into population and repair jobs** — replaced direct LLM calls.
- **Added `source_files` tracking** to `database.save_generated_question()` for judge verification.
- **Patched HTTP providers** — direct HTTP for OpenRouter/Cloudflare, normalized chat outputs.

Recovery points:

- Pre-migration: `backups/questions-20260612T025926Z`, SHA-256 `2f9917d39642ba92b6271c0b1582d4645175a3035b52340d4dad848aabc37a10`.
- Post-migration: `backups/questions-20260612T030150Z`, SHA-256 `b59305bda240841a14de8be2fb57d815d9d07456f0e61bcd2247b6cdeaa196f1`.

Current live snapshot:

- 400 total records.
- Topic 2 concepts are now split into `insertOne()`, `insertMany()`, and `_id and ObjectId`.
- Topic 2 backlog is complete and the selector has advanced to Topic 4 `replaceOne()`.
- The `question_shell` population contract is live, and successful shells are repaired immediately in the same run.
- The scope-audit loop now quarantines future-scope leaks before learner-facing use.
- The overnight runner now supports `-SingleQuestion` mode so repair and population can be forced to one record at a time when a concept is failing batch-level quality gates.
- The remaining work is to continue in canonical order and keep Topic 4 focused on the concepts that still have inventory gaps.
- Lesson prebuild and quality audit are 100% complete: all 58 syllabus concepts have prebuilt, validated, and exam-level audited lessons stored in MongoDB (`certcoach_db.lesson_artifacts`) with automatic sanitization of out-of-scope topics.
- The learner-facing study pattern is now captured in `memory/study_pattern_guardrails.md`: keep the micro-challenge question-only and keep lesson examples inside the active concept boundary.
- Resume point: continue Topic 4 from `replaceOne()` and do not skip to `updateOne()` until the selector advances.

Next operation: continue from the selector's current target and keep the repair/populate loop scoped to the exact concept.

Current sequential target: Topic 4, `CRUD Operations - Update` -> `replaceOne()`.

The complete release-blocker checklist and final-freeze standard are documented in `memory/preparation_tool_gap_assessment.md`.

## Approved Build Order

### Phase 1 - Repository and Model Configuration
- Separate study, population, and repair model configuration.
- Use `gemma4:12b` for question population and explanation repair.
- Use a fast model suitable for the 16 GB RAM / 6 GB VRAM minimum for study.
- Clean generated/runtime files from Git and create a recoverable checkpoint.

### Phase 2 - Study-Critical Runtime
- Bound lesson context to the active concept.
- Schedule only concepts with enough active questions.
- Require exactly five served questions and at least four correct before concept completion.
- Handle insufficient-question concepts explicitly.

### Phase 3 - Question-Bank Lifecycle
- Replace fixed-total deficits with concept-readiness reporting.
- Treat `3 Easy + 2 Medium` as the readiness gate while continuing ordered population toward configurable per-concept inventory targets.
- Distinguish active, needs-explanation-repair, and quarantined records.
- Count only active questions for practice readiness.
- Correct migration classification before live-bank writes.

### Phase 4 - Content Benchmark Integration
- Build a combined benchmark from the official MongoDB docs in this repo and `yixin0829/mongodb-dev-cert-prep`.
- Create a source-coverage matrix that maps local topics and subtopics to official sections and reference objectives.
- Tag each concept with authoritative source files, objective wording, example patterns, and exam traps.
- Use the combined benchmark to improve lesson prompts, question population, and explanation repair.
- Preserve CertCoach's workflow, readiness gates, and lifecycle rules unchanged.
- Start with Topic 1 and expand only after the first benchmark record is validated.
- Topic 1 is now recorded; Topic 2 is the next benchmark record in order.
- Topics 1 through 12 now have benchmark records; the remaining work is wiring the benchmark into prompts and validation.
- The benchmark layer is now wired in; the next tuning step is weak-focus prioritization and throughput stabilization.
- The scope-audit loop is now part of the runner: quarantine future-scope leaks before repair/population and recheck after each pass.
- Topic 2 concept tagging was corrected by the bank-wide remap, the `insertMany()` prompt now includes a concept-specific variation brief so the generator does not keep producing the same return-type question, and the `_id and ObjectId` validator now rejects stems that do not explicitly mention `_id` or `ObjectId`.

### Phase 5 - Live Database Operations
- Back up the `questions` collection.
- Apply mapping and corrected migration.
- Repair explanations in controlled batches with quality gates.
- Current live focus is Topic 4, starting with `replaceOne()`; the selector now honors the stored repair backlog by exact `topic_id + concept` scope.
- Use the study-pattern guardrails when drafting lessons or micro-challenges so later-topic material does not leak into the active concept.
- Treat structurally salvageable records as `needs_question_regeneration` instead of forcing them into explanation repair.
- Recalculate concept and difficulty deficits after migration and repair.
- Populate concepts toward the configured inventory target even after they become study-ready.
- Populate beyond readiness toward the configured inventory target and allow explicit Easy/Medium extras beyond it.
- **Quality gates**: Deterministic checks → Duplicate (stem hash) → LLM Judge (RAG-grounded) → Retry → Fallback model → Log.
- **Multi-provider chain**: Local Ollama → OpenRouter gpt-oss-120b/20b → Cloudflare Llama 3.3 70B.
- Canonical state flow is documented in [[canonical_state_flow|Canonical State Flow]] and should be treated as the routing rule for repair/regeneration/legacy decisions.

### Phase 6 - Smoke Test and Freeze
- Verify one full study flow and one timed mixed mock.
- Verify MongoDB persistence and insufficient-question behavior.
- Run the full automated suite.
- Declare the feature freeze and begin daily exam preparation.
