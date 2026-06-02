from certcoach.core.image_extractor import normalize_topic_name


def test_normalize_topic_name_maps_legacy_aliases():
    assert normalize_topic_name("CRUD Operations - Read (Basic & Cursor)") == "CRUD Operations - Read"
    assert normalize_topic_name("Query Operators (L2/L3/L5)") == "Query Operators & MQL"
    assert normalize_topic_name("Querying Arrays & Subdocuments") == "Querying Arrays & Embedded Documents"
    assert normalize_topic_name("MongoDB Atlas & Operations") == "Tools, Tooling & Atlas Search"
