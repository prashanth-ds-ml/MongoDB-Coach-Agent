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
- [[content_authoring_guidelines|Content Authoring Guidelines (MCQs + Flashcards)]]
- `diagrams/learner_journey.html`: the 12-step learner journey (build loop / practice loop / gated adaptive layer) mapped against current build status
- [[study_order_map|Study Order Map: Syllabus to Official Docs]]
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
- [[topic_03_benchmark|Topic 3 Benchmark Record]]
- [[topic_04_benchmark|Topic 4 Benchmark Record]]
- [[topic_05_benchmark|Topic 5 Benchmark Record]]
- [[topic_06_benchmark|Topic 6 Benchmark Record]]
- [[topic_07_benchmark|Topic 7 Benchmark Record]]
- [[topic_08_benchmark|Topic 8 Benchmark Record]]
- [[topic_09_benchmark|Topic 9 Benchmark Record]]
- [[topic_10_benchmark|Topic 10 Benchmark Record]]
- [[topic_11_benchmark|Topic 11 Benchmark Record]]
- [[topic_12_benchmark|Topic 12 Benchmark Record]]
- [[benchmark_integration_summary|Benchmark Integration Summary]]
- [[Resource Links]] (see also `resource_links.json`, the machine-readable source for this note)
- `memory/lessons/`: exported markdown lessons for Topics 3-10 (39 concepts), mirroring the validated lesson artifacts stored in `certcoach_db.lesson_artifacts`

## Audits And Migration

- [[lesson_practice_consistency_audit|Lesson-Practice Consistency Audit]]
- [[question_bank_inventory_comparison|Question-Bank Inventory Comparison]]
- [[legacy_bank_migration_report|Legacy Bank Migration Report]]
- [[forensic_pipeline_audit|Forensic Pipeline Audit]]
- [[syllabus_deep_audit_dashboard|Syllabus Deep-Audit Dashboard]]
- [[syllabus_deep_audit_details|Syllabus Deep-Audit Details]]
- [[audit_report_bson_data_types|BSON Data Types Audit Report]]
- [[cli_audit_2026-07-07|CLI Behavior Audit (2026-07-07)]]

## Companion Apps

- `mobile/`: Expo/React Native flashcard app, bundles `flashcards.json` locally, no backend coupling
- `web-flashcards/`: Vite/React web flashcard app, same dataset, browser-storage progress
- Both are standalone study aids, not part of the `certcoach` CLI's runtime or MongoDB flow.

## History

- [[session_log|Session Log]]
- [[progress_log|Progress Log]]
- [[decisions|Legacy Decisions]]
- [[active_context|Active Context (deprecated)]]: superseded by [[agent_context|Agent Context]]; kept only for old inbound links, do not treat as current

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
