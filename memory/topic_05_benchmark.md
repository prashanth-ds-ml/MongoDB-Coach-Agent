# Topic 5 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[content_benchmark_index|Content Benchmark Index]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 5
- `topic_title`: CRUD Operations - Delete
- `concept_name`: deleteOne() / deleteMany() / write concern impacts
- `local_subtopics`: deleteOne(); deleteMany(); write concern impacts
- `official_sources`:
  - official Topic 5 docs in `src/certcoach/data/`
- `benchmark_objectives`:
  - distinguish single-document and multi-document delete behavior
  - explain when a delete filter is too broad
  - understand the practical effect of write concern on deletes
- `example_patterns`:
  - delete a single match
  - delete many matches with a shared predicate
  - result interpretation with deleted counts
- `common_traps`:
  - using a broad filter when only one delete was intended
  - confusing delete behavior with update semantics
  - assuming a delete result means document backups exist
- `weak_focus`:
  - deleteOne versus deleteMany
  - filter precision and blast-radius risk
  - write concern impact on delete confidence
- `generation_notes`:
  - Keep delete questions concise and behavior-oriented.
  - Emphasize count outcomes and filter precision.
  - Reference repo objective wording here is inferred from its CRUD delete section.
- `coverage_rating`: strong
- `priority`: medium-high
- `status`: ready for prompt integration
