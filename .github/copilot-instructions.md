# Copilot Project Instructions

Use `AGENTS.md` as the authoritative repository guide. Before making changes, read `memory/agent_context.md` and `memory/session_handoff.md`. Load only task-specific references linked from `memory/Memory Home.md`.

Keep changes scoped, preserve unrelated work, update focused tests, and run:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\unit -q
```

