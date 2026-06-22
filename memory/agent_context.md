# Agent Context

Last verified: 2026-06-22

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
- Practice readiness requires active, directly mapped questions: exactly `3 Easy + 2 Medium` per concept.
- Passing a concept requires at least `4/5`.
- Population may continue beyond readiness toward configurable inventory targets, default `3 Easy + 2 Medium`.
- Repair/population processing follows canonical syllabus topic and concept order.
- The live loop is persistent across sessions: select the next incomplete `topic_id + concept`, work exactly one concept/batch at a time, repair or quarantine every record before learner-facing use, then recheck the selector before advancing.
- Every session must surface the current work packet before action, scoped only to the active topic and concept.
- Legacy, repair-pending, and quarantined records cannot enter learner-facing practice.
- Long repair/population runs use `scripts/run_phase4_overnight.ps1` with local model chain.
- Optional UI, analytics, and general platform work are deferred until after the exam.

## Live Snapshot

- Documentation coverage: 12/12 topics.
- Concepts: 58 total, 14 study-ready, 44 blocked.
- Question lifecycle: 339 total records.
- Current ordered target: Topic 4 -> `updateOne()`.
- Topic 1, Topic 2, Topic 3 are 100% complete and clean.
- Topic 4 `replaceOne()` is study-ready at `5 Easy + 3 Medium` active questions.
- Deficit for `updateOne()` concept: 0 Easy, 2 Medium.
- Bank-wide deficit: 204 questions (128 Easy, 76 Medium) remaining to complete all concepts.
- Qwen-7B speedup: Local Ollama `qwen2.5-coder:7b` executes question generation and repair in **48 seconds** (7.5x faster than Gemma-12B's 6 minutes) and is preferred for local operations.
- Backup verified: `backups/questions-20260622T031016Z` (338 records).

## Immediate Continuation

1. Populate the remaining 2 Medium questions for Topic 4 `updateOne()` using `qwen2.5-coder:7b`.
2. Proceed to updateMany(), $set, $push, etc. in Topic 4.
3. Fix plain pytest discovery.
4. Execute Phase 5 manual full-flow and mixed-mock verification.
5. Freeze features and begin daily exam preparation.

## Commands

```powershell
# Set local Qwen env vars and run overnight seeder for Topic 4
$env:POPULATION_MODEL_CHAIN_LOCAL_ONLY = "qwen2.5-coder:7b"
$env:REPAIR_MODEL_CHAIN_LOCAL_ONLY = "qwen2.5-coder:7b"
.\scripts\run_phase4_overnight.ps1 -Topic 4

# Run unit tests
.\.venv\Scripts\python.exe -m pytest tests\unit -q
```

## Deep References

- Release blockers: [[preparation_tool_gap_assessment|Preparation Tool Gap Assessment]]
- Current execution order: [[next_steps|Next Steps]]
- Product behavior: [[coach_flow_spec|Coach Flow Spec]]
- Decisions: [[decision_log|Decision Log]]
- Syllabus scope: [[project_exam_scope|Project Exam Scope]]
