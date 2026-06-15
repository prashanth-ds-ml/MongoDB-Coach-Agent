# 🔄 Session Handoff

*This file serves as the strict bridge between AI sessions. It must be read at the start of every session and updated at the very end of every session.*

Related: [[Memory Home]], [[active_context|Active Context]], [[session_log|Session Log]]

### Current Direction

The project is in study-readiness stabilization, not final freeze. The primary goal is to make the required daily study and practice path reliable, then stop feature work and begin exam preparation.

Required path:

```text
Daily agenda -> lesson -> concept-scoped Q&A -> five-question practice
-> answer review -> persisted progress -> mixed mock
```

There is no fixed global question-bank target. `3 Easy + 2 Medium` is the readiness gate, while default ordered population continues toward configurable per-concept inventory targets (`5 Easy + 5 Medium` by default).

### Completed This Session

- Switched the active private study model to `STUDY_MODEL=qwen3.5:4b`.
- Completed Phase 2 study-critical runtime stabilization.
- Bounded lesson reference context to the active concept.
- Required direct concept mapping, active content-contract status, and a `3 Easy + 2 Medium` mix for practice readiness.
- Blocked practice unless exactly three Easy and two Medium questions can be served.
- Required at least `4/5` before concept completion.
- Added explicit dashboard and practice blockers for insufficient concepts.
- Verified `99` automated tests.
- Read-only live snapshot: zero ready topics and 57 blocked concepts.
- Completed Phase 3 question-bank lifecycle stabilization.
- Removed the fixed global bank total and separated the `3 Easy + 2 Medium` study-readiness threshold from configurable per-concept population inventory targets.
- Added active-only concept study-readiness-deficit reporting.
- Added explicit extra Easy/Medium generation controls for variety, weak areas, and mock coverage.
- Corrected dry-run migration classification into migratable, needs-explanation-repair, and quarantined lifecycle states.
- Full read-only lifecycle snapshot: 351 total, 69 migratable, 216 explanation repairs, 66 quarantined.
- Readiness-only snapshot before migration/repair: 174 Easy and 116 Medium missing across 58 concepts.
- Verified 108 automated tests.
- Began Phase 4 live database operations.
- Created verified pre-migration and post-migration backups.
- Applied deterministic migration to all 351 question records.
- Current live lifecycle: 69 active, 216 pending explanation repair, 66 quarantined.
- Current readiness: 2 concepts ready; 162 Easy and 93 Medium readiness deficits.
- Prepared the bounded, resumable `scripts/run_phase4_overnight.ps1` runner.
- Updated the runner to process topics and concepts strictly in syllabus order and fixed numeric topic filtering so Topic 1 cannot match Topics 10-12.
- Aligned seeder counts with canonical topic ID plus concept, matching the study-readiness calculation exactly.
- Verified 121 automated tests after the Phase 4 ordering and inventory-target updates.

### Next Phase

Phase 4 continuation: run explanation repair and ordered inventory population in overnight batches only.

## ⚠️ Important Notes / Gotchas
- Ensure you read `memory/active_context.md` for broader project constraints.
- Always use `memory/session_log.md` for historical, append-only logs.
- Do not run long repair or population batches during daytime.
- The active private study model is `qwen3.5:4b`.
- Population continues beyond study readiness toward the configured per-concept inventory target; explicit extras can add further variety.
- Default overnight command: `.\scripts\run_phase4_overnight.ps1 -RepairBatchSize 25 -PopulationBatchSize 25`.
- Current automatic target: Topic 1 -> `BSON Data Types`; 9 repairs remain and the default inventory target is missing 1 Medium question.
