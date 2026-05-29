# Project Snapshot Mechanism Proposal

To capture the *state* of the project at a given moment, we should implement a standardized mechanism. This shouldn't be an optional addition; it should be part of the standard reporting procedure.

**Recommendation:** We will implement a new function/script that generates a dedicated, versioned snapshot file.

### 📂 Implementation Strategy

1.  **New File:** Create `src/scripts/utils/snapshot_generator.py`.
2.  **Snapshot Contents:** This script will read and combine critical data points:
    *   The `resource_links.json` (The syllabus blueprint).
    *   A summary of the current state of the `data/` directory (the source content).
    *   The current status of the task list (retrieved via `TaskList` tool).
    *   A timestamp and Git SHA to anchor the snapshot in time.
3.  **Execution:** The snapshot generation should be the final step before a major milestone commit.

### 🔄 Integration Points:

*   **In `metadata_writer.py` (Task 4):** After successfully writing a batch of metadata, this script should call the snapshot function to record the state of the *database* at that moment.
*   **In `process_directory` (Task 3):** After successfully chunking a batch, it should trigger a snapshot, capturing the `chunk_count` processed so far.

**I will update the plan to include this functionality, as it is vital for traceability.**

**Next Action:** I will now write the scaffolding code for `src/scripts/utils/snapshot_generator.py` and save it. Please confirm if this structure is acceptable for creating version-controlled project snapshots.