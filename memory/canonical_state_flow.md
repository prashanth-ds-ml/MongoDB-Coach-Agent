# Canonical State Flow

Last updated: 2026-06-18

This note defines the simple operational flow for topic-by-topic question maintenance.

## Goal

Keep one exact source of truth for each question record and route it to the right job before calling the model.

## Canonical States

- `active`
- `needs_explanation_repair`
- `needs_question_regeneration`
- `quarantined`
- `legacy`

## Exact Routing Rules

1. Pick one exact syllabus concept using `topic_id` plus exact `concept`.
2. Read the stored record status from MongoDB.
3. Route by status:
   - `active` -> learner-facing practice
   - `needs_explanation_repair` -> repair the explanation only
   - `needs_question_regeneration` -> regenerate the question shell
   - `quarantined` -> keep out of learner-facing flows
   - `legacy` -> migrate first, then reclassify
4. Validate the record after write.
5. Recount directly from MongoDB.
6. Advance only when the current concept has no remaining repair, regeneration, or legacy backlog.

## What Each Job Does

- `repair_explanations`
  - Reads `needs_explanation_repair`
  - Repairs explanation text only
  - Does not rewrite the question stem or answer choice structure

- `migrate_legacy_question_bank`
  - Promotes legacy content when it already satisfies the contract
  - Marks explanation-only failures as `needs_explanation_repair`
  - Marks structurally bad content as `needs_question_regeneration`
  - Quarantines content that should not be salvaged

- `nightly_seed_questions`
  - Generates a fresh `question_shell`
  - Stores the shell as repair-pending
  - Hands it to explanation repair in the same run

- `question_bank_comparison_report`
  - Counts stored bank states directly
  - Surfaces repair, regeneration, legacy, and quarantine backlog separately

- `next_phase4_topic`
  - Uses the stored backlog to select the first incomplete concept in syllabus order

## Simple Decision Tree

```text
exact concept -> classify stored status -> route job -> write result -> verify status -> recount -> move on
```

## Why This Works

- It removes fuzzy substring selection from operational routing.
- It keeps repair and regeneration separate.
- It makes the report, selector, and live MongoDB counts agree.
- It keeps Topic 1 and the rest of the syllabus in canonical order.
