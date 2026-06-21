from certcoach.core import config


def test_role_models_have_study_first_defaults(monkeypatch):
    for name in ("MODEL", "STUDY_MODEL", "POPULATION_MODEL", "REPAIR_MODEL"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(config, "load_environment", lambda: None)

    assert config.get_study_model() == "qwen3.5:4b"
    assert config.get_population_model() == "gemma4:12b"
    assert config.get_repair_model() == "gemma4:12b"


def test_study_model_keeps_legacy_model_as_compatibility_fallback(monkeypatch):
    monkeypatch.delenv("STUDY_MODEL", raising=False)
    monkeypatch.setenv("MODEL", "qwen2.5-coder:7b")
    monkeypatch.setattr(config, "load_environment", lambda: None)

    assert config.get_study_model() == "qwen2.5-coder:7b"
    assert config.get_population_model() == "gemma4:12b"


def test_repair_model_defaults_to_configured_population_model(monkeypatch):
    monkeypatch.delenv("REPAIR_MODEL", raising=False)
    monkeypatch.setenv("POPULATION_MODEL", "gemma4:12b-custom")
    monkeypatch.setattr(config, "load_environment", lambda: None)

    assert config.get_repair_model() == "gemma4:12b-custom"


def test_study_runtime_defaults_disable_reasoning(monkeypatch):
    monkeypatch.delenv("STUDY_REASONING", raising=False)
    monkeypatch.delenv("STUDY_NUM_CTX", raising=False)
    monkeypatch.setattr(config, "load_environment", lambda: None)

    assert config.get_study_reasoning() is False
    assert config.get_study_num_ctx() == 8192


def test_population_inventory_targets_default_above_readiness(monkeypatch):
    monkeypatch.delenv("POPULATION_EASY_TARGET", raising=False)
    monkeypatch.delenv("POPULATION_MEDIUM_TARGET", raising=False)
    monkeypatch.setattr(config, "load_environment", lambda: None)

    assert config.get_population_easy_target() == 5
    assert config.get_population_medium_target() == 5


def test_population_inventory_targets_cannot_drop_below_readiness(monkeypatch):
    monkeypatch.setenv("POPULATION_EASY_TARGET", "1")
    monkeypatch.setenv("POPULATION_MEDIUM_TARGET", "1")
    monkeypatch.setattr(config, "load_environment", lambda: None)

    assert config.get_population_easy_target() == 3
    assert config.get_population_medium_target() == 2


def test_model_chains_prioritize_ollama_before_cloud_fallbacks(monkeypatch):
    monkeypatch.setenv("POPULATION_MODEL_CHAIN", "openrouter:foo,cf:bar")
    monkeypatch.setenv("REPAIR_MODEL_CHAIN", "or:baz,cloudflare:qux")
    monkeypatch.setattr(config, "load_environment", lambda: None)

    population_chain = config.get_population_model_chain()
    repair_chain = config.get_repair_model_chain()

    assert population_chain[0] == {"provider": "ollama", "model": "gemma4:12b"}
    assert repair_chain[0] == {"provider": "ollama", "model": "gemma4:12b"}
    assert any(entry["provider"] != "ollama" for entry in population_chain[1:])
    assert any(entry["provider"] != "ollama" for entry in repair_chain[1:])
