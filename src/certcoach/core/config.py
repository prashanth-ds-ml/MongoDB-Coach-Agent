from __future__ import annotations

import os

from dotenv import load_dotenv


GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
GLOBAL_ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")

DEFAULT_STUDY_MODEL = "qwen3.5:4b"
DEFAULT_POPULATION_MODEL = "gemma4:12b"
DEFAULT_SELF_CONSISTENCY_MODEL = "qwen2.5-coder:7b"
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


def get_self_consistency_model() -> str:
    """Checks a generated question's internal coherence only (does the marked
    answer agree with its own explanation, are the options distinct) -- not a
    MongoDB fact-checker. Defaults to a fast, non-reasoning local model:
    benchmarked against deepseek-r1:8b (a reasoning model), which produced
    14000+ characters of "thinking" and still timed out before ever reaching
    a verdict. A quick internal-consistency check does not need deep
    reasoning, and a model that reliably answers is more useful than one that
    reasons carefully but never finishes."""
    load_environment()
    return os.getenv("SELF_CONSISTENCY_MODEL", DEFAULT_SELF_CONSISTENCY_MODEL)


def get_study_num_ctx() -> int:
    load_environment()
    return _int_setting("STUDY_NUM_CTX", 8192)


def get_study_reasoning() -> bool:
    load_environment()
    return _bool_setting("STUDY_REASONING", False)


def get_population_num_ctx() -> int:
    load_environment()
    return _int_setting("POPULATION_NUM_CTX", 4096)


def get_population_source_chars() -> int:
    """Caps how much of a resolved doc's text reaches the population prompt
    (both real generation in nightly_seed_questions.py and the inspect_doc.py
    dry-run). 8000 chars leaves headroom within the primary model's 4096-token
    context budget (get_population_num_ctx) even with a full avoid_block (up
    to 12 existing questions) and variation guidance included -- the prior
    1600-char default meant even a median-sized doc (~5,700 chars) was only
    ~28% visible to generation, and long docs (some exceed 100K chars) were
    under 2% visible."""
    load_environment()
    return _int_setting("POPULATION_SOURCE_CHARS", 8000)


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
        return float(os.getenv("OLLAMA_TIMEOUT", "180.0"))
    except ValueError:
        return 180.0


def get_population_model_chain() -> list[dict]:
    load_environment()
    chain_str = os.getenv("POPULATION_MODEL_CHAIN", "gemma4:12b")
    return _prioritize_local_models_first(
        [_parse_model_entry(e) for e in chain_str.split(",")],
        default_local_model=get_population_model(),
    )


def get_repair_model_chain() -> list[dict]:
    load_environment()
    chain_str = os.getenv("REPAIR_MODEL_CHAIN", "gemma4:12b")
    return _prioritize_local_models_first(
        [_parse_model_entry(e) for e in chain_str.split(",")],
        default_local_model=get_repair_model(),
    )


def _parse_model_entry(entry: str) -> dict:
    entry = entry.strip()
    if entry.startswith(("cf:", "cloudflare:")):
        return {"provider": "cloudflare", "model": entry.split(":", 1)[1]}
    if entry.startswith(("or:", "openrouter:")):
        return {"provider": "openrouter", "model": entry.split(":", 1)[1]}
    return {"provider": "ollama", "model": entry}


def _prioritize_local_models_first(chain: list[dict], default_local_model: str) -> list[dict]:
    local = [entry for entry in chain if entry.get("provider") == "ollama"]
    remote = [entry for entry in chain if entry.get("provider") != "ollama"]
    if not local and default_local_model:
        local = [{"provider": "ollama", "model": default_local_model}]
    return local + remote


def get_max_retries_per_model() -> int:
    load_environment()
    try:
        return max(1, int(os.getenv("MAX_RETRIES_PER_MODEL", "2")))
    except ValueError:
        return 2


def get_judge_enabled() -> bool:
    load_environment()
    return os.getenv("JUDGE_ENABLED", "true").strip().lower() in {"1", "true", "yes", "on"}


def get_judge_provider() -> str:
    load_environment()
    return os.getenv("JUDGE_PROVIDER", "openrouter")


def get_judge_model() -> str:
    load_environment()
    provider = get_judge_provider()
    defaults = {
        "openrouter": "nvidia/nemotron-3-ultra",
        "cloudflare": "@cf/meta/llama-3.3-70b-instruct",
        "ollama": get_repair_model(),
    }
    return os.getenv("JUDGE_MODEL", defaults.get(provider, "nvidia/nemotron-3-ultra"))


def get_openrouter_key() -> str:
    load_environment()
    return os.getenv("openrouter_api") or os.getenv("OPENROUTER_API_KEY", "")


def get_cloudflare_credentials() -> tuple[str, str]:
    load_environment()
    return os.getenv("cloudflare_account_id", ""), os.getenv("cloudflare_api_token", "")
