# 🧑‍🏫 CertCoach: Local RAG-Powered MongoDB Certification Prep

CertCoach is a local, AI-driven learning and study companion designed to help developers master the syllabus and clear the **MongoDB Associate Python Developer Certification** in one go.

Using a local Ollama instance (`qwen2.5:7b`), an interactive console interface, Spaced Repetition quiz cycles, a vector knowledge base (Chroma DB), and strict document-grounded RAG, CertCoach acts as your personal instructor to systematically guide you through exam topics, scenarios, and syntactic traps.

---

## ✨ Features

- **💡 Startup Readiness Briefing**: Prompts you to review critical syntactic traps across all 12 syllabus modules at daily launch.
- **⚡ Spaced Repetition (Anki Pop Quizzes)**: Automatically triggers Spaced-Repetition quizzes on due topics before your study agenda starts.
- **🗓️ Personalized Study Planner**: Generates a day-by-day study calendar customized to your experience level and exam date.
- **📚 Syllabus Gap & Coverage Auditor**: Audits official study documents and maps file coverage status directly in the CLI.
- **📖 Interactive Study Journal**: Exposes the complete history of your learning sessions and chat conversations in a terminal scroll pager.
- **💻 Scenario Simulator (Apply Mode)**: Generates and evaluates real-world coding/modeling scenarios tailored to the MongoDB exam.
- **🔒 Gated Mock Exams**: Locks the timed and full mock exams (60 questions) until you master at least 70% of the syllabus.

---

## 🛠️ Tech Stack & Architecture

- **Core**: Python 3.10+
- **Database**: MongoDB (Question Bank, Attempts, Streaks, User Profiles)
- **Vector Search / RAG**: Chroma DB (Knowledge base indexed with descriptive raw markdowns)
- **Local Intelligence**: Ollama (`qwen2.5:7b` model)
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
ollama pull qwen2.5:7b
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
2. Add a `.env` file inside that directory with your local Ollama connection details:
   ```env
   LOCAL_LLM_URL=http://localhost:11434
   MODEL=qwen2.5:7b
   ```

---

## 💻 Running the Application

To start the interactive learning CLI, simply run the globally registered entry point:
```bash
certcoach
```
*(On your very first launch, CertCoach will guide you through onboarding. You will be prompted to enter your MongoDB connection URI and your target exam date in `YYYY-MM-DD` format. Setup is saved automatically).*

---

## 📊 Ingestion & Seeding Pipelines

If you want to re-ingest raw syllabus files or seed your local MongoDB with practice questions, use these scripts:

0. **Cache Official MongoDB Docs Markdown**:
   Downloads direct `.md` versions of pages listed in MongoDB's `llms.txt` into `data/mongodb_docs/`, with a manifest for source URL, markdown URL, local path, status, hash, and fetch time. Use this as the broad source corpus before mapping pages to a specific exam syllabus:
   ```bash
   python src/scripts/utils/mongodb_docs_md_scraper.py --count-only
   python src/scripts/utils/mongodb_docs_md_scraper.py --dry-run
   python src/scripts/utils/mongodb_docs_md_scraper.py --limit 25
   python src/scripts/utils/mongodb_docs_md_scraper.py --workers 4
   python src/scripts/utils/mongodb_docs_md_scraper.py --workers 8 --delay 0.01 --progress-every 500 --manifest-every 100
   python src/scripts/utils/mongodb_docs_md_scraper.py --include "/docs/manual/" --include "/docs/languages/python/"
   ```
1. **Map Cached Docs to the Active Syllabus**:
   Resolve the curated official pages for the MongoDB Associate Python Developer syllabus, then copy the resolved docs into one folder per syllabus topic under `data/mongodb_docs/syllabus_mapped/associate_python_developer/` with a mapping manifest for citations:
   ```bash
   python src/scripts/utils/resolve_associate_python_developer_docs.py
   python src/scripts/utils/map_mongodb_docs_to_syllabus.py
   ```
2. **Clean Markdown Reference Files**:
   Strips boilerplate headings, formats HTML tables, and outputs cleaned text under `data/cleaned_markdowns/`:
   ```bash
   python src/scripts/utils/clean_markdown.py
   ```
3. **Index RAG Vector DB**:
   Chunks and indexes the prefixed reference documents into Chroma DB:
   ```bash
   python src/scripts/utils/knowledge_base_indexer.py
   ```
4. **Seed MongoDB Question Bank**:
   Parses the question datasets and seeds your local database:
   ```bash
   python src/scripts/seed_mongodb.py
   ```

---

## 🧪 Running Unit Tests

The test suite runs 100% offline using mock boundaries for database connections and LLM calls. Execute the test suite via `pytest`:
```bash
pytest tests/
```
