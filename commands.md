# CertCoach Command Cheat Sheet

Windows PowerShell command reference for running CertCoach from any folder.

## Setup

Run these from the repo folder when installing or after adding new command entry points:

```powershell
cd C:\Users\prash\Projects\mongodbcret
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
C:\Users\prash\Projects\mongodbcret\.venv\Scripts\certcoach.exe
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

Preview weighted gaps without creating questions:

```powershell
certcoach-seed-nightly --dry-run
```

Populate all remaining weighted questions:

```powershell
certcoach-seed-nightly
```

Populate a single topic fully:

```powershell
certcoach-seed-nightly --topic 11
```

Populate a smaller overnight batch:

```powershell
certcoach-seed-nightly --max-questions 50
```

Direct fallback:

```powershell
C:\Users\prash\Projects\mongodbcret\.venv\Scripts\certcoach-seed-nightly.exe --dry-run
```

## Repair Six-Part Explanations

Preview repairable questions:

```powershell
certcoach-repair-explanations --dry-run
```

Repair every structurally valid question that is missing the six-part template:

```powershell
certcoach-repair-explanations
```

Repair one topic:

```powershell
certcoach-repair-explanations --topic 11
```

Repair a small batch:

```powershell
certcoach-repair-explanations --max-questions 25
```

Direct fallback:

```powershell
C:\Users\prash\Projects\mongodbcret\.venv\Scripts\certcoach-repair-explanations.exe
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
C:\Users\prash\Projects\mongodbcret\.venv\Scripts\certcoach-dedupe-questions.exe --apply
```

## Recommended Maintenance Flow

After the repair job finishes, run this sequence before overnight population:

```powershell
certcoach-repair-explanations
certcoach-dedupe-questions
certcoach-dedupe-questions --apply
certcoach-seed-nightly --dry-run
certcoach-seed-nightly
```

Topic-specific version:

```powershell
certcoach-repair-explanations --topic 11
certcoach-dedupe-questions --topic 11
certcoach-dedupe-questions --topic 11 --apply
certcoach-seed-nightly --topic 11 --dry-run
certcoach-seed-nightly --topic 11
```

## Tests

Run the full unit test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest tests
```

Compile-check a changed job:

```powershell
python -m py_compile src\certcoach\jobs\dedupe_questions.py
```
