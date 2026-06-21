# Preparation Tool Gap Assessment

Related: [[Memory Home]], [[active_context|Active Context]], [[next_steps|Next Steps]], [[session_handoff|Session Handoff]]

## Objective

Make CertCoach a dependable primary preparation tool for the MongoDB Associate Python Developer certification. No tool can guarantee an exam result, so the release standard is reliable syllabus coverage, technically accurate practice, and a verified end-to-end study path.

## Current Live Snapshot

Captured on 2026-06-17:

- 12/12 syllabus topics have documentation coverage.
- 58 canonical syllabus concepts.
- 7 concepts are study-ready.
- 51 concepts are blocked by insufficient active questions.
- Readiness deficits: 151 Easy and 89 Medium.
- 374 total question records.
- 87 active records.
- 196 records pending explanation repair.
- 19 records migratable without LLM repair.
- 66 quarantined records.
- Current ordered Phase 4 target: Topic 1 -> `Collections vs Tables`.
- Current target status: repair-complete, population still under the configured inventory target, and the latest bounded run exposed a throughput timeout rather than a schema failure.
- Maintained unit suite: 123 passing tests.
- Plain `pytest` collection fails because `scratch/test_zhipu_vision.py` imports the optional, unavailable `zhipuai` package.

## Release Blockers

### 1. Complete Syllabus Question Readiness

- Run bounded Phase 4 repair and population batches in canonical topic/concept order.
- Make all 58 concepts meet the `3 Easy + 2 Medium` active-question readiness gate.
- Continue toward the configured default inventory target of `5 Easy + 5 Medium` to reduce repetition.
- Recalculate readiness after every batch.

### 2. Finish Legacy Question Lifecycle Work

- Repair records marked `needs_explanation_repair`.
- Apply deterministic promotion to safely migratable records.
- Review quarantined records and decide whether to rewrite or retire them.
- Ensure inactive records never leak into learner-facing practice or mocks.

### 3. Perform Human Content Quality Review

Automated validation is necessary but cannot guarantee exam accuracy. Review representative samples from every topic and generation style for:

- technically correct answers
- unambiguous stems
- plausible but incorrect distractors
- correct PyMongo versus `mongosh` syntax and casing
- syllabus relevance
- accurate seven-part explanations
- duplicate or near-duplicate scenarios

### 4. Complete Phase 5 End-to-End Verification

Manually verify:

- daily agenda -> concept lesson -> concept-scoped Q&A -> five-question practice
- answer review and failed-practice retry behavior
- concept completion only at `4/5` or better
- progress and attempt persistence after application restart
- insufficient-question concepts remain blocked
- timed mixed mock navigation, scoring, suspend/resume, and finalize behavior
- study sessions and mock attempts persist correctly in MongoDB

### 5. Fix Repository-Wide Test Discovery

- Configure pytest to exclude scratch experiments or move optional integration experiments outside test discovery.
- Make plain `pytest` pass without requiring unrelated optional packages.
- Keep the maintained unit suite passing.

## Exam-Fidelity Validation

Before final freeze:

- Confirm mixed-mock topic distribution matches the official exam blueprint.
- Confirm question difficulty and wording resemble certification-style decisions.
- Confirm multiple-response behavior is supported where required by the exam.
- Confirm high-weight domains receive adequate practice and mock representation.
- Run several real study sessions and verify weak concepts return through spaced repetition.
- Confirm repeated practice serves sufficient question variety.

## Deferred Until After Exam

These are not blockers for dependable preparation:

- new UI work
- additional dashboards or analytics
- new gamification
- scenario simulator expansion
- general-purpose platform expansion
- nonessential RAG or reranker improvements

## Recommended Continuation Order

1. Continue bounded Phase 4 overnight batches:

   ```powershell
   .\scripts\run_phase4_overnight.ps1 -RepairBatchSize 25 -PopulationBatchSize 25
   ```

2. Review a human quality sample after each completed topic.
3. Continue until all concepts are study-ready and inventory depth is acceptable.
4. Resolve or retire remaining quarantined records.
5. Fix plain pytest discovery.
6. Execute and record the Phase 5 manual smoke-test checklist.
7. Declare feature freeze and begin daily exam preparation.

## Completion Standard

CertCoach is ready for final freeze when:

- all scheduled concepts are study-ready
- the full required study path succeeds manually
- mixed mock resume/finalize succeeds manually
- MongoDB persistence is verified
- representative content samples pass human review
- automated tests pass, including plain pytest discovery
