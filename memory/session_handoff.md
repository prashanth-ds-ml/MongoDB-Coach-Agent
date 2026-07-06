# Session Handoff

Last updated: 2026-07-06 (session 2)

Related: [[Memory Home]], [[agent_context|Agent Context]], [[next_steps|Next Steps]], [[decision_log|Decision Log]], [[study_order_map|Study Order Map]]

## Current State

- Phase: Provenance/trust rollout (see [[agent_context|Agent Context]] for the full rule set). This supersedes the Phase 4 lesson/population narrative that previously occupied this file -- that thread is not abandoned, just secondary until practice has usable inventory again.
- The provenance system (core `database.py`/`content_contract.py` changes, 6 new job scripts, ~15 new/updated test files) was implemented in a prior working session that was **never committed to git and never documented in memory** -- this was discovered and reconstructed at the start of the 2026-07-05 session by reading the working-tree diff and querying the live DB directly, since this file's prior content (last updated 2026-07-03) described an entirely different, now-stale Phase 4 narrative.
- The 2026-07-06 session proved the doc-to-question generation loop end-to-end on real data (Topic 1 BSON Data Types) and fixed 4 real bugs surfaced along the way: a population deficit-calculator that ignored the provenance gate, a citation checker that falsely rejected verbatim quotes over markdown backticks, a self-consistency model that reasoned for 14K+ characters and never answered, and a doc-scoring function that couldn't match bare `$`-operator concepts to their own reference docs. See Decision Log 2026-07-06 for full reasoning on each.
- A later 2026-07-06 session found the user had confirmed 2 of the 4 `sourced` questions independently (via `certcoach-review-questions`, outside git) and built a new read-only report, `certcoach-map-questions-to-docs`, that maps every question to its syllabus topic/concept and official doc(s) and flags citation drift. See "Completed This Session (2026-07-06, continued)" below.
- Live DB right now: 379 total questions, 2 `confirmed` (Topic 1 BSON Data Types, Easy), 2 `sourced` awaiting review (Topic 10 Embedding vs Referencing Easy, Topic 11 PyMongo purpose Easy), 375 `suspect`. Practice and mocks still have **effectively zero usable inventory** -- 2 confirmed items for one concept is well short of the `3 Easy + 2 Medium` readiness gate.
- All 249 unit tests pass. Nothing from this thread is committed yet.
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

## Next Action

1. User to run `certcoach-review-questions` themselves (interactive, human-judgment step) to confirm the 2 remaining questions currently in the review queue.
2. Decide: purge the 25 unrecoverable screenshot questions via `certcoach-purge-screenshot-backlog` (backs up first, deletes only `suspect` + `pics_qa/`-sourced), or hold for manual review.
3. Decide: investigate, regenerate, or delete the 23 `topic_id: None` suspect records -- the new doc-mapping report gives all 23 an inferred topic/concept and a doc lead, so regeneration is now a viable option, not just purge.
4. Once a few questions are confirmed, try an actual practice session to verify the full loop works end-to-end for a learner, not just at the data layer.
5. Ask before committing the uncommitted provenance-system code and all three sessions' worth of fixes/tools to git -- this is a lot of accumulated, tested, uncommitted work now.
6. Resume the Phase 4 lesson/population thread (Topics 11-12 lesson exports, population from Topic 4 `$unset`) once provenance-confirmed inventory exists to make it meaningful again.

## Known Blockers

- Practice/mocks are non-functional right now: only 2 `confirmed` questions in the live bank, both for the same concept (2 more are `sourced` and awaiting human review).
- The provenance-system code and all three sessions' fixes are uncommitted -- growing risk the longer this stays in the working tree only.
- 50 concepts (pre-provenance count) were not study-ready under the old content-contract gate alone; the provenance gate is now the binding constraint regardless.
- The self-consistency check still can't reliably catch a subtle cross-check failure (marked-correct answer contradicting the explanation) on any tested local model -- deferred, not blocking today's loop.
- Phase 5 full study-flow and mixed-mock smoke tests remain manual and are blocked on having any meaningful `confirmed` inventory.

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

# Preview next Phase 4 concept (secondary thread)
.\.venv\Scripts\python.exe -m certcoach.jobs.next_phase4_topic

# Run unit tests
.\.venv\Scripts\python.exe -m pytest tests\unit -q
```
