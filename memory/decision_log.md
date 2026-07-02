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

## 2026-06-16T00:00:00+05:30
- Decision: Implement model chain with quality gates for population and repair jobs.
- Reason: Single-model dependency risks quality failures; fallback to Cloudflare/OpenRouter APIs (already configured) provides resilience without additional local VRAM.
- Decision: Quality pipeline: Deterministic checks → Duplicate detection (stem hash) → LLM Judge (RAG-grounded against source markdown) → Retry with fix hint → Fallback model.
- Reason: Catches 40%+ issues free (format/casing), prevents duplicates early, verifies technical faithfulness to source docs.
- Decision: Structured JSONL logging per attempt to `logs/model_quality.jsonl` with verdict, flags, latency, tokens, model, source files.
- Reason: Enables post-run analysis of fallback rates, duplicate rates, model performance, prompt tuning.
- Decision: Circuit breaker per model (3 failures → 5 min cooldown) prevents repeated calls to degraded endpoints.
- Reason: Protects overnight run throughput from stalled models.
- Decision: Require `source_files` metadata on every generated question for RAG judge verification.
- Reason: Judge needs ground truth to verify answer/explanation faithfulness without human expertise.
- Decision: Use external reference repo (yixin0829/mongodb-dev-cert-prep) as exam-fidelity benchmark.
- Reason: Provides 22 verified CRUD sub-objectives, PyMongo syntax patterns, and "Given scenario → identify correct output" question format matching certification style.
- Decision: Do not pull additional local models; use existing `gemma4:12b` + API fallbacks.
- Reason: VRAM unload/load cycles (30-60s) destroy throughput; API fallbacks are fast and free-tier sufficient.
- Decision: Use direct HTTP adapters for OpenRouter and Cloudflare Workers AI in `model_runner.py` instead of optional LangChain provider packages.
- Reason: The repair and population jobs should not fail when `langchain_openrouter` or `langchain_cloudflare` are absent; the provider APIs already expose stable HTTP endpoints, and the model runner only needs text completion responses.

## 2026-06-16T00:00:00+05:30 (Implementation Complete)

- Decision: Implement `model_runner.py` with full quality gate pipeline.
- Reason: Centralize multi-provider calling, deterministic checks, duplicate detection, circuit breaker, and JSONL logging in one module.
- Decision: Implement `judge_questions.py` with RAG-grounded verification.
- Reason: Verify technical faithfulness to source docs, catch invented types (Topic 1), validate explanation structure, and check context grounding.
- Decision: Wire quality gates into `nightly_seed_questions.py` and `repair_explanations.py` via `model_runner.generate_with_quality_gate()`.
- Reason: Replace fragile direct LLM calls with robust quality-gated generation that logs every attempt.
- Decision: Add `source_files` metadata field to `database.save_generated_question()`.
- Reason: Judge needs ground truth source files to verify answer/explanation faithfulness without human expertise.
- Historical decision (superseded): Configure cloud-first model chains: OpenRouter `gpt-oss-120b`/`gpt-oss-20b` → Cloudflare `@cf/meta/llama-3.3-70b-instruct` → Local Ollama fallback.
- Reason: Local models (`gemma4:12b`, `qwen3:14b`, `qwen2.5-coder:7b`) were timing out on structured JSON output; cloud models provide reliable structured output with free-tier rate limits.
- Status: Superseded by the later local-first ordering decision once the prompt/response contract was tightened and the string-vs-dict validation split was implemented.
- Decision: Use direct HTTP adapters for OpenRouter and Cloudflare in `model_runner.py` instead of optional LangChain provider packages.
- Reason: Eliminates optional dependency failures; provider HTTP APIs are stable and the runner only needs text completion responses.
- Decision: Prioritize local Ollama models before cloud fallback providers for population and repair chains.
- Reason: The tightened prompt/response contract should try the local model first to minimize remote latency and API dependency, while keeping cloud-free APIs as fallback if Ollama fails.
- Decision: Treat population and repair as separate response contracts.
- Reason: Population emits string options plus a `correct_answer`, while repair emits the seven-part explanation schema; the quality gate must validate them differently to avoid false failures.

## 2026-06-17T00:00:00+05:30

- Decision: Population now uses a lean `question_shell` contract and hands successful shells to immediate explanation repair.
- Reason: The full seven-part explanation contract was too expensive and unreliable on the population path, especially under local-first throughput constraints.
- Decision: Keep the seven-part explanation schema in the repair job, not the population job.
- Reason: Repair is the right place to produce rich explanation text; population should only create the minimum viable MCQ shell.

- Date: 2026-06-18
- Decision: `apply_repair()` must write `content_contract_*` fields under `metadata.*`.
- Reason: Top-level contract metadata leaves repaired shells stuck in `needs_explanation_repair`, which hides active records from readiness counts.

- Date: 2026-06-18
- Decision: `question_bank_comparison_report` must count stored `needs_explanation_repair` records directly, and `repair_explanations` must select repair candidates from that stored backlog.
- Reason: Audit-only reclassification undercounts repairable Topic 1 backlog and lets the sequencer skip ahead to later topics before Topic 1 is actually cleared.

- Date: 2026-06-18
- Decision: Split legacy classification into `repair` for explanation-only fixes and `regenerate` for structurally bad or Topic 1-rescued records, with a new `needs_question_regeneration` status.
- Reason: Topic 1 backlog contains both explanation-only repairs and question-shape problems; treating them as one category hides salvageable records and makes the sequencer inaccurate.

- Date: 2026-06-18
- Decision: Count repair backlog by exact `topic_id + concept` scope instead of free-text topic labels.
- Reason: Legacy Topic 1 records can carry malformed `metadata.topic` values even when the topic id and concept are correct, so free-text matching hides backlog from the selector.

- Date: 2026-06-18
- Decision: Include non-target difficulty records in concept-level backlog counts.
- Reason: Hard-difficulty records can still need repair and should keep a concept from appearing clean before the backlog is actually cleared.

- Date: 2026-06-18
- Decision: Add a repeat-until-clean overnight runner mode that reselects the next incomplete concept within the same topic after each repair/population pass.
- Reason: Topic 1 backlog is concept-ordered and can be drained more reliably by looping the existing repair/populate scripts until the selected concept is clean or the max-cycle cap is reached.

## 2026-06-18T00:00:00+05:30

- Decision: Run `mark_scope_leaks` before and after repair/population and quarantine future-scope records instead of leaving them active.
- Reason: Scope leaks are learner-facing regressions; quarantining them keeps practice strictly within the current syllabus concept.
- Decision: Advance Topic 2 in canonical order after `insertOne()` and `insertMany()` are clean, then move to `_id and ObjectId`.
- Reason: The ordered repair/populate loop is working, and moving forward only after the current concept is clean keeps the bank scoped and predictable.

- Date: 2026-06-18
- Decision: Allow bank-wide syllabus remapping to retag concept buckets, but treat any selector regression it triggers as a canonical-order checkpoint.
- Reason: Remapping fixes stale labels and mis-tagged questions, but it can also re-expose earlier-topic work; the selector must remain the source of truth before advancing.

- Date: 2026-06-18
- Decision: Add concept-specific variation guidance to Topic 2 population prompts, especially for `insertMany()`, to avoid repeated return-type questions.
- Reason: The duplicate gate was rejecting many near-identical `insertMany()` questions; explicit variation guidance improves throughput without weakening the quality checks.

- Date: 2026-06-18
- Decision: Add a Topic 2 `_id and ObjectId` stem guard that rejects questions which do not explicitly mention `_id` or `ObjectId`, and quarantine malformed active records instead of leaving them learner-facing.
- Reason: The quality gate allowed a malformed `_id and ObjectId` stem through even though it was not concept-scoped enough for safe practice; the new guard keeps the bank aligned with the syllabus and removes ambiguous items from the active set.

- Date: 2026-06-18
- Decision: Quarantine the final generic CRUD record that was left in Topic 2 `_id and ObjectId` after repair retries failed, and advance the selector to Topic 3 `find()`.
- Reason: The remaining record was not actually scoped to `_id and ObjectId`, so quarantining it prevented a future-scope leak and completed Topic 2 in canonical order.

- Date: 2026-06-18
- Decision: Add `-SingleQuestion` mode to `scripts/run_phase4_overnight.ps1` so repair and population can be forced to one record at a time while still using the repeat-until-clean loop.
- Reason: Topic 3 `find()` and similar concepts can stall on batch-level quality gates; single-question passes reduce timeout risk and make it easier to inspect and fix the exact failing record in the morning.

- Date: 2026-06-18
- Decision: Add a mandatory Topic 3 `find()/find_one()` repair checklist and let the overnight runner log repair/population batch failures without aborting repeat-until-clean mode.
- Reason: `findOne()` repairs were repeatedly missing required explanation fields, so the prompt now requires explicit cursor-vs-single-document wording and the runner keeps going long enough to capture the failure in logs rather than stopping the whole overnight pass.

- Date: 2026-06-19
- Decision: Force overnight long-run Topic loops to local-only model chains and close Topic 3 once the selector advances to Topic 4.
- Reason: OpenRouter and Cloudflare fallback calls were wasting time with repeated 402/400 failures, while Ollama was already succeeding; once Topic 3 reached full selector readiness, the next canonical target became Topic 4 `replaceOne()`.

- Date: 2026-06-19
- Decision: Hard-delete only quarantined records that are clearly unrecoverable or off-domain, and leave MongoDB-aligned quarantined concepts for remap or repair.
- Reason: Most quarantined records still map to syllabus concepts and should be preserved for remediation; only blank or clearly non-Mongo records were safe to remove without risking syllabus coverage.

- Date: 2026-06-19
- Decision: Process repair-pending and quarantined records by exact `topic_id + concept` in canonical syllabus order, using the same repair/populate loop.
- Reason: Flat status-based cleanup hides topic-specific backlog and makes it easy to miss mis-tagged or future-scope records; concept-scoped looping keeps remediation aligned with syllabus order and the selector.

- Date: 2026-06-20
- Decision: Treat the question-bank maintenance process as a durable cross-session loop: `selector -> exact topic/concept -> one question at a time -> repair/quarantine/validate -> recheck selector -> repeat` until every concept reaches the active inventory target.
- Reason: The bank is only ready when both the readiness gate and the population target are satisfied, and the workflow must survive restarts without losing the canonical topic/concept order.
- Decision: Add a hard leak guard for Topic 4 `replaceOne()` generation so future CRUD concepts and update operators are rejected before insertion.
- Reason: `update_one`, `update_many`, `$set`, and related later-scope terms were causing new `replaceOne()` questions to be quarantined instead of becoming active.
- Decision: Standardize the session status line to report active topic/concept, repair pending, quarantined total, quarantined repairable, hard-delete candidates, and population deficit before every one-question pass.
- Reason: The loop only works cleanly when each session starts with the same inventory snapshot and the same decision inputs.
- Decision: Scope every loop report and decision strictly to the current topic and current concept unless a broader bank-wide summary is explicitly requested.
- Reason: Cross-topic counts are useful for global reviews, but the live maintenance loop must stay focused on the active concept to avoid skipping backlog work.
- Decision: Require Ollama JSON mode in both local model adapter paths.
- Reason: Prompt-only JSON instructions still produced repeated parse failures from `gemma4:12b`; provider-level JSON mode improves response reliability before deterministic quality checks.
- Decision: Repair valid quarantined `replaceOne()` records before generating more shells when the quarantine bucket already contains usable MongoDB-aligned material.
- Reason: The generator repeatedly produced near-duplicate questions with prohibited future-scope distractors, while existing quarantined records can be corrected, revalidated, and promoted without increasing bank noise.
- Decision: Classify every quarantined record against the canonical syllabus before repair, but never activate a record as part of classification.
- Reason: Stem/correct-answer evidence can recover badly mapped questions, while separate validation, duplicate, and scope checks prevent an apparently confident mapping from becoming learner-facing prematurely.
- Decision: Preserve two inactive quarantine dispositions: `needs_manual_classification` for overlapping concepts and `keep_aside_misc` for contentless, off-domain, or unsupported questions.
- Reason: Forcing every record into a syllabus bucket would recreate the mapping errors this cleanup is intended to remove.

- Decision: Treat `quarantine_pending` as an incomplete concept in `next_phase4_topic` and triage quarantined records for the selected topic/concept before repair/population in the overnight runner.
- Reason: Quarantined backlog can be skipped if the selector only watches repair/regeneration/legacy statuses, so the maintenance loop must keep quarantined and repair-pending work in the same concept-scoped pass.

## 2026-06-29T00:00:00+05:30

- Decision: Start lesson prebuild in canonical syllabus order from Topic 1 `BSON Data Types`, separate from the active Phase 4 question-bank selector.
- Reason: Stored lessons should follow the syllabus contract from the beginning, while question-bank readiness must continue on its own ordered backlog.
- Decision: Store prebuilt lessons as concept-scoped artifacts in MongoDB with statuses `validated` or `needs_review`, and let the CLI prefer validated stored lessons before live generation.
- Reason: This removes learner-facing latency only when the lesson is already contract-compliant and avoids exposing unstable drafts.
- Decision: Run lesson prebuild with one corrective retry, but keep the better draft if the repair attempt degrades structure.
- Reason: The local lesson model can partially follow the contract, but naive repair retries can collapse the output further; the pipeline must preserve the stronger attempt.

## 2026-06-30T00:00:00+05:30

- Decision: Register a canonical lesson-completion loop per concept: `source bundle -> full lesson draft -> validation -> targeted repair -> missing-section generation -> validation -> store validated lesson -> concept-local practice audit -> remap/quarantine misaligned questions -> readiness recheck`.
- Reason: A lesson is not complete when the text alone is valid; the learner-facing concept loop is only trustworthy when the stored lesson and the active `3 Easy + 2 Medium` question set are aligned to the same concept boundary.
- Decision: Keep the lesson/practice cleanup local to the current concept before moving to the next concept.
- Reason: Topic-level or bank-wide cleanup during lesson build would blur scope, slow progress, and make it harder to prove that one concept is truly ready end-to-end.
- Decision: For Topic 1 `BSON Data Types`, treat `Collections vs Tables`, `Document structure`, document-relationship stems, query-operator leaks, and obvious junk stems as out of scope for the BSON lesson audit.
- Reason: The validated BSON lesson teaches BSON types, numeric/date precision, arrays, embedded documents, and `ObjectId`; questions outside that boundary create learner confusion even if they are still broadly MongoDB-related.
- Decision: Treat Topic 1 scope leakage as a validation failure, not a prompt preference.
- Reason: Prompt rules alone allowed `Document structure` and `Collections vs Tables` lessons to pass while still leaking `find()`, `findOne()`, `insertOne()`, projection, dot notation, and query terminology. Topic 1 lessons must fail until those future-topic references are removed.
- Decision: Add concept-specific cleanup for Topic 1 lessons after generation, including section regeneration for leaky sections and final concept-specific scrubs for `Document structure` and `Collections vs Tables`.
- Reason: The local lesson model can still sneak a few future-topic lines through even after prompt tightening; the concept loop needs deterministic cleanup to keep beginner-facing lessons strictly bounded.
- Decision: Add a hard `updateOne()` question-scope guard and variation brief that reject full-document replacement semantics and `replace_one()/replaceOne()` as the correct answer.
- Reason: The Topic 4 `updateOne()` pool had drifted completely into `replaceOne()` content, so the validator and prompt needed explicit concept-boundary enforcement before refill.
- Decision: Add the same hard scope guard and variation brief for `updateMany()` so multi-document update questions stay on update-operator semantics and do not drift into replacement wording.
- Reason: `updateMany()` is adjacent to `updateOne()` and shares the same replacement-vs-update failure mode; the generator needs concept-specific rejection logic before it can reliably populate the bank.
- Decision: Relax the syntax-example requirement for Topic 4 operator-family concepts and keep the operator-specific prompts focused on the update behavior itself.
- Reason: The repair model repeatedly failed `Topic 4` operator questions on a missing syntax-example section even after producing a correct explanation, so the hard gate blocked progress on otherwise valid content.
