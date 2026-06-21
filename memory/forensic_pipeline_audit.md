# Forensic Pipeline Audit

Last updated: 2026-06-18

Related: [[Memory Home]], [[session_handoff|Session Handoff]], [[next_steps|Next Steps]], [[decision_log|Decision Log]], [[preparation_tool_gap_assessment|Preparation Tool Gap Assessment]]

## Scope

This note traces the real execution path for:

- question population
- explanation repair
- migration / classification
- readiness sequencing

It focuses on what content is fed to the model, what the model is asked to produce, what the local gates verify, and where the current contract diverges from the intended design.

## Executive Summary

The system now has two distinct model contracts:

- `question_shell` for population
- `repair` for seven-part explanation repair

That split is the right direction. The earlier failure mode was asking the population model to do too much at once. The current population path is leaner and faster, but it also bypasses some of the stronger verification that exists in the normal question path.

The main forensic findings are:

- The population path now feeds the model only a lean MCQ shell prompt.
- The repair path feeds the model a much richer explanation prompt and then reconstructs the seven-part markdown.
- The quality gate behaves differently by response kind:
  - `repair` checks the explanation schema only.
  - `question_shell` checks the MCQ shell only.
  - the default `question` path runs duplicate detection and the RAG judge.
- A previous bug in `apply_repair()` wrote contract metadata at the wrong level. That kept repaired shells from becoming active. That bug is fixed now.

## Population Flow

Current entry point:

- [`src/certcoach/jobs/nightly_seed_questions.py`](C:/Users/prash/projects/MongoDB-Coach-Agent/src/certcoach/jobs/nightly_seed_questions.py)

Population order:

1. `next_phase4_topic` or manual topic/concept filter selects the next ordered syllabus concept.
2. `audit_weighted_deficits()` computes missing inventory in canonical topic/concept order.
3. `run_weighted_seed()` loads:
   - official markdown docs for the concept
   - weak-focus benchmark text
   - the full benchmark record if present
4. `generate_weighted_question()` builds the prompt for the model.
5. The prompt now asks for a lean shell, not a full seven-part explanation.
6. The model output is parsed into `SeedMCQ`.
7. The seeder validates the shell, checks duplicates, inserts the record as `needs_explanation_repair`, and immediately hands the record to the repair job.

What the model sees in population:

- topic name and syllabus key
- concept name
- difficulty and weighted target
- concept-specific markdown docs
- weak-focus benchmark slice
- a short prompt that says:
  - ask one narrow MCQ
  - produce exactly four options
  - provide `question`
  - provide a clear correct answer marker
  - provide `citation_source`
  - do not write the seven-part explanation

What the model does not need to do anymore:

- write a full explanation
- produce a full explanation schema
- satisfy the repair judge during population

Current population gate behavior:

- `response_kind="question_shell"` in [`src/certcoach/core/model_runner.py`](C:/Users/prash/projects/MongoDB-Coach-Agent/src/certcoach/core/model_runner.py)
- deterministic checks only
- no duplicate check inside `model_runner` for shell mode
- no RAG judge inside `model_runner` for shell mode

That is a throughput tradeoff. The seeder still does its own duplicate check before insert, but the shell path is not as strongly verified as the full question path.

## Repair Flow

Current entry point:

- [`src/certcoach/jobs/repair_explanations.py`](C:/Users/prash/projects/MongoDB-Coach-Agent/src/certcoach/jobs/repair_explanations.py)

Repair order:

1. `run_repair()` loads the bank audit and filters to records explicitly marked `needs_explanation_repair`.
2. The candidate list is ordered in syllabus topic/concept order.
3. `generate_repair()` builds a rich repair prompt from:
   - the existing question stem
   - the existing answer options
   - the current explanation
   - current trap analysis
   - weak-focus benchmark text
   - full benchmark context
   - source file metadata
4. The repair model returns structured explanation fields.
5. `RepairedExplanationSchema` enforces the explanation contract.
6. The repair job reconstructs the seven-part markdown explanation.
7. `apply_repair()` writes feedback, explanation, trap analysis, and contract metadata back to MongoDB.

What the model sees in repair:

- the exact question text
- all four options, with correctness markers
- current explanation text
- current trap analysis
- weak-focus benchmark text
- the full topic benchmark context
- source citation metadata
- explicit instructions for the seven-part explanation schema

What the model must return in repair:

- `feedbacks`
- `trap_analysis`
- `explanation_correct_answer`
- `explanation_why_correct`
- `explanation_why_wrong`
- `explanation_exam_trap`
- `explanation_memory_hook`
- `explanation_practice_recommendations`
- `explanation_syntax_example`

Repair-specific finding:

- The repair job is the only place where the seven-part explanation is assembled.
- That is correct architecturally.
- The issue was not the explanation format itself.
- The issue was the metadata write path, which briefly left repaired shells in `needs_explanation_repair`.

## Migration / Classification Flow

Current entry point:

- [`src/certcoach/jobs/migrate_legacy_question_bank.py`](C:/Users/prash/projects/MongoDB-Coach-Agent/src/certcoach/jobs/migrate_legacy_question_bank.py)

Migration behavior:

- active contract records are skipped
- quarantined records stay quarantined
- Topic 1 legacy content is repaired or normalized where possible
- explanation-only failures can become `needs_explanation_repair`
- structural failures become quarantined

Important distinction:

- migration is not the same thing as repair
- migration decides whether a record can enter the new contract
- repair decides whether the explanation can be improved

## Sequencer / Order Control

Current entry point:

- [`src/certcoach/jobs/next_phase4_topic.py`](C:/Users/prash/projects/MongoDB-Coach-Agent/src/certcoach/jobs/next_phase4_topic.py)

The sequencer chooses the first topic/concept that has:

- repair pending records, or
- Easy active count below target, or
- Medium active count below target

Current behavior:

- Topic 1 `Collections vs Tables` is complete and active.
- Topic 2 `insertOne()` is now the ordered focus.
- The sequencer is doing the right thing structurally.
- The backlog now sits in Topic 2 repair records, not in Topic 1 population gaps.

## Exact Failure Modes Observed

1. Overloaded population contract
- Earlier population runs asked the model to produce a full seven-part explanation.
- That was too expensive and too brittle for local-first throughput.
- The shell split fixed the biggest throughput problem.

2. Missing metadata propagation
- `apply_repair()` originally wrote contract metadata incorrectly.
- Repaired records stayed logically stale even after their explanation was fixed.
- This caused active counts and readiness counts to diverge from the real content.

3. Shell mode bypasses the strongest gate
- `question_shell` currently avoids duplicate and judge checks inside `model_runner`.
- The seeder still catches duplicates afterward.
- There is no equivalent judge-grounding check in the shell path.
- That is a deliberate speed tradeoff, but it is weaker than the full question path.

4. Repair backlog filtering is narrow
- Repair only processes records explicitly marked `needs_explanation_repair`.
- Structural/manual items are skipped.
- This is correct for safety, but it means some backlog can remain indefinitely unless another path handles it.

5. Retry cost is still high
- Each model attempt can take tens of seconds.
- When local output misses one required field, the retry path can easily eat minutes per slot.
- This is why lean population shells help, but the throughput ceiling still matters.

## What Is Actually Happening Now

- Population is now producing lean shells.
- Repair is now responsible for rich explanations.
- The metadata write bug has been fixed.
- Topic 1 `Collections vs Tables` is active and complete.
- Topic 2 `insertOne()` is the current ordered target.
- The remaining work is not a mystery contract mismatch anymore.
- The remaining work is backlog cleanup and throughput discipline.

## Audit Conclusion

The current design is mostly correct, but the pipeline only became understandable after separating it into:

- source/context loading
- shell generation
- repair generation
- persistence/update semantics

The two biggest historical problems were:

1. asking population to do too much, and
2. not writing repair metadata back to the right MongoDB fields.

Both are now identified. The remaining audit concern is that shell population is less strongly verified than the full question path, so if we keep this design, we should be explicit about that tradeoff.
