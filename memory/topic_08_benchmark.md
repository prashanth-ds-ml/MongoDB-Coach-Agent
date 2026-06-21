# Topic 8 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[content_benchmark_index|Content Benchmark Index]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 8
- `topic_title`: Aggregation Framework
- `concept_name`: $match / $project / $group / $sort / $limit / pipeline order
- `local_subtopics`: $match; $project; $group; $sort; $limit; pipeline order
- `official_sources`:
  - official Topic 8 docs in `src/certcoach/data/`
- `benchmark_objectives`:
  - identify the purpose of each common pipeline stage
  - order stages correctly for a desired result
  - recognize how pipeline order affects output
- `example_patterns`:
  - $match before $group
  - $project to shape output fields
  - $sort and $limit for ranked top-N results
- `common_traps`:
  - placing stages in the wrong order
  - using $project when filtering is required
  - confusing aggregation output shape with source document shape
- `weak_focus`:
  - `$match` before `$group`
  - `$project` versus `$match`
  - pipeline order as a correctness constraint, not just a style choice
- `generation_notes`:
  - Keep pipeline questions stage-focused.
  - Prefer “what happens next?” and “which stage belongs here?” patterns.
  - Reference repo objective wording here is inferred from its aggregation objective cluster.
- `coverage_rating`: strong
- `priority`: high
- `status`: ready for prompt integration
