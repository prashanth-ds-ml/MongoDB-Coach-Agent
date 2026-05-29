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
