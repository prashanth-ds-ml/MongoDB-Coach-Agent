# Project Memory: MongoDB Exam Scope

The definitive source of truth for all content generation within the CertCoach platform is the MongoDB Exam Blueprint.

**Why:** This blueprint dictates the exact syllabus, high-priority topics, and required technologies (PyMongo, Aggregation) to ensure the generated quizzes map directly to the actual certification exam structure. Relying solely on raw files without this structure risks covering irrelevant or outdated material.
**How to apply:** All future steps—from chunking (Module 1) to question generation (Module 2)—must use the domains listed here as the primary categorization system. For instance, when generating a "Syntax" question, it should prioritize `$match` or `$project` over other operators unless directed otherwise.