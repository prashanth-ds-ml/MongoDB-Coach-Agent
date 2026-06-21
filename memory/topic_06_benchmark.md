# Topic 6 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[content_benchmark_index|Content Benchmark Index]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 6
- `topic_title`: Query Operators & MQL
- `concept_name`: query operators / comparison / logical / element / evaluation / Atlas Search query basics
- `local_subtopics`: query operators; comparison operators; logical operators; element and evaluation operators; Atlas Search query basics
- `official_sources`:
  - official Topic 6 docs in `src/certcoach/data/`
- `benchmark_objectives`:
  - combine comparison and logical operators correctly
  - choose the right operator family for a query requirement
  - distinguish MQL operator behavior from Atlas Search concepts
- `example_patterns`:
  - `$eq`, `$ne`, `$gt`, `$lt`
  - `$and`, `$or`, `$not`
  - element and evaluation operator examples
- `common_traps`:
  - using the wrong operator family for the field type
  - mixing Atlas Search concepts into basic MQL questions
  - misreading operator precedence or query shape
- `weak_focus`:
  - comparison operators versus logical operators
  - element/evaluation operators versus basic field matching
  - when a question is actually asking for Atlas Search rather than MQL
- `generation_notes`:
  - Keep this topic operator-centric.
  - Avoid drifting into array-specific or aggregation-only examples.
  - Reference repo objective wording here is inferred from its query objective cluster.
- `coverage_rating`: strong
- `priority`: high
- `status`: ready for prompt integration
