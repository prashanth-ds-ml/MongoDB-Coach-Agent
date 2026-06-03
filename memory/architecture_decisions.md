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
