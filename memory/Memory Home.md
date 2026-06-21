# Memory Home

This is the Obsidian and cross-agent navigation hub. Start with the compact context, then open only the reference needed for the current task.

## Agent Startup

- [[agent_context|Agent Context]]: compact current state and non-negotiable constraints
- [[session_handoff|Session Handoff]]: latest checkpoint and immediate continuation
- [[next_steps|Next Steps]]: approved execution order

## Release Readiness

- [[preparation_tool_gap_assessment|Preparation Tool Gap Assessment]]: blockers and final-freeze standard
- [[progress|Feature Progress]]
- [[project_exam_scope|Project Exam Scope]]
- [[MongoDB_Exam_Blueprint|MongoDB Exam Blueprint]]

## Product And Architecture

- [[coach_flow_spec|Coach Flow Spec]]
- [[lesson_template_rules|Lesson Template Rules]]
- [[study_pattern_guardrails|Study Pattern Guardrails]]
- [[architecture_decisions|Architecture Decisions]]
- [[decision_log|Decision Log]]
- [[project_layout|Project Layout]]
- [[source_ingestion_pipeline|Source Ingestion Pipeline]]
- [[reference_repo_adoption|Reference Repo Adoption]]
- [[canonical_state_flow|Canonical State Flow]]
- [[content_benchmark_schema|Content Benchmark Schema]]
- [[content_benchmark_index|Content Benchmark Index]]
- [[topic_01_benchmark|Topic 1 Benchmark Record]]
- [[topic_02_benchmark|Topic 2 Benchmark Record]]
- [[benchmark_integration_summary|Benchmark Integration Summary]]
- [[Resource Links]]

## Audits And Migration

- [[lesson_practice_consistency_audit|Lesson-Practice Consistency Audit]]
- [[question_bank_inventory_comparison|Question-Bank Inventory Comparison]]
- [[legacy_bank_migration_report|Legacy Bank Migration Report]]
- [[forensic_pipeline_audit|Forensic Pipeline Audit]]

## History

- [[session_log|Session Log]]
- [[progress_log|Progress Log]]
- [[decisions|Legacy Decisions]]

## Context Loading Rule

Do not open every linked note. Use this routing:

| Task | Read |
|---|---|
| Resume work | `agent_context`, `session_handoff`, `next_steps` |
| Runtime behavior | `coach_flow_spec`, relevant source/tests |
| Question-bank operations | `preparation_tool_gap_assessment`, `next_steps` |
| Architecture change | `architecture_decisions`, `decision_log` |
| Syllabus/content change | `project_exam_scope`, `MongoDB_Exam_Blueprint` |
| Legacy bank investigation | `question_bank_inventory_comparison`, `legacy_bank_migration_report` |
| Historical investigation | `session_log`, `progress_log` |

## Obsidian Conventions

- Use wikilinks for project-memory notes.
- Put durable decisions in `decision_log.md`.
- Keep session history append-only in `session_log.md`.
- Keep the active context compact; link to details instead of duplicating them.
- Use templates under `templates/` for handoffs and decisions.
- Put temporary personal notes under `memory/local/`; Git ignores that folder.
