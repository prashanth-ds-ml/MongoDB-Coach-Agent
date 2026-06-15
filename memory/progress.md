# Feature Progress and Freeze Readiness

This document tracks the remaining study-readiness work required before declaring the final feature freeze.

---

## Freeze Status
* **Status:** **STUDY-READINESS STABILIZATION**
* **Rule:** Only work required to make the daily study, five-question practice, progress persistence, and mixed-mock path reliable is allowed. Optional feature work is deferred until after the exam.

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

## Content Readiness Snapshot

* **Premium Extracted Questions:** 69 official exam screenshots extracted to the DB.
* **Canonical syllabus:** 12 topics and 58 concepts.
* **Fixed question-bank target:** None.
* **Readiness rule:** Each scheduled concept must have official documentation plus at least three active Easy and two active Medium questions.
* **Current blocker:** The live bank has legacy content but no active-contract questions available to practice.

---

## Path to Exam Preparation

1. Complete the approved build order one phase at a time.
2. Make every scheduled concept study-ready.
3. Verify one full study flow and one timed mixed mock.
4. Freeze features.
5. Use CertCoach daily for exam preparation.

---

## Phase Checkpoint

* **Phase 0:** Complete and reviewed.
* **Phase 1:** Complete and reviewed.
* **Phase 2:** Complete and reviewed.
* **Phase 3:** Complete and reviewed.
* **Phase 4:** In progress; backup and deterministic migration complete, overnight repair/population pending.
* **Phase 1 result:** Model roles are separated, public defaults are documented, runtime/generated artifacts are excluded from Git, and no live database writes were performed.
* **Phase 2 result:** Lessons are concept-bounded; scheduling, practice, and completion share a strict `3 Easy + 2 Medium` active-question gate.
* **Live readiness snapshot:** Zero ready topics and 57 blocked concepts.
* **Phase 3 result:** The fixed global bank total is retired; lifecycle classification, active-only study-readiness reporting, and configurable per-concept inventory targets are ready for controlled database operations.
* **Full lifecycle snapshot:** 351 total records, 69 migratable, 216 needing explanation repair, and 66 quarantined.
* **Readiness-only deficits before migration/repair:** 174 Easy and 116 Medium.
* **Post-migration live state:** 69 active, 216 repair-pending, 66 quarantined, 2 study-ready concepts, 162 Easy and 93 Medium deficits.
* **Phase 4 daytime verification:** 111 tests passed and the post-migration backup was reverified.
* **Next allowed work:** Bounded overnight explanation repair and ordered population toward the configured per-concept inventory targets.
