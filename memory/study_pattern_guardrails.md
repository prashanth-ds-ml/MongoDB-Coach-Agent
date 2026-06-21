# Study Pattern Guardrails

Related: [[Memory Home]], [[coach_flow_spec|Coach Flow Spec]], [[lesson_template_rules|Lesson Template Rules]], [[canonical_state_flow|Canonical State Flow]]

Captured on 2026-06-19.

## Purpose

Keep learner-facing study material tightly scoped to the active topic and concept so the learner never sees future-topic material in a micro-challenge or lesson example.

## Rules

- Teach one exact concept at a time.
- Keep examples and traps inside the current concept boundary.
- Use a DO / DON'T pair only when the difference is one meaningful detail.
- Use the same vocabulary across lesson, micro-challenge, and recall sections.
- Micro-challenge output must contain only the question.
- Do not include the answer, hint, worked solution, or example response in micro-challenges.
- Prefer open-ended micro-challenges.
- Use multiple choice only when it genuinely improves clarity.
- If code is shown, explain it line by line.
- If the concept is syntax-heavy, include a concise syntax example and a clear trap example.
- If the concept is conceptual, avoid pulling in later-topic methods or workflows.

## Recommended Lesson Shape

1. Core Concept
2. Level-Based Breakdown
3. Syntax & Code Examples
4. Exam Radar
5. Micro-Challenge
6. 30-Second Recall

## Micro-Challenge Shape

- One question only.
- No answer.
- No hint.
- No worked solution.
- No example response.
- Stay within the current concept.

## Best-Fit Examples

- Topic 1: use BSON type, document shape, or `_id` behavior.
- Topic 3: use `find()`, `findOne()`, projections, cursors, or `countDocuments()`.
- Topic 4: use `replaceOne()`, `updateOne()`, `updateMany()`, or update operators only if they belong to the active concept.

## Why This Helps

- It prevents future-topic leakage.
- It keeps the learner focused on one mental model at a time.
- It makes the micro-challenge a real recall check instead of a disguised answer key.
- It gives us a stable template for later lesson generation and review.
