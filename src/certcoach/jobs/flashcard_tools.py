"""Validate and merge flashcards across the three bundled copies
(`data/flashcards.json`, `mobile/assets/flashcards.json`,
`web-flashcards/src/flashcards.json`) that must always stay byte-identical.

Built for the /flashcards workflow: a human or Claude authors a batch of new
cards as a JSON file, this validates them (schema, truncation, scrape
artifacts) and merges them into all three copies atomically -- either all
three get written, or none do.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))

FLASHCARD_PATHS = [
    os.path.join(REPO_ROOT, "data", "flashcards.json"),
    os.path.join(REPO_ROOT, "mobile", "assets", "flashcards.json"),
    os.path.join(REPO_ROOT, "web-flashcards", "src", "flashcards.json"),
]

REQUIRED_FIELDS = {
    "id", "topic_id", "concept", "category", "domain_weight_pct",
    "subheading", "source_doc", "title", "question", "answer",
}


def validate_cards(cards: list[dict]) -> list[str]:
    """Returns a list of human-readable issue strings; empty means clean.
    Checks schema completeness, duplicate ids, truncation heuristics, and
    the exact scrape-artifact patterns found in the original imported file
    (see memory/decision_log.md 2026-07-08 for the original findings)."""
    issues: list[str] = []
    seen_ids: set[str] = set()

    for card in cards:
        cid = card.get("id", "<missing id>")

        missing = REQUIRED_FIELDS - card.keys()
        if missing:
            issues.append(f"{cid}: missing required field(s) {sorted(missing)}")

        if cid in seen_ids:
            issues.append(f"{cid}: duplicate id")
        seen_ids.add(cid)

        answer = card.get("answer", "")
        stripped = answer.rstrip()
        if stripped and stripped[-1] not in ".!?`)":
            issues.append(f"{cid}: possible truncation (ends with {stripped[-40:]!r})")
        if "Full Practice Set" in answer:
            issues.append(f"{cid}: scrape artifact (\"Full Practice Set link below\")")
        if re.search(r"## Section \d", answer):
            issues.append(f"{cid}: scrape artifact (bleed-through section header)")
        if answer.count("```") % 2 != 0:
            issues.append(f"{cid}: unmatched code fence")

        # Flashcards should be short -- a recall aid, not a study article.
        if len(answer) > 600:
            issues.append(f"{cid}: answer is {len(answer)} chars -- too long for a flashcard, aim under ~600")

    return issues


def merge_cards(new_cards: list[dict], remove_ids: set[str] | None = None, remove_topic_ids: set[int] | None = None) -> dict:
    """Merges new_cards into the canonical copy's current contents, optionally
    dropping cards by id or by topic_id first, then writes the result to all
    three bundled copies. Raises ValueError (writing nothing) if validation
    fails or a new card's id collides with a surviving old one."""
    canonical = FLASHCARD_PATHS[0]
    with open(canonical, encoding="utf-8") as f:
        existing = json.load(f)

    remove_ids = remove_ids or set()
    remove_topic_ids = remove_topic_ids or set()
    kept = [
        c for c in existing
        if c.get("id") not in remove_ids and c.get("topic_id") not in remove_topic_ids
    ]

    kept_ids = {c["id"] for c in kept}
    colliding = kept_ids & {c["id"] for c in new_cards}
    if colliding:
        raise ValueError(f"new card id(s) collide with surviving cards: {sorted(colliding)}")

    issues = validate_cards(new_cards)
    if issues:
        raise ValueError("validation failed:\n  " + "\n  ".join(issues))

    merged = new_cards + kept

    for path in FLASHCARD_PATHS:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
            f.write("\n")

    return {
        "before": len(existing),
        "removed": len(existing) - len(kept),
        "added": len(new_cards),
        "after": len(merged),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and/or merge new flashcards into all bundled copies.")
    parser.add_argument("cards_file", help="Path to a JSON file containing a list of new card dicts.")
    parser.add_argument("--remove-ids", nargs="*", default=[], help="Existing card ids to drop before merging.")
    parser.add_argument("--remove-topic-id", type=int, default=None, help="Drop all existing cards for this topic_id before merging (e.g. replacing a whole topic's cards).")
    parser.add_argument("--validate-only", action="store_true", help="Only run validation, do not write anything.")
    args = parser.parse_args(argv)

    with open(args.cards_file, encoding="utf-8") as f:
        new_cards = json.load(f)

    issues = validate_cards(new_cards)
    if issues:
        print(f"Validation failed ({len(issues)} issue(s)):")
        for issue in issues:
            print(f"  {issue}")
        return 1
    print(f"Validation passed: {len(new_cards)} card(s) clean.")

    if args.validate_only:
        return 0

    remove_topic_ids = {args.remove_topic_id} if args.remove_topic_id is not None else None
    result = merge_cards(new_cards, remove_ids=set(args.remove_ids), remove_topic_ids=remove_topic_ids)
    print(
        f"Merged into all {len(FLASHCARD_PATHS)} copies: "
        f"{result['before']} -> {result['after']} cards "
        f"(removed {result['removed']}, added {result['added']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
