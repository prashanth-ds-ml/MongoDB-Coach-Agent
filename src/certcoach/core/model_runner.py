import os
import json
import time
import hashlib
import logging
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

try:
    from langchain_ollama import ChatOllama
except ImportError:  # pragma: no cover - optional dependency
    ChatOllama = None
from certcoach.core.config import (
    get_local_llm_url,
    get_ollama_timeout,
    get_population_num_ctx,
    get_population_model_chain,
    get_repair_model_chain,
    get_max_retries_per_model,
    get_repair_num_ctx,
    get_judge_enabled,
    get_judge_provider,
    get_judge_model,
)
from certcoach.core import database
from certcoach.core import planner


def _post_json(url: str, payload: Dict[str, Any], headers: Dict[str, str], timeout: float) -> Dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8")
    return json.loads(body) if body else {}


def _extract_text(result: Any) -> str:
    if result is None:
        return ""
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        if "content" in result and isinstance(result["content"], str):
            return result["content"]
        message = result.get("message")
        if isinstance(message, dict) and isinstance(message.get("content"), str):
            return message["content"]
        choices = result.get("choices")
        if isinstance(choices, list) and choices:
            first_choice = choices[0] or {}
            message = first_choice.get("message", {})
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
        return json.dumps(result)
    content = getattr(result, "content", None)
    if isinstance(content, str):
        return content
    return str(result)


def _parse_json_response(text: str) -> Any:
    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        return json.loads(candidate)
    raise ValueError("Could not parse JSON response")


class ModelCircuitBreaker:
    def __init__(self, model_name: str, max_failures: int = 3, cooldown_minutes: int = 5):
        self.model_name = model_name
        self.max_failures = max_failures
        self.cooldown_minutes = cooldown_minutes
        self.failure_count = 0
        self.last_failure_time = None
        self.cooldown_until = None

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.cooldown_until = time.time() + (self.cooldown_minutes * 60)

    def record_success(self):
        self.failure_count = 0
        self.last_failure_time = None
        self.cooldown_until = None

    def is_open(self) -> bool:
        if self.failure_count >= self.max_failures and self.cooldown_until:
            if time.time() < self.cooldown_until:
                return True
            else:
                self.failure_count = 0
                self.cooldown_until = None
                return False
        return False

    def __repr__(self) -> str:
        status = "OPEN" if self.is_open() else "CLOSED"
        return f"ModelCircuitBreaker(model={self.model_name}, failures={self.failure_count}, status={status})"


class ModelRunner:
    def __init__(self):
        self.circuit_breakers: Dict[str, ModelCircuitBreaker] = {}
        self._setup_logging()

    def _setup_logging(self):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{log_dir}/model_quality.jsonl"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _get_circuit_breaker(self, model_name: str) -> ModelCircuitBreaker:
        if model_name not in self.circuit_breakers:
            self.circuit_breakers[model_name] = ModelCircuitBreaker(model_name)
        return self.circuit_breakers[model_name]

    def _call_model(self, model_config: Dict[str, str], prompt: str, temperature: float = 0.25, 
                   num_ctx: int = 5120, timeout: float = 600.0, format_json: bool = False) -> Any:
        model_name = model_config.get("model")
        provider = model_config.get("provider")
        
        circuit_breaker = self._get_circuit_breaker(f"{provider}:{model_name}")
        
        if circuit_breaker.is_open():
            self.logger.warning(f"Circuit breaker OPEN for {provider}:{model_name}, skipping")
            return None

        try:
            if provider == "ollama":
                if ChatOllama is not None:
                    llm = ChatOllama(
                        model=model_name,
                        base_url=get_local_llm_url(),
                        temperature=temperature,
                        timeout=timeout,
                        num_ctx=num_ctx,
                        reasoning=False,
                        format="json",
                    )
                    result = llm.invoke(prompt)
                    result = _extract_text(result)
                else:
                    payload = {
                        "model": model_name,
                        "messages": [{"role": "user", "content": prompt}],
                        "options": {
                            "temperature": temperature,
                            "num_ctx": num_ctx,
                        },
                        "format": "json",
                        "stream": False,
                    }
                    response = _post_json(
                        f"{get_local_llm_url().rstrip('/')}/api/chat",
                        payload,
                        {"Content-Type": "application/json"},
                        timeout,
                    )
                    result = _extract_text(response)
                circuit_breaker.record_success()
                return result
                
            elif provider == "cloudflare":
                from certcoach.core.config import get_cloudflare_credentials
                
                account_id, api_token = get_cloudflare_credentials()
                if not account_id or not api_token:
                    self.logger.error("Cloudflare credentials not configured")
                    return None

                response = _post_json(
                    f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model_name}",
                    {
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature,
                    },
                    {
                        "Authorization": f"Bearer {api_token}",
                        "Content-Type": "application/json",
                    },
                    timeout,
                )
                result = _extract_text(response.get("result", response))
                circuit_breaker.record_success()
                return result
                
            elif provider == "openrouter":
                from certcoach.core.config import get_openrouter_key
                
                api_key = get_openrouter_key()
                if not api_key:
                    self.logger.error("OpenRouter API key not configured")
                    return None

                payload = {
                    "model": model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "stream": False,
                    "max_tokens": 4096,
                }
                if format_json:
                    payload["response_format"] = {"type": "json_object"}

                response = _post_json(
                    "https://openrouter.ai/api/v1/chat/completions",
                    payload,
                    {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    timeout,
                )
                result = _extract_text(response)
                circuit_breaker.record_success()
                return result
                
            elif provider == "nvidia":
                api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("nvidia", "")
                if not api_key:
                    self.logger.error("NVIDIA API key not configured")
                    return None

                payload = {
                    "model": model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "stream": False,
                    "max_tokens": 4096,
                }
                if format_json:
                    payload["response_format"] = {"type": "json_object"}

                response = _post_json(
                    "https://integrate.api.nvidia.com/v1/chat/completions",
                    payload,
                    {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    timeout,
                )
                result = _extract_text(response)
                circuit_breaker.record_success()
                return result
                
            else:
                self.logger.error(f"Unknown provider: {provider}")
                return None
                
        except Exception as exc:
            self.logger.error(f"Model call failed for {provider}:{model_name}: {exc}")
            circuit_breaker.record_failure()
            return None

    def _log_attempt(self, model_config: Dict[str, str], prompt: str, result: Any, 
                    success: bool, quality_issues: List[str] = None, 
                    retry_count: int = 0) -> None:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
            "model": model_config.get("model"),
            "provider": model_config.get("provider"),
            "prompt_length": len(prompt),
            "success": success,
            "quality_issues": quality_issues or [],
            "retry_count": retry_count,
            "result_preview": str(result)[:200] if result else None,
        }
        
        self.logger.info(json.dumps(log_entry))

    def _normalize_question_options(self, options: Any) -> list[dict]:
        if not isinstance(options, list):
            return []
        normalized = []
        for opt in options:
            if isinstance(opt, dict):
                normalized.append(opt)
            else:
                normalized.append({"code_snippet": str(opt), "is_correct": False})
        return normalized

    def _normalize_question_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        normalized = dict(payload or {})
        metadata = normalized.get("metadata", {}) or {}
        if not str(normalized.get("question", "")).strip() and str(normalized.get("question_text", "")).strip():
            normalized["question"] = normalized.get("question_text")
        if not str(normalized.get("citation_source", "")).strip() and str(metadata.get("citation_source", "")).strip():
            normalized["citation_source"] = metadata.get("citation_source")
        options = self._normalize_question_options(normalized.get("options", []))
        if not str(normalized.get("correct_answer", "")).strip():
            letter_alias = None
            for alias in ("correct_option_letter", "correctChoiceLetter", "answer_letter"):
                value = str(normalized.get(alias, "")).strip()
                if value:
                    letter_alias = value.upper()
                    break
            if letter_alias in {"A", "B", "C", "D"} and len(options) >= 4:
                idx = ["A", "B", "C", "D"].index(letter_alias)
                normalized["correct_answer"] = str(options[idx].get("code_snippet", "")).strip()
            else:
                for alias in ("correct_option", "answer", "correctChoice", "correctIndex"):
                    if str(normalized.get(alias, "")).strip():
                        normalized["correct_answer"] = normalized.get(alias)
                        break
                if not str(normalized.get("correct_answer", "")).strip():
                    for alias in ("correct_option_index", "answer_index"):
                        if str(normalized.get(alias, "")).strip():
                            idx = normalized.get(alias)
                            try:
                                idx_int = int(idx)
                                if 0 <= idx_int < len(options):
                                    normalized["correct_answer"] = str(options[idx_int].get("code_snippet", "")).strip()
                                else:
                                    normalized["correct_answer"] = str(idx_int)
                            except Exception:
                                normalized["correct_answer"] = str(idx)
                            break
        return normalized

    def _deterministic_checks(self, question_payload: Dict[str, Any], metadata: Dict) -> tuple[bool, List[str]]:
        issues = []
        question_payload = self._normalize_question_payload(question_payload)
        question_text = str(question_payload.get("question", "") or "").strip()
        options = self._normalize_question_options(question_payload.get("options", []))
        correct_answer = str(question_payload.get("correct_answer", "") or "").strip()
        
        if not question_text or not question_text.strip():
            issues.append("missing question text")
            
        if len(options) != 4:
            issues.append("does not have exactly four options")

        option_texts = [str(opt.get("code_snippet", "")).strip() for opt in options]
        if any(not text for text in option_texts):
            issues.append("contains blank option text")

        if any("placeholder" in text.lower() for text in option_texts):
            issues.append("contains placeholder option text")

        if len({text.lower() for text in option_texts}) != len(option_texts):
            issues.append("duplicate option text")

        if not correct_answer:
            issues.append("missing correct answer")
        elif correct_answer not in option_texts:
            issues.append("correct answer does not match any option")
        
        topic_name = metadata.get("topic") or metadata.get("syllabus_topic") or ""
        syntax_ok, syntax_msg = planner.validate_lexical_syntax_guard(
            topic_name,
            question_text,
            options
        )
        if not syntax_ok:
            issues.append(f"Casing validation failed: {syntax_msg}")
            
        return len(issues) == 0, issues

    def _repair_response_checks(self, payload: Dict[str, Any]) -> tuple[bool, List[str]]:
        issues: List[str] = []
        required_text_fields = [
            "trap_analysis",
            "explanation_correct_answer",
            "explanation_why_correct",
            "explanation_why_wrong",
            "explanation_exam_trap",
            "explanation_memory_hook",
            "explanation_syntax_example",
        ]
        for field in required_text_fields:
            if not str(payload.get(field, "")).strip():
                issues.append(f"missing {field}")

        feedbacks = payload.get("feedbacks", [])
        if not isinstance(feedbacks, list):
            issues.append("feedbacks is not a list")
        elif len(feedbacks) != 4:
            issues.append("feedbacks does not contain exactly four items")
        elif any(not str(item).strip() for item in feedbacks):
            issues.append("feedbacks contains blank entries")

        recs = payload.get("explanation_practice_recommendations", [])
        if not isinstance(recs, list):
            issues.append("explanation_practice_recommendations is not a list")
        elif len(recs) != 3:
            issues.append("explanation_practice_recommendations must contain exactly three items")
        elif any(not str(item).strip() for item in recs):
            issues.append("explanation_practice_recommendations contains blank entries")

        if "###" in str(payload.get("explanation_syntax_example", "")):
            issues.append("explanation_syntax_example must be plain text or fenced code only")

        return len(issues) == 0, issues

    def _shell_response_checks(self, payload: Dict[str, Any]) -> tuple[bool, List[str]]:
        issues: List[str] = []
        is_valid, det_issues = self._deterministic_checks(payload, payload.get("metadata", {}))
        issues.extend(det_issues)
        return len(issues) == 0, issues

    def _check_duplicate(self, question_text: str, topic: str, concept: str, 
                        difficulty: str) -> tuple[bool, str]:
        fingerprint = self._generate_fingerprint(topic, concept, question_text)
        
        if database.questions_col.find_one({"_id": question_text}):
            return True, "stable id already exists"
            
        if fingerprint and database.questions_col.find_one({"metadata.question_fingerprint": fingerprint}):
            return True, "question fingerprint already exists"
            
        if database.questions_col.find_one({"question_text": question_text}):
            return True, "exact question text already exists"
            
        nearby = database.questions_col.find({
            "metadata.topic": topic,
            "metadata.concept": concept,
            "metadata.difficulty": difficulty,
        })
        
        for existing in nearby:
            if self._token_similarity(existing.get("question_text", ""), question_text) >= 0.92:
                return True, f"near-duplicate of {existing.get('_id')}"
                
        return False, ""

    def _generate_fingerprint(self, topic: str, concept: str, question_text: str) -> str:
        import re
        normalized = self._normalize_question_for_duplicate_check(question_text)
        basis = f"{self._slug(topic, 48)}|{self._slug(concept, 48)}|{normalized}"
        return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]

    def _normalize_question_for_duplicate_check(self, text: str) -> str:
        import re
        text = (text or "").lower()
        text = re.sub(r"\(select (one|all that apply)\)", " ", text)
        text = re.sub(r"[^a-z0-9_$]+", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def _slug(self, text: str, max_len: int = 36) -> str:
        import re
        slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
        return (slug or "general")[:max_len].strip("-")

    def _token_similarity(self, left: str, right: str) -> float:
        left_tokens = set(self._normalize_question_for_duplicate_check(left).split())
        right_tokens = set(self._normalize_question_for_duplicate_check(right).split())
        if not left_tokens or not right_tokens:
            return 0.0
        return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)

    def generate_with_quality_gate(self, prompt: str, model_chain: List[Dict], 
                                  max_retries: int = 2, 
                                  source_files: List[str] = None,
                                  context_text: str = "",
                                  response_kind: str = "question") -> Dict[str, Any]:
        if source_files is None:
            source_files = []
            
        for attempt in range(max_retries + 1):
            self.logger.info(f"Quality gate attempt {attempt + 1}/{max_retries + 1}")
            num_ctx = get_repair_num_ctx() if response_kind == "repair" else get_population_num_ctx()
            
            for model_config in model_chain:
                self.logger.info(f"Trying model: {model_config.get('provider')}:{model_config.get('model')}")
                
                result = self._call_model(
                    model_config,
                    prompt,
                    temperature=0.25,
                    num_ctx=num_ctx,
                    timeout=get_ollama_timeout(),
                    format_json=True
                )
                
                if not result:
                    continue
                    
                try:
                    parsed_result = _parse_json_response(_extract_text(result))
                except Exception:
                    self.logger.warning(f"Failed to parse JSON from {model_config.get('provider')}:{model_config.get('model')}")
                    continue
                parsed_result = self._normalize_question_payload(parsed_result)
                
                quality_issues = []
                if response_kind == "repair":
                    is_valid, det_issues = self._repair_response_checks(parsed_result)
                    quality_issues.extend(det_issues)
                elif response_kind == "question_shell":
                    is_valid, det_issues = self._shell_response_checks(parsed_result)
                    quality_issues.extend(det_issues)
                else:
                    is_valid, det_issues = self._deterministic_checks(parsed_result, parsed_result.get("metadata", {}))
                    quality_issues.extend(det_issues)
                    
                    is_dup, dup_reason = self._check_duplicate(
                        parsed_result.get("question", ""),
                        parsed_result.get("metadata", {}).get("topic", ""),
                        parsed_result.get("metadata", {}).get("concept", ""),
                        parsed_result.get("metadata", {}).get("difficulty", "")
                    )
                    if is_dup:
                        quality_issues.append(f"duplicate: {dup_reason}")
                    
                    if get_judge_enabled():
                        from certcoach.core.judge_questions import judge_question
                        judge_issues = judge_question(
                            parsed_result,
                            source_files,
                            context_text
                        )
                        quality_issues.extend(judge_issues)
                
                if not quality_issues:
                    self._log_attempt(
                        model_config,
                        prompt,
                        result,
                        success=True,
                        quality_issues=[],
                        retry_count=attempt
                    )
                    return {
                        "result": parsed_result,
                        "model_used": f"{model_config.get('provider')}:{model_config.get('model')}",
                        "quality_issues": [],
                        "success": True
                    }
                else:
                    self._log_attempt(
                        model_config,
                        prompt,
                        result,
                        success=False,
                        quality_issues=quality_issues,
                        retry_count=attempt
                    )
                    self.logger.warning(f"Quality issues for {model_config.get('provider')}:{model_config.get('model')}: {'; '.join(quality_issues)}")
                    
        self.logger.error(f"All quality gate attempts failed after {max_retries + 1} attempts")
        return {
            "result": None,
            "model_used": None,
            "quality_issues": ["All attempts failed quality gates"],
            "success": False
        }

    def get_circuit_breaker_status(self) -> Dict[str, Dict]:
        status = {}
        for model_name, breaker in self.circuit_breakers.items():
            status[model_name] = {
                "failure_count": breaker.failure_count,
                "last_failure_time": breaker.last_failure_time,
                "cooldown_until": breaker.cooldown_until,
                "is_open": breaker.is_open()
            }
        return status


_model_runner_instance = None

def get_model_runner() -> ModelRunner:
    global _model_runner_instance
    if _model_runner_instance is None:
        _model_runner_instance = ModelRunner()
    return _model_runner_instance
