# 🧠 Active Context

**Project:** CertCoach RAG Platform
**Goal:** An end-to-end learning framework to prepare users for the MongoDB Associate Python Developer certification. It operates entirely locally using Ollama and ChromaDB, providing spaced-repetition, a smart question bank, trap analysis, and mock exams via a rich CLI interface.
**Current Phase:** Phase 2 (Local Engine & CLI Dashboard)
**Status:** ACTIVE (Executing implementation plan)

## Key Constraints & Architecture
- **Primary Guide:** All content generation uses `data/cleaned_markdowns/` (derived from the official PDF).
- **Architecture:** 100% Local. Ollama for generation, `sentence-transformers` for embeddings, and MongoDB for tracking learning history and the question bank.
- **Workflow:** The user studies via `src/cli_app.py`, triggering `retriever.py` and `quiz_generator.py`, with performance stored in `database.py`.

*See `session_handoff.md` and `session_log.md` for daily handoff context.*
