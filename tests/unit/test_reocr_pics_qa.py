from unittest.mock import patch


def test_collapse_repetition_truncates_a_repeating_block():
    from certcoach.jobs import reocr_pics_qa

    clean = "1. What is the relationship between the MongoDB database and MongoDB Atlas?\n(Select one.)\nThe MongoDB database is a core element."
    degenerate = clean + "\n```markdown\n\n" + clean + "\n```\n" + clean

    result = reocr_pics_qa.collapse_repetition(degenerate, probe_len=40)

    assert result.startswith("1. What is the relationship")
    assert result.count("core element") == 1


def test_collapse_repetition_leaves_non_repeating_text_untouched():
    from certcoach.jobs import reocr_pics_qa

    text = "A short, genuinely non-repeating transcript with no duplicated opening block."

    assert reocr_pics_qa.collapse_repetition(text, probe_len=40) == text


def test_collapse_repetition_handles_text_shorter_than_probe():
    from certcoach.jobs import reocr_pics_qa

    assert reocr_pics_qa.collapse_repetition("short", probe_len=120) == "short"


def test_transcript_filename_sanitizes_screenshot_name():
    from certcoach.jobs import reocr_pics_qa

    assert reocr_pics_qa.transcript_filename("Screenshot 2025-12-14 090435.png") == "Screenshot-2025-12-14-090435.md"


def test_get_available_vision_model_prefers_glm_ocr():
    from certcoach.jobs import reocr_pics_qa

    class FakeModel:
        def __init__(self, name):
            self.model = name

    class FakeModels:
        models = [FakeModel("llava:latest"), FakeModel("glm-ocr:latest")]

    with patch.object(reocr_pics_qa.ollama, "list", return_value=FakeModels()):
        assert reocr_pics_qa.get_available_vision_model() == "glm-ocr:latest"


def test_get_available_vision_model_falls_back_to_llava():
    from certcoach.jobs import reocr_pics_qa

    class FakeModel:
        def __init__(self, name):
            self.model = name

    class FakeModels:
        models = [FakeModel("llava:latest")]

    with patch.object(reocr_pics_qa.ollama, "list", return_value=FakeModels()):
        assert reocr_pics_qa.get_available_vision_model() == "llava:latest"


def test_get_available_vision_model_returns_none_when_unavailable():
    from certcoach.jobs import reocr_pics_qa

    class FakeModels:
        models = []

    with patch.object(reocr_pics_qa.ollama, "list", return_value=FakeModels()):
        assert reocr_pics_qa.get_available_vision_model() is None


def test_run_reocr_returns_zero_counts_when_no_vision_model():
    from certcoach.jobs import reocr_pics_qa

    with patch.object(reocr_pics_qa, "get_available_vision_model", return_value=None):
        result = reocr_pics_qa.run_reocr()

    assert result == {"processed": 0, "skipped": 0, "failed": 0}
