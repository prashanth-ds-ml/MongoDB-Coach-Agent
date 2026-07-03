# 🧑‍🏫 CertCoach: Local RAG-Powered MongoDB Certification Prep

CertCoach is a local, AI-driven learning and study companion designed to help developers master the syllabus and clear the **MongoDB Associate Python Developer Certification** in one disciplined attempt.

Using local Ollama models with separate study and content-production roles, an interactive console interface, spaced-repetition quiz cycles, a question bank, and strict document-grounded teaching prompts, CertCoach acts as your personal instructor to systematically guide you through exam topics, scenarios, and syntactic traps.

### Agent And Obsidian Workspace

The repository root is an Obsidian vault and includes vendor-neutral agent instructions:

- `AGENTS.md`: authoritative instructions for Codex, OpenCode, and compatible agents
- `CLAUDE.md`: Claude adapter
- `.github/copilot-instructions.md`: GitHub Copilot adapter
- `memory/Memory Home.md`: Obsidian navigation hub
- `memory/agent_context.md`: compact current context
- `memory/session_handoff.md`: latest checkpoint and next action

Agents should load only the startup files above, then follow links to task-specific references. This avoids loading the full project memory or source corpus into context.

---

## 📱 Companion Apps

Two standalone flashcard apps ship alongside the main CLI. Both bundle the same `flashcards.json` dataset locally and keep progress on-device — neither talks to `certcoach_db` or the CLI's model pipeline.

- `mobile/` — an Expo/React Native app (`cd mobile && npm install && npm start`).
- `web-flashcards/` — a Vite/React web app (`cd web-flashcards && npm install && npm run dev`).

---

## ✨ Features

- **💡 Startup Readiness Briefing**: Prompts you to review critical syntactic traps across all 12 syllabus modules at daily launch (mastery-gated).
- **🎯 Daily Mission Briefs**: Every agenda item starts with a clear mission, target concept, and win condition so the learner knows exactly what “done for today” means.
- **🧠 Structured Lesson Coach**: Lessons follow a bounded state machine: Teach one concept, resolve one Micro-Challenge, stay in concept-scoped Q&A, then move to practice and cumulative review.
- **⚡ Spaced Repetition (Anki Pop Quizzes)**: Automatically triggers Spaced-Repetition quizzes on due topics before your study agenda starts.
- **🛠️ Practice Recovery Guidance**: After every practice set, CertCoach surfaces reinforcement or remediation steps based on score and the weak concepts just exposed.
- **📌 Session Closeout Coaching**: At the end of a study session, CertCoach summarizes what got locked in, how readiness moved, and the best next agenda start.
- **🗓️ Personalized Study Planner**: Generates a day-by-day study calendar customized to your experience level and exam date.
- **🏆 Timed Non-Linear Exam Simulator**: Features a professional delayed-feedback timed simulator for Mocks and Practice:
  - **Dynamic Pacing HUD**: Evaluates average target response times and displays active pacing alerts (Ahead, Behind, or On Track).
  - **Non-Linear Navigation**: Navigate freely using `[N]ext`, `[P]revious`, `[R]eview Flag`, and direct jumps to any question number.
  - **Summary Grid**: Renders a compact progress grid detailing completed, skipped, and flagged questions.
  - **Delayed Review Mode**: Scrutinizes incorrect answers under a graded scorecard presenting comprehensive **Seven-Part Explanations**.
  - **Crash-Resilient Autosaver**: Automatically persists active exam state on every single question transition to survive crashes.
- **🛑 Active Error Book**: Keeps a dedicated collection of historical study mistakes, tracking fail counts, timestamps, and error patterns. Offers targeted practice sessions and interactive reviews of your weakest concepts directly from the CLI.
- **🧹 Startup VRAM Memory Manager**: Automatically scans and detects active models in graphics memory at launch, prompting to unload them (`keep_alive=0`) to clear VRAM space and prevent model weight-loading lag.
- **📚 Syllabus Gap & Coverage Auditor**: Audits official study documents and maps file coverage status directly in the CLI using the canonical 12-topic syllabus map and concept checkpoints.
- **💻 Scenario Simulator (Apply Mode)**: Generates and evaluates real-world coding/modeling scenarios tailored to the MongoDB exam.
- **🔒 Gated Mock Exams**: Locks the timed and full mock exams (60 questions) until you master at least 70% of the syllabus.
- **🔎 Local & Remote Document Reranking**: Enhances context accuracy by sorting vector database search results before sending them to the LLM. Supports OpenRouter API chat models (e.g., `gemma-2-9b-it`), local Ollama fallback, and dedicated local cross-encoder models like `dengcao/Qwen3-Reranker-4B:Q5_K_M`.
- **⚡ Hardware Pacing Optimizer**: Automatically diagnoses your CPU, RAM, and GPU VRAM on startup using `nvidia-smi` and PowerShell, recommending the best model configuration (e.g. `qwen2.5-coder:7b` to fit within 6 GB VRAM) for lag-free performance.

---

## 🛠️ Tech Stack & Architecture

- **Core**: Python 3.10+
- **Database**: MongoDB (Question Bank, Attempts, Streaks, User Profiles, Resumable Exam States)
- **Document Grounding**: Direct Semantic Grounding (injects complete, un-fragmented official documentation text directly into optimized `8192` context windows, ensuring 100% accuracy and zero vector RAG chunk fragmentation)
- **Local Intelligence**: Ollama (`qwen3.5:4b` for interactive study; `gemma4:12b` for question population and explanation repair)
- **User Interface**: `rich` (glassmorphism panels, tables, line-by-line keyboard scroll pagers)

---

## 🚀 Installation & Setup Guide

Follow these steps to set up CertCoach locally for your study preparation:

### 1. Prerequisites
Ensure you have the following installed on your machine:
- **Python**: Version `3.10` or higher
- **MongoDB Server**: A running local instance (`mongodb://localhost:27017`) or an Atlas connection URI
- **Ollama**: Installed and running in the background (`ollama serve`)

### 2. Pull the Local Models
Pull the fast interactive study model and the slower content-production model:
```bash
ollama pull qwen3.5:4b
ollama pull gemma4:12b
```
`qwen2.5-coder:7b` remains an optional study fallback.

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
   STUDY_MODEL=qwen3.5:4b
   STUDY_NUM_CTX=8192
   STUDY_REASONING=false
   POPULATION_MODEL=gemma4:12b
   POPULATION_NUM_CTX=4096
   REPAIR_MODEL=gemma4:12b
   REPAIR_NUM_CTX=8192
   OLLAMA_TIMEOUT=600
   MONGO_URI="mongodb+srv://<username>:<password>@yourcluster.mongodb.net/"
   ```
3. Use `.env.example` as the public reference. A legacy `MODEL` value is still accepted as a study-model fallback, but it does not control population or repair.

---

## 💻 Running the Application

To start the interactive learning CLI, simply run the globally registered entry point:
```bash
certcoach
```
*(On launch, CertCoach will guide you through onboarding. You will be prompted to enter your MongoDB connection URI and your target exam date in `YYYY-MM-DD` format. Startup configurations are saved automatically).*

### Cross-Machine Progress Sync

CertCoach stores learner progress in MongoDB. To continue from another machine, point both machines at the same `MONGO_URI`, then open:

```text
Settings & Extras -> Account Login / Sync Across Machines
```

Create an account or sign in with an existing account. CertCoach saves only the active account id locally in `~/.certcoach/session.json`; attempts, streaks, calendar, study sessions, active exam state, and readiness history remain in MongoDB.

---

## 🎓 Study Quick-Start Workflow (Day 1 Guide)

If you are a beginner, follow this step-by-step workflow to configure memory, seed your database, and start studying in under 5 minutes:

### Step 1: Force Clear Stuck VRAM Memory
Open PowerShell (as Administrator or normal user) and run this to terminate any stuck background LLM runners:
```powershell
taskkill /f /im ollama.exe
```

### Step 2: Launch Ollama App Cleanly
Search for "Ollama" in your Windows Start menu to start the application, or execute:
```powershell
start-process "C:\Users\prash\AppData\Local\Programs\Ollama\ollama app.exe"
```

### Step 3: Seed Your MongoDB Question Bank
Seed the entire Topic 1 question bank (Concepts A, B, and C) sequentially using the optimized, memory-safe seeder command:
```bash
.venv\Scripts\python scratch/populate_stage_by_stage.py 1
```
*(Give it 30-60 seconds on the very first prompt to load model weights into empty VRAM. Once loaded, it will output and ingest the questions rapidly).*

### Step 4: Launch the Coach CLI
Launch your study Coach:
```bash
certcoach
```

### Step 5: Begin Your Diagnostic Test
During onboarding, select `Yes` when prompted to take the 10-question Diagnostic Test. This allows CertCoach to evaluate your current knowledge, automatically skip topics you already know, and build a highly personalized day-by-day calendar.

### Step 6: Follow the Daily Agenda
Select `Option 1` from the main menu to start studying today's scheduled concept. CertCoach now shows a mission brief, teaches one active concept at a time, asks a micro-challenge, keeps follow-up Q&A inside the same concept, and then requires a 5-question practice gate.

To count the concept as complete, clear the practice gate with **4/5 or better**. After the quiz:

1. CertCoach shows the structured seven-part answer review for every question.
2. CertCoach gives a recovery or reinforcement plan based on the score and the weak concepts just exposed.
3. If the concept is locked in, CertCoach marks it complete, updates the cumulative cheat sheet for that topic, and keeps the existing mini-mock unlock rules intact.

At the end of the session, CertCoach logs the study session and shows a closeout summary with readiness movement and the best next agenda start.

### Daily Study Loop at a Glance

```text
Main Menu -> Start Today's Agenda
          -> Daily Mission Brief
          -> Lesson
          -> Micro-Challenge + concept-scoped Q&A
          -> 5-question Practice Gate
          -> Recovery / Reinforcement
          -> Concept Completion + Cumulative Cheat Sheet
          -> Optional Mini-Mock (after 3 mastered topics)
          -> Session Closeout
```

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

### 3. Weighted Nightly Seeder

For a smoother learner experience, run the weighted seeder before study sessions instead of generating questions during live practice. The weighted seeder prioritizes exam-heavy topics and concept-level gaps using `syllabus.json` weights.

```bash
certcoach-seed-nightly --max-questions 25
```

Useful modes:

```bash
certcoach-seed-nightly --dry-run
certcoach-seed-nightly --max-questions 50
certcoach-seed-nightly --topic 11 --dry-run
certcoach-seed-nightly --topic 11
certcoach-seed-nightly --topic "MongoDB Drivers & PyMongo"
certcoach-seed-nightly --topic 11 --extra-easy 3 --extra-medium 2 --max-questions 25
```

Study readiness begins at `3 Easy + 2 Medium` active questions per concept, but population does not stop there. By default, ordered population builds each concept toward `5 Easy + 5 Medium`, configurable with `POPULATION_EASY_TARGET` and `POPULATION_MEDIUM_TARGET`. Explicit extras can still add more for variety, weak areas, or mock coverage.

Recommended Windows Task Scheduler command:

```powershell
.\.venv\Scripts\certcoach-seed-nightly.exe --max-questions 25
```

For controlled Phase 4 overnight batches, run the repository script. Each run creates a verified backup, repairs a bounded batch, populates a bounded batch, and records a log under `logs/`:

```powershell
.\scripts\run_phase4_overnight.ps1 -RepairBatchSize 25 -PopulationBatchSize 25
```

Without overrides, the runner automatically selects the first concept with pending repairs or an inventory below the configured population target. It repairs and populates only that concept, then advances through the remaining concepts and topics in canonical syllabus order.

Optional topic-specific or extra-variety run:

```powershell
.\scripts\run_phase4_overnight.ps1 -Topic 11 -Concept "MongoClient" -RepairBatchSize 25 -PopulationBatchSize 25 -ExtraEasy 2 -ExtraMedium 1
```

To complete all missing study-readiness questions for a single topic, omit `--max-questions`:

```powershell
.\.venv\Scripts\certcoach-seed-nightly.exe --topic 11
```

After activating the virtual environment, `certcoach`, `certcoach-seed-nightly`, `certcoach-repair-explanations`, `certcoach-dedupe-questions`, and `certcoach-map-questions` can be run from any folder. If a command is not on `PATH`, call the executable directly:

```powershell
C:\Users\prash\projects\MongoDB-Coach-Agent\.venv\Scripts\certcoach-seed-nightly.exe --topic 11 --concept "MongoClient" --dry-run
```

### 4. Repair Existing Question Explanations

To audit and repair older question-bank items so answer reviews teach through the full seven-part template:

```powershell
certcoach-repair-explanations --dry-run
certcoach-repair-explanations --topic "CRUD Operations" --max-questions 10
certcoach-repair-explanations
```

The repair command preserves question text, option text, option letters, and the marked correct answer. It updates explanations, trap analysis, and option feedback. Questions with invalid structure, such as fewer than four options or no marked correct option, are skipped for manual reconstruction.

### 5. Question Bank Duplicate Cleanup

After explanation repair finishes, check the question bank for repeated generated questions before running another overnight populate. The dedupe command is safe by default: without `--apply`, it only prints duplicate groups and the documents it would remove.

```powershell
certcoach-dedupe-questions
certcoach-dedupe-questions --topic 11
certcoach-dedupe-questions --apply
```

Use this sequence when you want the full repair-and-populate maintenance flow:

```powershell
certcoach-repair-explanations
certcoach-dedupe-questions
certcoach-dedupe-questions --apply
certcoach-seed-nightly --dry-run
certcoach-seed-nightly
```

For a single topic, use the topic-specific sequence:

```powershell
certcoach-repair-explanations --topic 11
certcoach-dedupe-questions --topic 11
certcoach-dedupe-questions --topic 11 --apply
certcoach-seed-nightly --topic 11 --dry-run
certcoach-seed-nightly --topic 11
```

### 6. Question Syllabus Mapping & Alignment

To audit the database and automatically align any legacy or dynamic questions to the correct syllabus topics and concept subtopics using token and keyword matching:

```powershell
certcoach-map-questions --dry-run
certcoach-map-questions
```

Recommended nightly order:

1. Run `.\.venv\Scripts\python.exe -m certcoach.jobs.next_phase4_topic` to preview the next ordered concept.
2. Run `.\scripts\run_phase4_overnight.ps1 -RepairBatchSize 25 -PopulationBatchSize 25`.
3. Review the generated log under `logs/` and rerun the selector.
4. Start study with `certcoach` once the required concepts are study-ready.

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
