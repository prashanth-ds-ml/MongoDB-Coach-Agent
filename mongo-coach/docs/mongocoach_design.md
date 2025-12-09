# MongoCoach – Overall Design

## Goal

Build an AI-powered coach to help users clear the
**MongoDB Associate Developer – Python** certification on the first attempt.

## Agents

1. Scraper & Indexer Agent
2. Question Generator & Reviewer Agent
3. Tutor / Coach Agent
4. Curriculum Planner Agent
5. Analytics & Insights Agent

## Data Model (MongoDB – planned)

- `sources`: raw scraped pages with metadata
- `docs_chunks`: RAG-ready text chunks + embeddings
- `exam_objectives`: official objectives for ASSOC_DEV_PY
- `questions_bank`: curated + generated questions
- `users`: learner profiles
- `user_progress`: per-user mastery tracking
- `practice_sessions`: logs of question attempts

This document is a living spec to guide implementation.
