# Topic 11 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[content_benchmark_index|Content Benchmark Index]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 11
- `topic_title`: MongoDB Drivers & PyMongo
- `concept_name`: client/database/collection access / CRUD with PyMongo / aggregation with PyMongo / ObjectId handling / driver basics
- `local_subtopics`: client/database/collection access; CRUD with PyMongo; aggregation with PyMongo; ObjectId handling; driver basics
- `official_sources`:
  - official Topic 11 docs in `src/certcoach/data/`
- `benchmark_objectives`:
  - create and navigate MongoDB client, database, and collection objects
  - perform CRUD operations with PyMongo
  - execute aggregation pipelines through the driver
  - recognize `ObjectId` behavior in driver code
- `example_patterns`:
  - `MongoClient()` access chain
  - `insert_one()`, `find()`, `update_one()`, `delete_one()`
  - `aggregate()` with a pipeline list
- `common_traps`:
  - confusing shell/driver syntax with server-side MQL
  - treating ObjectId as a string in code paths that require the type
  - mixing collection access with document access
- `weak_focus`:
  - `MongoClient()` access chain
  - `insert_one()` versus `insertMany()` style differences in Python
  - `ObjectId` handling in driver code
  - aggregation pipeline syntax in PyMongo
- `generation_notes`:
  - Keep this topic code-focused and short.
  - Prefer Python snippets that mirror real driver usage.
  - Reference repo objective wording here is inferred from its PyMongo objective cluster.
- `coverage_rating`: strong
- `priority`: high
- `status`: ready for prompt integration
