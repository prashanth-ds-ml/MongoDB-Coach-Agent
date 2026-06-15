# Active Context

Related: [[Memory Home]], [[session_handoff|Session Handoff]], [[session_log|Session Log]], [[coach_flow_spec|Coach Flow Spec]], [[project_layout|Project Layout]]

**Project:** CertCoach
**Primary Goal:** Help the learner prepare for and pass the MongoDB Associate Python Developer certification through reliable daily lessons, retrieval practice, and mocks.
**Current Phase:** Phase 4 live database operations
**Status:** NOT YET FROZEN. Backup and deterministic migration are complete. Long-running explanation repair and population must run only in controlled overnight batches.

**Phase 4 Processing Order:** Process the first concept with pending repairs or inventory below the configured population target within the first incomplete syllabus topic. `3 Easy + 2 Medium` is only the study-readiness gate; default population continues toward `5 Easy + 5 Medium`.

---

## Required Product Surface
- Daily agenda for the canonical syllabus concepts.
- Concept-bound lesson and follow-up Q&A.
- Exactly three Easy and two Medium active, validated practice questions for each scheduled concept.
- Accurate answer review and explanation.
- MongoDB-backed learner progress and attempts.
- Timed mixed mock with resume/finalize behavior.

## Explicitly Deferred Until After the Exam
- New UI work and visual refinements.
- New analytics, gamification, or dashboard features.
- Scenario Simulator enhancements.
- Question Factory enhancements.
- Chroma/RAG or reranker improvements that do not block the required study path.
- General-purpose platform expansion.

## Operating Constraints
- `certcoach_db` is the single source of truth for questions and learner state.
- There is no fixed global question-bank target.
- Default ordered population uses configurable per-concept inventory targets above the readiness gate; additional generation can support weak areas, repetition avoidance, and mock variety.
- Do not run live-bank repair, migration, or population until its build-order phase is reached and reviewed.
- After freeze, allow only incorrect-content fixes, crashes, data-loss fixes, and exam-syllabus corrections.

*See `session_handoff.md`, `session_log.md`, and `coach_flow_spec.md` for daily handoff and mode rules.*
