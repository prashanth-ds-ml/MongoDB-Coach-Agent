from __future__ import annotations

import os

from dotenv import load_dotenv


GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
GLOBAL_ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")

DEFAULT_STUDY_MODEL = "qwen3.5:4b"
DEFAULT_POPULATION_MODEL = "gemma4:12b"
DEFAULT_REPAIR_MODEL = "gemma4:12b"
DEFAULT_LOCAL_LLM_URL = "http://localhost:11434"


def load_environment() -> None:
    """Load workspace settings first, then fill gaps from global settings."""
    load_dotenv()
    load_dotenv(GLOBAL_ENV_PATH)


def _bool_setting(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int_setting(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def get_local_llm_url() -> str:
    load_environment()
    return os.getenv("LOCAL_LLM_URL", DEFAULT_LOCAL_LLM_URL)


def get_study_model() -> str:
    load_environment()
    # MODEL remains a compatibility fallback for existing installations.
    return os.getenv("STUDY_MODEL") or os.getenv("MODEL") or DEFAULT_STUDY_MODEL


def get_population_model() -> str:
    load_environment()
    return os.getenv("POPULATION_MODEL", DEFAULT_POPULATION_MODEL)


def get_repair_model() -> str:
    load_environment()
    return os.getenv("REPAIR_MODEL") or get_population_model()


def get_study_num_ctx() -> int:
    load_environment()
    return _int_setting("STUDY_NUM_CTX", 8192)


def get_study_reasoning() -> bool:
    load_environment()
    return _bool_setting("STUDY_REASONING", False)


def get_population_num_ctx() -> int:
    load_environment()
    return _int_setting("POPULATION_NUM_CTX", 5120)


def get_population_source_chars() -> int:
    load_environment()
    return _int_setting("POPULATION_SOURCE_CHARS", 2200)


def get_population_easy_target() -> int:
    load_environment()
    return max(3, _int_setting("POPULATION_EASY_TARGET", 5))


def get_population_medium_target() -> int:
    load_environment()
    return max(2, _int_setting("POPULATION_MEDIUM_TARGET", 5))


def get_repair_num_ctx() -> int:
    load_environment()
    return _int_setting("REPAIR_NUM_CTX", 8192)


def get_ollama_timeout() -> float:
    load_environment()
    try:
        return float(os.getenv("OLLAMA_TIMEOUT", "600.0"))
    except ValueError:
        return 600.0
