# Decision Log

Timestamped record of product and architecture decisions.

Related: [[Memory Home]], [[active_context|Active Context]], [[coach_flow_spec|Coach Flow Spec]], [[architecture_decisions|Architecture Decisions]]

## 2026-06-03T00:00:00+05:30
- Decision: Keep the coach anchored to a single syllabus topic and concept during Teach and Check modes.
- Reason: Prevents leakage into later topics such as CRUD querying or updates before the learner has earned that context.
- Decision: Allow only concept-scoped follow-up examples, with at most two examples and no forward topic previews.
- Reason: Keeps the explanation useful without confusing the learner with premature material.
- Decision: Document the active flow in markdown alongside code changes.
- Reason: The flow is part of the product behavior and needs to stay discoverable for future edits.
- Decision: Require a content contract version on every question-bank record and flag missing versions as legacy.
- Reason: Structural audit alone cannot distinguish legacy records from compliant records, and missing versioning is the simplest reliable legacy signal.
- Decision: Add a deterministic migration job that can promote, repair, or quarantine bank records before they reach practice.
- Reason: The practice loop must never depend on render-time cleanup to hide legacy data quality problems.

## 2026-06-11T00:00:00+05:30
- Decision: Treat exam preparation as the primary product goal and freeze immediately after the required study path is reliable.
- Reason: Optional platform work delays the learner from beginning exam preparation.
- Decision: Retire the fixed total question-bank target.
- Reason: Study readiness depends on concept coverage and valid practice workflows, not an arbitrary global count.
- Decision: Require each scheduled concept to have official documentation and five active validated questions.
- Reason: The daily learning loop promises an exact five-question gate and must not schedule concepts that cannot complete it.
- Decision: Execute the approved build order one phase at a time and review before continuing.
- Reason: This limits scope drift and prevents premature live-database operations.
- Decision: Use `qwen3.5:4b` as the default study model for the minimum 16 GB RAM / 6 GB NVIDIA GPU target.
- Reason: The interactive study path needs good-enough responses at practical local latency.
- Decision: Use `gemma4:12b` for question population and explanation repair.
- Reason: Offline content work can trade speed for stronger structured generation and repair quality.
- Decision: Treat legacy `MODEL` as a study-only compatibility setting.
- Reason: Population and repair must never silently inherit an interactive model chosen for speed.
- Decision: Use direct active-contract concept mapping as the single readiness rule for scheduling, practice, and completion.
- Reason: Broad topic fallback can falsely present unrelated questions and mark an untested concept complete.
- Decision: Refuse to start concept practice unless three active Easy and two active Medium questions are available.
- Reason: A total-only gate allows Hard or arbitrary questions to replace the intended first-pass learning progression.
- Superseded decision: Do not use `4 Easy + 3 Medium` or any other default population buffer.
- Reason: Only study readiness is fixed. Additional volume should respond to retake variety, weak areas, and mock needs.
- Decision: Keep `3 Easy + 2 Medium` as the readiness gate, but continue ordered population toward configurable per-concept inventory targets (`5 Easy + 5 Medium` by default).
- Reason: A readiness minimum is sufficient to unlock study, but a deeper inventory reduces repetition and improves practice and mock variety.
- Decision: Count only active-contract records toward study readiness.
- Reason: Legacy, repair-pending, and quarantined records cannot safely enter practice.
- Decision: Route explanation-only quality failures to `needs_explanation_repair` and structural/content failures to quarantine.
- Reason: Explanation repair can preserve sound questions, while structurally unsafe questions require manual review or replacement.
- Decision: Treat style diversity as guidance within requested generation slots, not as an additional quota.
- Reason: Style balancing must not create a hidden population target.
- Superseded decision: Default population fills only the `3 Easy + 2 Medium` readiness deficit; extras require an explicit Easy/Medium request.
- Reason: The readiness threshold should unlock study, but stopping there creates unnecessary repetition.
- Decision: Run Phase 4 repair and population in syllabus topic and concept order.
- Reason: Completing earlier concepts before later concepts creates a usable study path sooner and makes overnight progress predictable.
