from unittest.mock import MagicMock, patch


def test_audit_weighted_deficits_filters_by_topic_id():
    from certcoach.jobs import nightly_seed_questions as job

    syllabus = [
        {
            "id": 1,
            "topic": "Topic One",
            "subtopics": ["A"],
            "exam_weight": "10%",
            "bank_topic_keys": ["Bank One"],
        },
        {
            "id": 2,
            "topic": "Topic Two",
            "subtopics": ["B"],
            "exam_weight": "10%",
            "bank_topic_keys": ["Bank Two"],
        },
    ]

    with patch.object(job.planner, "load_syllabus", return_value=syllabus), \
         patch.object(job, "_get_db_style_counts", return_value={"Type A": 0, "Type B": 0, "Type C": 0, "Type D": 0}):
        deficits = job.audit_weighted_deficits(total_bank_target=20, topic_filter="2")

    assert deficits
    assert all(target.topic_id == 2 for target, _ in deficits)


def test_audit_weighted_deficits_filters_by_exact_concept():
    from certcoach.jobs import nightly_seed_questions as job

    syllabus = [{
        "id": 1,
        "topic": "Topic One",
        "subtopics": ["First", "Second"],
        "exam_weight": "10%",
        "bank_topic_keys": ["Bank One"],
    }]

    with patch.object(job.planner, "load_syllabus", return_value=syllabus), \
         patch.object(job, "_get_db_style_counts", return_value={"Type A": 0, "Type B": 0, "Type C": 0, "Type D": 0}):
        deficits = job.audit_weighted_deficits(topic_filter="1", concept_filter="Second")

    assert deficits
    assert all(target.concept == "Second" for target, _ in deficits)


def test_topic_matches_bank_topic_substring():
    from certcoach.core.question_targets import QuestionTarget
    from certcoach.jobs.nightly_seed_questions import _topic_matches

    target = QuestionTarget(
        topic_id=11,
        topic="MongoDB Drivers & PyMongo",
        bank_topic="PyMongo Basics",
        concept="MongoClient",
        difficulty="Medium",
        target_count=5,
        exam_weight=0.18,
        concept_weight=0.20,
    )

    assert _topic_matches(target, "pymongo")
    assert _topic_matches(target, "11")
    assert not _topic_matches(target, "aggregation")


def test_style_counts_include_only_practice_ready_questions():
    """Contract-active alone is not enough to count toward the population
    target -- a question also needs provenance.state == 'confirmed', since
    database.is_practice_ready() now gates both. A contract-active-but-suspect
    record (the state of most of the legacy bank after the provenance
    backfill) must not silently satisfy the deficit and block regeneration."""
    from certcoach.jobs import nightly_seed_questions as job

    confirmed = {
        "metadata": {
            "question_style_type": "Type A",
            "content_contract_version": 2,
            "content_contract_status": "generated",
        },
        "provenance": {"state": "confirmed"},
    }
    contract_active_but_suspect = {
        "metadata": {
            "question_style_type": "Type B",
            "content_contract_version": 2,
            "content_contract_status": "generated",
        },
        "provenance": {"state": "suspect"},
    }
    legacy_no_contract = {"metadata": {"question_style_type": "Type B"}}
    questions_col = MagicMock()
    questions_col.find.return_value = [confirmed, contract_active_but_suspect, legacy_no_contract]

    with patch.object(job.database, "questions_col", questions_col):
        counts = job._get_db_style_counts(1, "Concept", "Easy")

    assert counts == {"Type A": 1, "Type B": 0, "Type C": 0, "Type D": 0}
    questions_col.find.assert_called_once_with({
        "metadata.topic_id": 1,
        "metadata.concept": "Concept",
        "metadata.difficulty": "Easy",
    }, {"metadata": 1, "provenance": 1})


def test_audit_weighted_deficits_defaults_scale_with_real_exam_weight():
    """Without an explicit --target-easy/--target-medium, the deficit should follow
    each concept's real exam-blueprint weight (question_targets.topic_exam_weight_map),
    not a flat number identical for every concept regardless of how heavily it's
    tested -- this is the behavior audit_weighted_deficits ignored before, always
    recomputing a flat get_population_easy_target()/get_population_medium_target()
    default instead of consuming target.target_count from build_weighted_targets."""
    from certcoach.jobs import nightly_seed_questions as job

    syllabus = [
        {"id": 12, "topic": "Low Topic", "subtopics": ["A"], "bank_topic_keys": ["Low Bank"]},
        {"id": 11, "topic": "High Topic", "subtopics": ["B"], "bank_topic_keys": ["High Bank"]},
    ]

    with patch.object(job.planner, "load_syllabus", return_value=syllabus), \
         patch.object(job, "_get_db_style_counts", return_value={"Type A": 0, "Type B": 0, "Type C": 0, "Type D": 0}):
        deficits = job.audit_weighted_deficits(total_bank_target=200)

    low_total = sum(missing for target, missing in deficits if target.topic_id == 12)
    high_total = sum(missing for target, missing in deficits if target.topic_id == 11)
    assert high_total > low_total


def test_audit_weighted_deficits_explicit_override_stays_flat_across_concepts():
    """An explicit --target-easy/--target-medium always wins outright and applies
    identically regardless of weight -- unchanged from before this feature."""
    from certcoach.jobs import nightly_seed_questions as job

    syllabus = [
        {"id": 12, "topic": "Low Topic", "subtopics": ["A"], "bank_topic_keys": ["Low Bank"]},
        {"id": 11, "topic": "High Topic", "subtopics": ["B"], "bank_topic_keys": ["High Bank"]},
    ]

    with patch.object(job.planner, "load_syllabus", return_value=syllabus), \
         patch.object(job, "_get_db_style_counts", return_value={"Type A": 0, "Type B": 0, "Type C": 0, "Type D": 0}):
        deficits = job.audit_weighted_deficits(target_easy=4, target_medium=3)

    low_total = sum(missing for target, missing in deficits if target.topic_id == 12)
    high_total = sum(missing for target, missing in deficits if target.topic_id == 11)
    assert low_total == high_total == 7


def test_audit_does_not_overpopulate_to_force_style_distribution():
    from certcoach.jobs import nightly_seed_questions as job

    syllabus = [{
        "id": 1,
        "topic": "Topic One",
        "subtopics": ["A"],
        "exam_weight": "10%",
        "bank_topic_keys": ["Bank One"],
    }]

    def style_counts(_topic_id, _concept, difficulty):
        if difficulty == "Easy":
            return {"Type A": 0, "Type B": 5, "Type C": 0, "Type D": 0}
        return {"Type A": 0, "Type B": 5, "Type C": 0, "Type D": 0}

    with patch.object(job.planner, "load_syllabus", return_value=syllabus), \
         patch.object(job, "_get_db_style_counts", side_effect=style_counts):
        deficits = job.audit_weighted_deficits(target_easy=5, target_medium=5)

    assert deficits == []


def test_audit_generates_explicit_extras_after_readiness():
    from certcoach.jobs import nightly_seed_questions as job

    syllabus = [{
        "id": 1,
        "topic": "Topic One",
        "subtopics": ["A"],
        "exam_weight": "10%",
        "bank_topic_keys": ["Bank One"],
    }]

    def style_counts(_topic_id, _concept, difficulty):
        if difficulty == "Easy":
            return {"Type A": 1, "Type B": 4, "Type C": 0, "Type D": 0}
        return {"Type A": 1, "Type B": 3, "Type C": 0, "Type D": 0}

    with patch.object(job.planner, "load_syllabus", return_value=syllabus), \
         patch.object(job, "_get_db_style_counts", side_effect=style_counts):
        default_deficits = job.audit_weighted_deficits(target_easy=3, target_medium=2)
        extra_deficits = job.audit_weighted_deficits(target_easy=3, target_medium=2, extra_easy=2, extra_medium=1)

    assert default_deficits == []
    assert sum(missing for _, missing in extra_deficits) == 3


def test_validate_question_quality_rejects_shallow_six_part_explanation():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "Which insert method should you use when adding one document?",
        "options": [
            {"code_snippet": "insertOne()", "is_correct": True},
            {"code_snippet": "insertMany()", "is_correct": False},
            {"code_snippet": "replaceOne()", "is_correct": False},
            {"code_snippet": "updateOne()", "is_correct": False},
        ],
        "explanation": "\n".join([
            "### 1. Correct Answer",
            "insertOne()",
            "### 2. Why Correct",
            "Because it inserts one document.",
            "### 3. Why Other Options Are Wrong",
            "insertMany() is for multiple documents.",
            "### 4. Exam Trap",
            "Confusing single-document and multi-document inserts.",
            "### 5. Memory Hook",
            "One = One.",
            "### 6. Follow-Up Practice Recommendation",
            "Review the MongoDB insert documents guide.",
            "### 7. Syntax Example",
            "```javascript\ninsertOne({ name: 'Ada' });\n```",
            "- This uses the single-document insert syntax.",
            "- The method returns insertion metadata for one document.",
        ]),
    }

    is_valid, issues = validate_question_quality(question)

    assert not is_valid
    assert any("sections are too short" in issue for issue in issues)


def test_validate_question_quality_rejects_section_six_without_bullets():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "Which insert method should you use when adding one document?",
        "options": [
            {"code_snippet": "insertOne()", "is_correct": True},
            {"code_snippet": "insertMany()", "is_correct": False},
            {"code_snippet": "replaceOne()", "is_correct": False},
            {"code_snippet": "updateOne()", "is_correct": False},
        ],
        "explanation": "\n".join([
            "### 1. Correct Answer",
            "insertOne() is the correct choice because it inserts a single document.",
            "### 2. Why Correct",
            "It matches the single-document requirement and returns insertion metadata.",
            "### 3. Why Other Options Are Wrong",
            "insertMany() is for multiple documents.",
            "replaceOne() replaces an existing document.",
            "updateOne() modifies matching fields, it does not insert a new document.",
            "### 4. Exam Trap",
            "The trap is confusing insert semantics with update semantics.",
            "### 5. Memory Hook",
            "One document, one insert call, one clear outcome.",
            "### 6. Follow-Up Practice Recommendation",
            "Review the insert documents guide and practice with one-document and many-document inserts.",
            "### 7. Syntax Example",
            "```javascript\ninsertOne({ name: 'Ada' });\n```",
            "- This uses the single-document insert syntax.",
            "- The method returns insertion metadata for one document.",
        ]),
    }

    is_valid, issues = validate_question_quality(question)

    assert not is_valid
    assert any("need more bullets" in issue for issue in issues)


def test_validate_question_quality_allows_not_required_syntax_example_for_conceptual_topic():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "Which BSON type best fits a flexible nested structure?",
        "metadata": {"topic_id": 1, "concept": "BSON Data Types"},
        "options": [
            {"code_snippet": "embedded document", "is_correct": True},
            {"code_snippet": "string", "is_correct": False},
            {"code_snippet": "boolean", "is_correct": False},
            {"code_snippet": "date", "is_correct": False},
        ],
        "explanation": "\n".join([
            "### 1. Correct Answer",
            "Embedded document is the correct choice because it can hold a nested structure with related fields.",
            "### 2. Why Correct",
            "MongoDB lets you group related values inside a document so you can keep the nested data close to the parent record and read it back in one query.",
            "### 3. Why Other Options Are Wrong",
            "string only stores text, so it cannot represent nested fields. boolean stores true or false only, so it is far too limited. date stores time information, not structure, so it does not model nested data.",
            "### 4. Exam Trap",
            "The trap is confusing a data value type with a structural container type. Nested documents are used when the shape of the information matters more than a simple scalar value.",
            "### 5. Memory Hook",
            "Think of an embedded document as a folder inside a folder: the parent keeps the related details together instead of scattering them into separate records.",
            "### 6. Follow-Up Practice Recommendation",
            "- Review how embedded documents keep related data together in one parent document.",
            "- Compare nested documents against flat scalar fields in a simple sample collection.",
            "- Practice identifying when the shape of the data matters more than a single value.",
            "### 7. Syntax Example",
            "Not required for this concept.",
        ]),
    }

    is_valid, issues = validate_question_quality(question)

    assert is_valid
    assert not issues


def test_validate_question_quality_rejects_invented_bson_type_names():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "Which BSON type can store an array of documents within a single document?",
        "metadata": {"topic_id": 1, "concept": "BSON Data Types"},
        "options": [
            {"code_snippet": "array", "is_correct": True},
            {"code_snippet": "embeddedDocument", "is_correct": False},
            {"code_snippet": "subdocumentArray", "is_correct": False},
            {"code_snippet": "documentArray", "is_correct": False},
        ],
        "explanation": "\n".join([
            "### 1. Correct Answer",
            "array",
            "### 2. Why Correct",
            "Because arrays can hold nested documents in MongoDB.",
            "### 3. Why Other Options Are Wrong",
            "The invented names are not official BSON types.",
            "### 4. Exam Trap",
            "Invented BSON type names.",
            "### 5. Memory Hook",
            "Use the official BSON vocabulary only.",
            "### 6. Follow-Up Practice Recommendation",
            "- Review the BSON reference.",
            "- Practice the official data types.",
            "### 7. Syntax Example",
            "Not required for this concept.",
        ]),
    }

    is_valid, issues = validate_question_quality(question)

    assert not is_valid
    assert any("invented BSON type names" in issue for issue in issues)


def test_validate_question_quality_can_validate_shell_without_explanation():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "Which BSON type should store text?",
        "metadata": {"topic_id": 1, "concept": "BSON Data Types", "topic": "MongoDB Overview & The Document Model"},
        "options": [
            {"code_snippet": "string", "is_correct": True},
            {"code_snippet": "boolean", "is_correct": False},
            {"code_snippet": "array", "is_correct": False},
            {"code_snippet": "date", "is_correct": False},
        ],
        "explanation": "",
        "citation_source": "topic_01_docs_manual_reference_bson_types__cf63661090.md",
    }

    is_valid, issues = validate_question_quality(question, require_explanation=False)

    assert is_valid
    assert not issues


def test_validate_question_quality_rejects_topic2_id_objectid_stems_without_keywords():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "Which two documents can successfully be added in the same collection?",
        "metadata": {"topic_id": 2, "concept": "_id and ObjectId", "topic": "CRUD Operations - Create"},
        "options": [
            {"code_snippet": "A", "is_correct": False},
            {"code_snippet": "B", "is_correct": False},
            {"code_snippet": "C", "is_correct": False},
            {"code_snippet": "D", "is_correct": True},
        ],
        "explanation": "\n".join([
            "### 1. Correct Answer",
            "D",
            "### 2. Why Correct",
            "Because the chosen option matches the expected identifier rule.",
            "### 3. Why Other Options Are Wrong",
            "The other options do not satisfy the identifier rule.",
            "### 4. Exam Trap",
            "Generic wording hides the _id / ObjectId concept.",
            "### 5. Memory Hook",
            "Use _id or ObjectId when the question is about identity.",
            "### 6. Follow-Up Practice Recommendation",
            "- Review how MongoDB assigns _id values.",
            "- Practice reading prompts that explicitly mention ObjectId.",
            "### 7. Syntax Example",
            "Not required for this concept.",
        ]),
    }

    is_valid, issues = validate_question_quality(question)

    assert not is_valid
    assert any("_id and ObjectId must explicitly reference _id or ObjectId" in issue for issue in issues)


def test_validate_question_quality_rejects_updateone_replace_semantics():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "A developer needs to replace an entire document's content with a new document. Which PyMongo call should they use?",
        "metadata": {"topic_id": 4, "concept": "updateOne()", "topic": "CRUD Operations - Update"},
        "options": [
            {"code_snippet": "collection.update_one({'name': 'cafe'}, {'$set': {'status': 'open'}})", "is_correct": False},
            {"code_snippet": "collection.replace_one({'name': 'cafe'}, {'status': 'open'})", "is_correct": True},
            {"code_snippet": "collection.update_many({'name': 'cafe'}, {'$set': {'status': 'open'}})", "is_correct": False},
            {"code_snippet": "collection.find_one({'name': 'cafe'})", "is_correct": False},
        ],
        "explanation": "\n".join([
            "### 1. Correct Answer",
            "B",
            "### 2. Why Correct",
            "It replaces the entire document.",
            "### 3. Why Other Options Are Wrong",
            "The others do not replace the whole document.",
            "### 4. Exam Trap",
            "Replacement is not the same as an operator update.",
            "### 5. Memory Hook",
            "Replace swaps the whole document.",
            "### 6. Follow-Up Practice Recommendation",
            "- Compare replace_one() and update_one().",
            "- Review update operators.",
            "- Practice choosing the right write method.",
            "### 7. Syntax Example",
            "```python\ncollection.replace_one({'name': 'cafe'}, {'status': 'open'})\n```",
            "- This uses replace_one() for a full-document swap.",
            "- The original document fields are overwritten except for _id.",
        ]),
    }

    is_valid, issues = validate_question_quality(question)

    assert not is_valid
    assert any("updateOne() question drifts into replaceOne() semantics" in issue for issue in issues)
    assert any("marks replaceOne() syntax as correct" in issue for issue in issues)


def test_validate_question_quality_rejects_updatemany_replace_semantics():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "A developer needs to replace the entire contents of many documents at once. Which PyMongo method should they use?",
        "metadata": {"topic_id": 4, "concept": "updateMany()", "topic": "CRUD Operations - Update"},
        "options": [
            {"code_snippet": "collection.update_many({'status': 'pending'}, {'$set': {'status': 'active'}})", "is_correct": False},
            {"code_snippet": "collection.replace_one({'status': 'pending'}, {'status': 'active'})", "is_correct": True},
            {"code_snippet": "collection.update_one({'status': 'pending'}, {'$set': {'status': 'active'}})", "is_correct": False},
            {"code_snippet": "collection.find({'status': 'pending'})", "is_correct": False},
        ],
        "explanation": "\n".join([
            "### 1. Correct Answer",
            "B",
            "### 2. Why Correct",
            "It replaces the entire document.",
            "### 3. Why Other Options Are Wrong",
            "The others do not replace the whole document.",
            "### 4. Exam Trap",
            "Replacement is not the same as an update.",
            "### 5. Memory Hook",
            "Replace means whole document.",
            "### 6. Follow-Up Practice Recommendation",
            "- Compare replace_one() and update_many().",
            "- Review update operators.",
            "- Practice choosing the right write method.",
            "### 7. Syntax Example",
            "```python\ncollection.replace_one({'status': 'pending'}, {'status': 'active'})\n```",
            "- This uses replace_one() for a full-document swap.",
            "- The original document fields are overwritten except for _id.",
        ]),
    }

    is_valid, issues = validate_question_quality(question)

    assert not is_valid
    assert any("updateMany() question drifts into replacement semantics" in issue for issue in issues)
    assert any("marks replaceOne() syntax as correct" in issue for issue in issues)


def test_concept_variation_guidance_prefers_insertmany_alternatives():
    from certcoach.core.question_targets import QuestionTarget
    from certcoach.jobs.nightly_seed_questions import _concept_variation_guidance

    target = QuestionTarget(
        topic_id=2,
        topic="CRUD Operations - Create",
        bank_topic="CRUD Operations",
        concept="insertMany()",
        difficulty="Medium",
        target_count=2,
        exam_weight=0.1,
        concept_weight=0.3,
    )

    guidance = _concept_variation_guidance(
        target,
        [
            "What is the structure of the object returned by insertMany()?",
            "Which method returns insertedIds?",
        ],
    )

    assert "do NOT ask the return-type / insertedIds question again" in guidance
    assert "ordered vs unordered behavior" in guidance


def test_concept_variation_guidance_keeps_updateone_off_replaceone():
    from certcoach.core.question_targets import QuestionTarget
    from certcoach.jobs.nightly_seed_questions import _concept_variation_guidance

    target = QuestionTarget(
        topic_id=4,
        topic="CRUD Operations - Update",
        bank_topic="CRUD Operations",
        concept="updateOne()",
        difficulty="Medium",
        target_count=2,
        exam_weight=0.1,
        concept_weight=0.3,
    )

    guidance = _concept_variation_guidance(target, [])

    assert "Do NOT ask about replacing an entire document" in guidance
    assert "replace_one()/replaceOne() as the correct answer" in guidance


def test_concept_variation_guidance_keeps_updatemany_off_replaceone():
    from certcoach.core.question_targets import QuestionTarget
    from certcoach.jobs.nightly_seed_questions import _concept_variation_guidance

    target = QuestionTarget(
        topic_id=4,
        topic="CRUD Operations - Update",
        bank_topic="CRUD Operations",
        concept="updateMany()",
        difficulty="Medium",
        target_count=2,
        exam_weight=0.1,
        concept_weight=0.3,
    )

    guidance = _concept_variation_guidance(target, [])

    assert "updating multiple matching documents" in guidance
    assert "replace_one()/replaceOne() as the correct answer" in guidance


def test_concept_variation_guidance_covers_topic4_operator_families():
    from certcoach.core.question_targets import QuestionTarget
    from certcoach.jobs.nightly_seed_questions import _concept_variation_guidance

    cases = {
        "$set": "assigning or overwriting a field value",
        "$push": "appending values to arrays",
        "$inc": "incrementing or decrementing numeric fields",
        "$unset": "removing fields from documents",
        "upsert": "inserting a new document when no match is found",
        "findAndModify": "atomic find-and-update behavior",
    }

    for concept, expected in cases.items():
        target = QuestionTarget(
            topic_id=4,
            topic="CRUD Operations - Update",
            bank_topic="CRUD Operations",
            concept=concept,
            difficulty="Medium",
            target_count=2,
            exam_weight=0.1,
            concept_weight=0.3,
        )
        guidance = _concept_variation_guidance(target, [])
        assert expected in guidance


def _seven_part_explanation() -> str:
    return "\n".join([
        "### 1. Correct Answer",
        "The options that pass both the field-order and syntax checks are correct.",
        "### 2. Why Correct",
        "Both marked options satisfy the query's select-all-that-apply criteria for a valid compound index call.",
        "### 3. Why Other Options Are Wrong",
        "The unmarked options either pass the wrong argument shape to createIndex() or use invalid positional "
        "arguments instead of a single document/list of tuples, so MongoDB rejects them before an index is built.",
        "### 4. Exam Trap",
        "Selecting only one option on a select-all-that-apply question loses full credit under no-partial-credit scoring.",
        "### 5. Memory Hook",
        "Select-all means evaluate every option independently, not just find the first correct one.",
        "### 6. Follow-Up Practice Recommendation",
        "- Review multi-response scoring rules.",
        "- Practice select-all-that-apply questions.",
        "### 7. Syntax Example",
        "```javascript\ndb.collection.createIndex({ a: 1, b: 1 });\n```",
    ])


def test_validate_question_quality_accepts_multi_response_with_two_correct():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "Which of the following are valid ways to specify a compound index? (Select all that apply.)",
        "metadata": {"topic_id": 9, "concept": "Compound indexes", "response_type": "multi"},
        "options": [
            {"code_snippet": "db.collection.createIndex({a: 1, b: 1})", "is_correct": True},
            {"code_snippet": "db.collection.createIndex({a: 1, b: -1})", "is_correct": True},
            {"code_snippet": "db.collection.createIndex('a', 'b')", "is_correct": False},
            {"code_snippet": "db.collection.createIndex([a, b])", "is_correct": False},
        ],
        "explanation": _seven_part_explanation(),
    }

    is_valid, issues = validate_question_quality(question)

    # This test targets the multi-response correct-option-count rule specifically;
    # it deliberately does not assert overall validity, since other unrelated
    # content-quality checks (explanation depth, syntax examples, etc.) are
    # covered by their own dedicated tests elsewhere in this file.
    assert not any("correct option" in issue for issue in issues)


def test_validate_question_quality_rejects_multi_response_with_only_one_correct():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "Which of the following are valid ways to specify a compound index? (Select all that apply.)",
        "metadata": {"topic_id": 9, "concept": "Compound indexes", "response_type": "multi"},
        "options": [
            {"code_snippet": "db.collection.createIndex({a: 1, b: 1})", "is_correct": True},
            {"code_snippet": "db.collection.createIndex({a: 1, b: -1})", "is_correct": False},
            {"code_snippet": "db.collection.createIndex('a', 'b')", "is_correct": False},
            {"code_snippet": "db.collection.createIndex([a, b])", "is_correct": False},
        ],
        "explanation": _seven_part_explanation(),
    }

    is_valid, issues = validate_question_quality(question)

    assert not is_valid
    assert any("fewer than two options are marked correct" in issue for issue in issues)


def test_validate_question_quality_still_requires_exactly_one_for_single_response():
    from certcoach.jobs.nightly_seed_questions import validate_question_quality

    question = {
        "question_text": "Which method inserts exactly one document?",
        "metadata": {"topic_id": 2, "concept": "insertOne()"},
        "options": [
            {"code_snippet": "insertOne()", "is_correct": True},
            {"code_snippet": "insertMany()", "is_correct": True},
            {"code_snippet": "updateOne()", "is_correct": False},
            {"code_snippet": "replaceOne()", "is_correct": False},
        ],
        "explanation": _seven_part_explanation(),
    }

    is_valid, issues = validate_question_quality(question)

    assert not is_valid
    assert any("does not have exactly one correct option" in issue for issue in issues)


def test_resolve_correct_answers_handles_multi_response_letters():
    from certcoach.jobs.nightly_seed_questions import SeedMCQ, _resolve_correct_answers

    mcq = SeedMCQ(
        question="Which of the following are valid?",
        options=["Option A text", "Option B text", "Option C text", "Option D text"],
        response_type="multi",
        correct_answers=["A", "C"],
    )

    resolved = _resolve_correct_answers(mcq)

    assert resolved == ["Option A text", "Option C text"]


def test_resolve_correct_answers_falls_back_to_singular_field():
    from certcoach.jobs.nightly_seed_questions import SeedMCQ, _resolve_correct_answers

    mcq = SeedMCQ(
        question="Which method inserts one document?",
        options=["insertOne()", "insertMany()", "updateOne()", "replaceOne()"],
        correct_answer="insertOne()",
    )

    resolved = _resolve_correct_answers(mcq)

    assert resolved == ["insertOne()"]
