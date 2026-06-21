# Question Bank Inventory Comparison

Related: [[Memory Home]], [[lesson_practice_consistency_audit|Lesson / Practice Consistency Audit]], [[legacy_bank_migration_report|Legacy Bank Migration Report]], [[architecture_decisions|Architecture Decisions]]

Last updated: 2026-06-03T00:00:00+05:30

## Purpose

Before any migration or quarantine action, compare the live question bank against:

- the active content contract
- the syllabus target set
- the current repairability rules

This report is the decision layer. It answers:

- What is active?
- What is legacy?
- What is repairable?
- What must be quarantined?
- Where are the target gaps?

## Report Command

Use the comparison report job to inspect the bank:

```bash
python -m certcoach.jobs.question_bank_comparison_report
```

Optional filters:

- `--topic` to narrow to a topic or concept
- `--limit` to cap the number of records processed

## What It Compares

### 1. Active vs Legacy

- Active records are current contract records with a valid version and allowed status.
- Legacy records are missing the current contract version or use a non-active status.

### 2. Repairable vs Quarantine

- Repairable records can be brought back into the current contract with deterministic fixes.
- Quarantine records are too risky or too inconsistent to trust in practice.

### 3. Target vs Inventory

The report compares the bank against the syllabus target set:

- topic
- concept
- difficulty
- target count
- current active count
- current legacy count
- delta from target

## Decision Rules

1. If a record is active and fits the target, keep it.
2. If a record is legacy but deterministically repairable, migrate it.
3. If a record is legacy and cannot be repaired safely, quarantine it.
4. If a target is underfilled after migration, seed new content for that target.
5. If a target is overfilled with low-quality duplicates, dedupe or retire the extras.

## Why This Exists

The comparison step prevents a common failure mode:

- migrating first
- discovering later that the bank shape was not what we thought it was

That is the wrong order. Comparison comes first so the next decision is grounded in the actual data.
