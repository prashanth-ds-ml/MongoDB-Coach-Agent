# CertCoach RAG Workflow Engine

This repository contains the CertCoach RAG Workflow Engine project, aiming to develop a multi-faceted EdTech product roadmap for preparing users for the "MongoDB Associate Python Developer" certification using local LLMs (Ollama) and cloud models (OpenRouter) for intelligence.

## Project Structure

- `src/`: Python source code containing CLI applications, data ingestion models, and knowledge base handlers.
- `workflows/`: Declarative workflows for the engine.
- `data/`: Raw input and ingestion sources.
- `chroma_db/`: Local vector database for embedded context.

## 🚀 Quick Start
To launch the interactive CertCoach CLI, activate your virtual environment, make sure the project is installed (`pip install -e .`), and run:
```powershell
.\.venv\Scripts\Activate.ps1
certcoach
```

> **📖 Full Command Reference:** See the new [commands.md](commands.md) file for a complete cheat sheet of all scripts, services (Ollama/MongoDB), and pipeline tools used in this project.

## Obsidian Vault

This repository is optimized to be opened as an **Obsidian Vault**. You can simply open the root directory in Obsidian. 

Configuration is pre-applied in the `.obsidian/` folder to manage attachments and link updates properly. Note: Your personal Workspace state (`.obsidian/workspace.json`) is excluded from Git commits via `.gitignore`.
