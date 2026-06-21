# Topic 1 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[project_exam_scope|Project Exam Scope]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 1
- `topic_title`: MongoDB Overview & The Document Model
- `concept_name`: BSON Data Types / Document structure / Collections vs Tables
- `local_subtopics`: BSON Data Types; Document structure; Collections vs Tables
- `official_sources`:
  - `src/certcoach/data/topic_01_docs_manual_core_data_modeling_introduction__c1bfc595e5.md`
  - `src/certcoach/data/topic_01_docs_manual_core_databases_and_collections__6c0162b19c.md`
  - `src/certcoach/data/topic_01_docs_manual_core_document__a8bd5970ef.md`
  - `src/certcoach/data/topic_01_docs_manual_introduction__47ffc8215c.md`
  - `src/certcoach/data/topic_01_docs_manual_reference_bson_types__cf63661090.md`
- `benchmark_objectives`:
  - BSON value types and how they differ from plain JSON values
  - document shape and schema flexibility within the same collection
  - collection-versus-table terminology and the MongoDB document model
- `example_patterns`:
  - BSON examples covering `ObjectId`, strings, numbers, booleans, arrays, embedded documents, `null`, and dates
  - side-by-side comparison of two valid documents in the same collection with different fields
  - MongoDB collection storage contrasted with relational table rows and fixed columns
- `common_traps`:
  - treating collections as if they require fixed columns
  - confusing BSON document flexibility with lack of structure
  - assuming every document in a collection must share the same shape
  - mixing up BSON types with JSON text representation
- `weak_focus`:
  - BSON vs JSON value representation
  - document shape flexibility within one collection
  - collections versus tables wording
  - `ObjectId` and default `_id` behavior
- `generation_notes`:
  - Keep prompts exam-facing and short.
  - Prefer examples that show flexible document shape without drifting into CRUD syntax.
  - For repair, emphasize why the correct answer aligns with document-model terminology, not just generic NoSQL claims.
  - Reference repo objective wording here is an inference from its Topic 1 objective cluster, not a verbatim canonical schema.
- `coverage_rating`: strong
- `priority`: high
- `status`: ready for prompt integration

## Crosswalk

| Local Concept | Official Doc Anchors | Reference Repo Signal | Use |
|---|---|---|---|
| BSON Data Types | `reference_bson_types`, `core_data_modeling_introduction` | Topic 1 objective cluster around BSON types | Use for type-recognition questions, valid-value traps, and comparison against JSON/plain text |
| Document structure | `core_document`, `core_data_modeling_introduction` | Topic 1 objective cluster around documents with different shapes | Use for schema-flexibility questions and same-collection co-existence scenarios |
| Collections vs Tables | `core_databases_and_collections`, `core_document` | Topic 1 objective cluster around document model vs relational model | Use for terminology questions and relational-vs-document comparisons |

## Initial Source Pack

- Official docs are the correctness layer.
- The reference repo is the exam-style phrasing layer.
- For Topic 1, the highest-value content is:
  - BSON type recognition
  - document shape flexibility
  - collection versus table comparison

## Next Use

Use this record as the first benchmark input for:

1. concept lesson prompts
2. repair prompts for Topic 1 questions
3. MCQ population hints for Topic 1
4. human review of Topic 1 explanation quality
