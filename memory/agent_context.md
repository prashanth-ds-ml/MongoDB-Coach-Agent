# Agent Context

Last verified: 2026-07-02

## Mission

CertCoach prepares the learner for the MongoDB Associate Python Developer certification through concept-scoped lessons, validated retrieval practice, persisted progress, and mixed mocks.

## Current Phase

Phase 4 live question-bank operations with quality-gated model chain. Application foundation implemented; content readiness and Phase 5 verification block final freeze.

## Required Product Path

```text
daily agenda -> concept lesson -> scoped Q&A -> five-question practice
-> answer review -> persisted progress -> mixed mock
```

## Non-Negotiable Rules

- MongoDB collection `certcoach_db.questions` is the question-bank source of truth.
- Practice readiness requires active, directly mapped questions: exactly `3 Easy + 2 Medium`.
- Passing a concept requires at least `4/5`.
- Population may continue beyond readiness toward configurable inventory targets, default `5 Easy + 5 Medium`.
- Repair/population processing follows canonical syllabus topic and concept order.
- The live loop is persistent across sessions: select the next incomplete `topic_id + concept`, work exactly one question at a time, repair or quarantine every record before learner-facing use, then recheck the selector before advancing.
- Every session must surface the current work packet before action, scoped only to the active topic and concept: current topic, current concept, repair-pending count, quarantined count, quarantined-repairable count, hard-delete candidates, and remaining population deficit by Easy/Medium.
- For the live loop, treat quarantined records as a triage bucket: repairable quarantine stays in the concept loop, while only clearly unrecoverable/off-domain records are eligible for deletion.
- Legacy, repair-pending, and quarantined records cannot enter learner-facing practice.
- Long repair/population runs use `scripts/run_phase4_overnight.ps1`.
- Optional UI, analytics, gamification, simulator, and general platform work are deferred until after the exam.

## Live Snapshot

- Documentation coverage: 12/12 topics.
- Concepts: 58 total, 8 study-ready, 50 blocked.
- Question lifecycle: 516 total records.
- Current ordered target: Topic 4 -> `$unset`.
- Topic 3 is complete from the selector perspective; the `find()`, `findOne()`, `Projections`, `Cursors`, `sort/limit/skip`, and `countDocuments()` concepts are all study-ready and the selector has advanced to Topic 4.
- Topic 4 now carries the next repair/population backlog. `replaceOne()` is fully populated at `6 Easy + 5 Medium`, `updateOne()` is study-ready at `3 Easy + 2 Medium`, `updateMany()` is study-ready at `3 Easy + 2 Medium`, `$set` is study-ready at `3 Easy + 2 Medium`, `$push` is study-ready at `3 Easy + 2 Medium`, and `$inc` is study-ready at `3 Easy + 2 Medium`; the ordered target has advanced to `$unset`.
- Topic 2 counts remain split into `insertOne()`, `insertMany()`, and `_id and ObjectId`, with the Topic 2 backlog cleared and the final generic CRUD stem quarantined.
- Quarantine triage removed 3 blank/off-domain hard-delete candidates; the remaining quarantined items are still being split between remap and repair.
- Bank-wide quarantine triage is now explicit: 121 records are canonically mapped and pending repair, 28 are held for manual classification, and 16 are labeled `keep_aside_misc`. Classification never activates a record.
- Loop correction: `quarantine_pending` now keeps a concept incomplete in `next_phase4_topic`, and the overnight runner triages quarantined records for the selected topic/concept before explanation repair and population.
- Repeat-until-clean runner mode applies a scope-audit -> repair -> populate -> recheck loop per concept, and the overnight runner now enforces a local-only model chain for long repair/populate runs to avoid dead remote fallback delays.
- The durable bank-maintenance loop is now: `selector -> exact concept -> one question -> validate/repair/quarantine -> recheck selector -> repeat`, and it must continue across sessions until all topic/concept backlogs are cleared.
- Reporting rule: always show the active topic/concept plus `repair pending`, `quarantined total`, `quarantined repairable`, `hard-delete candidates`, and `population missing Easy/Medium` for that same topic/concept before deciding the next single-question pass.
- Learner-facing lesson pattern is now documented in `memory/study_pattern_guardrails.md`: one concept, one micro-challenge question only, no answer/hint/example response, and no future-topic leakage.
- Stored lesson prebuild is now operational: lesson artifacts are saved per exact `topic_id + concept`, the CLI prefers validated stored lessons before live generation, and Topic 1 `BSON Data Types` is now the first validated concept lesson.
- The registered durable lesson loop is: `source bundle -> lesson draft -> validation -> targeted repair -> missing-section generation -> validation -> stored lesson -> concept-local practice audit -> remap/quarantine misaligned questions -> readiness recheck`.
- Topic 1 is now complete across all three concepts under the stricter no-future-topic lesson rule: `BSON Data Types`, `Document structure`, and `Collections vs Tables` each have validated stored lessons, and the concept-local practice pools were cleaned where needed.
- Topic 1 lesson validation is now stricter by design: future-topic methods, query language, projection, dot notation, Atlas/platform references, and misc concept leakage are treated as validation failures, not tolerated as style issues.
- Maintained regression coverage: report selector regression passed after the backlog-scope fix, scope-audit routing quarantines future-scope leaks, the Topic 2 stem guard has a focused unit test, and Topic 3 `findOne()` / `countDocuments()` repair-checklist regressions are pinned.
- Maintained regression coverage also includes the stricter Topic 1 lesson validator, lesson-repair prompt path, and missing-section/leaky-section lesson fallback; the focused unit suite currently passes at `158 passed`.
- Known repository-wide test blocker: plain `pytest` collects `scratch/test_zhipu_vision.py`, which requires optional `zhipuai`.

## New Infrastructure (2026-06-17)

- **Model chain config** in `config.py`: `get_population_model_chain()`, `get_repair_model_chain()`, judge config.
- **Providers**: Local `gemma4:12b` (first pass), OpenRouter, Cloudflare Workers AI (fallback).
- **Quality pipeline implemented**: Deterministic checks -> Duplicate (stem hash) -> LLM Judge (RAG-grounded) -> Retry -> Fallback.
- **Logging**: JSONL to `logs/model_quality.jsonl` per attempt.
- **Circuit breaker**: 3 failures -> 5 min cooldown per model.
- **Source tracking implemented**: `source_files` metadata on questions for judge verification.
- **Exam fidelity benchmark**: yixin0829/mongodb-dev-cert-prep (22 CRUD objectives, PyMongo examples).
- **Core quality modules**: `model_runner.py` (quality gates, circuit breaker, multi-provider), `judge_questions.py` (RAG judge with source verification).
- **Current execution note**: Topic 4 is the active ordered target. `replaceOne()` is fully populated, `updateOne()`, `updateMany()`, `$set`, `$push`, and `$inc` are study-ready, and the next ordered target is `$unset`. The overnight runner is local-only for long repair/populate runs.
- **Current Topic 1 queue**: the first quarantined `BSON Data Types` record `1cf65439-edd6-4eb4-9c5e-b0d9e4e03b05` and the next Topic 1 quarantine `4641b52f-8d87-4530-bf95-1a69929daa89` have both been repaired and promoted; the next Topic 1 quarantine is `certcoach-t01-bson-data-types-easy-004-0ccef6dd`.
- **Learner study note**: the micro-challenge contract is question-only, the lesson template should stay inside the active concept, and the new guardrail note is linked from Memory Home for later reuse.

## Immediate Continuation

1. Continue Topic 4 `replaceOne()`, then the rest of Topic 4.
2. In parallel, drain the quarantine repair queue in canonical order, starting with Topic 1 `BSON Data Types` record `1cf65439-edd6-4eb4-9c5e-b0d9e4e03b05`.
3. For each quarantine record: review classification, repair or regenerate, validate, check duplicate/scope, then promote; leave ambiguous and misc records inactive.
4. Fix plain pytest discovery.
5. Apply the registered strict lesson loop to Topic 2 `insertOne()` and continue Topic 2 in order.
6. Execute Phase 5 manual full-flow and mixed-mock verification.
7. Freeze features and begin daily exam preparation.

## Commands

```powershell
.\.venv\Scripts\python.exe -m certcoach.jobs.next_phase4_topic
.\scripts\run_phase4_overnight.ps1 -RepairBatchSize 25 -PopulationBatchSize 25
.\.venv\Scripts\python.exe -m pytest tests\unit -q
```

## Deep References

- Release blockers: [[preparation_tool_gap_assessment|Preparation Tool Gap Assessment]]
- Current execution order: [[next_steps|Next Steps]]
- Product behavior: [[coach_flow_spec|Coach Flow Spec]]
- Decisions: [[decision_log|Decision Log]]
- Exam scope: [[project_exam_scope|Project Exam Scope]]

## Resume Point

- Continue Topic 4 from `$unset`.
- Do not advance to later update operators until the selector advances.
- Keep the micro-challenge rule question-only, with no answer, hint, worked solution, or example response.
- Preserve the same one-question-at-a-time loop across sessions until every topic and concept reaches the active inventory target and no repair/quarantine backlog remains.
