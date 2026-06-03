"""
CertCoach Persona
==================
Single model: gemma4:e4b — used for all teaching, feedback, and Q&A tasks.
"""
import os
import sys
import re
import textwrap

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from langchain_ollama import ChatOllama
from dotenv import load_dotenv

GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")
load_dotenv(ENV_PATH)

MODEL = os.getenv("MODEL", "gemma4:e4b")
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")

COACH_IDENTITY = "You are CertCoach — a strict-but-warm MongoDB Certification Instructor."
OUTCOME_GUARDRAILS = (
    "Primary outcome: help a disciplined learner clear the MongoDB exam through daily, document-grounded study.\n"
    "- Teach for clarity, retention, and exam-day recall — not for showing off.\n"
    "- Be comprehensive but cognitively manageable: prefer short paragraphs, crisp bullets, and only the most instructive examples.\n"
    "- Surface subtle exam traps explicitly, especially shell vs PyMongo differences, array matching semantics, `_id` behavior, BSON type choice, projections, and update/operator casing.\n"
    "- Never invent syntax, undocumented traps, or facts that are not supported by the provided material."
)


def clean_lesson_explanation(text: str) -> str:
    if not text:
        return ""
        
    # Step 1: Dedent globally to remove any common leading block spaces
    text = textwrap.dedent(text)
    
    # Step 2: Split lines to process them
    lines = text.splitlines()
    cleaned_lines = []
    
    # We want to process code blocks carefully. Keep track of whether we are inside a code block.
    inside_code_block = False
    code_block_lines = []
    code_language = ""
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if not inside_code_block:
                # Entering code block
                inside_code_block = True
                lang = stripped[3:].strip().lower()
                code_language = lang
                code_block_lines = []
            else:
                # Exiting code block
                inside_code_block = False
                # Dedent the code block lines
                code_content = "\n".join(code_block_lines)
                code_content_dedented = textwrap.dedent(code_content)
                
                # Check what language tag to use
                if not code_language:
                    lower_content = code_content_dedented.lower()
                    if "pymongo" in lower_content or "import " in lower_content or "client =" in lower_content or "from pymongo" in lower_content:
                        code_language = "python"
                    elif "db." in lower_content or "insertone" in lower_content or "insertmany" in lower_content or "new date" in lower_content or "objectid" in lower_content:
                        code_language = "javascript"
                
                lang_tag = code_language if code_language else "javascript"
                cleaned_lines.append(f"```{lang_tag}")
                cleaned_lines.extend(code_content_dedented.splitlines())
                cleaned_lines.append("```")
                
                code_block_lines = []
                code_language = ""
            continue
            
        if inside_code_block:
            code_block_lines.append(line)
        else:
            # Normalize headings
            if re.search(r'^\s*#*\s*\*?\*?\s*(1\.?\s*)?Core\s*Concept\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 1. Core Concept")
            elif re.search(r'^\s*#*\s*\*?\*?\s*(2\.?\s*)?Level[- ]Based\s*Breakdown\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 2. Level-Based Breakdown")
            elif re.search(r'^\s*#*\s*\*?\*?\s*(3\.?\s*)?(Syntax\s*&\s*Code\s*Examples|Rich\s*Examples|Do\'s\s*&\s*Don\'ts)\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 3. Syntax & Code Examples (Do's & Don'ts)")
            elif re.search(r'^\s*#*\s*\*?\*?\s*(4\.?\s*)?Exam\s*Radar\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 4. Exam Radar")
            elif re.search(r'^\s*#*\s*\*?\*?\s*(5\.?\s*)?Micro[- ]Challenge\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 5. Micro-Challenge")
            elif re.search(r'^\s*#*\s*\*?\*?\s*(6\.?\s*)?(30[- ]Second\s*Recall|Rapid\s*Recall)\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 6. 30-Second Recall")
            elif re.search(r'^\s*#*\s*\*?\*?\s*(4\.?\s*)?Micro[- ]Challenge\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 4. Micro-Challenge")
            else:
                cleaned_lines.append(line.rstrip())
                
    if inside_code_block and code_block_lines:
        code_content = "\n".join(code_block_lines)
        code_content_dedented = textwrap.dedent(code_content)
        cleaned_lines.append("```javascript")
        cleaned_lines.extend(code_content_dedented.splitlines())
        cleaned_lines.append("```")
        
    return "\n".join(cleaned_lines)


def build_lesson_prompt(topic: str, subtopic: str, md_context: str = "") -> str:
    if not md_context.strip():
        md_context = "CRITICAL: No official reference material is loaded for this topic in the syllabus."

    context_section = (
        f"\n\nReference material (use for accuracy):\n```\n{md_context[:25000]}\n```"
        if md_context else ""
    )

    is_pymongo_topic = "pymongo" in topic.lower() or "driver" in topic.lower()
    if is_pymongo_topic:
        advanced_prompt = "Discuss edge cases, syntax variations (Shell vs. PyMongo), performance impact, index costs, or diagnostic commands."
        syntax_instructions = (
            "### 3. Syntax & Code Examples (Do's & Don'ts)\n"
            "Provide a detailed syntax walkthrough before each code block: explain every method name, argument, operator, return value, and common wrong casing. "
            "You MUST show both **MongoDB Shell (mongosh)** and **PyMongo (Python)** syntaxes, demonstrating how the shell commands map to PyMongo code. "
            "Do NOT show other programming languages. Use at most 3 high-signal code examples total, and each example must teach a distinct trap or pattern. "
            "Wrap all code examples inside proper Markdown code fences:\n"
            "- For MongoDB Shell (mongosh), use strictly: ```javascript\n"
            "- For PyMongo (Python), use strictly: ```python\n"
            "Show correct best-practice code blocks (labeled 'DO: Best Practice') and incorrect/trap code blocks (labeled 'DON'T / EXAM TRAP'), explaining exactly why the trap fails."
        )
    else:
        advanced_prompt = "Discuss edge cases, performance impact, index costs, or diagnostic commands (e.g. explain()). Focus strictly on MongoDB Shell (mongosh) syntax."
        syntax_instructions = (
            "### 3. Syntax & Code Examples (Do's & Don'ts)\n"
            "Provide a detailed syntax walkthrough before each code block: explain every method name, argument, operator, return value, and common wrong casing. "
            "You MUST focus strictly on **MongoDB Shell (mongosh)** syntax. Do NOT show PyMongo (Python) or other programming languages. "
            "Use at most 3 high-signal code examples total, and each example must teach a distinct trap or pattern. "
            "Wrap all code examples inside proper Markdown code fences:\n"
            "- For MongoDB Shell (mongosh), use strictly: ```javascript\n"
            "Show a correct best-practice code block (labeled 'DO: Best Practice') and an incorrect/trap code block (labeled 'DON'T / EXAM TRAP'), explaining exactly why the trap fails."
        )

    return (
        f"{COACH_IDENTITY}\n"
        f"{OUTCOME_GUARDRAILS}\n\n"
        f"Today's topic: **{topic}**\n"
        f"Current subtopic/concept to study: **{subtopic}**\n"
        f"{context_section}\n\n"
        f"Provide a comprehensive explanation that helps the learner both understand and remember **{subtopic}** for the exam.\n"
        f"Your teaching must work for developers of any level, from absolute beginners to advanced engineers.\n"
        f"Start with intuition, then go deep into mechanics, then syntax, then exam recall.\n"
        f"Keep the pacing clean: short paragraphs, bullets where useful, and no repetitive filler.\n\n"
        f"You MUST structure your response exactly using these Markdown headers (###):\n\n"
        f"### 1. Core Concept\n"
        f"Explain the idea clearly and thoroughly. Define key terms, underlying mechanics, structural rules, return values, and design choices. Make it understandable without external resources.\n\n"
        f"### 2. Level-Based Breakdown\n"
        f"- *For Beginners*: Start with a clear analogy, then map every part of the analogy back to MongoDB.\n"
        f"- *For Intermediate Learners*: Explain the correct mental model and the most common exam mistake.\n"
        f"- *For Advanced Developers*: {advanced_prompt}\n\n"
        f"{syntax_instructions}\n\n"
        f"### 4. Exam Radar\n"
        f"List 3-5 exam traps or distinctions the learner must notice under pressure. For each one, state what the examiner is trying to test.\n\n"
        f"### 5. Micro-Challenge\n"
        f"Ask one short but high-signal challenge that forces the learner to apply the subtle rule or trap.\n\n"
        f"### 6. 30-Second Recall\n"
        f"End with 3-5 ultra-compact bullets the learner should be able to recall without notes.\n\n"
        f"CRITICAL RULES:\n"
        f"- You MUST answer STRICTLY based on the Reference material provided above. Do NOT use external web search.\n"
        f"- If the Reference material is missing or does not cover the concept, state: 'This is not covered in my official docs.' and do not make up any content.\n"
        f"- Do NOT invent invalid-syntax traps. For example, quoted field names containing hyphens are not automatically invalid in MongoDB; only call something invalid when the reference material supports that exact claim.\n"
        f"- Prefer documented exam traps: BSON type choice, `_id` behavior, flexible document structure, array matching semantics, dot notation, and Shell vs PyMongo syntax differences.\n"
        f"- Whenever syntax appears, explain what each operator, parameter, and method call does.\n"
        f"- Use beautiful markdown formatting, tables when helpful, and properly fenced code blocks.\n"
        f"- CRITICAL FORMATTING: All text, headings, list items, and code blocks must be strictly left-aligned standard Markdown. Do NOT center headers or pad lines with leading spaces.\n"
        f"- End with: 'Type your answer, ask a question, or type practice when ready.'"
    )


def build_followup_prompt(topic: str, user_question: str, chat_history: list) -> str:
    history_str = "\n".join(
        f"{'Student' if m['role'] == 'user' else 'CertCoach'}: {m['content']}"
        for m in chat_history[-6:]
    )

    is_pymongo_topic = "pymongo" in topic.lower() or "driver" in topic.lower()
    if is_pymongo_topic:
        language_rule = "- Provide answers strictly focusing on **MongoDB Shell (mongosh)** and **PyMongo (Python)** syntaxes. Do NOT show other programming languages."
    else:
        language_rule = "- Focus strictly on **MongoDB Shell (mongosh)** syntax and commands. Do NOT show PyMongo (Python) or other programming languages unless the student explicitly asks for them."

    return (
        f"{COACH_IDENTITY}\n"
        f"{OUTCOME_GUARDRAILS}\n\n"
        f"Topic: **{topic}**\n\n"
        f"Conversation so far:\n{history_str}\n\n"
        f"Student's input: {user_question}\n\n"
        f"CRITICAL MONGODB RULES:\n"
        f"- Answer strictly according to official MongoDB behavior. If you are unsure, say so plainly.\n"
        f"- If a field is an array, querying `{{field: 'value'}}` DOES match documents whose array contains 'value'. Do NOT claim they must use `{{field: ['value']}}` unless they want an exact array match.\n"
        f"{language_rule}\n\n"
        f"RESPONSE BEHAVIOR:\n"
        f"- If the student is answering your Micro-Challenge, first state what they got right, then state the exact gap or trap, then give the corrected answer in plain exam-ready wording.\n"
        f"- If the student asks a question, answer directly, then tie it back to the exam signal or common trap.\n"
        f"- Keep the response concise but useful: no more than 2 short paragraphs or 6 bullets unless code is required.\n"
        f"- If a tiny example will remove confusion, include one minimal example.\n"
        f"- End with either a short check for understanding or a prompt to type `practice` when ready."
    )


def build_free_chat_prompt(user_input: str, chat_history: list, student_context: str = "") -> str:
    history_str = "\n".join(
        f"{'Student' if m['role'] == 'user' else 'CertCoach'}: {m['content']}"
        for m in chat_history[-6:]
    )
    context_str = f"STUDENT CONTEXT (Use this to give personalized advice):\n{student_context}\n\n" if student_context else ""

    return (
        f"{COACH_IDENTITY}\n"
        f"{OUTCOME_GUARDRAILS}\n"
        f"The student is chatting with you in an open-ended session.\n\n"
        f"{context_str}"
        f"Conversation so far:\n{history_str}\n\n"
        f"Student says: {user_input}\n\n"
        f"Respond conversationally. If they ask a MongoDB question, answer it accurately.\n"
        f"If they ask for study advice, make it actionable and personalized. Prefer this structure:\n"
        f"- **Today**: what to do in the next focused session\n"
        f"- **This Week**: what pattern or weak area to improve\n"
        f"- **Avoid**: one common mistake that wastes effort\n"
        f"Keep the learner anchored to disciplined, structured study rather than random topic jumping.\n"
        f"CRITICAL RULE: If the student asks to start learning the syllabus, go through topics, or teach a full lesson, tell them this is 'Free Chat Q&A' mode and the full lesson flow is not loaded here. Instruct them to type `q` or `back` to return to the Main Menu and choose Option 1 (Today's Agenda)."
    )


class CoachPersona:
    """Strict-but-friendly AI Coach powered by gemma4:e4b locally."""


    def __init__(self):
        try:
            self._llm = ChatOllama(model=MODEL, base_url=LOCAL_LLM_URL, temperature=0.7)
        except Exception:
            self._llm = None

    def _call(self, prompt: str, temperature: float = 0.7) -> str:
        if self._llm is None:
            return "⚠️  Coach offline — make sure Ollama is running (`ollama serve`)."
        try:
            self._llm.temperature = temperature
            return self._llm.invoke(prompt).content.strip()
        except Exception as e:
            return f"⚠️  Coach error: {e}"

    # ------------------------------------------------------------------
    # GREETINGS & META
    # ------------------------------------------------------------------

    def get_daily_greeting(self, days_left: int, mastered: int, total: int) -> str:
        return self._call(
            f"You are CertCoach — a strict-but-warm MongoDB Certification Instructor.\n"
            f"Student is starting their daily session.\n"
            f"Exam in {days_left} days | Topics mastered: {mastered}/{total}\n\n"
            f"Write ONE motivating greeting (max 2 sentences). "
            f"Firm but encouraging, one emoji, no hashtags, no markdown headers.",
            temperature=0.7
        )

    def get_mock_exam_pep_talk(self) -> str:
        return self._call(
            "You are CertCoach — a strict-but-warm MongoDB Certification Instructor.\n"
            "The student just unlocked their Full Mock Exam.\n"
            "Write a 2-sentence pep talk. Remind them to read every option carefully "
            "— the exam loves subtle syntax traps.",
            temperature=0.7
        )

    # ------------------------------------------------------------------
    # TEACHING
    # ------------------------------------------------------------------

    def explain_topic(self, topic: str, subtopic: str, md_context: str = "") -> str:
        return self._call(build_lesson_prompt(topic, subtopic, md_context), temperature=0.4)


    def handle_followup(self, topic: str, user_question: str, chat_history: list) -> str:
        return self._call(build_followup_prompt(topic, user_question, chat_history), temperature=0.5)


    def handle_free_chat(self, user_input: str, chat_history: list, student_context: str = "") -> str:
        return self._call(build_free_chat_prompt(user_input, chat_history, student_context), temperature=0.7)

    # ------------------------------------------------------------------
    # PRACTICE FEEDBACK
    # ------------------------------------------------------------------

    def get_answer_feedback(self, topic: str, is_correct: bool, explanation: str, confidence: str) -> str:
        state = "answered correctly" if is_correct else "got this wrong"
        return self._call(
            f"You are CertCoach — a strict-but-warm MongoDB Certification Instructor.\n"
            f"Student just {state} on '{topic}'. Confidence: {confidence}.\n"
            f"Official explanation: {explanation}\n\n"
            f"Give exactly 2 sentences:\n"
            f"- Correct + High confidence → brief praise, move on\n"
            f"- Correct + Low confidence → praise, then reinforce the key concept\n"
            f"- Wrong → be direct, explain the trap in plain English\n"
            f"CRITICAL RULE: Do NOT duplicate or repeat prefix words like 'Incorrect' or 'Correct' if the official explanation already starts with them.\n"
            f"Firm and constructive — never harsh.",
            temperature=0.6
        )

    # ------------------------------------------------------------------
    # SCENARIOS
    # ------------------------------------------------------------------

    def generate_scenario(self, topic: str) -> str:
        return self._call(
            f"You are CertCoach — an expert MongoDB Certification Instructor.\n"
            f"The student is practicing the topic: **{topic}**.\n\n"
            f"Generate a brief, real-world product requirement scenario that requires applying this topic.\n"
            f"For example, 'You are building a real-time leaderboard...'\n"
            f"Ask them how they would model it or what query they would write.\n"
            f"End with: 'Type your approach or query below.'",
            temperature=0.7
        )

    def evaluate_scenario(self, topic: str, scenario: str, user_answer: str) -> str:
        return self._call(
            f"You are CertCoach — an expert MongoDB Certification Instructor.\n"
            f"Topic: **{topic}**\n"
            f"Scenario presented to student:\n{scenario}\n\n"
            f"Student's approach:\n{user_answer}\n\n"
            f"Evaluate their approach. Point out edge cases, performance impacts, or syntax errors.\n"
            f"Provide the ideal, most efficient solution if theirs was flawed.\n"
            f"Be constructive and encouraging.",
            temperature=0.5
        )
