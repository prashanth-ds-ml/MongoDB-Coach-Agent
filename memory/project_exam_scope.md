# Project Memory: MongoDB Exam Scope

The definitive source of truth for all content generation within the CertCoach platform is the MongoDB Exam Blueprint.

**Why:** This blueprint dictates the exact syllabus, high-priority topics, and required technologies (PyMongo, Aggregation) to ensure the generated quizzes map directly to the actual certification exam structure. Relying solely on raw files without this structure risks covering irrelevant or outdated material.
**How to apply:** All future steps—from chunking (Module 1) to question generation (Module 2)—must use the domains listed here as the primary categorization system. For instance, when generating a "Syntax" question, it should prioritize `$match` or `$project` over other operators unless directed otherwise.
Related: [[Memory Home]], [[active_context|Active Context]], [[MongoDB_Exam_Blueprint|MongoDB Exam Blueprint]]

## Product Scope

CertCoach is an exam-preparation tool, not a general learning platform. Work is justified only when it directly improves the required study path:

```text
Daily agenda
-> concept lesson
-> concept-scoped Q&A
-> exactly five validated practice questions
-> answer review
-> progress update
-> mixed mock practice
```

## Concept Readiness Contract

A syllabus concept is ready to schedule only when:

- official documentation exists for the concept
- the lesson can be generated from bounded, concept-relevant context
- at least five unique active questions are mapped to the concept
- those questions pass structural and semantic validation
- explanations are accurate and learner-ready

There is no fixed global question-bank target. The readiness gate is `3 Easy + 2 Medium`; ordered population continues toward configurable per-concept inventory targets and may go beyond them for weak-area practice, repetition reduction, or mixed-mock variety.

## Freeze Boundary

The project is ready to freeze when:

- the planner schedules only study-ready concepts
- every scheduled concept can complete its exact five-question gate
- one full daily study flow passes manually
- one timed mixed mock passes manually, including resume/finalize
- learner progress persists correctly in MongoDB
- automated tests pass

After freeze, defer all feature work until after the exam.
