# Reference Repo Adoption

Related: [[Memory Home]], [[project_exam_scope|Project Exam Scope]], [[source_ingestion_pipeline|Source Ingestion Pipeline]], [[decision_log|Decision Log]]

Captured on 2026-06-17.

## Purpose

Use `yixin0829/mongodb-dev-cert-prep` together with the official MongoDB docs already in this repo as a combined content benchmark, not as a replacement for the CertCoach workflow.

The combined benchmark is valuable because:

- the official docs provide correctness and authoritative coverage
- the reference repo provides exam-objective alignment and concise study-guide phrasing

The reference repo itself is valuable because it is:

- tightly aligned to the MongoDB Associate Developer exam objectives
- rich in short MQL and PyMongo examples
- written in a study-guide style that is easy to scan
- organized around concrete objective wording rather than abstract topic names

CertCoach already exceeds both in workflow depth, persistence, and readiness gating, so adoption should be selective.

## What To Adopt

- Objective crosswalks from the reference repo into CertCoach syllabus concepts, validated against official docs.
- Short, scenario-first examples for `find`, `insert`, `update`, `aggregate`, indexes, and PyMongo.
- The exam-objective weighting as a prioritization hint for inventory and review.
- The reference repo's concise explanation style for concept lessons and answer rationales.
- Official-doc citations for any concept pack, lesson, or repair prompt.
- Atlas sample dataset orientation for hands-on examples and practice prompts.

## What Not To Adopt

- Do not flatten CertCoach back into a static study guide.
- Do not replace the existing readiness gate, lifecycle states, or persisted progress model.
- Do not copy its objective grouping verbatim when the local syllabus is already more granular and better aligned to the generation pipeline.
- Do not expose reference-material examples directly as learner answers unless they are adapted to CertCoach's explanation format and validation rules.

## Adoption Strategy

1. Build a source-coverage matrix from official docs and the reference repo objectives to the local syllabus concepts.
2. Tag each local concept with the most relevant official doc section, reference objective, example pattern, or PyMongo snippet.
3. Use the combined benchmark to improve prompt scaffolding for concept lessons and explanation generation.
4. Feed the objective weights into repair and population prioritization when concepts are under inventory targets.
5. Keep the local coaching workflow unchanged: daily agenda, scoped Q&A, five-question practice, answer review, progress persistence, and mixed mock.

## Benchmark Contract

Use the schema in [[content_benchmark_schema|Content Benchmark Schema]] as the canonical shape for the combined benchmark records.

## Expected Outcome

- Better content fidelity for exam-style wording.
- More varied and realistic question stems.
- Easier manual review because explanations are anchored to concrete objective language.
- No regression in operational behavior, because CertCoach remains the system of record for learner state and question lifecycle.
