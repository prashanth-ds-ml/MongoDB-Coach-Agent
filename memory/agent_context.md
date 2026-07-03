# Agent Context

Last verified: 2026-07-03

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

- Documentation coverage: 12/12 topics. Concepts: 58 total, 8 study-ready, 50 blocked. Question lifecycle: 516 total records.
- Current ordered target: Topic 4 -> `$unset`. Topics 1-3 are complete from the selector's perspective; Topic 4's `replaceOne()`, `updateOne()`, `updateMany()`, `$set`, `$push`, and `$inc` are all study-ready or fully populated.
- Bank-wide quarantine triage: 121 records mapped and pending repair, 28 held for manual classification, 16 kept aside as misc. `next_phase4_topic` treats `quarantine_pending` as an incomplete concept, so quarantine drains in the same canonical loop as repair/population.
- Stored lesson prebuild is complete for all 58 concepts (validated, exam-audited, stored in `certcoach_db.lesson_artifacts`); 39 are also exported as markdown under `memory/lessons/` (Topics 3-10). Topics 11-12 exports are pending via `scripts/enhance_all_lessons.py`.
- Learner-facing lesson pattern: `memory/study_pattern_guardrails.md` (one concept, one question-only micro-challenge, no future-topic leakage).
- Maintained unit suite: 165 passing. `pyproject.toml` now sets `testpaths = ["tests/unit"]`, so plain `pytest` no longer risks collecting `scratch/test_zhipu_vision.py`.
- Full history of what changed and when: [[progress_log|Progress Log]].

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

- Continue Topics 11 and 12 lesson markdown exports using `scripts/enhance_all_lessons.py` (safe to re-run; skips already-generated files).
- Do not advance to later update operators until the selector advances.
- Keep the micro-challenge rule question-only, with no answer, hint, worked solution, or example response.
- Preserve the same one-question-at-a-time loop across sessions until every topic and concept reaches the active inventory target and no repair/quarantine backlog remains.
