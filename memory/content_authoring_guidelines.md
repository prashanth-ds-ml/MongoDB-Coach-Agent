# Content Authoring Guidelines (MCQs + Flashcards)

Last updated: 2026-07-08

Related: [[Memory Home]], [[coach_flow_spec|Coach Flow Spec]], [[decision_log|Decision Log]]

Shared reference for the `/flashcards` and `/mcqs` skills. Since session 11, Claude authors
this content directly instead of relying on local Ollama generation, to move faster toward the
user's primary goal (pass the exam at the earliest). This does not relax any existing gate --
authored MCQs still go through the identical citation-verify/self-consistency/confirm pipeline
every other question does (see `jobs/ingest_authored_content.py`); flashcards still get
validated (`jobs/flashcard_tools.py`) before merging. Local Ollama stays exactly where it
already was: the self-consistency check, and later the adaptive coach once real attempt
tracking exists.

## What makes a good MCQ here

- **One clear idea per question.** No double-barreled stems.
- **Every wrong option is a real, nameable misconception** -- if you can't say *why* a real
  test-taker would pick a distractor, it's a bad distractor. Prefer traps grounded in something
  the exam actually tests: casing/shell-vs-driver syntax, off-by-one/ordering assumptions,
  aggregation stage confusion, a specific documented limitation.
- **Grounded, never invented.** The correct answer and its citation must trace to a real,
  verbatim quote (10-30 words) from the concept's official doc. If nothing in the doc supports a
  fact you want to test, don't invent it -- pick a different fact or leave the citation empty
  (an honest empty quote fails the gate cleanly; an invented one is worse).
- **Explanation teaches, not just justifies.** Say specifically why each wrong option fails, not
  just "incorrect."
- **Difficulty match**: Easy = a single documented fact/rule; Medium = applying or combining
  facts, spotting a subtler trap.
- **Exam-style taxonomy** (`question_style_type`, matches the app's existing four types --
  reuse these names/definitions exactly, don't invent new ones):
  - **Type A** -- Syntax Selection & Trap Spotting (correct query/command/method call form)
  - **Type B** -- Theory, Constraints & Data Modeling (rules, limitations, architecture/modeling)
  - **Type C** -- Predicting Query Output (what a query/aggregation/operation returns)
  - **Type D** -- Troubleshooting, Errors & Performance (errors, exceptions, performance)
- **The syntax-example section has a hard rule, easy to get wrong**: for Type B (and any
  concept `_question_needs_syntax_example()` in `nightly_seed_questions.py` marks as not
  syntax-heavy), that section must say exactly "Not required for this concept." -- providing a
  real code example there anyway *fails* the quality gate. Don't author one for Type B.
- **Casing discipline**: mongosh-only topics must stay in camelCase syntax everywhere,
  including inside wrong-option code -- the quality gate blanket-rejects any snake_case
  appearing anywhere in a non-PyMongo topic's options, even inside a deliberate trap distractor.
  Write PyMongo-vs-mongosh confusion traps by describing the mistake in the option's *feedback*
  text instead of literally showing snake_case syntax in a standard-topic option.
- **Seven-part explanation, exact headings** (see `jobs/ingest_authored_content.py`'s
  `_assemble_explanation` for the exact template): Correct Answer, Why Correct, Why Other
  Options Are Wrong, Exam Trap, Memory Hook, Follow-Up Practice Recommendation (3-5 bullets),
  Syntax Example.

## What makes a good flashcard here

The old flashcard file (pre session-11) got this wrong: one card per broad exam objective, each
a multi-paragraph study note with embedded code blocks. That's reference material, not
something recallable in 5 seconds, which is the entire point of a flashcard between practice
sessions. The bar going forward:

- **Atomic.** One fact or rule per card, not a whole concept/objective bundled together.
- **A genuine recall prompt.** Phrase `question` as an actual question someone has to retrieve
  an answer to -- not a restated heading ("Exam objective 2.1...").
- **Short answer.** 1-3 sentences, ideally under ~300 characters and always under 600 (the
  validator in `flashcard_tools.py` flags anything longer). No large code dumps -- a tiny inline
  snippet only if the rule genuinely can't be stated without one.
- **Concept-level, not domain-level.** One card belongs to exactly one syllabus concept
  (`topic_id` + `concept`, matching MCQ granularity), not just a domain/category. This is what
  will eventually let `get_remediation_for_wrong_attempt` match a missed MCQ to the *exact*
  relevant card instead of just "something in CRUD."
- **Doc-grounded.** Quote or closely paraphrase the actual official doc; `source_doc` records
  which file it came from.
- **Schema** (see `jobs/flashcard_tools.py` for the validator): every card needs `id`,
  `topic_id`, `concept`, `category` (the exam-domain name, kept for the existing
  domain-matching code), `domain_weight_pct`, `subheading` (the closest original numbered exam
  objective, e.g. "1.1" -- shared across every card under one concept, not unique per card),
  `source_doc`, `title` (short, unique per card), `question`, `answer`. `category`, `question`,
  `answer`, `title`, `subheading` are the exact field names `mobile/` and `web-flashcards/`
  already read -- never rename them.

## Reference examples (already live, already validated)

- Flashcards: `data/flashcards.json`'s 17 Topic 1 cards (BSON Data Types, Document structure,
  Collections vs Tables) -- the first batch built to this standard.
- MCQs: the 3 solid confirmed/sourced questions found during the session-11 quality audit
  (`certcoach-t11-pymongo-purpose-easy-003-...`, `certcoach-t01-bson-data-types-easy-002-...`,
  `certcoach-t01-bson-data-types-easy-005-...` -- query `provenance.state` for current examples,
  since the live set changes).

## Tools

- `python -m certcoach.jobs.flashcard_tools <new_cards.json> [--remove-topic-id N] [--validate-only]`
  -- validates and merges new flashcards into all three bundled copies atomically.
- `certcoach.jobs.ingest_authored_content.ingest_authored_question(authored_dict)` -- runs one
  authored MCQ through the full existing pipeline (duplicate check, quality gate, insert,
  citation verify, self-consistency) and stores its resulting provenance. See the module
  docstring for the exact `authored` dict shape.
