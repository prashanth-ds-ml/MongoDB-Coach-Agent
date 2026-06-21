# Topic 3 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[content_benchmark_index|Content Benchmark Index]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 3
- `topic_title`: CRUD Operations - Read
- `concept_name`: find() / findOne() / Projections / Cursors / sort-limit-skip / countDocuments()
- `local_subtopics`: find(); findOne(); Projections; Cursors; sort/limit/skip; countDocuments()
- `official_sources`:
  - official Topic 3 docs in `src/certcoach/data/`
- `benchmark_objectives`:
  - filter documents with equality and basic operators
  - return only selected fields with projections
  - interpret cursor behavior and pagination controls
  - compare `findOne()` with `find()`
- `example_patterns`:
  - `find()` with a filter and projection
  - `findOne()` for a single matching document
  - cursor chaining with `sort()`, `limit()`, and `skip()`
- `common_traps`:
  - confusing projection inclusion and exclusion rules
  - forgetting `findOne()` returns a single document, not a cursor
  - assuming `countDocuments()` behaves like a cursor method
  - mixing cursor iteration with result materialization
- `weak_focus`:
  - projection inclusion versus exclusion rules
  - cursor chaining with `sort()`, `limit()`, and `skip()`
  - `findOne()` versus `find()`
  - `countDocuments()` versus cursor traversal
- `generation_notes`:
  - Keep queries scoped to read semantics.
  - Prefer output-shape questions over syntax trivia.
  - Use exam-style distractors around projection and cursor misuse.
  - Reference repo objective wording here is inferred from its CRUD read section.
- `coverage_rating`: strong
- `priority`: high
- `status`: ready for prompt integration

## Crosswalk

| Local Concept | Official Doc Anchors | Reference Repo Signal | Use |
|---|---|---|---|
| find() | Topic 3 read docs | CRUD read objective cluster | Use for filter, projection, and cursor questions |
| findOne() | Topic 3 read docs | CRUD read objective cluster | Use for single-document retrieval questions |
| Projections / Cursors / sort-limit-skip / countDocuments() | Topic 3 read docs | CRUD read objective cluster | Use for output-shape, pagination, and count behavior questions |
