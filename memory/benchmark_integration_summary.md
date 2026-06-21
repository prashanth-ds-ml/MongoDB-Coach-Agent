# Benchmark Integration Summary

Related: [[Memory Home]], [[next_steps|Next Steps]], [[session_handoff|Session Handoff]], [[reference_repo_adoption|Reference Repo Adoption]], [[content_benchmark_index|Content Benchmark Index]]

Captured on 2026-06-17.

## Why This Happened

We compared CertCoach against `yixin0829/mongodb-dev-cert-prep` and decided not to clone it. Instead:

- official MongoDB docs remain the correctness layer
- the external repo remains the exam-style benchmark layer
- CertCoach remains the workflow and state-management layer

## What Was Added

1. Combined benchmark schema in `memory/content_benchmark_schema.md`.
2. Ordered benchmark index for all 12 syllabus topics in `memory/content_benchmark_index.md`.
3. Topic benchmark records for Topics 1 through 12 in `memory/topic_01_benchmark.md` through `memory/topic_12_benchmark.md`.
4. Weak-focus fields on every topic record so the highest-value traps come first.
5. Planner helpers to load benchmark content and weak-focus slices from the memory vault.
6. Integration of the benchmark context into:
   - lesson generation
   - population generation
   - repair generation
7. Regression tests to ensure the benchmark loader and weak-focus loader work.

## What Changed In Behavior

- Lesson prompts now see:
  - weak-focus benchmark slice first
  - official markdown docs second
  - full benchmark record third
- Population prompts now receive the same weak-focus-first context ordering.
- Repair prompts now receive the same weak-focus-first context ordering.
- Existing CLI and unit tests still pass after the integration.

## What We Learned

- Topic 1 is not just about BSON facts; the recurring weak points are BSON vs JSON representation, document shape flexibility, collections vs tables, and `_id` behavior.
- CRUD create/read/update/delete are strong candidates for benchmark-driven prompt tuning because the reference repo maps cleanly to those exam objectives.
- Query operators, arrays, aggregation, indexes, data modeling, PyMongo, and Atlas Search all benefit from weak-focus prioritization because the exam mostly tests distinctions, not definitions alone.

## Verification

- Focused slice: 71 passed
- Full unit suite: 126 passed, 1 warning

## Current State

- The benchmark layer is implemented and wired into the prompt paths.
- The next quality-improvement cycle is not structural integration; it is tuning the weak-focus text where the overnight runs still struggle.

## Next Build Order

1. Keep Phase 4 live-db batches bounded and monitor throughput.
2. Review repaired/populated content for representative concepts after each topic.
3. Tune weak-focus text for any topic that still produces low-quality output.
4. Continue until all concepts are study-ready and inventory depth is acceptable.
5. Resolve or retire quarantined records.
6. Finish the remaining Phase 5 and Phase 6 verification steps.
