# 📖 Session Log

*Append-only log of high-level progress.*

Related: [[Memory Home]], [[active_context|Active Context]], [[session_handoff|Session Handoff]], [[progress_log|Progress Log]]

## 2026-04-16
- Project paused after completing all major planning and coding scaffolding for the core pipeline (cleaning markdown, chunking, and metadata generation).
- Codebase analysis performed, capturing architecture across 5 core modules.

## 2026-04-22
- Migrated legacy `project_activity.md`, `project_snapshot.md`, and `project_summary_log.md` into this new token-efficient Obsidian memory system.

## 2026-04-23
- Implemented Option A for the RAG engine: Deleted the old Chroma DB instance and fully re-indexed the knowledge base strictly using the newly extracted `Primary_Exam_Guide.md` as the exclusive source of truth.

## 2026-04-30
- Implemented the "Perfect Learning Loop" pedagogical flow in the CLI app.
- Added Anki-style spaced repetition to the daily agenda based on confidence and accuracy.
- Upgraded the `run_teach_session` to chunk explanations and auto-advance through the daily agenda.
- Shifted the CLI to a Hybrid Conversational interface, adding a persistent Smart Router and a `run_free_chat_session` mode.

## 2026-06-03
- Tightened the coach flow into a bounded Teach -> Check -> Practice -> Review state machine.
- Added timestamped memory files for progress, decisions, and flow specifications.
- Updated the lesson persona so follow-up answers stay within the current concept instead of drifting into later topics.

## 2026-06-06
- Implemented the Casing Guard validation repair in `planner.py` to support python keywords and neutral methods in PyMongo topics.
- Added strict Pydantic flat schema formatting rules to `nightly_seed_questions.py` prompt to prevent Ollama output formatting errors.
- Declared a complete Feature Freeze across all features and UI modules.
- Created `progress.md` and `decisions.md` Obsidian memory docs, and updated other memory guides to prioritize immediate exam preparation.

## 2026-06-11
- Completed Phase 1 repository and model configuration stabilization.
- Switched the active study model to `qwen3.5:4b`; retained `gemma4:12b` for population and repair.
- Completed Phase 2 study-critical runtime stabilization.
- Unified scheduling, practice, and completion around direct active-contract concept readiness.
- Finalized Phase 2 readiness and normal practice as exactly three Easy plus two Medium questions, with no Hard or arbitrary fallback.
- Verified 99 tests and confirmed through a read-only live snapshot that 57 concepts are currently blocked pending question-bank lifecycle work.
- Completed Phase 3 question-bank lifecycle stabilization without database writes.
- Replaced fixed-total and default-buffer population with readiness-only (`3 Easy + 2 Medium`) active-question deficit reporting.
- Added explicit extra Easy/Medium generation controls for useful population beyond readiness.
- Final Phase 3 verification passed 108 tests; read-only readiness deficits are 174 Easy and 116 Medium before migration and repair.
- Began Phase 4 with verified pre-migration and post-migration backups.
- Applied deterministic migration across all 351 questions: 69 active, 216 pending explanation repair, and 66 quarantined.
- Prepared a bounded overnight runner that backs up, repairs, populates readiness gaps, and logs each run.
- Reverified the post-migration backup and passed 111 automated tests; long-running overnight jobs were intentionally not started during daytime.
- Changed Phase 4 overnight processing from broad-bank batches to strict syllabus order; Topic 1 is the current target.
- Fixed canonical topic-ID counting so Topic 1 selector and seeder agree on 4 Easy and 2 Medium remaining questions.
- Full dry-run classified 351 records into 69 migratable without LLM explanation repair, 216 needing explanation repair, and 66 quarantined.
- Updated Phase 4 to process one exact concept at a time in canonical syllabus order.
- Separated study readiness (`3 Easy + 2 Medium`) from default population inventory (`5 Easy + 5 Medium`, configurable).
- Verified 121 unit tests; at that checkpoint the automatic target was Topic 1 -> `BSON Data Types`.

## 2026-06-15
- Documented the remaining blockers preventing final feature freeze in `memory/preparation_tool_gap_assessment.md`.
- Prioritized question-bank readiness, legacy lifecycle completion, human content review, Phase 5 end-to-end smoke testing, and plain pytest discovery repair.
- Recorded the final-freeze completion standard so future sessions can resume from a durable checklist.
- Added a vendor-neutral `AGENTS.md` with thin Claude and Copilot adapters.
- Created an Obsidian `Memory Home`, compact `agent_context`, templates, and a three-file startup budget for token-efficient cross-agent work.
- Reduced active context and session handoff notes to current-state pointers; historical detail remains in append-only logs.

## 2026-06-17
- Re-read the active memory set and aligned the snapshot docs with the current local-first model chain.
- Separated the population and repair response contracts so string-option generation no longer fails judge validation.
- Confirmed the live assessment note now reflects the latest unit-test count and the current throughput bottleneck rather than the earlier schema mismatch.
- Current operating target is Topic 1 -> `Collections vs Tables`.
- Current maintained unit suite is 123 passing tests.
- Current Phase 4 blocker is throughput tuning for bounded local-first population batches.
