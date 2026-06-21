# Project Layout

Last updated: 2026-06-03T00:00:00+05:30

Related: [[Memory Home]], [[active_context|Active Context]], [[source_ingestion_pipeline|Source Ingestion Pipeline]], [[decision_log|Decision Log]]

## Canonical Areas

- `src/certcoach/` is the packaged application code and runtime state.
- `data/` is the source corpus and seeding input used by helper scripts.
- `memory/` stores the shared, tracked Obsidian project knowledge base.
- `memory/local/` stores private or temporary notes and is ignored by Git.
- `templates/` stores shared Obsidian note templates.
- `AGENTS.md` is the authoritative vendor-neutral agent instruction entrypoint.
- `scratch/` contains experimental or maintenance scripts that are not part of the primary CLI path.

## Intentional Runtime Data

- `src/certcoach/data/chat_logs/`
- `src/certcoach/data/user_profiles.json`
- `src/certcoach/data/user_attempts.json`
- `src/certcoach/data/syllabus.json`
- `src/certcoach/data/Primary_Exam_Guide.md`

## Intentional Source Data

- `data/raw_markdowns/`
- `data/cleaned_markdowns/`
- `data/extracted_questions.json`
- `data/Primary_Exam_Guide.md`

## Removed Generated Snapshots

- `data/cleaned_profile.json`
- `src/certcoach/data/raw_profile.json`
- `src/certcoach/data/cleaned_profile.json`
- `src/certcoach/data/extracted_questions.json`

## Cleanup Rule

If a file is only a generated snapshot or scratch output and is not referenced by the active CLI or seeding pipeline, remove it. If the file is part of runtime state, question generation, or the official docs corpus, keep it and document it here.
