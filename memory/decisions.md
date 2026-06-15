# 🏛️ Architecture & Model Decisions

This document records the definitive technical decisions made for the CertCoach platform to lock down the architecture for exam preparation.

---

## 🖥️ Local Model Selection & Hardware Strategy

### 1. Interactive Study Model: `qwen3.5:4b`
* **Decision:** Use `qwen3.5:4b` for lessons, follow-up Q&A, feedback, and daily coaching.
* **Rationale:** It provides good teaching quality while leaving enough VRAM headroom on the minimum supported 16 GB RAM / 6 GB NVIDIA GPU laptop.
* **Configuration:** Disable reasoning output and use an `8192` context window for interactive study.

### 2. Population and Repair Model: `gemma4:12b`
* **Decision:** Use `gemma4:12b` for question generation and explanation repair.
* **Rationale:** Content production prioritizes MongoDB reasoning quality over interactive latency.
* **Configuration:** Use a `600.0` second timeout to allow CPU offloading on the minimum supported laptop.

### 3. Study Fallback: `qwen2.5-coder:7b`
* **Decision:** Keep `qwen2.5-coder:7b` as an optional study and development fallback.
* **Rationale:** It is fast and code-focused, but leaves less VRAM headroom than the default study model.

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
