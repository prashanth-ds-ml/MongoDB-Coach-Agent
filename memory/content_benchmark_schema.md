# Content Benchmark Schema

Related: [[Memory Home]], [[reference_repo_adoption|Reference Repo Adoption]], [[project_exam_scope|Project Exam Scope]], [[source_ingestion_pipeline|Source Ingestion Pipeline]]

Captured on 2026-06-17.

## Purpose

Define the shared benchmark record used to combine:

- official MongoDB docs already present in this repo
- the external `mongodb-dev-cert-prep` repo
- CertCoach's local syllabus and question lifecycle

The benchmark should improve content fidelity and exam alignment without changing CertCoach's workflow or state model.

## Benchmark Record

Each concept should have one record with these fields:

- `topic_id`
- `topic_title`
- `concept_name`
- `local_subtopics`
- `official_sources`
- `benchmark_objectives`
- `example_patterns`
- `common_traps`
- `weak_focus`
- `generation_notes`
- `coverage_rating`
- `priority`
- `status`

## Field Rules

- `official_sources` must point to the authoritative MongoDB docs already in the repo.
- `benchmark_objectives` may include one or more objectives from the reference repo.
- `example_patterns` should prefer short MQL or PyMongo snippets over long prose.
- `common_traps` should capture exam-style misconceptions, not generic study advice.
- `weak_focus` should list the highest-value mistakes or distinctions to emphasize when inventory is thin.
- `coverage_rating` should be one of `strong`, `partial`, or `thin`.
- `priority` should reflect exam weight plus current inventory or repair need.
- `status` should reflect whether the concept is ready, thin, or still blocked.

## Usage

Use the benchmark record to:

1. constrain concept lesson generation
2. improve MCQ population prompts
3. guide explanation repair
4. prioritize inventory work in weak areas
5. support human review of weak or undercovered concepts

## Non-Goals

- Do not replace `syllabus.json`.
- Do not duplicate the full official docs corpus.
- Do not mirror the external repo's folder structure.
- Do not use the benchmark as a learner-facing artifact.

## Implementation Sequence

1. Create the crosswalk for Topic 1.
2. Validate the schema against official docs and the reference repo.
3. Extend the schema to CRUD and query topics.
4. Feed the benchmark into lesson and generation prompts.
5. Add regression checks for schema completeness and source grounding.
