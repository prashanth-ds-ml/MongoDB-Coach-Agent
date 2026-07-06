# Session Handoff

Last updated: 2026-07-06 (session 3)

Related: [[Memory Home]], [[agent_context|Agent Context]], [[next_steps|Next Steps]], [[decision_log|Decision Log]], [[study_order_map|Study Order Map]]

## Current State

- Phase: Provenance/trust rollout, now committed (see [[agent_context|Agent Context]] for the full rule set). This supersedes the Phase 4 lesson/population narrative that previously occupied this file -- that thread is not abandoned, just secondary until practice has usable inventory again.
- **Committed to git** (branch `codex/publish-bank-loop`, nothing pushed): `730d8e7` (provenance/trust rollout -- 107 files) and `f350d2a` (unrelated flashcards.json data sync, split out separately). The 3-sessions-deep uncommitted-work risk flagged in every prior handoff is resolved for that work specifically -- but see below, the weighted-target work built *after* those commits is itself uncommitted again.
- **Learner history wiped for a fresh start** (user's explicit request): `user_attempts`, `user_study_sessions`, `user_profiles`, `lesson_artifacts` all cleared (20/4/3/58 docs), backed up to `backups/learner-history-backup-20260706-201216/`. Question bank and login untouched.
- **Topic 1 BSON Data Types reset to true zero**: user chose "discard and redo" over keeping the 2 already-confirmed questions, so those were also deleted (backed up to `backups/bson-data-types-confirmed-backup-20260706-210908/`). Concept #1 in canonical study order now has 0 confirmed, 0 sourced, 29 inert `suspect` legacy questions left purely as generation reference.
- **25 unrecoverable screenshot-sourced suspects purged** (`certcoach-purge-screenshot-backlog`, auto-backed up). The 23 orphan (`topic_id: None`) suspects were kept, folded into the seeding loop as regeneration signal per `map_questions_to_docs.py`'s inferred topic/concept -- not purged, not confirmed.
- **Population targets are now exam-weighted, not flat** (see Decision Log 2026-07-06 continued for full reasoning): `question_targets.build_weighted_targets` cascades the real `EXAM_DOMAIN_WEIGHTS` (51/18/17/8/4/2, previously used only by the mock exam) down through topic and concept, so high-weight concepts (Drivers 18%, Indexes 17%) get deeper targets and low-weight ones (Tools 2%) stay near the floor. The `3 Easy + 2 Medium` readiness gate itself is unchanged -- it mirrors a hardcoded practice-session composition in `cli.py`, a separate product/UX decision this work did not touch. `nightly_seed_questions.audit_weighted_deficits` now actually consumes the weighted target for the default (no `--target-easy`/`--target-medium`) path; explicit CLI overrides still apply flatly as before. Generation shortfalls (concept can't reach target after retries) are now reported explicitly at the end of a `certcoach-seed-nightly` run instead of silently accepted.
- Live DB right now: 354 total questions, 0 `confirmed`, 0 `sourced`, 354 `suspect` (all inert, reference-only). **Practice has zero usable inventory** -- starting genuinely from scratch at concept #1.
- All 255 unit tests pass (249 baseline + 6 new: 5 for the weight cascade in `question_targets.py`, 1 more replacing a test that encoded the old flat-target behavior, plus 2 in `nightly_seed_questions` verifying the weighted-vs-explicit-override paths).
- New reference: [[study_order_map|Study Order Map]] -- the full syllabus-to-official-docs mapping for all 58 concepts across 93 docs, in canonical study order.

## Completed This Session (2026-07-05)

1. **Reconstructed the undocumented provenance system** by reading `git diff HEAD` across `database.py`, `content_contract.py`, `cli.py`, `judge_questions.py`, `nightly_seed_questions.py`, `config.py`, and all six new `jobs/` scripts, then verified against the live DB rather than trusting docstrings alone.
2. **Ran `certcoach-reocr-pics-qa`** to completion: 69/69 screenshots transcribed (66 newly OCR'd with `glm-ocr:latest`, 3 already done, 0 failures) into `src/certcoach/data/pics_qa_transcripts/`.
3. **Found and fixed a real bug in `analyze_backlog.py`**: `_has_real_doc_lead()` only matched a question's `citation_source` against a literal filename in `cleaned_markdowns/`, but every legacy question stores `citation_source` as a human-readable title (e.g. `"Find One Document"`) or a mongodb.com URL, never the corpus's real filenames -- so the check always returned `False` for the legacy backlog regardless of whether real docs existed. Added a topic-level fallback (`_topic_has_cleaned_markdowns`) that checks whether any `topic_{NN}_*` file exists for the question's `topic_id`. Updated 3 existing unit tests in `tests/unit/test_analyze_backlog.py` that had encoded the old, narrower behavior, and added one new test for the corrected behavior. All 239 tests still pass.
4. **Re-ran `certcoach-analyze-backlog`** with the fix: of 376 suspect questions, 353 now correctly show a real regeneration lead (topic has official docs), 23 (`topic_id: None`) have no lead at all, 0 are duplicates. Before the fix, the script reported 0 `has_doc_lead` and would have wrongly signaled that all 376 (minus 26 screenshot ones) were safe to delete.
5. **Ran `certcoach-recover-screenshot-citations`** against the true screenshot-sourced count (26 records, not the ~333 the docstrings assumed -- most suspect questions are legacy-generated, not screenshot-sourced). Result: 1 recovered to `sourced`, 25 confirmed unrecoverable (no supporting quote findable in the transcript), consistent with the known original-extraction-rewrote-content problem documented in `purge_screenshot_backlog.py`.

## Completed This Session (2026-07-06)

1. **Deleted `scratch/`** (24 unreferenced, already-gitignored debug scripts, including the known pytest hazard file) after confirming nothing imports it.
2. **Drafted then dropped `inspect_doc.py`** (a per-doc question-yield estimator) after the user redirected toward the simplest working loop; removed the file, its test, and its entry point rather than leave dead scaffolding.
3. **Fixed `nightly_seed_questions._get_db_style_counts()`** to gate on `database.is_practice_ready()` instead of `is_contract_active()` alone -- the deficit calculator was blind to the provenance gate and reported 0 generation slots needed for concepts that are actually 100% unconfirmed.
4. **Proved the full doc-to-question loop live** on Topic 1 → BSON Data Types: correct doc pulled, MCQ generated with a style tag and citation, seven-part explanation attached.
5. **Fixed `database.verify_citation()`** to strip markdown emphasis punctuation before comparing quote to source -- a genuinely verbatim quote was being rejected only because the doc wrapped the same words in backticks.
6. **Benchmarked 5 local Ollama models** for the self-consistency check and switched the default from `deepseek-r1:8b` (produced 14,000+ characters of reasoning and still timed out) to `qwen2.5-coder:7b` (fast and correct on the genuinely-good test case). Noted but deferred: none of the 5 models reliably caught a deliberately-broken test case, a separate prompt-design weakness.
7. **Reprocessed the 2 live test questions** through the fixed pipeline -- both now `sourced`.
8. **Improved `review_questions.py`**: full seven-part explanation now renders as Markdown (was silently truncated at 800 characters, cutting off the last 4 of 7 sections); source filename is now a clickable `file://` link (Windows Terminal renders this as clickable; older console hosts won't); removed the "Source excerpt" preview entirely (redundant now that the file is one click away, and its own quote-matching logic didn't share the markdown fix in #5).
9. **Fixed `planner.score_md_file_for_concept()`** to strip `$` from concept tokens -- bare-operator concepts (`$set`, `$elemMatch`, `$match`, etc.) were scoring 0 against their own dedicated reference docs because filenames never contain a literal `$`. Improved doc resolution for Topics 4, 7, and 8.
10. **Built and saved [[study_order_map|Study Order Map]]**: all 58 syllabus concepts mapped to their official doc(s) in canonical study order, generated after the fix above.

## Completed This Session (2026-07-06, continued)

1. **Verified live state instead of trusting the last snapshot**: found the working tree byte-identical to the prior handoff, but the live DB had moved -- the user confirmed 2 of the 4 `sourced` questions independently via `certcoach-review-questions` between sessions, and 2 new suspect records had appeared. Corrected a mid-investigation false alarm: an initial query used top-level `topic_id`/`concept` fields, which don't exist on question documents (they live under `metadata.*`), and wrongly suggested 375/379 suspect records had no topic at all; re-querying the correct field path confirmed the real count matches the known 23.
2. **Built `certcoach-map-questions-to-docs`** (`src/certcoach/jobs/map_questions_to_docs.py`), a read-only report requested by the user to map every question to its syllabus topic/concept and official doc(s), explicitly scoped to no DB writes (user's choice among three offered options). Reuses `find_best_concept()` from the existing `map_questions.py` job for topic-id-less records and the same `planner.score_md_file_for_concept()`/`prioritize_md_files()` scoring that built [[study_order_map|Study Order Map]]. Added entry point `certcoach-map-questions-to-docs` (`pyproject.toml`) and 8 unit tests (`tests/unit/test_map_questions_to_docs.py`).
3. **Ran it against the live bank**: 356/379 questions had stored topic/concept; the 23 orphaned records were placed via inference (none stayed fully unmapped). 238 questions resolve to a concept-exact official doc, 118 fall back to topic-level docs (genuine corpus gaps, same pattern as `study_order_map.md`), 23 have no topic to resolve a doc against at all. 333/379 questions carry a citation value that isn't one of the resolved official docs -- expected, since legacy `citation_source` is a human-readable title or URL, never a real filename. Full per-question detail written to a scratch CSV (not committed, regenerate with `--out <path>` when needed).
4. Reinstalled the package (`pip install -e .`) to register the new entry point; full suite verified at 249/249 passing.

## Completed This Session (2026-07-06, session 3)

1. **Committed** the 3-sessions-deep provenance/trust rollout (`730d8e7`) and a separate unrelated flashcards.json sync (`f350d2a`); deleted a stray garbled debug file that had no reference anywhere.
2. **Wiped learner history** (`user_attempts`, `user_study_sessions`, `user_profiles`, `lesson_artifacts`) at the user's explicit request, backed up first, to give a genuinely fresh start.
3. **Reset Topic 1 BSON Data Types to true zero**, including deleting its 2 already-confirmed questions per the user's explicit "discard and redo" choice, backed up first.
4. **Purged the 25 confirmed-unrecoverable screenshot suspects**; kept the 23 orphan suspects as regeneration signal rather than purging them.
5. **Built the exam-weighted population target system**: `question_targets.topic_exam_weight_map()` cascades the real `EXAM_DOMAIN_WEIGHTS` down through topic and concept (replacing the flat 5E/5M-for-everyone default); `nightly_seed_questions.audit_weighted_deficits` now consumes it for the default path; added a shortfall report; updated `AGENTS.md`/`agent_context.md`'s documented rule. 255/255 tests pass. **This code (question_targets.py, nightly_seed_questions.py, database.py, AGENTS.md, agent_context.md, 2 test files) is not committed.**
6. Dry-ran the new weighted targets against Topic 1 BSON Data Types (confirmed correct: 16 slots, 7 Easy + 9 Medium) but stopped before any live generation -- no questions generated yet this session.

## Next Action

1. Ask before committing the weighted-target work (9 modified files, listed above) -- it's tested but uncommitted, the same pattern that grew risky before.
2. Start the per-concept loop at concept #1 (Topic 1, BSON Data Types -- now genuinely at zero): `certcoach-seed-nightly --topic 1 --concept "BSON Data Types"`, which now uses the exam-weighted target instead of a flat one. A first small batch (`--max-questions 3`) was suggested but not yet run.
3. Run `certcoach-review-questions` scoped to Topic 1 to confirm what gets generated.
4. Check the weighted target was actually reached (not just the 3E+2M floor) before moving to concept #2 in `study_order_map.md` order; watch for the new shortfall report at the end of the seed run if the doc corpus can't sustain it.
5. Once a few concepts are confirmed, run an actual practice session to verify the learner-facing loop, not just the data layer.
6. Resume the Phase 4 lesson/population thread (Topics 11-12 lesson exports, population from Topic 4 `$unset`) only after provenance-confirmed inventory exists to make it meaningful again.

## Known Blockers

- Practice/mocks have **zero** usable inventory right now (Topic 1's prior 2 confirmed questions were deliberately reset) -- this is the expected starting state for the fresh-start loop, not a bug.
- The self-consistency check still can't reliably catch a subtle cross-check failure (marked-correct answer contradicting the explanation) on any tested local model -- deferred, not blocking today's loop.
- Phase 5 full study-flow and mixed-mock smoke tests remain manual and are blocked on having any meaningful `confirmed` inventory.
- The exam-weighted population target has been unit-tested and sanity-checked against the real syllabus (weights sum to 100%, high/low-weight concepts differentiate as expected) but not yet exercised through a real `certcoach-seed-nightly` run -- Topic 1 is the first live test.

## Commands

```powershell
# Provenance/trust pipeline
.\.venv\Scripts\python.exe -m certcoach.jobs.analyze_backlog
.\.venv\Scripts\python.exe -m certcoach.jobs.map_questions_to_docs --out <path.csv>
.\.venv\Scripts\python.exe -m certcoach.jobs.backfill_provenance --dry-run
.\.venv\Scripts\python.exe -m certcoach.jobs.reocr_pics_qa
.\.venv\Scripts\python.exe -m certcoach.jobs.recover_screenshot_citations
.\.venv\Scripts\python.exe -m certcoach.jobs.purge_screenshot_backlog
.\.venv\Scripts\python.exe -m certcoach.jobs.review_questions

# Per-concept seeding loop (now exam-weighted by default)
.\.venv\Scripts\python.exe -m certcoach.jobs.nightly_seed_questions --topic 1 --concept "BSON Data Types"

# Preview next Phase 4 concept (secondary thread)
.\.venv\Scripts\python.exe -m certcoach.jobs.next_phase4_topic

# Run unit tests
.\.venv\Scripts\python.exe -m pytest tests\unit -q
```
