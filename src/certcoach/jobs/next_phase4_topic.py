from __future__ import annotations

import argparse
import sys

from certcoach.core import planner
from certcoach.core.config import get_population_easy_target, get_population_medium_target
from certcoach.jobs.question_bank_comparison_report import build_inventory_report


def _group_concepts_by_topic(report: dict) -> dict[int, list[dict]]:
    by_topic: dict[int, list[dict]] = {}
    for concept in report.get("concepts", []):
        by_topic.setdefault(int(concept["topic_id"]), []).append(concept)
    return by_topic


def select_next_topic(
    report: dict,
    syllabus: list[dict] | None = None,
    topic_filter: int | None = None,
    easy_target: int | None = None,
    medium_target: int | None = None,
) -> dict | None:
    concepts_by_key = {
        (int(concept["topic_id"]), concept["concept"]): concept
        for concept in report.get("concepts", [])
    }
    syllabus = syllabus or [
        {
            "id": topic_id,
            "topic": concepts[0]["topic"],
            "subtopics": [concept["concept"] for concept in concepts],
        }
        for topic_id, concepts in sorted(_group_concepts_by_topic(report).items())
    ]
    easy_target = max(3, easy_target if easy_target is not None else get_population_easy_target())
    medium_target = max(2, medium_target if medium_target is not None else get_population_medium_target())

    for topic_item in syllabus:
        topic_id = int(topic_item["id"])
        if topic_filter is not None and topic_id != topic_filter:
            continue
        concepts = [
            concepts_by_key[(topic_id, concept)]
            for concept in topic_item.get("subtopics", [])
            if (topic_id, concept) in concepts_by_key
        ]
        first_incomplete = next(
            (
                concept for concept in concepts
                if concept.get("repair_pending", 0) > 0
                or concept.get("quarantine_pending", 0) > 0
                or concept.get("regeneration_pending", 0) > 0
                or concept.get("legacy_pending", 0) > 0
                or concept["easy_active"] < easy_target
                or concept["medium_active"] < medium_target
            ),
            None,
        )
        if first_incomplete:
            return {
                "topic_id": topic_id,
                "topic": topic_item["topic"],
                "concept": first_incomplete["concept"],
                "concept_count": len(concepts),
                "ready_concepts": sum(1 for concept in concepts if concept["study_ready"]),
                "easy_readiness_deficit": sum(concept["easy_readiness_deficit"] for concept in concepts),
                "medium_readiness_deficit": sum(concept["medium_readiness_deficit"] for concept in concepts),
                "concept_easy_readiness_deficit": first_incomplete["easy_readiness_deficit"],
                "concept_medium_readiness_deficit": first_incomplete["medium_readiness_deficit"],
                "concept_easy_population_deficit": max(0, easy_target - first_incomplete["easy_active"]),
                "concept_medium_population_deficit": max(0, medium_target - first_incomplete["medium_active"]),
                "concept_repair_pending": first_incomplete.get("repair_pending", 0),
                "concept_quarantine_pending": first_incomplete.get("quarantine_pending", 0),
                "concept_regeneration_pending": first_incomplete.get("regeneration_pending", 0),
                "concept_legacy_pending": first_incomplete.get("legacy_pending", 0),
                "population_easy_target": easy_target,
                "population_medium_target": medium_target,
            }
    return None


def get_next_topic(topic_filter: int | None = None) -> dict | None:
    return select_next_topic(build_inventory_report(), planner.load_syllabus(), topic_filter)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Select the first syllabus concept needing repair or population.")
    parser.add_argument("--id-only", action="store_true", help="Print only the selected topic id.")
    parser.add_argument("--concept-only", action="store_true", help="Print only the first not-ready concept.")
    parser.add_argument("--topic", type=int, default=None, help="Restrict selection to one exact syllabus topic id.")
    args = parser.parse_args(argv)
    topic = get_next_topic(args.topic)
    if not topic:
        print("")
        return 0
    if args.id_only:
        print(topic["topic_id"])
    elif args.concept_only:
        print(topic["concept"])
    else:
        print(
            f"Topic {topic['topic_id']}: {topic['topic']} | "
            f"ready concepts {topic['ready_concepts']}/{topic['concept_count']} | "
            f"next concept: {topic['concept']} | "
            f"population missing Easy {topic['concept_easy_population_deficit']}, "
            f"Medium {topic['concept_medium_population_deficit']} | "
            f"repair pending {topic['concept_repair_pending']} | "
            f"quarantine pending {topic['concept_quarantine_pending']} | "
            f"regeneration pending {topic['concept_regeneration_pending']} | "
            f"legacy pending {topic['concept_legacy_pending']} | "
            f"topic missing Easy {topic['easy_readiness_deficit']}, Medium {topic['medium_readiness_deficit']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
