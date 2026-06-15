# CertCoach Flow Spec

Version: 1.0
Last updated: 2026-06-03T00:00:00+05:30

Related: [[Memory Home]], [[active_context|Active Context]], [[project_layout|Project Layout]]

See also: [[lesson_template_rules|Lesson Template Rules]]

## Modes

### Teach
- Input: one syllabus topic and one concept.
- Output: explanation, one micro-challenge, and bounded recall cues.
- Boundary: do not introduce later-topic material.
- Micro-challenge must test only the current concept and must not require a later-topic method or workflow.
- Depth rule: assume the learner is seeing the concept for the first time, then explain the concept, the syntax, and the do/don't examples in detail before moving on.
- Syntax rule: if code is shown, walk the learner through the example line by line and explain why the correct pattern is preferred.

### Check
- Input: learner answer or clarification question about the current concept.
- Output: correction, trap explanation, or direct clarification.
- Boundary: stay inside the same topic and concept.

### Practice
- Input: five-question concept gate.
- Output: quiz questions grounded in the explained subtopics.
- Boundary: practice questions must stay within the current topic and its current concept set.

### Review
- Input: completed concept and practice result.
- Output: cumulative cheat sheet, key traps, and next-step gating.
- Boundary: summarize what the learner has already seen; do not preload later nodes.

### Free Chat
- Input: open-ended study or MongoDB questions.
- Output: direct answers and advice.
- Boundary: if the learner wants the full lesson flow, redirect them back to the main agenda.

## Transition Rules

1. Teach one concept at a time.
2. Handle micro-challenge feedback before moving forward.
3. Unlock practice only for the active concept.
4. Move to cumulative review after practice completes.
5. Advance to the next agenda item only after the current concept is complete.
