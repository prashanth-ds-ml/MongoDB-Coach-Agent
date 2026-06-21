from unittest.mock import MagicMock, patch


def test_structural_repair_requires_four_options_and_one_correct():
    from certcoach.jobs.repair_explanations import is_structurally_repairable

    ok, reason = is_structurally_repairable({"question_text": "Q", "options": []})
    assert ok is False
    assert "exactly 4 options" in reason

    ok, reason = is_structurally_repairable({
        "question_text": "Q",
        "options": [{"is_correct": False}, {"is_correct": False}, {"is_correct": False}, {"is_correct": False}],
    })
    assert ok is False
    assert "exactly one correct" in reason


def test_repair_selection_requires_explicit_pending_status():
    from certcoach.jobs.repair_explanations import is_marked_for_explanation_repair

    assert is_marked_for_explanation_repair({
        "metadata": {"content_contract_status": "needs_explanation_repair"}
    })
    assert not is_marked_for_explanation_repair({
        "metadata": {"content_contract_status": "quarantined"}
    })
    assert not is_marked_for_explanation_repair({
        "metadata": {"content_contract_status": "migrated"}
    })


def test_numeric_topic_filter_matches_exact_topic_id_only():
    from certcoach.jobs.repair_explanations import _topic_matches

    assert _topic_matches({"metadata": {"topic_id": 1, "topic": "Topic 1"}}, "1")
    assert not _topic_matches({"metadata": {"topic_id": 10, "topic": "Topic 10"}}, "1")
    assert not _topic_matches({"metadata": {"topic_id": 11, "topic": "Topic 11"}}, "1")


def test_concept_filter_matches_exact_concept_only():
    from certcoach.jobs.repair_explanations import _concept_matches

    question = {"metadata": {"concept": "BSON Data Types"}}

    assert _concept_matches(question, "bson data types")
    assert not _concept_matches(question, "BSON")


def test_repair_order_key_uses_syllabus_topic_and_concept_order():
    from certcoach.jobs.repair_explanations import _syllabus_order_key

    syllabus = [
        {"id": 1, "subtopics": ["First", "Second"]},
        {"id": 2, "subtopics": ["Third"]},
    ]
    questions = [
        {"_id": "q3", "metadata": {"topic_id": 2, "concept": "Third"}},
        {"_id": "q2", "metadata": {"topic_id": 1, "concept": "Second"}},
        {"_id": "q1", "metadata": {"topic_id": 1, "concept": "First"}},
    ]

    ordered = sorted(questions, key=lambda question: _syllabus_order_key(question, syllabus))

    assert [question["_id"] for question in ordered] == ["q1", "q2", "q3"]


def test_apply_repair_updates_explanation_and_feedbacks():
    from certcoach.jobs import repair_explanations as repair

    q = {
        "_id": "q1",
        "options": [
            {"option_letter": "A", "feedback": ""},
            {"option_letter": "B", "feedback": ""},
            {"option_letter": "C", "feedback": ""},
            {"option_letter": "D", "feedback": ""},
        ],
    }
    repaired = repair.RepairedExplanation(
        explanation="### 1. Correct Answer\nA\n### 2. Why Correct\nBecause\n### 3. Why Other Options Are Wrong\nNo\n### 4. Exam Trap\nTrap\n### 5. Memory Hook\nHook\n### 6. Follow-Up Practice Recommendation\nPractice\n### 7. Syntax Example\nNot required for this concept.",
        feedbacks=["fa", "fb", "fc", "fd"],
        trap_analysis="trap",
    )

    questions_col = MagicMock()
    with patch.object(repair.database, "questions_col", questions_col):
        repair.apply_repair(q, repaired)

    update_doc = questions_col.update_one.call_args[0][1]["$set"]
    assert update_doc["explanation"].startswith("### 1. Correct Answer")
    assert update_doc["options"][2]["feedback"] == "fc"
    assert update_doc["metadata.explanation_repair_source"] == "certcoach_repair_explanations"
    assert update_doc["metadata.content_contract_status"] == "generated"
    assert update_doc["metadata.content_contract_version"] == 2


def test_repair_quality_helper_passes_candidate_to_validator():
    from certcoach.jobs import repair_explanations as repair

    q = {
        "metadata": {"topic_id": 2, "topic": "CRUD Operations - Create", "concept": "insertOne()", "difficulty": "Easy"},
        "options": [
            {"option_letter": "A", "is_correct": True},
            {"option_letter": "B", "is_correct": False},
            {"option_letter": "C", "is_correct": False},
            {"option_letter": "D", "is_correct": False},
        ],
    }
    repaired = repair.RepairedExplanation(
        explanation="### 1. Correct Answer\nA\n### 2. Why Correct\nBecause.\n### 3. Why Other Options Are Wrong\nNo.\n### 4. Exam Trap\nTrap.\n### 5. Memory Hook\nHook.\n### 6. Follow-Up Practice Recommendation\nPractice.\n### 7. Syntax Example\nNot required for this concept.",
        feedbacks=["fa", "fb", "fc", "fd"],
        trap_analysis="trap",
    )

    with patch.object(repair, "validate_question_quality", return_value=(True, [])) as validate:
        issues = repair._repair_quality_issues(q, repaired)

    assert issues == []
    candidate = validate.call_args[0][0]
    assert candidate["explanation"] == repaired.explanation
    assert candidate["options"][0]["feedback"] == "fa"


def test_generate_repair_includes_syntax_example_instruction_for_syntax_heavy_concepts():
    from certcoach.jobs import repair_explanations as repair

    q = {
        "_id": "q1",
        "metadata": {
            "topic_id": 2,
            "topic": "CRUD Operations - Create",
            "syllabus_topic": "CRUD Operations - Create",
            "concept": "insertMany()",
            "difficulty": "Medium",
            "citation_source": "topic_02_docs_manual_tutorial_insert_documents__056e20bc9d.md",
        },
        "question_text": "Which insertMany() behavior is correct?",
        "context": {"scenario_description": "bulk insert"},
        "options": [
            {"option_letter": "A", "code_snippet": "opt A", "is_correct": True, "feedback": ""},
            {"option_letter": "B", "code_snippet": "opt B", "is_correct": False, "feedback": ""},
            {"option_letter": "C", "code_snippet": "opt C", "is_correct": False, "feedback": ""},
            {"option_letter": "D", "code_snippet": "opt D", "is_correct": False, "feedback": ""},
        ],
        "explanation": "",
        "trap_analysis": "",
    }

    captured = {}

    class _FakeRunner:
        def generate_with_quality_gate(self, **kwargs):
            captured["prompt"] = kwargs["prompt"]
            return {
                "success": False,
                "result": None,
                "quality_issues": ["all failed"],
                "model_used": None,
            }

    with patch.object(repair, "get_model_runner", return_value=_FakeRunner()), \
         patch.object(repair, "get_repair_model_chain", return_value=[]):
        result = repair.generate_repair(q)

    assert result is None
    assert "This concept is syntax-heavy" in captured["prompt"]
    assert "explanation_syntax_example` MUST be a short fenced code block" in captured["prompt"]


def test_generate_repair_includes_find_syntax_example_instruction_for_pymongo_read_concepts():
    from certcoach.jobs import repair_explanations as repair

    q = {
        "_id": "q2",
        "metadata": {
            "topic_id": 3,
            "topic": "CRUD Operations - Read",
            "syllabus_topic": "CRUD Operations - Read",
            "concept": "find()",
            "difficulty": "Easy",
            "citation_source": "topic_03_docs_languages_python_pymongo_driver_current_crud_query_find__406fc1e937.md",
        },
        "question_text": "Which PyMongo method returns a single document as a Python dictionary?",
        "context": {"scenario_description": "single-document query"},
        "options": [
            {"option_letter": "A", "code_snippet": "opt A", "is_correct": True, "feedback": ""},
            {"option_letter": "B", "code_snippet": "opt B", "is_correct": False, "feedback": ""},
            {"option_letter": "C", "code_snippet": "opt C", "is_correct": False, "feedback": ""},
            {"option_letter": "D", "code_snippet": "opt D", "is_correct": False, "feedback": ""},
        ],
        "explanation": "",
        "trap_analysis": "",
    }

    captured = {}

    class _FakeRunner:
        def generate_with_quality_gate(self, **kwargs):
            captured["prompt"] = kwargs["prompt"]
            return {
                "success": False,
                "result": None,
                "quality_issues": ["all failed"],
                "model_used": None,
            }

    with patch.object(repair, "get_model_runner", return_value=_FakeRunner()), \
         patch.object(repair, "get_repair_model_chain", return_value=[]):
        result = repair.generate_repair(q)

    assert result is None
    assert "find()/find_one() concepts" in captured["prompt"]
    assert "cursor returned by find()" in captured["prompt"]
    assert "Find is for a crowd; find_one is for one" in captured["prompt"]
    assert "contrast cursor vs single-document behavior" in captured["prompt"]


def test_generate_repair_includes_findone_mandatory_contract_checklist():
    from certcoach.jobs import repair_explanations as repair

    q = {
        "_id": "q3",
        "metadata": {
            "topic_id": 3,
            "topic": "CRUD Operations - Read",
            "syllabus_topic": "CRUD Operations - Read",
            "concept": "findOne()",
            "difficulty": "Medium",
            "citation_source": "topic_03_docs_languages_python_pymongo_driver_current_crud_query_find__406fc1e937.md",
        },
        "question_text": "Which PyMongo method returns one document as a Python dictionary?",
        "context": {"scenario_description": "single-document query"},
        "options": [
            {"option_letter": "A", "code_snippet": "opt A", "is_correct": True, "feedback": ""},
            {"option_letter": "B", "code_snippet": "opt B", "is_correct": False, "feedback": ""},
            {"option_letter": "C", "code_snippet": "opt C", "is_correct": False, "feedback": ""},
            {"option_letter": "D", "code_snippet": "opt D", "is_correct": False, "feedback": ""},
        ],
        "explanation": "",
        "trap_analysis": "",
    }

    captured = {}

    class _FakeRunner:
        def generate_with_quality_gate(self, **kwargs):
            captured["prompt"] = kwargs["prompt"]
            return {
                "success": False,
                "result": None,
                "quality_issues": ["all failed"],
                "model_used": None,
            }

    with patch.object(repair, "get_model_runner", return_value=_FakeRunner()), \
         patch.object(repair, "get_repair_model_chain", return_value=[]):
        result = repair.generate_repair(q)

    assert result is None
    assert "For Topic 3 find()/find_one() repairs, treat the following as mandatory" in captured["prompt"]
    assert "The memory hook must explicitly contrast cursor vs single-document behavior" in captured["prompt"]
    assert "The practice recommendations must contain exactly 3 items" in captured["prompt"]


def test_normalize_practice_recommendations_trims_or_pads_to_three_items():
    from certcoach.jobs.repair_explanations import _normalize_practice_recommendations

    question = {"metadata": {"concept": "findOne()", "topic": "CRUD Operations - Read"}}

    assert len(_normalize_practice_recommendations(question, ["one", "two", "three", "four"])) == 3
    padded = _normalize_practice_recommendations(question, ["only one"])
    assert len(padded) == 3
    assert all(item.strip() for item in padded)


def test_synthesize_syntax_example_uses_concept_specific_fallback():
    from certcoach.jobs.repair_explanations import _normalize_syntax_example

    question = {
        "metadata": {
            "concept": "replaceOne()",
            "topic": "CRUD Operations - Update",
        }
    }

    example = _normalize_syntax_example(question, "", True)

    assert "replace_one" in example
    assert "plain replacement document" in example
    assert example.count("```") >= 2
