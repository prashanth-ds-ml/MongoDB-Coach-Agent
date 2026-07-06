def _options(correct_letters):
    letters = ["A", "B", "C", "D"]
    return [
        {"option_letter": letter, "code_snippet": f"Option {letter} text", "is_correct": letter in correct_letters}
        for letter in letters
    ]


def test_validate_options_requires_exactly_one_correct_for_single_response():
    from certcoach.core.judge_questions import _validate_options

    issues = _validate_options(_options({"A"}), response_type="single")

    assert issues == []


def test_validate_options_rejects_two_correct_for_single_response():
    from certcoach.core.judge_questions import _validate_options

    issues = _validate_options(_options({"A", "B"}), response_type="single")

    assert any("exactly one correct option" in issue for issue in issues)


def test_validate_options_accepts_two_correct_for_multi_response():
    from certcoach.core.judge_questions import _validate_options

    issues = _validate_options(_options({"A", "C"}), response_type="multi")

    assert issues == []


def test_validate_options_rejects_multi_response_with_only_one_correct():
    from certcoach.core.judge_questions import _validate_options

    issues = _validate_options(_options({"A"}), response_type="multi")

    assert any("fewer than two options are marked correct" in issue for issue in issues)


def test_validate_options_defaults_to_single_response():
    from certcoach.core.judge_questions import _validate_options

    issues = _validate_options(_options({"A", "B"}))

    assert any("exactly one correct option" in issue for issue in issues)


def test_judge_question_reads_response_type_from_metadata():
    from certcoach.core.judge_questions import judge_question

    question = {
        "metadata": {"response_type": "multi"},
        "question_text": "Which of the following are true? (Select all that apply.)",
        "options": _options({"A", "C"}),
        "explanation": "### 1. Correct Answer\nA and C.",
    }

    issues = judge_question(question, source_files=[], context_text="")

    assert not any("correct option" in issue for issue in issues)
