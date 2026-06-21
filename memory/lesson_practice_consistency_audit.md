# Lesson / Practice Consistency Audit

Related: [[Memory Home]], [[coach_flow_spec|Coach Flow Spec]], [[lesson_template_rules|Lesson Template Rules]], [[architecture_decisions|Architecture Decisions]], [[project_exam_scope|Project Exam Scope]]

Last updated: 2026-06-03T00:00:00+05:30

## Executive Summary

CertCoach now has a shared content contract in code, but it still needs the legacy bank to be migrated for the learner experience to become fully consistent.

The system is enforced across three layers:

1. Prompt generation
2. Question validation / repair
3. CLI rendering / normalization

The shared contract now lives in `src/certcoach/core/content_contract.py`, and both question generation and repair stamp content metadata with a version. The audit path also flags generated records that predate the current contract.

The remaining problem is not the absence of rules. It is the presence of legacy bank content and a few remaining operational gaps around how that content is migrated, quarantined, and revalidated. That creates drift:

- Lesson text can be too loose or too specific for Topic 1.
- Practice questions can still contain legacy malformed options.
- Explanations can look clean even when the stored question is still semantically wrong.

The result is a system that looks patched from the outside, but not yet governed by one canonical contract.

## Senior-Role Review

### 1. Prompt / LLM Architect

Primary job: constrain model output so it does not improvise beyond the syllabus concept.

What is working:

- Teach mode is explicitly scoped to one topic and one concept.
- The prompt now asks for six fixed sections.
- Topic 1 gets special handling for open-ended micro-challenges and concept-only syntax.

What is still weak:

- The model can still drift if the prompt wording is not exact enough.
- Topic 1 must be treated as a special-case template, not just a general rule with a note attached.
- The model should not be trusted to infer when a question should become multiple choice versus open-ended without a stronger rule.

Design conclusion:

- Prompt rules are necessary, but they are not sufficient.
- The prompt needs to be backed by an explicit template spec that both the generator and validator consume.

### 2. Backend / Platform Engineer

Primary job: make the data flow deterministic and resistant to stale content.

Code path review:

- `src/certcoach/core/persona.py:64-279` defines the lesson prompt contract and the lesson text cleaner.
- `src/certcoach/jobs/nightly_seed_questions.py:39-372` defines question-generation rules and the quality validator.
- `src/certcoach/jobs/repair_explanations.py:92-180` repairs explanation content but not the question text itself.
- `src/certcoach/core/database.py:514-540` audits explanations structurally, not semantically.
- `src/certcoach/cli.py:849-939` formats practice explanations and sanitizes feedback before display.

Key engineering issue:

- The repair job can improve explanations while leaving the underlying bad question intact.
- The audit can mark content compliant if it has the right headings and enough text, even if the content is semantically weak.
- The renderer can clean up display artifacts, but it cannot fix the stored record.

Design conclusion:

- The system needs a canonical content contract plus a repair/migration path that can rewrite bad stored records, not just explain them better.

### 3. Data / Quality Engineer

Primary job: protect the question bank from legacy bad records and bad new inserts.

Current gap:

- The bank still contains earlier generated items with wrong option vocab, weak distractors, or bad micro-challenge shape.
- Validation only blocks future inserts after the rule exists.
- Existing content must be repaired or retired explicitly.

What should happen:

- Every stored question should carry a content version.
- Questions that predate the contract should be tagged as legacy.
- Topic 1 questions should be revalidated against a stricter semantic rule set before they are allowed back into practice.

Design conclusion:

- If the database is the source of practice, then the database must also become the source of truth for content versioning and repair status.

### 4. QA / SDET

Primary job: make failures reproducible and visible before they reach the learner.

What is covered by tests now:

- Prompt text includes the expected rules.
- The lesson cleaner normalizes common malformed structures.
- The question validator rejects a set of malformed Topic 1 options.
- The repair pipeline passes repaired content back through validation.

What is not covered enough:

- End-to-end bank migration from legacy bad records.
- Golden tests for actual live lesson output shapes.
- Regression tests for Topic 1 micro-challenge style over multiple prompt variations.
- Tests that verify the repair job can rewrite or quarantine semantically bad legacy items, not just explanations.

Design conclusion:

- Unit tests are good enough for local correctness, but there needs to be at least one integration-level bank audit test over real stored examples.

### 5. Curriculum / Instructional Designer

Primary job: keep the learner experience aligned with the pedagogy of first-time learning.

Current good direction:

- Teach mode is now trying to behave like a first-contact lesson, not a recap.
- Syntax examples are supposed to be walked line by line.
- DO / DON'T contrast is the right pedagogy.

Where it still leaks:

- Topic 1 can still drift into examples that are too operational.
- Micro-challenges can become answer dumps instead of questions.
- Practice explanations can read like generic bank feedback rather than a concept-specific review.

Design conclusion:

- The lesson template should read like a teaching script, not like a flexible formatting suggestion.

## Root Cause Map

The recurring inconsistency comes from four separate failure modes:

1. **Prompt drift**: the model fills gaps in the prompt with its own structure.
2. **Legacy inventory**: old questions and explanations survive after the rule changes.
3. **Render-only fixes**: the CLI cleans output but does not fix stored truth.
4. **Shallow validation**: compliance checks structure more than meaning.

This means a clean-looking output is not proof that the underlying learning object is correct.

## Code-Level Audit

### Lesson Generation

File: `src/certcoach/core/persona.py`

What it does:

- Builds the lesson prompt.
- Separates teach, follow-up, and free chat behavior.
- Normalizes lesson output into markdown-ish sections.

Risk:

- The prompt still depends on natural-language rules being interpreted correctly by the model.
- If Topic 1 rules are not explicit enough, the model invents a more convenient example pattern.

### Question Generation

File: `src/certcoach/jobs/nightly_seed_questions.py`

What it does:

- Generates new weighted MCQs from documentation context.
- Validates the generated output against a structural quality gate.

Risk:

- Validation rejects some invented BSON vocabulary, but it does not exhaustively validate semantic correctness.
- A question can be structurally valid and still teach the wrong idea if the bank context is weak or the model substitutes a close but wrong concept.

### Repair

File: `src/certcoach/jobs/repair_explanations.py`

What it does:

- Repairs explanations, feedback strings, and trap analysis.
- Revalidates the repaired record.

Risk:

- It does not rewrite question text or option text.
- It is therefore incapable of fully repairing a bad legacy question.

### Audit and Display

Files: `src/certcoach/core/database.py`, `src/certcoach/cli.py`

What they do:

- Audit explanations for structural completeness.
- Sanitize and render explanations to the terminal.

Risk:

- Structural compliance is not the same as instructional quality.
- Sanitization can hide the symptom without curing the record.

## Recommended Architecture

### Layer 1: Canonical Spec

Create one source of truth for:

- section order
- Topic 1 special rules
- open-ended vs multiple-choice policy
- allowed vocabulary for concept-only topics
- minimum explanation shape

This should live in code, then be rendered into:

- teach prompt text
- generator rules
- repair rules
- validation rules
- documentation notes

### Layer 2: Ingest Gate

Every new question should pass:

- structural validation
- semantic Topic 1 vocabulary validation
- duplicate / near-duplicate checks
- explanation template validation

Anything that fails should never enter the live bank.

### Layer 3: Legacy Migration

Old records need a separate process:

- detect legacy content by version or audit failure
- rewrite or quarantine bad question text and option text
- repair explanation content
- re-run validation

### Layer 4: Renderer Hygiene

The CLI should continue to normalize display, but only as a display concern.

It should not be treated as the place where quality is fixed.

## Practical Fix Order

1. Freeze the canonical lesson template in one spec file.
2. Wire prompt generation and validation to that same spec.
3. Add semantic Topic 1 checks for question text and option text.
4. Add a repair path for legacy question text, not just explanations.
5. Tag content with a version so the bank can distinguish legacy from compliant items.
6. Run a migration over existing Topic 1 items.
7. Add integration tests using real bank samples.

## Current Status

Implemented:

- Shared content contract module for Topic 1 semantic checks and contract versioning.
- Version stamping for generated questions and repaired records.
- Audit signal for any record that is missing the current contract version.
- Deterministic migration job for promoting, repairing, or quarantining legacy bank content.
- Practice retrieval now excludes inactive contract records.

Still pending:

- Run the migration job against the live bank.
- Review quarantined records.
- End-to-end fixtures that replay the exact bad CLI output from the audit trail.

The codebase is no longer confused about the existence of the problem. The remaining work is to finish the migration layer so old records stop bypassing the new contract.

## Code Path Deep Dive

### 1. Teach-mode prompt construction

File: `src/certcoach/core/persona.py`

Relevant functions:

- `build_lesson_prompt(topic, subtopic, md_context)`
- `clean_lesson_explanation(text)`
- `build_followup_prompt(topic, subtopic, user_question, chat_history)`

What happens:

- `build_lesson_prompt` assembles the full instruction stack for the model.
- It injects the six-section structure directly into the prompt text.
- It adds special rules for Topic 1 and for concept-only topics.
- `clean_lesson_explanation` then post-processes the returned lesson before it is shown to the learner.

Important details:

- The prompt is doing two jobs at once: teaching policy and formatting policy.
- Because it is natural-language guidance, the model can still “reinterpret” it.
- The cleaner is a fallback, not a guarantee.
- The cleaner normalizes headings, code fences, and micro-challenge labels, but it does not truly validate meaning.

Failure modes:

- The model can output the wrong shape but still look formally close.
- The cleaner can make malformed text readable without correcting the instructional mistake.
- Topic 1 can still drift into operational examples unless the rules remain explicit and narrow.

### 2. Practice explanation formatting

File: `src/certcoach/cli.py`

Relevant functions:

- `clean_feedback_for_role(feedback, is_correct)`
- `format_explanation_template(correct_option_letter, q_item)`

What happens:

- The renderer does not trust the stored option feedback verbatim.
- It tries to pull a relevant section from the stored feedback.
- It then rebuilds the explanation into a fixed six-part structure for display.

Important details:

- This is display normalization only.
- It helps hide stale formatting, but it does not repair bad bank content.
- The rendered review can look polished even when the stored question is semantically weak.

Failure modes:

- Generic fallback feedback can leak through when the stored item is poor.
- Wrong answers may still have contradictory or stale feedback in the bank.
- The panel structure can create a false sense of quality if the underlying item was never fixed.

### 3. Question generation and validation

File: `src/certcoach/jobs/nightly_seed_questions.py`

Relevant functions:

- `generate_weighted_question(target, context_text, avoid_questions)`
- `validate_question_quality(question)`
- `run_weighted_seed(...)`

What happens:

- The model gets a generation prompt plus the quality rules.
- The result is converted into a structured question object.
- `validate_question_quality` checks structure and some topic-specific content constraints.

Important details:

- The validator is the real gate for new content.
- It currently blocks some fake BSON vocab, but it is still mostly a structural gate.
- It does not fully understand semantic teaching quality.

Failure modes:

- A question can be structurally valid and still teach the wrong conceptual distinction.
- Legacy vocabulary can be blocked for new insertions but still remain in old records.
- If the documentation context itself is weak, the model can still produce a plausible but poor question.

### 4. Repair pipeline

File: `src/certcoach/jobs/repair_explanations.py`

Relevant functions:

- `generate_repair(q)`
- `apply_repair(q, repaired)`
- `run_repair(...)`

What happens:

- The repair job regenerates explanations and feedback.
- It validates the repaired result before writing it back.

Important details:

- It explicitly does **not** change question text, option text, or option letters.
- That means it cannot truly fix a bad legacy question.
- It is useful for explanation quality, but not for content integrity.

Failure modes:

- The explanation becomes compliant while the question remains misleading.
- The repaired text can look “fixed” in audits while the bank item is still wrong at its core.

### 5. Database audit

File: `src/certcoach/core/database.py`

Relevant function:

- `audit_question_explanations(min_explanation_chars=500)`

What happens:

- The audit checks for marker words, minimum length, and option feedback presence.

Important details:

- This is a coarse compliance audit.
- It cannot reliably detect semantic mismatch or invented terminology.
- A long, well-shaped explanation can still be wrong.

Failure modes:

- Structural compliance gets treated as if it means instructional correctness.
- The audit can under-report semantic problems in legacy records.

## Role-Based Fix Plan

### Staff Prompt Engineer

Responsibilities:

- Move the teaching contract out of scattered prose and into one canonical spec.
- Make Topic 1 rules explicit and non-negotiable.
- Remove vague fallback language that allows the model to improvise the format.

Deliverable:

- One canonical prompt/spec source that emits prompt text for teach, follow-up, repair, and generation.

### Staff Backend Engineer

Responsibilities:

- Add content versioning to stored questions.
- Distinguish legacy bank records from compliant records.
- Ensure repair jobs can quarantine or rewrite bad legacy items instead of only fixing explanations.

Deliverable:

- A migration path for old question records plus a version marker for new content.

### Staff Data Engineer

Responsibilities:

- Define which fields need semantic validation for Topic 1.
- Enforce rejection of invented type names and other invalid vocabulary before insert.
- Build a cleanup pass for existing bank records.

Deliverable:

- A Topic 1 normalization/repair script that can process live bank items in batches.

### Staff QA Lead

Responsibilities:

- Add regression tests using real stored lesson/question examples.
- Lock in golden outputs for Topic 1.
- Catch cases where the renderer hides a bank defect instead of fixing it.

Deliverable:

- End-to-end tests for lesson generation, question generation, and explanation repair using representative fixtures.

### Staff Learning Designer

Responsibilities:

- Verify that Topic 1 lessons remain first-time-learner friendly.
- Ensure micro-challenges are checking the right cognitive move.
- Keep DO/DON'T examples meaningfully different and concept-bound.

Deliverable:

- A locked teaching template that matches how people actually learn first-contact MongoDB concepts.

## What Should Be Fixed First

1. Freeze the canonical lesson/question contract in one spec.
2. Make generation, validation, repair, and rendering all consume that same contract.
3. Add semantic Topic 1 validation on both question text and option text.
4. Add repair for question text and options, not just explanation text.
5. Introduce content versioning and a legacy flag.
6. Run a targeted migration on existing Topic 1 items.
7. Add integration tests that fail on the exact drift the user saw in the CLI.

## Success Criteria

The flow is actually fixed when all of these are true:

- Teach mode no longer produces invalid Topic 1 syntax examples.
- Micro-challenges stay open-ended unless multiple choice is truly required.
- Practice questions never invent BSON type names.
- Repair jobs can quarantine or rewrite legacy bad question text.
- The CLI renderer no longer needs to hide quality problems created upstream.

Until those are all true together, the system is still only partially consistent.
