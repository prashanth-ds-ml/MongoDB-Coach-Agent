# Topic 2 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[content_benchmark_index|Content Benchmark Index]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 2
- `topic_title`: CRUD Operations - Create
- `concept_name`: insertOne() / insertMany() / _id and ObjectId
- `local_subtopics`: insertOne(); insertMany(); _id and ObjectId
- `official_sources`:
  - `src/certcoach/data/topic_02_CRUD_Create_L1_01.md`
  - `src/certcoach/data/topic_02_CRUD_Create_L1_02.md`
  - `src/certcoach/data/topic_02_docs_languages_python_pymongo_driver_current_crud_insert__7dd55cbb21.md`
  - `src/certcoach/data/topic_02_docs_manual_tutorial_insert_documents__056e20bc9d.md`
- `benchmark_objectives`:
  - insert one document and understand the insert result shape
  - insert multiple documents and compare result semantics
  - explain automatic `_id` behavior and `ObjectId` usage
- `example_patterns`:
  - `insertOne()` with a single document and an implicit `_id`
  - `insertMany()` with multiple documents and per-document outcomes
  - PyMongo insert examples that show `inserted_id` and `inserted_ids`
- `common_traps`:
  - assuming `_id` must always be manually provided
  - confusing `insertOne()` and `insertMany()` result shapes
  - treating insert acknowledgements as proof of downstream query readiness
  - forgetting that duplicate-key behavior is tied to `_id` uniqueness
- `weak_focus`:
  - when `_id` is auto-generated versus supplied
  - single-insert versus bulk-insert return semantics
  - `inserted_id` versus `inserted_ids`
  - duplicate-key consequences on create
- `generation_notes`:
  - Keep inserts tied to document creation, not broader CRUD theory.
  - Prefer result-shape questions that distinguish single vs bulk insert behavior.
  - Use concise code snippets and avoid drift into read/update semantics.
  - Reference repo objective wording here is inferred from its CRUD create section, not copied verbatim.
- `coverage_rating`: strong
- `priority`: high
- `status`: ready for prompt integration

## Crosswalk

| Local Concept | Official Doc Anchors | Reference Repo Signal | Use |
|---|---|---|---|
| insertOne() | `topic_02_CRUD_Create_L1_01`, `insert_documents` tutorial | CRUD create objective cluster | Use for single-document insert behavior and return-shape questions |
| insertMany() | `topic_02_CRUD_Create_L1_02`, PyMongo insert doc | CRUD create objective cluster | Use for bulk-insert behavior, acknowledgements, and error handling |
| _id and ObjectId | Create lesson files + PyMongo insert doc | CRUD create objective cluster | Use for default `_id` generation, uniqueness, and ObjectId recognition |

## Initial Source Pack

- Official docs explain the exact insert API behavior.
- The reference repo should guide the style of short, practical examples.
- The highest-value Topic 2 content is:
  - one-document vs many-document insert behavior
  - `_id` generation
  - PyMongo result interpretation

## Next Use

Use this record as the benchmark input for:

1. Topic 2 lesson prompts
2. Topic 2 repair prompts
3. CRUD create population hints
4. manual review of insert questions
