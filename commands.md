# CertCoach Command Cheat Sheet

This document contains all the essential commands needed to run, test, and develop the CertCoach project on Windows (PowerShell).

## 1. Environment Setup
Before running any scripts, always activate your virtual environment:
```powershell
.\.venv\Scripts\Activate.ps1
```
*(If you see `(.venv)` in your terminal prompt, you are good to go!)*

Install or update dependencies:
```powershell
pip install -r requirements.txt
```

## 2. Running the Application
The CertCoach CLI is now installed globally via `pip install -e .`. To start the interactive learning platform, just run:
```powershell
certcoach
```

## 3. Local Services
CertCoach relies on a local LLM and a local database. Make sure these are running in the background before starting the CLI.

Start Ollama (required for `gemma4:e4b` Coach Persona):
```powershell
ollama serve
```

Start Local MongoDB (Required for the upcoming Phase 6 data migration):
```powershell
# Using default local connection
mongodb://localhost:27017
```

## 4. Data Processing Scripts
If you need to manually ingest or extract documentation, use the scripts located in `scripts/` and `src/scripts/`:

Extract text from the official PDF Guide:
```powershell
python scripts/extract_pdf.py
```

Process and clean raw markdowns:
```powershell
python scripts/process.py
```

Scrape official MongoDB docs:
```powershell
python src/scripts/scrape_docs.py
```

Seed MongoDB with JSON questions (Upcoming Phase):
```powershell
python src/scripts/utils/seed_mongo.py
```

## 5. Testing
Run the unit test suite (like `test_indexer.py`) using `pytest`:
```powershell
pytest tests/
```

## 6. Workflows
If you are using the automated `antigravity-cli` workflow engine to run the declarative YAML pipelines:
```powershell
antigravity run workflows/certcoach_pipeline.yaml
```
