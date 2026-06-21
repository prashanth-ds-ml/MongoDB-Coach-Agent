# Topic 9 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[content_benchmark_index|Content Benchmark Index]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 9
- `topic_title`: Indexes & Performance
- `concept_name`: single-field / compound / unique / covered queries / performance tradeoffs
- `local_subtopics`: single-field indexes; compound indexes; unique indexes; covered queries; performance tradeoffs
- `official_sources`:
  - official Topic 9 docs in `src/certcoach/data/`
- `benchmark_objectives`:
  - identify when an index helps a query
  - distinguish common index types
  - understand basic tradeoffs between write cost and read performance
- `example_patterns`:
  - choosing a supporting index for a filter/sort pattern
  - unique index behavior
  - covered query recognition
- `common_traps`:
  - assuming every index improves every query
  - ignoring write overhead and storage cost
  - confusing compound index order with arbitrary field order
- `weak_focus`:
  - compound index field order
  - covered query recognition
  - read-performance gain versus write amplification
- `generation_notes`:
  - Keep performance questions practical and scenario-based.
  - Use indexed-vs-unindexed comparisons where helpful.
  - Reference repo objective wording here is inferred from its index objective cluster.
- `coverage_rating`: strong
- `priority`: high
- `status`: ready for prompt integration
