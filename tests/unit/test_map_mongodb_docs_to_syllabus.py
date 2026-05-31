from src.scripts.utils.map_mongodb_docs_to_syllabus import (
    score_doc,
    slugify,
    terms_for_topic,
)


def test_slugify_builds_stable_folder_names():
    assert slugify("CRUD Operations - Create") == "crud_operations_create"
    assert slugify("Query Operators & MQL") == "query_operators_mql"


def test_terms_for_topic_combines_syllabus_fields():
    topic = {
        "topic": "CRUD Operations - Read",
        "subtopics": ["find()", "sort/limit/skip"],
        "question_keywords": ["projection"],
        "bank_topic_keys": ["Finding Documents in a MongoDB Collection"],
    }

    terms = terms_for_topic(topic)

    assert "crud operations" in terms
    assert "read" in terms
    assert "find" in terms
    assert "sort" in terms
    assert "projection" in terms


def test_score_doc_prefers_curated_paths():
    topic = {
        "id": 3,
        "topic": "CRUD Operations - Read",
        "subtopics": ["find()", "Projections"],
        "question_keywords": ["find", "projection"],
        "bank_topic_keys": [],
    }
    entry = {
        "source_url": "https://www.mongodb.com/docs/manual/tutorial/query-documents/",
        "markdown_url": "https://www.mongodb.com/docs/manual/tutorial/query-documents.md",
    }

    score, matched_terms = score_doc(topic, entry, "# Query Documents\nUse find and projection.")

    assert score >= 100
    assert any(term.startswith("path:") for term in matched_terms)


def test_score_doc_penalizes_non_python_driver_for_pymongo_topic():
    topic = {
        "id": 11,
        "topic": "MongoDB Drivers & PyMongo",
        "subtopics": ["MongoClient"],
        "question_keywords": ["driver", "mongoclient"],
        "bank_topic_keys": [],
    }
    csharp_entry = {
        "source_url": "https://www.mongodb.com/docs/drivers/csharp/current/connect/mongoclient/",
        "markdown_url": "https://www.mongodb.com/docs/drivers/csharp/current/connect/mongoclient.md",
    }
    pymongo_entry = {
        "source_url": "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/mongoclient/",
        "markdown_url": "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/mongoclient.md",
    }

    csharp_score, _ = score_doc(topic, csharp_entry, "# MongoClient")
    pymongo_score, _ = score_doc(topic, pymongo_entry, "# MongoClient")

    assert pymongo_score > csharp_score
