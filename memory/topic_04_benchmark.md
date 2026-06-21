# Topic 4 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[content_benchmark_index|Content Benchmark Index]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 4
- `topic_title`: CRUD Operations - Update
- `concept_name`: replaceOne() / updateOne() / updateMany() / $set / $push / $inc / $unset / upsert / findAndModify
- `local_subtopics`: replaceOne(); updateOne(); updateMany(); $set; $push; $inc; $unset; upsert; findAndModify
- `official_sources`:
  - official Topic 4 docs in `src/certcoach/data/`
- `benchmark_objectives`:
  - distinguish replacement from modifier-based updates
  - apply field-level updates with common operators
  - explain upsert behavior and update scope
  - recognize legacy `findAndModify` terminology
- `example_patterns`:
  - `$set` for targeted field changes
  - `$inc` for numeric increments
  - `$push` for array updates
  - upsert examples with create-on-miss behavior
- `common_traps`:
  - confusing replacement with partial update
  - applying array operators to non-array fields
  - forgetting update filters control which documents change
  - treating upsert as always creating a document
- `weak_focus`:
  - replacement versus modifier-based updates
  - upsert behavior and create-on-miss semantics
  - `$set` versus `$inc` versus `$push`
  - when `findAndModify` is the legacy term being tested
- `generation_notes`:
  - Keep the update operator focus narrow.
  - Use result-shape and behavior questions to separate update APIs.
  - Prefer question stems that test operator choice and side effects.
  - Reference repo objective wording here is inferred from its CRUD update section.
- `coverage_rating`: strong
- `priority`: high
- `status`: ready for prompt integration
