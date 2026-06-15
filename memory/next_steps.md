# Next Steps: Study-Readiness Build Order

Related: [[Memory Home]], [[active_context|Active Context]], [[decision_log|Decision Log]]

The project is not frozen yet. Complete and review one phase at a time. Do not run live-bank repair, migration, or population early.

---

## Current Phase: Phase 4 - Live Database Operations (Daytime Checkpoint Complete)

Completed daytime operations:

- Created and verified a pre-migration backup of 351 records.
- Applied deterministic migration: 69 active, 216 pending explanation repair, and 66 quarantined.
- Created and verified a post-migration backup of 351 records.
- Prepared and validated `scripts/run_phase4_overnight.ps1`.
- Restricted explanation repair to records explicitly marked `needs_explanation_repair`.
- Made the overnight runner automatically select the first concept with pending repairs or inventory below the configured target, in canonical syllabus order.
- Aligned repair and population filters with exact canonical topic IDs so Topic 1 cannot touch or count Topics 10-12.

Recovery points:

- Pre-migration: `backups/questions-20260612T025926Z`, SHA-256 `2f9917d39642ba92b6271c0b1582d4645175a3035b52340d4dad848aabc37a10`.
- Post-migration: `backups/questions-20260612T030150Z`, SHA-256 `b59305bda240841a14de8be2fb57d815d9d07456f0e61bcd2247b6cdeaa196f1`.

Current live snapshot:

- 351 total records.
- 69 active records.
- 216 pending explanation repair.
- 66 quarantined.
- 2 study-ready concepts.
- Readiness deficits: 162 Easy and 93 Medium.

Next operation: run bounded repair and ordered inventory-population batches overnight only.

Current sequential target: Topic 1, `MongoDB Overview & The Document Model` -> `BSON Data Types`; study-ready but still has 9 pending repairs and is missing 1 Medium question toward the default `5 Easy + 5 Medium` inventory target.

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

### Phase 4 - Live Database Operations
- Back up the `questions` collection.
- Apply mapping and corrected migration.
- Repair explanations in controlled `gemma4:12b` batches.
- Recalculate concept and difficulty deficits after migration and repair.
- Populate concepts toward the configured inventory target even after they become study-ready.
- Populate beyond readiness toward the configured inventory target and allow explicit Easy/Medium extras beyond it.

### Phase 5 - Smoke Test and Freeze
- Verify one full study flow and one timed mixed mock.
- Verify MongoDB persistence and insufficient-question behavior.
- Run the full automated suite.
- Declare the feature freeze and begin daily exam preparation.
