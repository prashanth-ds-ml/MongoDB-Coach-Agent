## Roadmap & Next Priorities

### Completed

1.  **MongoDB Backend Migration**
    *   `certcoach_db` is now the primary backend for questions, profiles, attempts, study sessions, draft questions, and active exam state.

2.  **Question Bank and Mock Exams**
    *   The CLI can pull questions from MongoDB for practice, mini-mocks, timed mocks, and full mock exams.
    *   The exam simulator supports timed navigation, flags, delayed review, autosave, and resume.

3.  **Study Intelligence**
    *   Daily agenda generation, concept-level completion, spaced repetition, readiness metrics, study session logging, and gated mock unlocks are implemented.

4.  **Latest Local Changes**
    *   Added streak-freeze rewards and retention.
    *   Added MongoDB URI reconfiguration from the settings menu.
    *   Added a mongosh vs PyMongo casing contrast sheet.

### Pending

1.  **Release Hygiene**
    *   Keep runtime study logs and ad hoc scratch scripts out of release commits unless they are intentionally promoted to product assets.
    *   Continue running `pytest tests` before every push.

2.  **Warning Cleanup**
    *   Replace `datetime.utcnow()` usage with timezone-aware UTC helpers across `src/` and tests.

3.  **Manual Smoke Test**
    *   Launch `certcoach` against a real MongoDB URI and verify onboarding, settings URI hot-swap, one practice quiz, and one mock resume/finalize flow.
