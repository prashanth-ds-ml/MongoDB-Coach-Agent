# 🧠 Active Context

**Project:** CertCoach RAG Platform
**Goal:** An end-to-end learning framework to prepare users for the MongoDB Associate Python Developer certification. It operates entirely locally using Ollama and ChromaDB, providing spaced-repetition, a smart question bank, trap analysis, and mock exams via a rich CLI interface.
**Current Phase:** Phase 6 (Completed, Feature Frozen)
**Status:** LOCK / FREEZE (Preparing for exam study phase starting tomorrow)

---

## 🔒 Lock Details
- **Codebase:** All feature development and UI enhancements are frozen.
- **Goal:** Shift focus entirely from writing tool functionality to taking quizzes, reading explanations, and mastering the MongoDB blueprint topics.
- **Storage:** Local MongoDB (`certcoach_db`) acts as the single source of truth for questions and student state.
- **Historical note:** Phase 2.5 hardened the coach flow into a bounded Teach -> Check -> Practice -> Review state machine before the later feature freeze.

*See `session_handoff.md`, `session_log.md`, and `coach_flow_spec.md` for daily handoff and mode rules.*
