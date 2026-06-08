# 📊 Feature Progress & Feature Freeze State

This document captures the current status of all features and flows in the CertCoach platform, establishing a strict **Feature Freeze** to focus entirely on exam preparation.

---

## 🔒 Feature Freeze Status
* **Status:** **FROZEN & LOCKED**
* **Effective Date:** June 6, 2026
* **Rule:** No new feature development, architectural changes, or CLI UI refactorings are permitted. The code is locked in its current functional state. Any future edits are strictly limited to content quality correction or bug fixes.

---

## 🛠️ Completed Platform Features

### 1. 🗄️ MongoDB Persistence Engine
* **Status:** Complete & Unified
* **Details:** Replaced all local JSON databases with a persistent MongoDB instance (`certcoach_db`).
* **Collections:**
  - `questions`: Holds all seed MCQs, metadata, and 7-part detailed explanations.
  - `profiles`: Tracks user progress, streaks, confidence scores, and overall readiness.
  - `attempts`: Stores performance logs for every question answered.
  - `sessions`: Logs daily study history.
  - `active_exams`: Tracks active timed mock exam state to support suspend/resume.

### 2. 💻 Interactive CLI Dashboard (`src/certcoach/cli.py`)
* **Status:** Complete & Conversational
* **Details:** A console-based visual interface featuring:
  - **Onboarding Flow:** Generates user profiles and configures database connection.
  - **Daily Agenda Dashboard:** Displays streak freeze status,Pop Quiz availability, readiness score, and today's target concepts.
  - **Hybrid Chat Mode:** Integrated a Smart Router that intercepts natural language questions and drops the user into an open-ended conversational session with the AI Coach.
  - **Full Timed Mock Simulator:** Supports timed mock navigation, flagging questions for review, autosave, and exam resumption.

### 3. 🧠 Spaced Repetition (Anki Engine)
* **Status:** Complete
* **Details:** Implemented a SuperMemo-style algorithm that schedules future concept reviews based on user confidence ratings (1-5) and accuracy.

### 4. 🎛️ Nightly Seeder Pipeline (`src/certcoach/jobs/nightly_seed_questions.py`)
* **Status:** Complete & Balanced
* **Details:**
  - Audits database deficits against the target syllabus blueprint.
  - Distributes and generates missing questions across four specific styles:
    - **Type A:** Syntax Selection & Trap Spotting
    - **Type B:** Theory, Constraints & Data Modeling
    - **Type C:** Predicting Query Output (Aggregation / Array matching)
    - **Type D:** Troubleshooting, Errors & Performance
  - Supports loading local LLMs with custom timeouts.

### 5. 🔎 Casing Guard and Syntax Validator (`src/certcoach/core/planner.py`)
* **Status:** Completed & Optimized
* **Details:**
  - **Standard Topics:** Rejects PyMongo snake_case in favor of strict `mongosh` camelCase.
  - **Driver Topics (PyMongo):** Rejects `mongosh` camelCase and permits Python/PyMongo code containing python keywords or neutral methods (like `aggregate`, `cursor`, `next`, `sort`, `limit`, etc.) without triggering validation retries.

---

## 📈 Content Generation & Database Quality Metrics

* **Premium Extracted Questions:** 69 official exam screenshots extracted to the DB.
* **Target Question Bank:** 540 questions.
* **Current Missing Slots:** 463 slots.
* **Legacy Explanations Needing Repair:** ~280 questions need conversion to the 7-part compliance format.

---

## 🎯 Plan for Exam Preparation (Starting Tomorrow)

To prepare for the exam, the focus shifts entirely to consuming and testing:
1. **Bulk Ingestion (Overnight):** Run the seeder to populate all remaining 463 questions using `gemma4:12b` overnight.
2. **Explanation Compliance:** Run the repair script (`certcoach-repair-explanations`) to fix the formatting of the 280+ legacy questions.
3. **Practice & Mocks:** Start using the CLI app from tomorrow morning to take daily pop quizzes, concept practice sessions, and timed mock exams.
