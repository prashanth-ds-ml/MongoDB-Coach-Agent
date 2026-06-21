# Topic 7 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[content_benchmark_index|Content Benchmark Index]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 7
- `topic_title`: Querying Arrays & Embedded Documents
- `concept_name`: array matching / embedded document queries / $elemMatch / dot notation
- `local_subtopics`: array matching; embedded document queries; $elemMatch; dot notation
- `official_sources`:
  - official Topic 7 docs in `src/certcoach/data/`
- `benchmark_objectives`:
  - query arrays by matching at least one element
  - target embedded document fields using dot notation
  - use `$elemMatch` when multiple conditions must apply to one array element
- `example_patterns`:
  - dot-notation filters on nested fields
  - `$elemMatch` for compound array conditions
  - comparisons between whole-array and element-level matching
- `common_traps`:
  - applying dot notation when `$elemMatch` is required
  - assuming all array elements must satisfy a condition unless stated
  - confusing embedded document matching with exact whole-document equality
- `weak_focus`:
  - dot notation versus `$elemMatch`
  - matching one array element versus multiple constraints on the same element
  - nested document field targeting
- `generation_notes`:
  - Keep the distinction between dot notation and `$elemMatch` explicit.
  - Use nested data examples that are short but unambiguous.
  - Reference repo objective wording here is inferred from its arrays objective cluster.
- `coverage_rating`: strong
- `priority`: high
- `status`: ready for prompt integration
