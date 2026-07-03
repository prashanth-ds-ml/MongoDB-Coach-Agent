"""Prebuild canonical lesson artifacts one concept at a time."""
from __future__ import annotations

import argparse

from certcoach.core import lesson_bank


def main() -> None:
    parser = argparse.ArgumentParser(description="Prebuild one lesson artifact in canonical syllabus order.")
    parser.add_argument("--topic-id", type=int, default=None, help="Exact syllabus topic id to prebuild.")
    parser.add_argument("--concept", default=None, help="Exact syllabus concept to prebuild.")
    args = parser.parse_args()

    artifact = lesson_bank.prebuild_lesson(topic_id=args.topic_id, concept=args.concept)
    print(
        f"Prebuilt lesson | Topic {artifact['topic_id']} | {artifact['topic']} | "
        f"{artifact['concept']} | status={artifact['status']} | "
        f"issues={len(artifact.get('validation_issues', []))}"
    )
    for issue in artifact.get("validation_issues", []):
        print(f"- {issue}")


if __name__ == "__main__":
    main()
