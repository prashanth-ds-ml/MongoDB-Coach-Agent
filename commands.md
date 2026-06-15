# CertCoach Command Cheat Sheet

Windows PowerShell command reference for running CertCoach from any folder.

## Setup

Run these from the repo folder when installing or after adding new command entry points:

```powershell
cd C:\Users\prash\projects\MongoDB-Coach-Agent
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Reload the PowerShell profile if a newly added global command is not recognized:

```powershell
. $PROFILE
```

## Study

Start the interactive coach:

```powershell
certcoach
```

Direct fallback:

```powershell
C:\Users\prash\projects\MongoDB-Coach-Agent\.venv\Scripts\certcoach.exe
```

What the current study loop looks like inside the CLI:

```text
Main Menu -> Start Today's Agenda
          -> Daily Mission Brief
          -> Lesson + Micro-Challenge + Follow-up Q&A
          -> 5-question Practice Gate
          -> Recovery / Reinforcement Plan
          -> Concept Completion + Cumulative Cheat Sheet
          -> Optional Mini-Mock (after 3 mastered topics)
          -> Session Closeout
```

Notes:

- A concept counts as complete only after a **4/5 or better** score on the 5-question practice gate.
- Existing progression features remain in place: topic/concept tracking, cumulative traps, mini-mock unlock after 3 mastered topics, and the timed exam simulator.

## Account Sync Across Machines

Use the same `MONGO_URI` on every machine, then open:

```text
certcoach -> Settings & Extras -> Account Login / Sync Across Machines
```

After login, progress is stored in MongoDB and follows the learner across machines.

## Populate Questions

Preview the next concept needing repair or population:

```powershell
.\.venv\Scripts\python.exe -m certcoach.jobs.next_phase4_topic
```

Run the controlled syllabus-ordered overnight workflow:

```powershell
.\scripts\run_phase4_overnight.ps1 -RepairBatchSize 25 -PopulationBatchSize 25
```

Preview population for one exact concept:

```powershell
certcoach-seed-nightly --topic 1 --concept "BSON Data Types" --dry-run
```

Populate one exact concept toward configured inventory targets:

```powershell
certcoach-seed-nightly --topic 1 --concept "BSON Data Types" --max-questions 25
```

Override the configured inventory targets for one run:

```powershell
certcoach-seed-nightly --topic 1 --concept "BSON Data Types" --target-easy 7 --target-medium 7 --max-questions 25
```

Study readiness begins at `3 Easy + 2 Medium`; default ordered population continues toward `5 Easy + 5 Medium`, configurable through `POPULATION_EASY_TARGET` and `POPULATION_MEDIUM_TARGET`.

## Repair Seven-Part Explanations

Preview repairable questions for one exact concept:

```powershell
certcoach-repair-explanations --topic 1 --concept "BSON Data Types" --dry-run
```

Repair a controlled concept-scoped batch:

```powershell
certcoach-repair-explanations --topic 1 --concept "BSON Data Types" --max-questions 25
```

Direct fallback:

```powershell
C:\Users\prash\projects\MongoDB-Coach-Agent\.venv\Scripts\certcoach-repair-explanations.exe --topic 1 --concept "BSON Data Types" --dry-run
```

## Remove Duplicate Questions

Report duplicate question groups only:

```powershell
certcoach-dedupe-questions
```

Report duplicates for one topic:

```powershell
certcoach-dedupe-questions --topic 11
```

Remove duplicate copies after reviewing the dry-run output:

```powershell
certcoach-dedupe-questions --apply
```

Direct fallback:

```powershell
C:\Users\prash\projects\MongoDB-Coach-Agent\.venv\Scripts\certcoach-dedupe-questions.exe --apply
```

## Recommended Maintenance Flow

Use the bounded runner for normal maintenance:

```powershell
.\.venv\Scripts\python.exe -m certcoach.jobs.next_phase4_topic
.\scripts\run_phase4_overnight.ps1 -RepairBatchSize 25 -PopulationBatchSize 25
```

## Tests

Run the full unit test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\unit -q
```

Compile-check a changed job:

```powershell
python -m py_compile src\certcoach\jobs\dedupe_questions.py
```
