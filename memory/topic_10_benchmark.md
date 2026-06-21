# Topic 10 Benchmark Record

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[content_benchmark_index|Content Benchmark Index]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Record

- `topic_id`: 10
- `topic_title`: Data Modeling
- `concept_name`: embedding / referencing / schema design tradeoffs / document growth / denormalization
- `local_subtopics`: embedding; referencing; schema design tradeoffs; document growth; denormalization
- `official_sources`:
  - official Topic 10 docs in `src/certcoach/data/`
- `benchmark_objectives`:
  - choose embedding when related data is read together
  - choose referencing when relationships or reuse require it
  - explain tradeoffs around growth, duplication, and update cost
- `example_patterns`:
  - one-to-few embedding examples
  - one-to-many or many-to-many referencing examples
  - tradeoff comparisons for read-heavy versus update-heavy workloads
- `common_traps`:
  - treating embedding as universally better than referencing
  - ignoring document size and growth constraints
  - mixing normalization language from relational design without adapting to MongoDB context
- `weak_focus`:
  - embedding versus referencing tradeoffs
  - document growth and update fan-out
  - when duplication is acceptable versus harmful
- `generation_notes`:
  - Keep modeling questions anchored in workload tradeoffs.
  - Avoid turning this into a generic database design essay.
  - Reference repo objective wording here is inferred from its data-modeling objective cluster.
- `coverage_rating`: strong
- `priority`: high
- `status`: ready for prompt integration
