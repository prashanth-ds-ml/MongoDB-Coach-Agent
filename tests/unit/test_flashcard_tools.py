from unittest.mock import patch


def _card(**overrides):
    card = {
        "id": "fc-test-1",
        "topic_id": 1,
        "concept": "BSON Data Types",
        "category": "Overview & Document Model",
        "domain_weight_pct": 8,
        "subheading": "1.1",
        "source_doc": "topic_01_docs_manual_reference_bson_types__cf63661090.md",
        "title": "Test card",
        "question": "What is being tested?",
        "answer": "A short, clean answer that ends properly.",
    }
    card.update(overrides)
    return card


def test_validate_cards_accepts_clean_card():
    from certcoach.jobs.flashcard_tools import validate_cards

    assert validate_cards([_card()]) == []


def test_validate_cards_flags_missing_required_field():
    from certcoach.jobs.flashcard_tools import validate_cards

    card = _card()
    del card["source_doc"]

    issues = validate_cards([card])

    assert len(issues) == 1
    assert "missing required field" in issues[0]
    assert "source_doc" in issues[0]


def test_validate_cards_flags_duplicate_ids():
    from certcoach.jobs.flashcard_tools import validate_cards

    issues = validate_cards([_card(), _card()])

    assert any("duplicate id" in issue for issue in issues)


def test_validate_cards_flags_truncation():
    from certcoach.jobs.flashcard_tools import validate_cards

    card = _card(answer="This answer cuts off mid-word for th")

    issues = validate_cards([card])

    assert any("truncation" in issue for issue in issues)


def test_validate_cards_flags_scrape_artifacts():
    from certcoach.jobs.flashcard_tools import validate_cards

    card1 = _card(id="fc-a", answer="Some real content.\nFull Practice Set link below")
    card2 = _card(id="fc-b", answer="Some content.\n## Section 2: CRUD (51%)\nMore.")

    issues = validate_cards([card1, card2])

    assert any("Full Practice Set" in issue for issue in issues)
    assert any("bleed-through section header" in issue for issue in issues)


def test_validate_cards_flags_unmatched_code_fence():
    from certcoach.jobs.flashcard_tools import validate_cards

    card = _card(answer="```javascript\ndb.foo.find()\nUnfinished fence.")

    issues = validate_cards([card])

    assert any("unmatched code fence" in issue for issue in issues)


def test_validate_cards_flags_overlong_answer():
    from certcoach.jobs.flashcard_tools import validate_cards

    card = _card(answer=("word " * 200).strip() + ".")

    issues = validate_cards([card])

    assert any("too long for a flashcard" in issue for issue in issues)


def test_merge_cards_writes_all_three_copies_in_sync(tmp_path):
    import certcoach.jobs.flashcard_tools as ft

    paths = [tmp_path / "a.json", tmp_path / "b.json", tmp_path / "c.json"]
    for p in paths:
        p.write_text('[{"id": "old-1", "topic_id": 2}]', encoding="utf-8")

    with patch.object(ft, "FLASHCARD_PATHS", [str(p) for p in paths]):
        result = ft.merge_cards([_card()])

    assert result == {"before": 1, "removed": 0, "added": 1, "after": 2}
    contents = [p.read_text(encoding="utf-8") for p in paths]
    assert contents[0] == contents[1] == contents[2]


def test_merge_cards_can_remove_by_topic_id(tmp_path):
    import certcoach.jobs.flashcard_tools as ft

    paths = [tmp_path / "a.json", tmp_path / "b.json", tmp_path / "c.json"]
    for p in paths:
        p.write_text('[{"id": "old-1", "topic_id": 2}, {"id": "old-2", "topic_id": 3}]', encoding="utf-8")

    with patch.object(ft, "FLASHCARD_PATHS", [str(p) for p in paths]):
        result = ft.merge_cards([_card()], remove_topic_ids={2})

    assert result == {"before": 2, "removed": 1, "added": 1, "after": 2}


def test_merge_cards_rejects_colliding_ids(tmp_path):
    import certcoach.jobs.flashcard_tools as ft

    paths = [tmp_path / "a.json", tmp_path / "b.json", tmp_path / "c.json"]
    for p in paths:
        p.write_text('[{"id": "fc-test-1", "topic_id": 9}]', encoding="utf-8")

    with patch.object(ft, "FLASHCARD_PATHS", [str(p) for p in paths]):
        try:
            ft.merge_cards([_card()])
            assert False, "expected ValueError"
        except ValueError as exc:
            assert "collide" in str(exc)


def test_merge_cards_rejects_invalid_new_cards(tmp_path):
    import certcoach.jobs.flashcard_tools as ft

    paths = [tmp_path / "a.json", tmp_path / "b.json", tmp_path / "c.json"]
    for p in paths:
        p.write_text("[]", encoding="utf-8")

    bad_card = _card()
    del bad_card["answer"]

    with patch.object(ft, "FLASHCARD_PATHS", [str(p) for p in paths]):
        try:
            ft.merge_cards([bad_card])
            assert False, "expected ValueError"
        except ValueError as exc:
            assert "validation failed" in str(exc)
