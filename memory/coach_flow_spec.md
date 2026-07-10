# CertCoach Flow Spec

Version: 2.1 (locked)
Last updated: 2026-07-07

Related: [[Memory Home]], [[agent_context|Agent Context]], [[project_layout|Project Layout]]

See also: [[lesson_template_rules|Lesson Template Rules]]

## Status

This is the locked, code-verified spec for the **learner-facing journey**: what an exam
candidate experiences running `certcoach` (main menu -> daily agenda -> lesson -> practice ->
mock). It supersedes v1.0's abstract mode descriptions wherever they had drifted from the real
implementation (see Changelog).

The separate **content-build / maintainer loop** (study source -> dry-run yield -> generate ->
Docket review -> confirm, used to populate the question bank) is a different pipeline and is
out of scope here -- see `diagrams/learner_journey.html` group 1, or [[next_steps|Next Steps]].

## The Locked Journey

### Stage 0 -- Entry (`main_menu`, `cli.py`)

`certcoach` opens on the main menu. Option 1, "Start Today's Study Agenda," is built by
`planner.generate_daily_agenda(user_id)`.

Selection logic (`planner.get_syllabus_status`): the next agenda item is the first syllabus
topic, in canonical order, that (a) has official docs (`has_topic_documentation`) and (b) has
at least one uncompleted concept (`readiness_concepts`). **Question-bank inventory is not a
factor here** -- a concept with zero confirmed questions still surfaces as today's lesson.

### Stage 1 -- Concept lesson (`run_teach_session`, `cli.py:467`)

1. Daily Mission Brief panel: days left to exam, mastery %.
2. For each subtopic in the topic, in order:
   - Resolve official doc(s) via `planner.resolve_concept_docs` (relative-threshold matcher:
     a candidate doc must score at least half the concept's top score).
   - If no doc resolves, skip the subtopic silently ("not covered in reference documents").
   - Show each resolved doc **verbatim, one at a time** (`planner.load_md_context`) -- never
     merged into one panel, never an AI paraphrase. The learner presses Enter for the next doc
     or types `practice` to jump ahead early.
3. After all docs for a subtopic: an open Q&A loop -- the learner can ask a free-form question
   (`coach.handle_followup`, scoped strictly to the current topic + subtopic), type
   `next`/`done` to advance, or `practice` to jump to the quiz.

### Stage 2 -- Scoped practice (`run_practice_questions`, `cli.py:1475`)

- Exactly **3 Easy + 2 Medium** confirmed questions for the subtopics just explained -- never
  more, never fewer, no substitution from other concepts.
- Gate: if fewer than 3 Easy + 2 Medium confirmed questions exist for the concept, the learner
  sees "No confirmed questions are available yet" (or gets fewer than 5). Lesson delivery still
  happened -- only the quiz is blocked. This is the `is_practice_ready` gate documented in
  [[agent_context|Agent Context]].
- A score of >= 4/5 marks the subtopic complete (then the topic, once every subtopic is done)
  and shows the cumulative cheat-sheet checkpoint.

### Stage 3 -- Mini-Mock offer (still inside `run_teach_session`)

- Gated on `mastered_count >= 3` **topics** -- below that, this step is skipped entirely, no
  banner shown.
- Once unlocked: the learner picks a 10- or 20-question speed check drawn from the general
  confirmed pool for the same bank keys, or skips.

### Stage 4 -- Continue or return

- "Ready for the next agenda item?" (Y/n) either loops back to Stage 1 for the next agenda item
  or returns to the main menu.

### Stage 5 -- Full / Timed Mock (main menu, independent of the daily agenda)

- Locked until **70% syllabus mastery** (`MOCK_EXAM_UNLOCK_THRESHOLD`); shown as locked menu
  items below that.
- Full Mock: 53 questions. Timed Mock: 20 questions. Both apportioned by real exam domain
  weights (`EXAM_DOMAIN_WEIGHTS`), per-concept round-robin capped, with an explicit shortfall
  report -- never silently padded.

### Stage 6 -- Free Chat

- Open-ended MongoDB/study questions, reachable any time from the main menu, separate from the
  fixed agenda. Redirects the learner back to the agenda if they want the structured flow.

## Gate Reference (exact numbers, `core/planner.py`)

| Gate | Constant | Value |
|---|---|---|
| Lesson eligibility | doc coverage + uncompleted concept | no question-count minimum |
| Practice unlock per concept | `PRACTICE_EASY_COUNT` / `PRACTICE_MEDIUM_COUNT` | 3 Easy + 2 Medium confirmed |
| Subtopic / topic mastery | practice score | >= 4 of 5 |
| Mini-Mock unlock | mastered topics | >= 3 |
| Full / Timed Mock unlock | `MOCK_EXAM_UNLOCK_THRESHOLD` | 70% syllabus mastery |

## Explicitly Out of Scope (gated, not built)

- Adaptive weak-area coaching, spaced-revision notes, and scheduled flashcards are deferred
  until the user reports 3 topics/concepts mastered (see [[agent_context|Agent Context]]'s
  Immediate Continuation and the personal-memory deferral). Do not begin designing these until
  that signal arrives.
- The content-build/maintainer loop (dry-run yield, generation, Docket review/confirm) feeds
  this journey's question inventory but is not part of the learner-facing flow itself.

## Content Lifecycle (per concept, feeds this journey's inventory)

The content-build/maintainer loop (out of scope for the learner-facing stages above, but the
same person runs both today) closes two gaps as of this lock:

1. **Study** the concept's official doc(s), one at a time (same doc-resolution/display Stage 1
   uses) -- `certcoach-preview-concept`.
2. **Chunk + inspect** that doc (`inspect_doc.chunk_doc_text`, markdown-header split) for citable
   fact yield, now reported both by difficulty *and* by exam-style taxonomy (Type A Syntax/Trap,
   Type B Theory/Constraints, Type C Predicting Output, Type D Troubleshooting/Performance) --
   `print_taxonomy_yield_report`. A fact's taxonomy suggestion is trusted only if valid for the
   topic (`nightly_seed_questions.style_weights_for_topic`'s allowed set); anything else is
   reported as unclassified, never guessed.
3. **Generate** from those chunks -- `certcoach-generate-from-doc`. Style-type assignment prefers
   each fact's own content-aware taxonomy suggestion from step 2, falling back to the topic's
   weighted-random draw only when a fact has no valid suggestion (`generate_from_doc.assign_style_types`).
4. **Map + backfill existing questions** to the same topic/concept/doc --
   `certcoach-map-questions-to-docs --write` persists `metadata.topic_id`/`metadata.concept`
   only onto documents currently missing them (never overwrites an already-tagged document,
   never touches `provenance.state`), so orphan legacy records stop being invisible to
   topic/concept-scoped review.
5. **Review** the fresh `draft`/`sourced` questions in Docket as before, with a **read-only
   legacy reference panel** (`GET /api/legacy`, `database.get_legacy_reference_questions`)
   showing old-bank `suspect` questions already mapped to the same concept for context -- never
   an actionable confirm/suspect target, matching how `suspect` is documented elsewhere as inert.
6. **Confirm** into the final DB (unchanged) -> repeat for the next doc/concept in canonical
   order -> once enough concepts clear the practice-readiness gate, Stages 2-5 above (practice,
   mini-mock, full/timed mock) become usable.

## Q&A / Free Chat Boundaries (unchanged from v1.0, still enforced by `coach.handle_followup`)

- **Check**: stays inside the same topic and concept; correction, trap explanation, or direct
  clarification only.
- **Free Chat**: open answers to any MongoDB/study question; redirects to the agenda if the
  learner wants the structured flow.

## Changelog

- **2026-07-07 (v2.1)**: Added the Content Lifecycle section above, closing the two gaps
  identified right after v2.0's lock: taxonomy-blind inspection/generation (now content-aware,
  with a topic-valid-set clamp) and the disconnected legacy-question mapping (now backfills
  orphans and surfaces legacy questions as read-only review context). Also removed a batch of
  confirmed zero-caller dead code across `database.py`, `planner.py`, `dedupe_questions.py`,
  `nightly_seed_questions.py`, `repair_explanations.py`, `config.py`, `content_contract.py`,
  `question_targets.py`, and deleted the orphaned `lesson_aligned_practice_builder.py`
  (Phase-4-era, superseded, zero callers) -- see Decision Log 2026-07-07 session 9.
- **2026-07-07 (v2.0, this lock)**: Rewrote from abstract mode descriptions (Teach/Check/
  Practice/Review/Free Chat boundaries only) to the concrete, code-verified stage-by-stage
  journey above, after session 7 found and fixed two real bugs where the written spec no
  longer matched what the CLI actually does: lesson eligibility had been wrongly coupled to
  question-bank readiness, and the documented six-section AI lesson had already been replaced
  by verbatim official-doc display. v1.0's six-section lesson template (Level Breakdown, Exam
  Radar, Micro-Challenge, 30-Second Recall, etc.) is retired from this flow specifically; it
  still exists for `certcoach-prebuild-lesson`/`lesson_bank.py`, untouched.
- **2026-06-03 (v1.0)**: Original abstract Teach/Check/Practice/Review/Free Chat mode
  boundaries. Superseded above; the Q&A/Free Chat boundary rules are carried forward unchanged.
