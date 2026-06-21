# Lesson Template Rules

Related: [[Memory Home]], [[coach_flow_spec|Coach Flow Spec]], [[active_context|Active Context]]

## Teach Mode Contract

1. Use these six top-level sections in order:
   - Core Concept
   - Level-Based Breakdown
   - Syntax & Code Examples
   - Exam Radar
   - Micro-Challenge
   - 30-Second Recall
2. Core Concept must define the concept, name the key terms, explain the mechanics, and explain the design choice or tradeoff.
3. Level-Based Breakdown must contain exactly three audience levels:
   - Beginners
   - Intermediate Learners
   - Advanced Developers
4. Syntax & Code Examples must include a DO example and a DON'T / EXAM TRAP example when syntax applies.
5. The DO and DON'T examples must differ by one meaningful detail; do not reuse the same code in both examples.
6. For concept-only lessons, use only BSON/document-literal examples that belong to the current concept and do not introduce CRUD write methods unless they are already part of the concept.
7. Exam Radar must contain 3-5 traps or distinctions, each with the exam signal being tested.
8. Micro-Challenge must be one question only, with no answer, no hint, and no example response.
9. Micro-Challenge should stay inside the current concept and should not require a later-topic method, operator, or workflow.
10. Default to a short open-ended question. Use multiple choice only when it genuinely improves clarity.
11. For Topic 1 and other concept-only lessons, prefer open-ended micro-challenges and avoid multiple choice unless it is essential.
12. If the Micro-Challenge is multiple choice, label options with A/B/C/D and show the full text of the choice.
13. 30-Second Recall must end with 3-5 short bullets that can be memorized quickly.

## Learner Benefit Rules

- Keep the DO example and DON'T / EXAM TRAP example as a minimal contrast pair.
- Use the same concept vocabulary in the lesson, micro-challenge, and recall section.
- Do not leak later-topic syntax or workflows into the current concept.
- If the learner is likely to confuse two nearby ideas, make that distinction explicit in Exam Radar and the Micro-Challenge.

## Formatting Rules

- Use stable subsection labels inside each section.
- Prefer short paragraphs, flat bullets, and bold labels over nested bullet stacks.
- Keep line breaks intentional and readable.
- Keep all examples inside the current syllabus topic and concept.
