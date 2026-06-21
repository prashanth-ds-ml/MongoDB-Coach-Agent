import json
from unittest.mock import MagicMock, patch


class _FakeHttpResponse:
    def __init__(self, payload: dict):
        self._body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self._body


def test_generate_with_quality_gate_uses_openrouter_http_response(monkeypatch):
    from certcoach.core import model_runner as runner

    monkeypatch.setattr(runner, "get_judge_enabled", lambda: False)
    monkeypatch.setattr(runner.planner, "validate_lexical_syntax_guard", lambda *args, **kwargs: (True, ""))

    questions_col = MagicMock()
    questions_col.find_one.return_value = None
    questions_col.find.return_value = []

    payload = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "question": "Which BSON type can store nested structure?",
                            "options": [
                                "embedded document",
                                "string",
                                "boolean",
                                "date",
                            ],
                            "correct_answer": "embedded document",
                            "metadata": {
                                "topic": "Topic 1",
                                "concept": "BSON Data Types",
                                "difficulty": "Easy",
                            },
                        }
                    )
                }
            }
        ]
    }

    def fake_urlopen(*args, **kwargs):
        return _FakeHttpResponse(payload)

    with patch.object(runner.database, "questions_col", questions_col), \
         patch.object(runner.urllib.request, "urlopen", side_effect=fake_urlopen), \
         patch("certcoach.core.config.get_openrouter_key", return_value="test-key"):
        result = runner.get_model_runner().generate_with_quality_gate(
            prompt="test prompt",
            model_chain=[{"provider": "openrouter", "model": "test-model"}],
            max_retries=0,
            source_files=["topic_1.md"],
            context_text="Which BSON type can store nested structure?",
        )

    assert result["success"] is True
    assert result["result"]["question"] == "Which BSON type can store nested structure?"
    assert result["model_used"] == "openrouter:test-model"


def test_generate_with_quality_gate_allows_repair_contract(monkeypatch):
    from certcoach.core import model_runner as runner

    monkeypatch.setattr(runner, "get_judge_enabled", lambda: False)

    questions_col = MagicMock()
    questions_col.find_one.return_value = None
    questions_col.find.return_value = []

    payload = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "feedbacks": ["A", "B", "C", "D"],
                            "trap_analysis": "Trap",
                            "explanation_correct_answer": "Correct answer",
                            "explanation_why_correct": "Why correct",
                            "explanation_why_wrong": "Why wrong",
                            "explanation_exam_trap": "Trap detail",
                            "explanation_memory_hook": "Memory hook",
                            "explanation_practice_recommendations": ["rec 1", "rec 2", "rec 3"],
                            "explanation_syntax_example": "Not required for this concept.",
                        }
                    )
                }
            }
        ]
    }

    def fake_urlopen(*args, **kwargs):
        return _FakeHttpResponse(payload)

    with patch.object(runner.database, "questions_col", questions_col), \
         patch.object(runner.urllib.request, "urlopen", side_effect=fake_urlopen), \
         patch("certcoach.core.config.get_openrouter_key", return_value="test-key"):
        result = runner.get_model_runner().generate_with_quality_gate(
            prompt="repair prompt",
            model_chain=[{"provider": "openrouter", "model": "test-model"}],
            max_retries=0,
            response_kind="repair",
        )

    assert result["success"] is True
    assert result["result"]["feedbacks"] == ["A", "B", "C", "D"]


def test_generate_with_quality_gate_normalizes_legacy_question_fields(monkeypatch):
    from certcoach.core import model_runner as runner

    monkeypatch.setattr(runner, "get_judge_enabled", lambda: False)
    monkeypatch.setattr(runner.planner, "validate_lexical_syntax_guard", lambda *args, **kwargs: (True, ""))

    questions_col = MagicMock()
    questions_col.find_one.return_value = None
    questions_col.find.return_value = []

    payload = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "question_text": "Which BSON type can store nested structure?",
                            "options": [
                                "embedded document",
                                "string",
                                "boolean",
                                "date",
                            ],
                            "correct_option_letter": "A",
                        }
                    )
                }
            }
        ]
    }

    def fake_urlopen(*args, **kwargs):
        return _FakeHttpResponse(payload)

    with patch.object(runner.database, "questions_col", questions_col), \
         patch.object(runner.urllib.request, "urlopen", side_effect=fake_urlopen), \
         patch("certcoach.core.config.get_openrouter_key", return_value="test-key"):
        result = runner.get_model_runner().generate_with_quality_gate(
            prompt="test prompt",
            model_chain=[{"provider": "openrouter", "model": "test-model"}],
            max_retries=0,
            source_files=["topic_1.md"],
            context_text="Which BSON type can store nested structure?",
        )

    assert result["success"] is True
    assert result["result"]["question"] == "Which BSON type can store nested structure?"
    assert result["result"]["correct_answer"] == "embedded document"


def test_generate_with_quality_gate_allows_question_shell_without_explanations(monkeypatch):
    from certcoach.core import model_runner as runner

    monkeypatch.setattr(runner, "get_judge_enabled", lambda: False)
    monkeypatch.setattr(runner.planner, "validate_lexical_syntax_guard", lambda *args, **kwargs: (True, ""))

    questions_col = MagicMock()
    questions_col.find_one.return_value = None
    questions_col.find.return_value = []

    payload = {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "question": "Which BSON type can store text?",
                            "options": [
                                "string",
                                "boolean",
                                "array",
                                "date",
                            ],
                            "correct_answer": "string",
                            "metadata": {
                                "topic": "Topic 1",
                                "concept": "BSON Data Types",
                                "difficulty": "Easy",
                                "citation_source": "topic_01_docs_manual_reference_bson_types__cf63661090.md",
                            },
                        }
                    )
                }
            }
        ]
    }

    def fake_urlopen(*args, **kwargs):
        return _FakeHttpResponse(payload)

    with patch.object(runner.database, "questions_col", questions_col), \
         patch.object(runner.urllib.request, "urlopen", side_effect=fake_urlopen), \
         patch("certcoach.core.config.get_openrouter_key", return_value="test-key"):
        result = runner.get_model_runner().generate_with_quality_gate(
            prompt="shell prompt",
            model_chain=[{"provider": "openrouter", "model": "test-model"}],
            max_retries=0,
            source_files=["topic_1.md"],
            context_text="Which BSON type can store text?",
            response_kind="question_shell",
        )

    assert result["success"] is True
    assert result["result"]["question"] == "Which BSON type can store text?"
    assert result["result"]["citation_source"] == "topic_01_docs_manual_reference_bson_types__cf63661090.md"


def test_ollama_langchain_adapter_requests_json_mode(monkeypatch):
    from certcoach.core import model_runner as runner

    captured = {}

    class FakeChatOllama:
        def __init__(self, **kwargs):
            captured.update(kwargs)

        def invoke(self, prompt):
            return '{"question": "test"}'

    monkeypatch.setattr(runner, "ChatOllama", FakeChatOllama)

    result = runner.ModelRunner()._call_model(
        {"provider": "ollama", "model": "test-model"},
        "return json",
    )

    assert result == '{"question": "test"}'
    assert captured["format"] == "json"


def test_ollama_http_adapter_requests_json_mode(monkeypatch):
    from certcoach.core import model_runner as runner

    captured = {}

    def fake_post_json(url, payload, headers, timeout):
        captured.update(payload)
        return {"message": {"content": '{"question": "test"}'}}

    monkeypatch.setattr(runner, "ChatOllama", None)
    monkeypatch.setattr(runner, "_post_json", fake_post_json)

    result = runner.ModelRunner()._call_model(
        {"provider": "ollama", "model": "test-model"},
        "return json",
    )

    assert result == '{"question": "test"}'
    assert captured["format"] == "json"
