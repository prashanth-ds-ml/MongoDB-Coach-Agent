# Topic 12 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[content_benchmark_index|Content Benchmark Index]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 12
- `topic_title`: Tools, Tooling & Atlas Search
- `concept_name`: Atlas overview / sample datasets / Atlas Search indexes / Atlas Search queries / tooling basics
- `local_subtopics`: Atlas overview; Atlas sample datasets; Atlas Search indexes; Atlas Search queries; tooling and operational basics
- `official_sources`:
  - official Topic 12 docs in `src/certcoach/data/`
- `benchmark_objectives`:
  - identify Atlas as the managed MongoDB platform context
  - understand sample datasets and tooling basics
  - distinguish Atlas Search index setup from basic query usage
- `example_patterns`:
  - Atlas sample dataset use cases
  - search index creation and query examples
  - tooling workflow examples around Atlas features
- `common_traps`:
  - confusing Atlas Search with regular MQL query operators
  - assuming all Atlas features are part of core server CRUD behavior
  - mixing tooling and application-layer driver behavior
- `weak_focus`:
  - Atlas Search versus core MQL query operators
  - when a question is about tooling rather than data access
  - sample dataset workflow versus production query workflow
- `generation_notes`:
  - Keep Atlas Search and Atlas tooling clearly separated from core query topics.
  - Use scenario-based prompts that identify the correct feature family.
  - Reference repo objective wording here is inferred from its tooling/Atlas objective cluster.
- `coverage_rating`: strong
- `priority`: medium-high
- `status`: ready for prompt integration
