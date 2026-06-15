# 🏛️ Architecture Decisions

*Record of key technical choices and their rationales.*

## Model Architecture (100% Local Execution)
- **Decision:** Utilize local Ollama models completely (e.g., Gemma family or Llama 3) for all tasks including tracking, dialogue, vector embeddings, and heavy content generation (MCQs, explanations).
- **Reason:** Guarantees absolute offline privacy, infinite free requests/rate limits, and fully self-contained local operation.

## Workflow Orchestration
- **Decision:** Use `antigravity-cli` with declarative YAML files (`workflows/*.yaml`).
- **Reason:** Provides a repeatable, automated testing and execution environment that runs in isolated/dockerized setups, ensuring the data ingestion pipeline is robust.

## Coaching Analytics State & Persistence
- **Decision:** Stick to using MongoDB completely for all application state, tracking topics covered, learning analytics, and question memory.
- **Reason:** Aligns natively with the target certification domain (MongoDB Associate Developer), avoiding secondary databases (like SQLite) and allowing seamless usage of document collections and aggregation pipelines.

## Bounded Coach State Machine
- **Decision:** Keep the learner experience segmented into Teach, Check, Practice, Review, and Free Chat modes with explicit transition rules.
- **Reason:** Prevents cross-topic drift and keeps explanations anchored to the current syllabus concept until the learner is ready to move on.

## Timestamped Project Memory
- **Decision:** Maintain timestamped markdown memory files for progress, decisions, and flow specifications under `memory/`.
- **Reason:** The project now depends on repeatable pedagogy decisions, and those need to remain visible without digging through code history.

## Canonical Content Contract
- **Decision:** Treat lesson generation, question validation, legacy repair, and CLI rendering as separate layers that all consume the same canonical content contract.
- **Reason:** Prompt tweaks alone cannot guarantee consistency when old bank records and render-time sanitization still influence the learner experience.

## Contract Versioning
- **Decision:** Stamp generated and repaired content with a content contract version so the bank can distinguish compliant records from legacy records.
- **Reason:** Versioning makes it possible to audit, migrate, and quarantine old items instead of silently letting them persist.

## Ordered Question-Bank Operations
- **Decision:** Process repair and population by canonical syllabus topic and concept order.
- **Reason:** Earlier concepts become usable first, and bounded overnight jobs remain predictable and resumable.

## Readiness vs. Inventory
- **Decision:** Keep `3 Easy + 2 Medium` as the study-readiness gate and use configurable per-concept population inventory targets of `5 Easy + 5 Medium` by default.
- **Reason:** The readiness minimum unlocks study, while a deeper inventory reduces repetition and improves mock variety without imposing a fixed global bank size.
