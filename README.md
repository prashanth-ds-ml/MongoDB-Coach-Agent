# 🧑‍🏫 CertCoach: Local RAG-Powered MongoDB Certification Prep

CertCoach is a local, AI-driven learning and study companion designed to help developers master the syllabus and clear the **MongoDB Associate Python Developer Certification** in one go.

Using a local Ollama instance (`qwen2.5-coder:7b`), an interactive console interface, Spaced Repetition quiz cycles, a vector knowledge base, and strict document-grounded RAG, CertCoach acts as your personal instructor to systematically guide you through exam topics, scenarios, and syntactic traps.

---

## ✨ Features

- **💡 Startup Readiness Briefing**: Prompts you to review critical syntactic traps across all 12 syllabus modules at daily launch (mastery-gated).
- **⚡ Spaced Repetition (Anki Pop Quizzes)**: Automatically triggers Spaced-Repetition quizzes on due topics before your study agenda starts.
- **🗓️ Personalized Study Planner**: Generates a day-by-day study calendar customized to your experience level and exam date.
- **🏆 Timed Non-Linear Exam Simulator**: Features a professional delayed-feedback timed simulator for Mocks and Practice:
  - **Dynamic Pacing HUD**: Evaluates average target response times and displays active pacing alerts (Ahead, Behind, or On Track).
  - **Non-Linear Navigation**: Navigate freely using `[N]ext`, `[P]revious`, `[R]eview Flag`, and direct jumps to any question number.
  - **Summary Grid**: Renders a compact progress grid detailing completed, skipped, and flagged questions.
  - **Delayed Review Mode**: Scrutinizes incorrect answers under a graded scorecard presenting comprehensive **6-Part Explanations**.
  - **Crash-Resilient Autosaver**: Automatically persists active exam state on every single question transition to survive crashes.
- **🧹 Startup VRAM Memory Manager**: Automatically scans and detects active models in graphics memory at launch, prompting to unload them (`keep_alive=0`) to clear VRAM space and prevent model weight-loading lag.
- **📚 Syllabus Gap & Coverage Auditor**: Audits official study documents and maps file coverage status directly in the CLI.
- **💻 Scenario Simulator (Apply Mode)**: Generates and evaluates real-world coding/modeling scenarios tailored to the MongoDB exam.
- **🔒 Gated Mock Exams**: Locks the timed and full mock exams (60 questions) until you master at least 70% of the syllabus.

---

## 🛠️ Tech Stack & Architecture

- **Core**: Python 3.10+
- **Database**: MongoDB (Question Bank, Attempts, Streaks, User Profiles, Resumable Exam States)
- **Document Grounding**: Direct Semantic Grounding (injects complete, un-fragmented official documentation text directly into optimized `8192` context windows, ensuring 100% accuracy and zero vector RAG chunk fragmentation)
- **Local Intelligence**: Ollama (`qwen2.5-coder:7b` model)
- **User Interface**: `rich` (glassmorphism panels, tables, line-by-line keyboard scroll pagers)

---

## 🚀 Installation & Setup Guide

Follow these steps to set up CertCoach locally for your study preparation:

### 1. Prerequisites
Ensure you have the following installed on your machine:
- **Python**: Version `3.10` or higher
- **MongoDB Server**: A running local instance (`mongodb://localhost:27017`) or an Atlas connection URI
- **Ollama**: Installed and running in the background (`ollama serve`)

### 2. Pull the Coach Model
Before launching, make sure the local LLM model is pulled and ready in Ollama:
```bash
ollama pull qwen2.5-coder:7b
```
*(You can customize the model inside your environment configurations).*

### 3. Clone and Navigate
```bash
git clone https://github.com/prashanth-ds-ml/MongoDB-Coach-Agent.git
cd MongoDB-Coach-Agent
```

### 4. Create and Activate Virtual Environment
* **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
* **macOS/Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 5. Install Dependencies
Install all required libraries and register the package globally in editable mode:
```bash
pip install -r requirements.txt
pip install -e .
```

### 6. Configuration Variables
Setup your global configuration variables:
1. Create a directory named `.certcoach` in your user home directory (e.g. `C:\Users\YourUser\.certcoach` or `~/.certcoach`).
2. Add a `.env` file inside that directory with your local Ollama connection details and MongoDB URI:
   ```env
   LOCAL_LLM_URL=http://localhost:11434
   MODEL=qwen2.5-coder:7b
   MONGO_URI="mongodb+srv://<username>:<password>@yourcluster.mongodb.net/"
   ```
3. Copy this configuration file to your local workspace directory as well to keep configurations synchronized.

---

## 💻 Running the Application

To start the interactive learning CLI, simply run the globally registered entry point:
```bash
certcoach
```
*(On launch, CertCoach will guide you through onboarding. You will be prompted to enter your MongoDB connection URI and your target exam date in `YYYY-MM-DD` format. Startup configurations are saved automatically).*

---

## 📊 Ingestion & Seeding Pipelines

CertCoach includes a highly optimized, memory-safe, and doc-grounded question seeding pipeline:

### 1. Unified Topic-Level Question Seeder
We use a stage-by-stage concept seeder script to populate your MongoDB question collection to the perfect syllabus target (15 Easy, 20 Medium, 10 Hard per topic). It is designed to be **VRAM-safe** by checking active models on startup, capping context windows to `8192` to avoid WDDM/RTX memory spillover (0% CPU offload), recovering truncated JSON payloads, and automatically unloading weights at completion.

To seed the entire set of BSON and document structure questions for **Topic 1** in controlled stages with a single command:
```bash
.venv\Scripts\python scratch/populate_stage_by_stage.py 1
```

You can select other topics (2–12) or seed all topics sequentially with automatic memory flushes between topics by launching the interactive seeder CLI:
```bash
.venv\Scripts\python scratch/populate_stage_by_stage.py
```

### 2. General Data Ingestion Utilities
If you want to re-ingest raw syllabus files, clean markdowns, or index files, use these helper scripts:
* **Resolve & Map Syllabus Documents**: curates and maps crawled pages into structural folders matching syllabus topics:
  ```bash
  python src/scripts/utils/resolve_associate_python_developer_docs.py
  python src/scripts/utils/map_mongodb_docs_to_syllabus.py
  ```
* **Clean Markdown Reference Files**: strips boilerplate headers and formats HTML tables into clean text:
  ```bash
  python src/scripts/utils/clean_markdown.py
  ```
* **Index RAG Vector DB**: chunks and indexes reference documents into Chroma DB:
  ```bash
  python src/scripts/utils/knowledge_base_indexer.py
  ```
* **Seed Static MongoDB Question Bank**: parses raw datasets and seeds your local database:
  ```bash
  python src/scripts/seed_mongodb.py
  ```

---

## 🧪 Running Unit Tests

The test suite runs 100% offline using mock boundaries for database connections and LLM calls. Execute the test suite via `pytest`:
```bash
pytest tests/
```
