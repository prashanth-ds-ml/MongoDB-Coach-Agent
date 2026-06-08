# 📖 Session Log

*Append-only log of high-level progress.*

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

## 2026-06-06
- Implemented the Casing Guard validation repair in `planner.py` to support python keywords and neutral methods in PyMongo topics.
- Added strict Pydantic flat schema formatting rules to `nightly_seed_questions.py` prompt to prevent Ollama output formatting errors.
- Declared a complete Feature Freeze across all features and UI modules.
- Created `progress.md` and `decisions.md` Obsidian memory docs, and updated other memory guides to prioritize immediate exam preparation.
