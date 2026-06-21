# Legacy Bank Migration Report

Related: [[Memory Home]], [[lesson_practice_consistency_audit|Lesson / Practice Consistency Audit]], [[architecture_decisions|Architecture Decisions]], [[lesson_template_rules|Lesson Template Rules]]

Last updated: 2026-06-03T00:00:00+05:30

## What Was Implemented

### 1. Shared content contract

File: `src/certcoach/core/content_contract.py`

This module now centralizes:

- the current content contract version
- Topic 1 semantic detection
- invented BSON type detection
- Topic 1 option normalization
- Topic 1 question template suggestions
- practice eligibility checks

This gives the codebase one place to describe what counts as current versus legacy content.

### 2. Version stamping

Generated and repaired records now receive:

- `metadata.content_contract_version`
- `metadata.content_contract_status`
- `metadata.content_contract_source`

This makes the bank auditable and lets legacy content be distinguished from migrated content.

### 3. Practice filtering

Practice retrieval now excludes records that are not active under the current contract.

That means quarantined and unversioned legacy items no longer leak into the learner-facing practice loop.

### 4. Deterministic migration job

File: `src/certcoach/jobs/migrate_legacy_question_bank.py`

The migration job does three things:

- promotes already-compliant records to the current contract version
- deterministically repairs obvious Topic 1 legacy vocabulary in question text and options
- quarantines records that cannot be safely repaired

### 5. Audit tightening

The explanation audit now treats missing content contract versioning as a legacy signal.

That means old records are visible in audit output instead of blending in with current content.

## Operational Flow

1. Generate or repair content.
2. Stamp the record with the content contract version.
3. Run the migration job on the existing bank.
4. Quarantine anything that cannot be safely repaired.
5. Keep practice retrieval restricted to active content only.
6. Re-run the explanation audit after migration.

## What Gets Repaired Automatically

The migration job can repair the obvious Topic 1 vocabulary drift:

- `embeddedDocument` -> `embedded document`
- `subdocument` -> `embedded document`
- `documentArray` -> `array`
- `subdocumentArray` -> `array`
- `embeddedDocumentArray` -> `array`

If the repaired record still fails validation, it is quarantined instead of being shown to learners.

## What Still Needs Human Review

- legacy records with bad explanation quality after structural migration
- records whose question text cannot be safely mapped to a canonical Topic 1 template
- any quarantined record that is important enough to rewrite by hand rather than drop

## Recommended Runbook

1. Run the migration job in dry-run mode first.
2. Review the promoted, repaired, and quarantined counts.
3. Re-run the migration in apply mode.
4. Run the explanation repair job on the active bank if explanation quality is still weak.
5. Run the full unit test suite.
6. Audit the bank again and verify that legacy counts dropped to zero or an expected quarantine floor.

## Current Status

The bank now has a versioned contract, a migration path, and a quarantine path.

The remaining work is operational:

- run the migration on the live bank
- inspect quarantined records
- decide which quarantined items should be hand-rewritten versus retired
- confirm practice only serves active contract records
