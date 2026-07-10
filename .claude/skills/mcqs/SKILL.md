---
name: mcqs
description: Audit the existing question pool for a syllabus topic/concept (improve, discard, or fix single/multi-select misclassification), then author new exam-taxonomy-aware MCQs to fill what's still missing -- all through the existing citation-verify/self-consistency pipeline, no local Ollama generation call.
---

# MCQs

Two jobs in one pass for a syllabus topic/concept: **audit what's already in the bank** (every
`draft`/`sourced`/`suspect` question tagged to it -- never touch `confirmed`), then **author new
questions** to close whatever gap remains against the concept's real weighted target. Both use
the same authoring/ingestion path, so "improve an old question" and "write a new one" are the
same mechanism.

Read `memory/content_authoring_guidelines.md` first -- taxonomy definitions, the exact
quality-gate rules (syntax-example and casing, both easy to get wrong), and where to find
current solid-question examples. **Every question this skill inserts -- new or a replacement for
an old one -- goes through the identical citation-verify + self-consistency + confirm pipeline
every other question does.** Nothing here is ever auto-confirmed.

## Argument

`$ARGUMENTS` is a topic/concept reference: `--topic <id> --concept "<name>"`, a bare topic id
(covers every concept in that topic), or `next` (first topic short of its weighted target).

## Phase A -- Audit the existing pool

1. **Resolve the target topic/concept(s)** from `src/certcoach/data/syllabus.json` /
   `planner.load_syllabus()` -- `topic_id`, `topic`, `bank_topic_keys`, `subtopics`, `md_files`.
2. **Pull every existing question tagged to this topic/concept, any state except `confirmed`**:
   `database.questions_col.find({"metadata.topic_id": topic_id, "metadata.concept": concept, "provenance.state": {"$ne": "confirmed"}})`.
   Confirmed questions are a closed human decision -- don't re-litigate them here. (If you
   suspect orphans exist for this concept with `metadata.topic_id: None`, that's a separate,
   already-queued backfill job -- `certcoach-map-questions-to-docs --write` -- not this skill's
   job; mention it in your report if relevant, don't try to fix it here.)
3. **Read the concept's official doc(s) in full** (`planner.resolve_concept_docs` + read each
   resolved file from `cleaned_markdowns/`) -- you need this to judge each existing question
   against the real source, not just against how it reads on its own.
4. **Actually review the full pull from step 2, `suspect` included -- don't default to skipping
   the legacy `suspect` backlog wholesale.** A concept can easily carry 20-30+ old `suspect`
   records; that volume is not a reason to leave them all unexamined. For each one, decide one of
   four things:
   - **Keep as-is** -- already solid: accurate, on-topic, well-formed, citation checks out.
     Leave it alone.
   - **Improve** -- the core idea is sound but execution is weak (paraphrased/broken citation,
     thin or generic explanation, wrong difficulty, or a real single-vs-multi misclassification --
     see step 5), **or the underlying fact is genuinely correct but the question currently
     asserts something factually wrong** (e.g. claims a BSON array can't contain another array,
     when nesting is explicitly documented) -- if the concept's own official doc(s) can correct
     it, do that instead of just discarding. Author a full replacement (Phase B's authoring
     process, same schema) grounded in the doc, ingest it via
     `ingest_authored_content.ingest_authored_question`, then mark the old one suspect with a
     reason that names the replacement: `database.mark_question_suspect(old_id, f"superseded by {new_id}: <why>")`.
     Never edit a legacy question's fields in place -- always supersede through the same gate
     everything else goes through. **One well-grounded replacement can supersede several
     near-duplicate legacy questions at once** if they're all testing the same underlying fact
     with cosmetic rewording -- you don't need a 1:1 replacement count.
   - **Move** -- the question is well-formed and testable, but tagged to the wrong topic/concept
     (e.g. an "embedding vs. referencing" question mistagged under a BSON-typing concept because
     both share a source doc). Update `metadata.topic_id`/`metadata.concept` (and
     `metadata.syllabus_topic` if it changes) directly via `database.questions_col.update_one` so
     a future `/mcqs` pass on the *correct* topic/concept actually finds it in its own step-2
     pull. Leave it `suspect` with an updated reason unless you're also fixing its citation right
     now -- moving it correctly is enough; a full rewrite for the new concept is that future
     pass's job, not required here.
   - **Discard** -- fundamentally flawed with nothing worth salvaging even with doc help:
     off-topic, vacuous/templated filler that tests no real fact, or redundant with a question
     already `confirmed`/`sourced`/newly-authored for this same concept. Mark suspect with a
     concrete reason via `database.mark_question_suspect(old_id, reason)`.
   - **Don't just discard-and-stop when the concept is short of its weighted target** (check
     Phase B's target math -- step 6 -- before finalizing any discard). If a discarded question's
     "slot" isn't actually needed (concept already at or past target once Phase B's new
     authoring is accounted for), leaving it discarded is correct. But if the concept is still
     short, use the discard as a cue to author one more genuinely distinct fact from the doc
     rather than letting the gap sit unfilled -- more non-duplicate, well-grounded questions is
     the goal; going a little past the target is fine, being short is not.
   - **Once several old records are confirmed pure duplicates of each other or of newly-authored
     replacements, or are pure zero-value filler, it's fine to actually delete them** (not just
     leave them `suspect` indefinitely) rather than accumulate permanent clutter -- but back them
     up first (`backups/<concept-slug>-legacy-cleanup-<date>/questions.json`, matching this
     project's existing backup convention for any destructive DB operation) before running the
     delete.
5. **Check single- vs multi-select classification specifically**, for every question you touch
   (and any you're on the fence about):
   - Is `response_type` consistent with the actual correct-answer set in the doc? A question
     whose stem says "select all that apply" but has only one `is_correct` option (or vice
     versa) is miscategorized -- that's an "improve," not a "keep."
   - Does the doc support a genuine multi-select for this fact? (E.g. "which of the following
     are valid BSON types," "which of these operators work on array fields" -- concepts with a
     real set of correct answers, not just one right answer dressed up as several options.)
     If an existing single-select question is testing something that's naturally multi-select,
     that's a real quality improvement, not just a technicality -- rewrite it as multi.
   - Don't force multi-select where it doesn't fit just for variety. Most facts are genuinely
     single-answer; only convert where the doc actually supports more than one correct option.

## Phase B -- Fill what's missing (same pass, not a separate invocation)

6. **Check the real gap** after Phase A's decisions: `certcoach.core.question_targets.weighted_target_for_concept`
   against `database.get_active_question_counts_by_difficulty(topic_id, concepts=[concept])`
   (or run `certcoach-preview-concept --topic <id> --concept "<name>"` for the full report).
   Don't generate past what's actually needed.
7. **Pick a taxonomy type per new question** using
   `certcoach.jobs.nightly_seed_questions.style_weights_for_topic(topic_id)` for the topic's
   valid Type A-D set and rough weighting -- don't default every question to the same type, and
   prefer multi-select where the doc genuinely supports it (see step 5's criteria) rather than
   defaulting everything to single.
8. **Author each new question** as a dict matching
   `ingest_authored_content.build_authored_question`'s expected shape: stem, 4 options
   (`is_correct`/`is_trap`, `response_type` single or multi), a real verbatim `citation_quote`
   (10-30 words, character-for-character -- never paraphrase, leave it empty rather than invent
   one), and the full seven-part `explanation_sections`. Double-check the syntax-example and
   casing rules -- the two most common ways an otherwise-good question fails the gate.

## Ingesting (both phases funnel through here)

9. **Write the full batch** (Phase A's replacements + Phase B's new questions) to one scratch
   JSON file and ingest:
   ```
   python -m certcoach.jobs.ingest_authored_content <scratch_file.json>
   ```
   This runs every question -- replacement or new -- through: duplicate check, quality gate,
   insert, citation verify, self-consistency (local Ollama, unchanged). A broader whole-bank
   duplicate sweep beyond this per-insert check is a separate, later pass -- not this skill's job.
10. **Report one combined summary**: existing questions reviewed (kept / improved / moved /
    discarded / deleted, with reasons and categories -- e.g. "13 off-topic duplicates of each
    other, 3 vacuous filler, 2 factually wrong but corrected"), any single-to-multi conversions
    made and why, new questions authored and their resulting `sourced`/`draft`/skipped outcomes,
    coverage before vs. after against the weighted target, and anything you're unsure about that
    needs a human look.

## Do not

- Do not touch `confirmed` questions.
- Do not edit a legacy question's fields in place (beyond a `Move`'s `topic_id`/`concept`
  retag) -- supersede content via a fresh authored replacement plus `mark_question_suspect`, same
  as everything else in this pipeline.
- Do not mark anything `confirmed` yourself -- that stays a human decision, always.
- Do not invent a citation quote if nothing in the doc supports the fact -- leave it empty and
  let the gate report it, or pick a different testable fact instead.
- Do not give a Type A (syntax-heavy) question an empty/placeholder syntax example, or a Type B
  question a real one -- see the guidelines doc for the exact rule.
- Do not test content the doc doesn't cover, even to round out a taxonomy distribution or hit a
  round number.
- Do not force a multi-select conversion where the doc doesn't genuinely support more than one
  correct answer.
- Do not silently skip the `suspect` legacy backlog because it's large -- review it (see step 4);
  a big pool is exactly where duplicate/off-topic/filler cleanup and salvageable-fact rewrites
  have the most value.
- Do not discard a redundant/flawed question and leave the concept short of target without at
  least considering a genuinely distinct replacement -- see step 4's target-math check.
- Do not delete any question record without backing it up first, even when it's a confirmed
  duplicate or filler -- follow this project's existing backup-before-destructive-op convention.
