## Roadmap & Next Priorities

1.  **[High Priority] Phase 6: MongoDB Backend Migration**
    *   **Goal:** Replace the temporary SQLite state tracker with a true MongoDB local backend.
    *   **Action:** Add `pymongo` to `requirements.txt`. Rewrite `src/scripts/core/database.py` to handle `certcoach_db`.
    *   **Outcome:** Practice what we preach—using Document databases and Aggregation pipelines for the study analytics!

2.  **[High Priority] Seed the Database**
    *   **Goal:** Upload the 69 extracted official questions.
    *   **Action:** Write a short seed script to ingest `data/extracted_questions.json` directly into the new MongoDB `questions` collection.

3.  **[Medium Priority] Implement Mock Exam CLI Loop**
    *   **Goal:** Allow users to simulate the real test.
    *   **Action:** Add an option in `cli_app.py` that pulls 20 random questions from the MongoDB `questions` collection and times the user.
