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
                f"### 3. Syntax & Code Examples (Do's & Don'ts)\n"
                f"Provide clean, syntax-highlighted code blocks for comparison. You MUST show both **MongoDB Shell (mongosh)** and **PyMongo (Python)** syntaxes, demonstrating how the shell commands map to PyMongo code. Do NOT show other programming languages. Wrap all code examples inside proper Markdown code fences:\n"
                f"- For MongoDB Shell (mongosh), use strictly: ```javascript\n"
                f"- For PyMongo (Python), use strictly: ```python\n"
                f"Show correct best practices code blocks for both (labeled 'DO: Best Practices') and incorrect/trap code blocks (labeled 'DON'T / EXAM TRAP') side-by-side or sequentially, explaining exactly why the trap fails."
            )
        else:
            advanced_prompt = "Discuss edge cases, performance impact, index costs, or diagnostic commands (e.g. explain()). Focus strictly on MongoDB Shell (mongosh) syntax."
            syntax_instructions = (
                f"### 3. Syntax & Code Examples (Do's & Don'ts)\n"
                f"Provide clean, syntax-highlighted code blocks for comparison. You MUST focus strictly on **MongoDB Shell (mongosh)** syntax. Do NOT show PyMongo (Python) or other programming languages. Wrap all code examples inside proper Markdown code fences:\n"
                f"- For MongoDB Shell (mongosh), use strictly: ```javascript\n"
                f"Show a correct best practices code block (labeled 'DO: Best Practices') and an incorrect/trap code block (labeled 'DON'T / EXAM TRAP') side-by-side or sequentially, explaining exactly why the trap fails."
            )

        return self._call(
            f"You are CertCoach — an expert MongoDB Certification Instructor.\n\n"
            f"Today's topic: **{topic}**\n"
            f"Current subtopic/concept to study: **{subtopic}**\n"
            f"{context_section}\n\n"
            f"Provide a comprehensive, highly detailed explanation focusing strictly on the current concept: **{subtopic}**.\n"
            f"Your teaching must benefit developers of any level—from absolute beginners to advanced engineers.\n\n"
            f"You MUST structure your response exactly using these Markdown headers (###):\n\n"
            f"### 1. Core Concept\n"
            f"Explain the underlying database mechanics, structural rules, and design choices. Go as deep and detailed as possible. Break down the mechanical steps or storage trade-offs if applicable.\n\n"
            f"### 2. Level-Based Breakdown\n"
            f"- *For Beginners*: Use a clear, intuitive real-world analogy to anchor the concept.\n"
            f"- *For Advanced Developers*: {advanced_prompt}\n\n"
            f"{syntax_instructions}\n\n"
            f"### 4. Micro-Challenge\n"
            f"Ask an engaging 1-question challenge related to the subtle edge cases or traps of this subtopic to check their understanding.\n\n"
            f"CRITICAL RULES:\n"
            f"- You MUST answer STRICTLY based on the Reference material provided above. Do NOT use external web search.\n"
            f"- If the Reference material is missing or does not cover the concept, state: 'This is not covered in my official docs.' and do not make up any content.\n"
            f"- Use beautiful markdown formatting, code highlights, and tables if helpful.\n"
            f"- CRITICAL FORMATTING: All text, headings, list items, and code blocks must be strictly left-aligned standard Markdown. Do NOT center headers or text manually. Do NOT pad lines with leading spaces or tabs to center them. Any manual space padding ruins the terminal border and word wrapping layout.\n"
            f"- End with: 'Type your answer or ask any questions.'",
            temperature=0.4
        )


    def handle_followup(self, topic: str, user_question: str, chat_history: list) -> str:
        history_str = "\n".join(
            f"{'Student' if m['role'] == 'user' else 'CertCoach'}: {m['content']}"
            for m in chat_history[-6:]
        )
        
        is_pymongo_topic = "pymongo" in topic.lower() or "driver" in topic.lower()
        if is_pymongo_topic:
            language_rule = "- Provide answers strictly focusing on **MongoDB Shell (mongosh)** and **PyMongo (Python)** syntaxes. Do NOT show other programming languages."
        else:
            language_rule = "- Focus strictly on **MongoDB Shell (mongosh)** syntax and commands. Do NOT show PyMongo (Python) or other programming languages in your responses unless the student explicitly asks for them."

        return self._call(
            f"You are CertCoach — a strict-but-warm MongoDB Certification Instructor.\n"
            f"Topic: **{topic}**\n\n"
            f"Conversation so far:\n{history_str}\n\n"
            f"Student's input: {user_question}\n\n"
            f"CRITICAL MONGODB RULES:\n"
            f"- You MUST answer STRICTLY based on official MongoDB best practices. If you don't know, say so.\n"
            f"- If a field is an array, querying `{{field: 'value'}}` DOES return documents where the array contains 'value'. Do NOT tell the student they need to wrap it in an array like `{{field: ['value']}}` unless they are looking for an exact array match.\n"
            f"{language_rule}\n\n"
            f"If the student is answering your interactive practice question, evaluate their MongoDB syntax, correct them if needed, and praise them if right.\n"
            f"If they ask a question, answer clearly and concisely.\n"
            f"End with a short follow-up like 'Does that clear it up?' or ask if they are ready to type 'practice' for the MCQs.",
            temperature=0.5
        )


    def handle_free_chat(self, user_input: str, chat_history: list, student_context: str = "") -> str:
        history_str = "\n".join(
            f"{'Student' if m['role'] == 'user' else 'CertCoach'}: {m['content']}"
            for m in chat_history[-6:]
        )
        
        context_str = f"STUDENT CONTEXT (Use this to give personalized advice):\n{student_context}\n\n" if student_context else ""
        
        return self._call(
            f"You are CertCoach — a strict-but-warm MongoDB Certification Instructor.\n"
            f"The student is chatting with you in an open-ended session.\n\n"
            f"{context_str}"
            f"Conversation so far:\n{history_str}\n\n"
            f"Student says: {user_input}\n\n"
            f"Respond conversationally. If they ask a MongoDB question, answer it. "
            f"If they ask for study advice, proactively use their STUDENT CONTEXT to point out weak topics or suggest next steps based on their agenda. Be concise, use markdown.\n"
            f"CRITICAL RULE: If the student asks to start learning the syllabus, go through topics, or teach them a lesson, tell them that this is the 'Free Chat Q&A' mode and you don't have the full lesson modules loaded here. Instruct them to type `q` or `back` to return to the Main Menu, and then select Option 1 (Today's Agenda) to start their structured study plan.",
            temperature=0.7
        )

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
