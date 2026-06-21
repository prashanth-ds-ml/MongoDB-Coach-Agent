# CertCoach Agent Guide

This is the vendor-neutral instruction entrypoint for Codex, Claude, Copilot, OpenCode, and other coding agents.

## Startup Context Budget

Read only these files before ordinary work:

1. `AGENTS.md`
2. `memory/agent_context.md`
3. `memory/session_handoff.md`

Then read only the task-specific references linked from `memory/Memory Home.md`. Do not preload all files under `memory/`, `data/`, or `src/certcoach/data/`.

## Project Goal

Make CertCoach a dependable preparation tool for the MongoDB Associate Python Developer certification. The required path is:

```text
daily agenda -> concept lesson -> scoped Q&A -> five-question practice
-> answer review -> persisted progress -> mixed mock
```

## Current Constraints

- `certcoach_db` is the source of truth for learner state and questions.
- `3 Easy + 2 Medium` active questions is the study-readiness gate.
- Ordered population continues toward configurable per-concept inventory targets, default `5 Easy + 5 Medium`.
- Repair and population run in canonical syllabus topic/concept order.
- Long live-bank repair/population jobs run only as controlled overnight batches.
- Do not add optional product features before the preparation-readiness blockers are cleared.
- Do not expose legacy, repair-pending, or quarantined questions to practice or mocks.

## Engineering Workflow

- Prefer existing project patterns and narrowly scoped changes.
- Preserve unrelated user changes.
- Add or update focused tests for behavior changes.
- Run `.\.venv\Scripts\python.exe -m pytest tests\unit -q`.
- Plain `pytest` currently has a known scratch-test discovery blocker; see `memory/preparation_tool_gap_assessment.md`.
- Update `memory/session_handoff.md` at the end of substantial work.
- Append durable decisions to `memory/decision_log.md`; do not rewrite history.

## Context Routing

- Current status and constraints: `memory/agent_context.md`
- Immediate continuation: `memory/session_handoff.md`
- Prioritized work: `memory/next_steps.md`
- Release blockers: `memory/preparation_tool_gap_assessment.md`
- Product behavior: `memory/coach_flow_spec.md`
- Architecture decisions: `memory/architecture_decisions.md`
- Syllabus scope: `memory/project_exam_scope.md`
- Commands: `commands.md`

## Documentation Rules

- Keep `memory/agent_context.md` under roughly 800 words.
- Keep `memory/session_handoff.md` focused on current state, latest changes, and the next action.
- Put historical detail in append-only logs.
- Link to deep references instead of copying them into active context.
- Use exact dates and live metrics when updating snapshots.

## Key Commands (Windows PowerShell)

```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Install in editable mode after changes
pip install -e .

# Run unit tests (use this, not plain pytest)
.\.venv\Scripts\python.exe -m pytest tests\unit -q

# Preview next concept needing repair/population
.\.venv\Scripts\python.exe -m certcoach.jobs.next_phase4_topic

# Run bounded Phase 4 overnight repair + populate
.\scripts\run_phase4_overnight.ps1 -RepairBatchSize 25 -PopulationBatchSize 25

# Start the CLI
certcoach
```

## Entry Points (from pyproject.toml)

| Command | Module |
|---------|--------|
| `certcoach` | `certcoach.cli:main_menu` |
| `certcoach-seed-nightly` | `certcoach.jobs.nightly_seed_questions:main` |
| `certcoach-repair-explanations` | `certcoach.jobs.repair_explanations:main` |
| `certcoach-dedupe-questions` | `certcoach.jobs.dedupe_questions:main` |
| `certcoach-map-questions` | `certcoach.jobs.map_questions:main` |
| `certcoach-extract` | `certcoach.core.image_extractor:process_pics_qa` |

## Repo Structure Notes

- **Root is an Obsidian vault** — contains `.obsidian/` config and markdown memory files under `memory/`.
- **Source layout**: `src/certcoach/` (main package), `src/scripts/` (legacy utilities), `src/antigravity_cli/` (separate CLI).
- **Tests**: `tests/unit/` — run with `python -m pytest tests\unit -q` to avoid collecting `scratch/test_zhipu_vision.py`.
- **Configuration**: `~/.certcoach/.env` (not repo-local) — see `.env.example` for schema.
- **Logs**: `logs/phase4-overnight-*.log` — created by overnight runner.
- **Backups**: `backups/questions-*/` — created before repair/population runs.

## Non-Obvious Conventions

- **VRAM-safe operations**: Population scripts check `nvidia-smi` and unload models (`keep_alive=0`) between stages.
- **Question lifecycle states**: `active`, `repair_pending`, `quarantined`, `legacy` — only `active` questions reach learners.
- **Canonical order**: All repair/population follows `syllabus.json` topic → concept sequence.
- **Environment**: Requires local MongoDB (`mongodb://localhost:27017` or Atlas URI) and running Ollama (`ollama serve`).
- **Models**: `qwen3.5:4b` (study), `gemma4:12b` (population/repair) — configured in `~/.certcoach/.env`.