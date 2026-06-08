# 🏛️ Architecture & Model Decisions

This document records the definitive technical decisions made for the CertCoach platform to lock down the architecture for exam preparation.

---

## 🖥️ Local Model Selection & Hardware Strategy

### 1. Primary Model: `gemma4:12b`
* **Decision:** Selected `gemma4:12b` as the primary LLM for all question generation, coaching, and explanation repair.
* **Rationale:** In testing, `gemma4:12b` displayed perfect reasoning on array query evaluations and 0 quality retries, whereas larger model alternatives (e.g. Qwen-14B) hallucinated PyMongo methods and made pipeline tracing errors.
* **Configuration:** Timeout is configured to `600.0` (10 minutes) to allow for CPU offloading of the 8.9 GB model weights on laptops with 6 GB VRAM and 16 GB RAM (offload ratio ~58% CPU / 42% GPU).

### 2. Alternative Model for Faster Development: `qwen2.5-coder:7b`
* **Decision:** Maintain `qwen2.5-coder:7b` as the fallback model for rapid testing/development.
* **Rationale:** Its smaller memory footprint (4.7 GB) fits entirely within GPU VRAM, allowing instant response times for quick debugging cycles, though final production seeding is deferred to the 12B model.

---

## 🗃️ Storage & Database Strategy

### 1. Unified MongoDB Backend (`certcoach_db`)
* **Decision:** Abandon JSON database files entirely and use local MongoDB (`pymongo`) collections.
* **Rationale:** As a MongoDB Associate Developer tool, using MongoDB for internal persistence reinforces practical knowledge of collection indexing, document updates, and aggregation pipelines.

---

## 🔠 Lexical Casing Rules (Casing Guard)

### 1. CamelCase vs. SnakeCase Enforcement
* **Decision:** Apply strict lexical parsing rules based on domain classification:
  - **Standard Topics (Overview, CRUD, Indexes, Modeling, Tools):** Reject Python/PyMongo snake_case. Enforce camelCase (`insertOne`, `findOne`, `createIndex`, etc.).
  - **Driver Topics (PyMongo):** Reject `mongosh` camelCase. Enforce snake_case (`insert_one`, `find_one`, `create_index`, etc.).
  - **Python/Driver Neutral Methods:** Allow camelCase-neutral method calls like `.aggregate(...)` or `.limit(...)` and Python-specific keywords (like `none`, `import`, `def`) in driver topics to prevent false positives and infinite retries.
