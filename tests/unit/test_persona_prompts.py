from unittest.mock import patch


def test_explain_topic_prompt_requires_analogy_and_detailed_syntax():
    from certcoach.core.persona import CoachPersona

    coach = CoachPersona()
    with patch.object(coach, "_call", return_value="ok") as mock_call:
        coach.explain_topic("CRUD Operations - Create", "insertOne()", "insert docs context")

    prompt = mock_call.call_args[0][0]
    assert "real-world analogy" in prompt
    assert "detailed syntax walkthrough" in prompt
    assert "explain what each operator, parameter, and method call does" in prompt
    assert "Do not give a short summary" in prompt
