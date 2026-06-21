import os
import json
import re
from typing import Dict, List, Any

from langchain_ollama import ChatOllama
from certcoach.core.config import (
    get_judge_enabled,
    get_judge_provider,
    get_judge_model,
    get_ollama_timeout,
    get_local_llm_url,
)
from certcoach.core import database
from certcoach.core import planner
from certcoach.core.model_runner import get_model_runner


def _load_env() -> tuple[str, str]:
    return get_judge_model(), get_local_llm_url()


def _parse_six_part_explanation(explanation: str) -> Dict[str, str]:
    SEVEN_PART_HEADINGS = [
        "### 1. Correct Answer",
        "### 2. Why Correct",
        "### 3. Why Other Options Are Wrong",
        "### 4. Exam Trap",
        "### 5. Memory Hook",
        "### 6. Follow-Up Practice Recommendation",
        "### 7. Syntax Example",
    ]
    
    sections: Dict[str, str] = {}
    current_heading: str | None = None
    for raw_line in explanation.splitlines():
        stripped = raw_line.strip()
        if stripped in SEVEN_PART_HEADINGS:
            current_heading = stripped
            sections[current_heading] = ""
            continue
        if current_heading:
            sections[current_heading] = f"{sections[current_heading]}{raw_line.rstrip()}\n"
    return {heading: sections.get(heading, "").strip() for heading in SEVEN_PART_HEADINGS}


def _count_bullet_lines(section: str) -> int:
    return sum(1 for line in section.splitlines() if line.strip().startswith(("-", "*")) or re.match(r"^\d+\.", line.strip()))


def _count_code_fences(section: str) -> int:
    return section.count("```")


def _normalize_options(options: Any) -> list[dict]:
    if not isinstance(options, list):
        return []
    normalized = []
    for opt in options:
        if isinstance(opt, dict):
            normalized.append(opt)
        else:
            normalized.append({"code_snippet": str(opt), "is_correct": False})
    return normalized


def _question_needs_syntax_example(question: Dict) -> bool:
    metadata = question.get("metadata", {}) or {}
    if metadata.get("question_style_type") == "Type B":
        return False
        
    topic_id = metadata.get("topic_id")
    if isinstance(topic_id, int) and topic_id in {2, 3, 4, 5, 6, 7, 8, 9, 11, 12}:
        return True

    haystack = " ".join(
        str(part or "")
        for part in (
            metadata.get("topic"),
            metadata.get("syllabus_topic"),
            metadata.get("concept"),
            question.get("question_text"),
            " ".join(str(option.get("code_snippet", "")) for option in _normalize_options(question.get("options", []))),
        )
    ).lower()
    return any(hint in haystack for hint in (
        "insertone", "insertmany", "find(", "findone", "updateone", "updatemany", "deleteone", "deletemany",
        "projection", "cursor", "sort", "limit", "skip", "aggregate", "lookup", "unwind", "group", "match",
        "elemMatch", "dot notation", "mongoclient", "pymongo", "explain", "index", "atlas search", "search",
        "connection string", "uri"
    ))


def _validate_explanation_structure(explanation: str, needs_syntax_example: bool) -> List[str]:
    issues = []
    sections = _parse_six_part_explanation(explanation)
    
    missing_headings = [heading for heading, content in sections.items() if not content]
    if not needs_syntax_example:
        missing_headings = [heading for heading in missing_headings if heading != "### 7. Syntax Example"]
    if missing_headings:
        issues.append("missing seven-part headings or content: " + ", ".join(missing_headings))
        
    EXPLANATION_SECTION_MIN_LENGTHS = {
        "### 1. Correct Answer": 20,
        "### 2. Why Correct": 65,
        "### 3. Why Other Options Are Wrong": 100,
        "### 4. Exam Trap": 45,
        "### 5. Memory Hook": 40,
        "### 6. Follow-Up Practice Recommendation": 80,
        "### 7. Syntax Example": 20,
    }
    
    EASY_EXPLANATION_SECTION_MIN_LENGTHS = {
        "### 1. Correct Answer": 15,
        "### 2. Why Correct": 50,
        "### 3. Why Other Options Are Wrong": 75,
        "### 4. Exam Trap": 30,
        "### 5. Memory Hook": 30,
        "### 6. Follow-Up Practice Recommendation": 60,
    }
    
    min_lengths = EASY_EXPLANATION_SECTION_MIN_LENGTHS if "easy" in str(explanation).lower() else EXPLANATION_SECTION_MIN_LENGTHS
    short_sections = [
        heading
        for heading, min_length in min_lengths.items()
        if len(sections.get(heading, "")) < min_length
    ]
    if not needs_syntax_example:
        short_sections = [heading for heading in short_sections if heading != "### 7. Syntax Example"]
    if short_sections:
        issues.append("seven-part explanation sections are too short: " + ", ".join(short_sections))
        
    EXPLANATION_SECTION_MIN_BULLETS = {
        "### 6. Follow-Up Practice Recommendation": 2,
    }
    
    EASY_EXPLANATION_SECTION_MIN_BULLETS = {
        "### 6. Follow-Up Practice Recommendation": 2,
    }
    
    min_bullets = EASY_EXPLANATION_SECTION_MIN_BULLETS if "easy" in str(explanation).lower() else EXPLANATION_SECTION_MIN_BULLETS
    short_bullet_sections = [
        heading
        for heading, min_bullet_count in min_bullets.items()
        if _count_bullet_lines(sections.get(heading, "")) < min_bullet_count
    ]
    if short_bullet_sections:
        issues.append("seven-part explanation sections need more bullets: " + ", ".join(short_bullet_sections))
        
    syntax_section = sections.get("### 7. Syntax Example", "")
    if needs_syntax_example:
        if "```" not in syntax_section:
            issues.append("missing syntax example code block for a syntax-heavy concept")
        if _count_code_fences(syntax_section) < 1:
            issues.append("syntax example needs a fenced code block")
        if len(syntax_section.strip()) < 80:
            issues.append("syntax example is too short")
    elif syntax_section.strip() and not any(
        marker in syntax_section.strip().lower()
        for marker in ("not required", "not needed", "optional", "no syntax example")
    ):
        issues.append("syntax example should explicitly say it is not required for this concept")
        
    if len(explanation.strip()) < 550:
        issues.append("seven-part explanation is too short")
        
    return issues


def _validate_options(options: List[Dict]) -> List[str]:
    issues = []
    normalized = _normalize_options(options)
    
    if len(normalized) != 4:
        issues.append("does not have exactly four options")
        
    option_texts = [str(opt.get("code_snippet", "")).strip() for opt in normalized]
    if any(not text for text in option_texts):
        issues.append("contains blank option text")
        
    if any("placeholder" in text.lower() for text in option_texts):
        issues.append("contains placeholder option text")
        
    if len({text.lower() for text in option_texts}) != len(option_texts):
        issues.append("duplicate option text")

    if any(isinstance(opt, dict) and opt.get("is_correct") for opt in normalized) and sum(
        1 for opt in normalized if isinstance(opt, dict) and opt.get("is_correct")
    ) != 1:
        issues.append("does not have exactly one correct option")
        
    return issues


def _validate_question_text(question_text: str) -> List[str]:
    issues = []
    if not question_text or not question_text.strip():
        issues.append("missing question text")
    return issues


def _validate_casing_rules(question_text: str, options: List[Dict], metadata: Dict) -> List[str]:
    issues = []
    
    topic_name = metadata.get("topic") or metadata.get("syllabus_topic") or ""
    syntax_ok, syntax_msg = planner.validate_lexical_syntax_guard(
        topic_name,
        question_text,
        options
    )
    if not syntax_ok:
        issues.append(f"Casing validation failed: {syntax_msg}")
        
    return issues


def _validate_topic1_concepts(options: List[Dict], question_text: str, metadata: Dict) -> List[str]:
    issues = []
    
    from certcoach.core.content_contract import has_invented_topic1_type, is_topic1_concept_only
    
    topic_text = " ".join(
        str(part or "")
        for part in (
            metadata.get("topic"),
            metadata.get("syllabus_topic"),
            metadata.get("concept"),
            question_text,
            " ".join(str(option.get("code_snippet", "")) for option in _normalize_options(options)),
        )
    ).lower()
    
    normalized = _normalize_options(options)

    if is_topic1_concept_only(metadata, topic_text):
        if any(has_invented_topic1_type(str(option.get("code_snippet", ""))) for option in normalized):
            issues.append("contains invented BSON type names")
        if has_invented_topic1_type(str(question_text)):
            issues.append("question text contains invented BSON type names")
            
    return issues


def _verify_source_files(question: Dict, source_files: List[str]) -> List[str]:
    issues = []
    
    if not source_files:
        issues.append("No source files provided for verification")
        return issues
        
    citation_source = question.get("metadata", {}).get("citation_source", "")
    if not citation_source:
        issues.append("Missing citation_source in metadata")
        return issues
        
    source_file_found = False
    for source_file in source_files:
        if citation_source in source_file or source_file in citation_source:
            source_file_found = True
            break
            
    if not source_file_found:
        issues.append(f"Citation source '{citation_source}' not found in provided source files")
        
    return issues


def _verify_context_grounding(question: Dict, context_text: str) -> List[str]:
    issues = []
    
    if not context_text:
        issues.append("No context text provided for grounding verification")
        return issues
        
    question_text = question.get("question_text", "")
    options_text = " ".join(str(opt.get("code_snippet", "")) for opt in _normalize_options(question.get("options", [])))
    
    context_lower = context_text.lower()
    question_lower = question_text.lower()
    options_lower = options_text.lower()
    
    if question_lower not in context_lower:
        issues.append("Question text not found in documentation context")
        
    if options_lower and options_lower not in context_lower:
        issues.append("Answer options not found in documentation context")
        
    return issues


def judge_question(question: Dict, source_files: List[str], context_text: str) -> List[str]:
    issues = []
    
    if not get_judge_enabled():
        return issues
        
    metadata = question.get("metadata", {})
    
    issues.extend(_validate_question_text(question.get("question_text", "")))
    issues.extend(_validate_options(question.get("options", [])))
    issues.extend(_validate_casing_rules(
        question.get("question_text", ""),
        question.get("options", []),
        metadata
    ))
    issues.extend(_validate_topic1_concepts(
        question.get("options", []),
        question.get("question_text", ""),
        metadata
    ))
    issues.extend(_validate_explanation_structure(
        question.get("explanation", ""),
        _question_needs_syntax_example(question)
    ))
    
    issues.extend(_verify_source_files(question, source_files))
    issues.extend(_verify_context_grounding(question, context_text))
    
    return issues


def judge_explanation_repair(original_question: Dict, repaired_explanation: str, 
                            source_files: List[str], context_text: str) -> List[str]:
    issues = []
    
    if not get_judge_enabled():
        return issues
        
    repaired_question = dict(original_question)
    repaired_question["explanation"] = repaired_explanation
    
    issues.extend(_validate_explanation_structure(
        repaired_explanation,
        _question_needs_syntax_example(repaired_question)
    ))
    
    issues.extend(_verify_source_files(repaired_question, source_files))
    issues.extend(_verify_context_grounding(repaired_question, context_text))
    
    return issues


def main():
    print("Judge Questions Module - Core RAG-grounded quality verification")
    print("This module provides:")
    print("1. Question validation with source file verification")
    print("2. Context grounding verification")
    print("3. Explanation structure validation")
    print("4. Integration with model_runner quality gates")
    
    model_runner = get_model_runner()
    print(f"\nCircuit breaker status: {model_runner.get_circuit_breaker_status()}")


if __name__ == "__main__":
    main()
