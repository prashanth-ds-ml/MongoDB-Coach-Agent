from unittest.mock import MagicMock, patch


def test_get_first_lesson_target_uses_topic1_first_concept():
    from certcoach.core import lesson_bank

    syllabus = [{
        "id": 1,
        "topic": "MongoDB Overview & The Document Model",
        "subtopics": ["BSON Data Types", "Document structure"],
        "md_files": ["topic_01_docs_manual_reference_bson_types__cf63661090.md"],
    }]

    with patch.object(lesson_bank.planner, "load_syllabus", return_value=syllabus):
        target = lesson_bank.get_first_lesson_target()

    assert target.topic_id == 1
    assert target.topic == "MongoDB Overview & The Document Model"
    assert target.concept == "BSON Data Types"


def test_validate_lesson_markdown_accepts_clean_lesson():
    from certcoach.core.lesson_bank import validate_lesson_markdown

    lesson = """
### 1. Core Concept
Definition

### 2. Level-Based Breakdown
#### Beginners
Intro
#### Intermediate Learners
More detail
#### Advanced Developers
Tradeoff

### 3. Syntax & Code Examples
#### DO: Best Practice
Use a BSON example.
#### DON'T / EXAM TRAP
Avoid the wrong BSON type.

### 4. Exam Radar
- BSON vs JSON
- Flexible schema
- Array vs scalar

### 5. Micro-Challenge
Which BSON type would you use for a field that stores an exact timestamp value?

### 6. 30-Second Recall
- BSON supports more types than JSON.
- Documents can nest arrays and subdocuments.
- Choose BSON types based on stored behavior.
"""

    result = validate_lesson_markdown(lesson)

    assert result["is_valid"] is True
    assert result["issues"] == []


def test_validate_lesson_markdown_rejects_micro_challenge_answer():
    from certcoach.core.lesson_bank import validate_lesson_markdown

    lesson = """
### 1. Core Concept
Text
### 2. Level-Based Breakdown
Text
### 3. Syntax & Code Examples
Text
### 4. Exam Radar
Text
### 5. Micro-Challenge
Which BSON type stores multiple values?
Correct Answer: Array
### 6. 30-Second Recall
- One
- Two
- Three
"""

    result = validate_lesson_markdown(lesson)

    assert result["is_valid"] is False
    assert "micro-challenge contains forbidden answer or hint content" in result["issues"]


def test_validate_lesson_markdown_rejects_topic1_future_topic_leaks():
    from certcoach.core.lesson_bank import validate_lesson_markdown

    lesson = """
### 1. Core Concept
Documents are records.

### 2. Level-Based Breakdown
#### Beginners
Text
#### Intermediate Learners
Text
#### Advanced Developers
Text

### 3. Syntax & Code Examples
Use `db.users.findOne()` and `db.users.insertOne({name: "A"})`.

### 4. Exam Radar
- Beware of $project and dot notation.

### 5. Micro-Challenge
Explain why a MongoDB document can contain nested fields.

### 6. 30-Second Recall
- One
- Two
- Three
"""

    result = validate_lesson_markdown(lesson, topic_id=1, concept="Document structure")

    assert result["is_valid"] is False
    assert "CRUD read method leak: findOne()" in result["issues"]
    assert "CRUD write method leak: insertOne()" in result["issues"]
    assert "Aggregation/query operator leak: $project" in result["issues"]
    assert "Future concept leak: dot notation" in result["issues"]


def test_prebuild_lesson_stores_validated_artifact():
    from certcoach.core import lesson_bank

    syllabus = [{
        "id": 1,
        "topic": "MongoDB Overview & The Document Model",
        "subtopics": ["BSON Data Types"],
        "md_files": ["topic_01_docs_manual_reference_bson_types__cf63661090.md"],
    }]
    coach = MagicMock()
    coach.explain_topic.return_value = """
### 1. Core Concept
Definition
### 2. Level-Based Breakdown
#### Beginners
Intro
#### Intermediate Learners
Detail
#### Advanced Developers
Tradeoff
### 3. Syntax & Code Examples
#### DO: Best Practice
Use BSON literals.
#### DON'T / EXAM TRAP
Do not confuse JSON and BSON types.
### 4. Exam Radar
- BSON vs JSON
- Arrays
- ObjectId
### 5. Micro-Challenge
Name one BSON type that does not exist in plain JSON.
### 6. 30-Second Recall
- BSON extends JSON.
- ObjectId is a BSON type.
- Arrays preserve order.
"""
    coach.repair_topic_lesson.return_value = coach.explain_topic.return_value

    with patch.object(lesson_bank.planner, "load_syllabus", return_value=syllabus), \
         patch.object(lesson_bank.planner, "prioritize_md_files", return_value=syllabus[0]["md_files"]), \
         patch.object(lesson_bank.planner, "score_md_file_for_concept", return_value=10), \
         patch.object(lesson_bank.planner, "load_md_context", return_value="official docs"), \
         patch.object(lesson_bank.planner, "load_topic_benchmark_focus", return_value=""), \
         patch.object(lesson_bank.planner, "load_topic_benchmark_context", return_value=""), \
         patch.object(lesson_bank.database, "upsert_lesson_artifact") as upsert:
        artifact = lesson_bank.prebuild_lesson(coach=coach)

    assert artifact["status"] == "validated"
    assert artifact["topic_id"] == 1
    assert artifact["concept"] == "BSON Data Types"
    upsert.assert_called_once()


def test_prebuild_lesson_falls_back_to_section_repair_for_missing_sections():
    from certcoach.core import lesson_bank

    syllabus = [{
        "id": 1,
        "topic": "MongoDB Overview & The Document Model",
        "subtopics": ["BSON Data Types"],
        "md_files": ["topic_01_docs_manual_reference_bson_types__cf63661090.md"],
    }]
    coach = MagicMock()
    coach.explain_topic.return_value = "### 1. Core Concept\nBSON is MongoDB's native format."
    coach.repair_topic_lesson.return_value = "###"
    coach.generate_lesson_section.side_effect = [
        "#### Beginners\nStart here.\n#### Intermediate Learners\nGo deeper.\n#### Advanced Developers\nTradeoffs.",
        "#### DO: Best Practice\nUse BSON literals.\n#### DON'T / EXAM TRAP\nDo not confuse JSON and BSON.",
        "- BSON vs JSON: the exam tests storage semantics.",
        "Name one BSON type that does not exist in plain JSON.",
        "- BSON extends JSON.\n- ObjectId is BSON.\n- Arrays preserve order.",
    ]

    with patch.object(lesson_bank.planner, "load_syllabus", return_value=syllabus), \
         patch.object(lesson_bank.planner, "prioritize_md_files", return_value=syllabus[0]["md_files"]), \
         patch.object(lesson_bank.planner, "score_md_file_for_concept", return_value=10), \
         patch.object(lesson_bank.planner, "load_md_context", return_value="official docs"), \
         patch.object(lesson_bank.planner, "load_topic_benchmark_focus", return_value=""), \
         patch.object(lesson_bank.planner, "load_topic_benchmark_context", return_value=""), \
         patch.object(lesson_bank.database, "upsert_lesson_artifact"):
        artifact = lesson_bank.prebuild_lesson(coach=coach)

    assert artifact["status"] == "validated"
    assert "### 6. 30-Second Recall" in artifact["lesson_markdown"]


def test_prebuild_lesson_regenerates_leaky_topic1_sections():
    from certcoach.core import lesson_bank

    syllabus = [{
        "id": 1,
        "topic": "MongoDB Overview & The Document Model",
        "subtopics": ["Document structure"],
        "md_files": ["topic_01_docs_manual_core_document__a8bd5970ef.md"],
    }]
    coach = MagicMock()
    coach.explain_topic.return_value = """
### 1. Core Concept
Documents are records and queries read them.

### 2. Level-Based Breakdown
#### Beginners
Text
#### Intermediate Learners
Text
#### Advanced Developers
Text

### 3. Syntax & Code Examples
Use dot notation and findOne().

### 4. Exam Radar
- Watch query behavior.

### 5. Micro-Challenge
Explain embedded documents.

### 6. 30-Second Recall
- One
- Two
- Three
"""
    coach.repair_topic_lesson.return_value = coach.explain_topic.return_value
    coach.generate_lesson_section.side_effect = [
        "Documents are records composed of fields and values.",
        "Use embedded documents and arrays as document literals only.",
        "- Embedded documents stay inside one parent document.",
    ]

    with patch.object(lesson_bank.planner, "load_syllabus", return_value=syllabus), \
         patch.object(lesson_bank.planner, "prioritize_md_files", return_value=syllabus[0]["md_files"]), \
         patch.object(lesson_bank.planner, "score_md_file_for_concept", return_value=10), \
         patch.object(lesson_bank.planner, "load_md_context", return_value="official docs"), \
         patch.object(lesson_bank.planner, "load_topic_benchmark_focus", return_value=""), \
         patch.object(lesson_bank.planner, "load_topic_benchmark_context", return_value=""), \
         patch.object(lesson_bank.database, "upsert_lesson_artifact"):
        artifact = lesson_bank.prebuild_lesson(topic_id=1, concept="Document structure", coach=coach)

    assert artifact["status"] == "validated"
    assert "findOne()" not in artifact["lesson_markdown"]
    assert "dot notation" not in artifact["lesson_markdown"].lower()


def test_prebuild_lesson_repairs_invalid_recall_section():
    from certcoach.core import lesson_bank

    syllabus = [{
        "id": 2,
        "topic": "CRUD Operations - Create",
        "subtopics": ["insertOne()"],
        "md_files": ["topic_02_CRUD_Create_L1_01.md"],
    }]
    coach = MagicMock()
    coach.explain_topic.return_value = """
### 1. Core Concept
Text

### 2. Level-Based Breakdown
#### Beginners
Text
#### Intermediate Learners
Text
#### Advanced Developers
Text

### 3. Syntax & Code Examples
#### DO: Best Practice
Text
#### DON'T / EXAM TRAP
Text

### 4. Exam Radar
- One
- Two
- Three

### 5. Micro-Challenge
Write one valid insertOne() example.

### 6. 30-Second Recall
###
"""
    coach.repair_topic_lesson.return_value = coach.explain_topic.return_value
    coach.generate_lesson_section.return_value = "- insertOne() inserts exactly one document.\n- MongoDB generates _id if omitted.\n- The result includes acknowledged and insertedId."

    with patch.object(lesson_bank.planner, "load_syllabus", return_value=syllabus), \
         patch.object(lesson_bank.planner, "prioritize_md_files", return_value=syllabus[0]["md_files"]), \
         patch.object(lesson_bank.planner, "score_md_file_for_concept", return_value=10), \
         patch.object(lesson_bank.planner, "load_md_context", return_value="official docs"), \
         patch.object(lesson_bank.planner, "load_topic_benchmark_focus", return_value=""), \
         patch.object(lesson_bank.planner, "load_topic_benchmark_context", return_value=""), \
         patch.object(lesson_bank.database, "upsert_lesson_artifact"):
        artifact = lesson_bank.prebuild_lesson(topic_id=2, concept="insertOne()", coach=coach)

    assert artifact["status"] == "validated"
    assert "- insertOne() inserts exactly one document." in artifact["lesson_markdown"]


def test_prebuild_lesson_uses_deterministic_recall_fallback_when_model_recall_stays_invalid():
    from certcoach.core import lesson_bank

    syllabus = [{
        "id": 2,
        "topic": "CRUD Operations - Create",
        "subtopics": ["insertOne()"],
        "md_files": ["topic_02_CRUD_Create_L1_01.md"],
    }]
    coach = MagicMock()
    coach.explain_topic.return_value = """
### 1. Core Concept
Text

### 2. Level-Based Breakdown
#### Beginners
Text
#### Intermediate Learners
Text
#### Advanced Developers
Text

### 3. Syntax & Code Examples
#### DO: Best Practice
Text
#### DON'T / EXAM TRAP
Text

### 4. Exam Radar
- One
- Two
- Three

### 5. Micro-Challenge
Write one valid insertOne() example.

### 6. 30-Second Recall
*
"""
    coach.repair_topic_lesson.return_value = coach.explain_topic.return_value
    coach.generate_lesson_section.return_value = "*"

    with patch.object(lesson_bank.planner, "load_syllabus", return_value=syllabus), \
         patch.object(lesson_bank.planner, "prioritize_md_files", return_value=syllabus[0]["md_files"]), \
         patch.object(lesson_bank.planner, "score_md_file_for_concept", return_value=10), \
         patch.object(lesson_bank.planner, "load_md_context", return_value="official docs"), \
         patch.object(lesson_bank.planner, "load_topic_benchmark_focus", return_value=""), \
         patch.object(lesson_bank.planner, "load_topic_benchmark_context", return_value=""), \
         patch.object(lesson_bank.database, "upsert_lesson_artifact"):
        artifact = lesson_bank.prebuild_lesson(topic_id=2, concept="insertOne()", coach=coach)

    assert artifact["status"] == "validated"
    assert "- `insertOne()` inserts exactly one document." in artifact["lesson_markdown"]
