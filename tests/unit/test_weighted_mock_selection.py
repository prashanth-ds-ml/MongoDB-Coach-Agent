from unittest.mock import MagicMock, patch


def _question(topic_id: int, concept: str, qid: str) -> dict:
    return {
        "_id": qid,
        "metadata": {"topic_id": topic_id, "concept": concept, "content_contract_version": 2, "content_contract_status": "generated"},
        "provenance": {"state": "confirmed"},
    }


def test_apportion_largest_remainder_sums_to_total_at_n53():
    from certcoach.core import database

    result = database.apportion_largest_remainder(53, database.EXAM_DOMAIN_WEIGHTS)

    assert sum(result.values()) == 53
    assert result["CRUD Operations"] == 27
    assert result["Drivers & PyMongo"] == 10
    assert result["Indexes"] == 9
    assert result["Overview & Document Model"] == 4
    assert result["Data Modeling"] == 2
    assert result["Tools & Tooling"] == 1


def test_apportion_largest_remainder_sums_to_total_for_arbitrary_n():
    from certcoach.core import database

    for n in (1, 5, 20, 53, 100):
        result = database.apportion_largest_remainder(n, database.EXAM_DOMAIN_WEIGHTS)
        assert sum(result.values()) == n
        assert all(v >= 0 for v in result.values())


def test_round_robin_pick_caps_a_dominant_concept():
    from certcoach.core import database

    pools = {
        "insertOne()": [f"i{i}" for i in range(20)],
        "insertMany()": [f"m{i}" for i in range(2)],
    }

    picked = database._round_robin_pick(pools, limit=6)

    assert len(picked) == 6
    insert_many_count = sum(1 for p in picked if p.startswith("m"))
    assert insert_many_count == 2  # the whole small pool gets pulled in, not starved


def test_round_robin_pick_stops_when_pools_exhausted():
    from certcoach.core import database

    pools = {"a": ["a1", "a2"], "b": ["b1"]}

    picked = database._round_robin_pick(pools, limit=10)

    assert len(picked) == 3


def test_get_weighted_mock_questions_reports_domain_shortfall_never_pads():
    from certcoach.core import database

    # Only Indexes (topic 9) is starved; every other domain has plenty.
    bank = []
    for topic_id in range(1, 13):
        if topic_id == 9:
            continue
        for i in range(10):
            bank.append(_question(topic_id, f"concept-{topic_id}-{i}", f"q{topic_id}-{i}"))

    questions_col = MagicMock()
    questions_col.find.side_effect = lambda query: [
        q for q in bank if q["metadata"]["topic_id"] in query["metadata.topic_id"]["$in"]
    ]

    with patch.object(database, "questions_col", questions_col):
        result = database.get_weighted_mock_questions(53)

    assert "Indexes" in result["domain_shortfall"]
    assert result["domain_shortfall"]["Indexes"]["available"] == 0
    assert result["domain_shortfall"]["Indexes"]["needed"] == 9
    # Never padded: total selected is short by exactly the missing domain's target.
    assert len(result["questions"]) == 53 - 9


def test_get_weighted_mock_questions_only_uses_confirmed_inventory():
    from certcoach.core import database

    confirmed = _question(2, "insertOne()", "confirmed-q")
    draft = {
        "_id": "draft-q",
        "metadata": {"topic_id": 2, "concept": "insertOne()", "content_contract_version": 2, "content_contract_status": "generated"},
        "provenance": {"state": "draft"},
    }

    questions_col = MagicMock()
    questions_col.find.return_value = [confirmed, draft]

    with patch.object(database, "questions_col", questions_col):
        result = database.get_weighted_mock_questions(1)

    all_ids = [q["_id"] for q in result["questions"]]
    assert "draft-q" not in all_ids
