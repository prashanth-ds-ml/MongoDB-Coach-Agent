from unittest.mock import patch, MagicMock
from certcoach.jobs.map_questions import clean_keyword, find_best_concept, run_mapping


def test_clean_keyword():
    assert clean_keyword("insertOne()") == "insertone"
    assert clean_keyword("Projections/Cursors") == "projectionscursors"
    assert clean_keyword("dot notation") == "dotnotation"


def test_find_best_concept():
    subtopics = ["insertOne()", "insertMany()", "_id and ObjectId"]
    
    # Matches insertOne()
    q1 = "How do we execute insertOne to add a single document?"
    options1 = [{"code_snippet": "db.collection.insertOne({name: 'test'})"}]
    assert find_best_concept(q1, options1, subtopics) == "insertOne()"
    
    # Matches _id and ObjectId
    q2 = "What is the structure of ObjectId?"
    options2 = [{"code_snippet": "new ObjectId()"}]
    assert find_best_concept(q2, options2, subtopics) == "_id and ObjectId"


@patch("certcoach.jobs.map_questions.database")
@patch("certcoach.jobs.map_questions.planner")
def test_run_mapping(mock_planner, mock_database):
    mock_planner.load_syllabus.return_value = [
        {
            "id": 2,
            "topic": "CRUD Operations - Create",
            "subtopics": ["insertOne()", "insertMany()"],
            "bank_topic_keys": ["CRUD Operations"]
        }
    ]
    
    mock_database.questions_col.find.return_value = [
        {
            "_id": "q1",
            "metadata": {
                "topic": "CRUD Operations",
                "topic_id": 1,
                "syllabus_topic": "Old Topic",
                "concept": "Old Concept"
            },
            "question_text": "How do we call insertOne?",
            "options": []
        }
    ]
    
    res = run_mapping(dry_run=True)
    
    assert res["total"] == 1
    assert res["mapped"] == 1
    assert res["updated"] == 1
    mock_database.questions_col.update_one.assert_not_called()
