"""Interactive CertCoach teaching, feedback, and Q&A persona."""
import os
import sys
import re
import textwrap

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from langchain_ollama import ChatOllama
from certcoach.core.config import (
    get_local_llm_url,
    get_study_model,
    get_study_num_ctx,
    get_study_reasoning,
)

MODEL = get_study_model()
LOCAL_LLM_URL = get_local_llm_url()
STUDY_NUM_CTX = get_study_num_ctx()
STUDY_REASONING = get_study_reasoning()

COACH_IDENTITY = "You are CertCoach — a Senior Staff Engineer and a strict-but-constructive MongoDB Certification Lead."
OUTCOME_GUARDRAILS = (
    "Primary outcome: help a disciplined learner clear the MongoDB exam through daily, document-grounded study.\n"
    "- Conduct explanations like a Senior Staff Engineer reviewing code: focus on syntax rules, casing correctness, and engine performance.\n"
    "- Ground feedback in production reality: explicitly warn about COLLSCAN costs, sorting memory limits, and PyMongo driver exceptions.\n"
    "- Be comprehensive but cognitively manageable: prefer short paragraphs, crisp bullets, and only the most instructive examples.\n"
    "- Surface subtle exam traps explicitly, especially shell vs PyMongo differences, array matching semantics, _id behavior, BSON type choice, projections, and update/operator casing.\n"
    "- Never invent syntax, undocumented traps, or facts that are not supported by the provided material."
)

TEACH_SCOPE_RULES = (
    "Scope rules:\n"
    "- Stay strictly within the current syllabus topic and the current concept.\n"
    "- You may mention a prerequisite only if it is needed to explain the current concept.\n"
    "- Do not introduce later-topic methods, operators, workflows, or mock-exam style questions.\n"
    "- If the learner asks for examples, keep them inside the current concept and do not cross into the next syllabus node.\n"
)

TEACH_DEPTH_RULES = (
    "Depth rules:\n"
    "- Assume the learner is seeing the concept for the first time.\n"
    "- Explain the core idea before moving to examples.\n"
    "- Define each key term, explain why it exists, and show how it behaves in MongoDB.\n"
    "- When syntax is shown, walk line-by-line through the example and explain every meaningful token, argument, operator, and return value.\n"
    "- Use at least one strong DO example and one clear DON'T / EXAM TRAP example whenever syntax is part of the concept.\n"
    "- For the DO example, explain why it is correct and when the learner should use it.\n"
    "- For the DON'T example, explain exactly what breaks or why it is the wrong choice.\n"
    "- Do not use later-topic methods or workflows just to make the example feel richer.\n"
    "- Keep examples concept-bound and first-time-learner friendly, even when the topic is simple.\n"
)

TEACH_FORMAT_RULES = (
    "Format rules:\n"
    "- Use a stable internal layout inside each section so the lesson reads cleanly.\n"
    "- In Core Concept, prefer explicit mini-subsections such as Definition, Key Terms, Underlying Mechanics, and Design Choices.\n"
    "- In Level-Based Breakdown, keep the three audience levels clearly labeled.\n"
    "- In Syntax & Code Examples, use clearly labeled DO and DON'T / EXAM TRAP subsections and explain the example directly underneath.\n"
    "- Avoid deeply nested bullet stacks; prefer short paragraphs, flat bullets, or bold subsection labels.\n"
    "- Keep line breaks intentional so the rendered lesson is easy to scan.\n"
)

TEACH_TEMPLATE_RULES = (
    "Template rules:\n"
    "- The lesson must always use these six top-level sections in order: Core Concept, Level-Based Breakdown, Syntax & Code Examples, Exam Radar, Micro-Challenge, 30-Second Recall.\n"
    "- Core Concept must define the concept, name the key terms, explain the mechanics, and explain the design choice or tradeoff.\n"
    "- Level-Based Breakdown must contain exactly three audiences: Beginners, Intermediate Learners, and Advanced Developers.\n"
    "- Syntax & Code Examples must include a DO example and a DON'T / EXAM TRAP example when syntax applies.\n"
    "- The DO and DON'T examples must differ by one meaningful detail; do not reuse the same code in both examples.\n"
    "- For Topic 1 and other concept-only lessons, syntax examples must stay at the BSON/document-literal level. Do not use CRUD helpers, query operators, update operators, driver calls, or insert/find/update methods.\n"
    "- Exam Radar must contain 3-5 traps or distinctions, each with the exam signal being tested.\n"
    "- Micro-Challenge must be one question only, with no answer, no hint, and no example response.\n"
    "- Default to a short open-ended question. Use multiple choice only when it genuinely improves clarity.\n"
    "- For Topic 1 and other concept-only lessons, prefer open-ended micro-challenges and avoid multiple choice unless it is essential.\n"
    "- For Topic 1 and other concept-only lessons, the micro-challenge must not use invented BSON type names.\n"
    "- If the Micro-Challenge is multiple choice, label options with A/B/C/D and show the full text of the choice.\n"
    "- 30-Second Recall must end with 3-5 short bullets that fit in memory without notes.\n"
)

FOLLOWUP_SCOPE_RULES = (
    "Scope rules:\n"
    "- Stay strictly within the current syllabus topic and current concept.\n"
    "- Answer the learner's question or correct their micro-challenge response directly.\n"
    "- If the learner requests more examples, give at most two and keep them inside the current concept.\n"
    "- If the request belongs to a later topic, say it is deferred until that topic is reached.\n"
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
    in_micro_challenge = False
    
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
                in_micro_challenge = False
            elif re.search(r'^\s*#*\s*\*?\*?\s*(2\.?\s*)?Level[- ]Based\s*Breakdown\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 2. Level-Based Breakdown")
                in_micro_challenge = False
            elif re.search(r'^\s*#*\s*\*?\*?\s*(3\.?\s*)?(Syntax\s*&\s*Code\s*Examples|Rich\s*Examples|Do\'s\s*&\s*Don\'ts)\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 3. Syntax & Code Examples (Do's & Don'ts)")
                in_micro_challenge = False
            elif re.search(r'^\s*#*\s*\*?\*?\s*(4\.?\s*)?Exam\s*Radar\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 4. Exam Radar")
                in_micro_challenge = False
            elif re.search(r'^\s*#*\s*\*?\*?\s*(4\.?\s*)?Micro[- ]Challenge\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 4. Micro-Challenge")
                in_micro_challenge = True
            elif re.search(r'^\s*#*\s*\*?\*?\s*(5\.?\s*)?Micro[- ]Challenge\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 5. Micro-Challenge")
                in_micro_challenge = True
            elif re.search(r'^\s*#*\s*\*?\*?\s*(6\.?\s*)?(30[- ]Second\s*Recall|Rapid\s*Recall)\b', stripped, re.IGNORECASE):
                cleaned_lines.append("### 6. 30-Second Recall")
                in_micro_challenge = False
            elif in_micro_challenge and re.match(r'^(Correct Answer|Corrected Answer|Answer|Explanation|Hint|Solution)\s*[:\-]?', stripped, re.IGNORECASE):
                continue
            elif in_micro_challenge and re.match(r'^[1-4]\s*[\).:-]?\s*(.*)$', stripped, re.IGNORECASE):
                choice_text = re.sub(r'^[1-4]\s*[\).:-]?\s*', '', stripped).strip()
                letter = {"1": "A", "2": "B", "3": "C", "4": "D"}[stripped[0]]
                cleaned_lines.append(f"- {letter}) {choice_text}" if choice_text else f"- {letter})")
            elif re.match(r'^\s*[•\-\*]?\s*(Definition|Key Terms|Underlying Mechanics|Mechanics|Design Choices|Explanation|Beginners|For Beginners|Intermediate Learners|For Intermediate Learners|Advanced Developers|For Advanced Developers|DO: Best Practice|DON\'T\s*/\s*EXAM TRAP|Question|Correct Answer|Explanation)\s*:?\s*$', stripped, re.IGNORECASE):
                label = re.sub(r'^\s*[•\-\*]?\s*', '', stripped).strip().rstrip(":")
                label = re.sub(r'\s+', ' ', label)
                cleaned_lines.append(f"#### {label}")
            else:
                if in_micro_challenge and re.match(r'^[ABCD]\s*$', stripped, re.IGNORECASE):
                    cleaned_lines.append(f"- {stripped}")
                else:
                    cleaned_lines.append(line.strip())
                
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
    is_conceptual_topic = any(
        marker in f"{topic} {subtopic}".lower()
        for marker in (
            "bson data types",
            "document structure",
            "collections vs tables",
            "document model",
            "overview & the document model",
        )
    )
    if is_pymongo_topic:
        advanced_prompt = "Discuss edge cases, syntax variations (Shell vs. PyMongo), performance impact, index costs, or diagnostic commands."
        syntax_instructions = (
            "### 3. Syntax & Code Examples (Do's & Don'ts)\n"
            "Teach the syntax as if this is the learner's first time seeing it. Provide a detailed syntax walkthrough before each code block: explain every method name, argument, operator, return value, and common wrong casing. "
            "You MUST show both **MongoDB Shell (mongosh)** and **PyMongo (Python)** syntaxes, demonstrating how the shell commands map to PyMongo code. "
            "Do NOT show other programming languages. Use at most 3 high-signal code examples total, and each example must teach a distinct trap or pattern. "
            "Use clearly labeled DO and DON'T / EXAM TRAP subsections and avoid deeply nested bullets. "
            "For concept-only lessons, use only BSON/document-literal examples that belong to the current concept; do NOT introduce CRUD write methods unless they are already part of the concept. "
            "For Topic 1, do not use field-name validity traps; keep the contrast focused on BSON value types, embedded documents, arrays, and document shape. "
            "For Topic 1, do not show `db.collection.insertOne(...)`, `find(...)`, update operators, or any other method-call example in the syntax section.\n"
            "Wrap all code examples inside proper Markdown code fences:\n"
            "- For MongoDB Shell (mongosh), use strictly: ```javascript\n"
            "- For PyMongo (Python), use strictly: ```python\n"
            "Show correct best-practice code blocks (labeled 'DO: Best Practice') and incorrect/trap code blocks (labeled 'DON'T / EXAM TRAP'), explaining exactly why the trap fails.\n"
            "After each example, explain what the learner should notice, what would change if one part changed, and why this pattern is preferred in MongoDB."
        )
    else:
        advanced_prompt = "Discuss edge cases, performance impact, index costs, or diagnostic commands (e.g. explain()). Focus strictly on MongoDB Shell (mongosh) syntax."
        syntax_instructions = (
            "### 3. Syntax & Code Examples (Do's & Don'ts)\n"
            "Teach the syntax as if this is the learner's first time seeing it. Provide a detailed syntax walkthrough before each code block: explain every method name, argument, operator, return value, and common wrong casing. "
            "You MUST focus strictly on **MongoDB Shell (mongosh)** syntax. Do NOT show PyMongo (Python) or other programming languages. "
            "Use at most 3 high-signal code examples total, and each example must teach a distinct trap or pattern. "
            "Use clearly labeled DO and DON'T / EXAM TRAP subsections and avoid deeply nested bullets. "
            "For concept-only lessons, use only BSON/document-literal examples that belong to the current concept; do NOT introduce CRUD write methods unless they are already part of the concept. "
            "For Topic 1, do not use field-name validity traps; keep the contrast focused on BSON value types, embedded documents, arrays, and document shape. "
            "For Topic 1, do not show `db.collection.insertOne(...)`, `find(...)`, update operators, or any other method-call example in the syntax section.\n"
            "Wrap all code examples inside proper Markdown code fences:\n"
            "- For MongoDB Shell (mongosh), use strictly: ```javascript\n"
            "Show a correct best-practice code block (labeled 'DO: Best Practice') and an incorrect/trap code block (labeled 'DON'T / EXAM TRAP'), explaining exactly why the trap fails.\n"
            "After each example, explain what the learner should notice, what would change if one part changed, and why this pattern is preferred in MongoDB."
        )

    return (
        f"{COACH_IDENTITY}\n"
        f"{OUTCOME_GUARDRAILS}\n\n"
        f"MODE: TEACH\n"
        f"Today's topic: **{topic}**\n"
        f"Current subtopic/concept to study: **{subtopic}**\n"
        f"{context_section}\n\n"
        f"{TEACH_SCOPE_RULES}\n"
        f"{TEACH_DEPTH_RULES}\n"
        f"{TEACH_FORMAT_RULES}\n"
        f"{TEACH_TEMPLATE_RULES}\n"
        f"Provide a comprehensive explanation that helps the learner both understand and remember **{subtopic}** for the exam.\n"
        f"Your teaching must work for developers of any level, from absolute beginners to advanced engineers.\n"
        f"Start with intuition, then go deep into mechanics, then syntax, then exam recall.\n"
        f"Do not preload later-topic material. If a later-topic idea would help, name it only as deferred context and move back to the current concept.\n"
        f"Keep the pacing clean: short paragraphs, bullets where useful, and no repetitive filler.\n\n"
        f"Do not give a short summary.\n\n"
        f"You MUST structure your response exactly using these Markdown headers (###):\n\n"
        f"### 1. Core Concept\n"
        f"Explain the idea clearly and thoroughly. Define key terms, underlying mechanics, structural rules, return values, and design choices. Make it understandable without external resources.\n\n"
        f"### 2. Level-Based Breakdown\n"
        f"- *For Beginners*: Start with a clear real-world analogy, then map every part of the analogy back to MongoDB.\n"
        f"- *For Intermediate Learners*: Explain the correct mental model and the most common exam mistake.\n"
        f"- *For Advanced Developers*: {advanced_prompt}\n\n"
        f"{syntax_instructions}\n\n"
        f"### 4. Exam Radar\n"
        f"List 3-5 exam traps or distinctions the learner must notice under pressure. For each one, state what the examiner is trying to test.\n\n"
        f"### 5. Micro-Challenge\n"
        f"Ask one short but high-signal challenge that forces the learner to apply only the current concept. "
        f"Prefer a short open-ended question. Use multiple choice only when it genuinely improves clarity. "
        f"For Topic 1 and other concept-only lessons, ask an open-ended question that names the correct BSON type or document shape and does not use invented type names. "
        f"If you use multiple choice, include 3-4 complete answer choices with full text, labeled A/B/C/D, not bare numbers. "
        f"Do not leave option labels like A/B/C/D without the actual choice text. "
        f"Do not ask a question that requires a later topic or a later-topic method such as CRUD writes, query operators, aggregation stages, filters, updates, or inserts unless that exact syntax is already part of the current concept. "
        f"For Topic 1 and other conceptual topics, stay on BSON type choice, document structure, or schema reasoning only.\n\n"
        f"### 6. 30-Second Recall\n"
        f"End with 3-5 ultra-compact bullets the learner should be able to recall without notes. Keep them bounded to the current concept.\n\n"
        f"CRITICAL RULES:\n"
        f"- You MUST answer STRICTLY based on the Reference material provided above. Do NOT use external web search.\n"
        f"- If the Reference material is missing or does not cover the concept, state: 'This is not covered in my official docs.' and do not make up any content.\n"
        f"- Do NOT invent invalid-syntax traps. For example, quoted field names containing hyphens are not automatically invalid in MongoDB; only call something invalid when the reference material supports that exact claim.\n"
        f"- Prefer documented exam traps: BSON type choice, `_id` behavior, flexible document structure, array matching semantics, dot notation, and Shell vs PyMongo syntax differences.\n"
        f"- Do not answer your own Micro-Challenge inside the lesson. The Micro-Challenge section must contain only the challenge prompt and nothing else.\n"
        f"- Do not include an answer, solution, hint, or example response directly under the Micro-Challenge heading.\n"
        f"- If the challenge is multiple choice, each option must be a full text choice, not just a letter.\n"
        f"- Whenever syntax appears, explain what each operator, parameter, and method call does.\n"
        f"- Use beautiful markdown formatting, tables when helpful, and properly fenced code blocks.\n"
        f"- CRITICAL FORMATTING: All text, headings, list items, and code blocks must be strictly left-aligned standard Markdown. Do NOT center headers or pad lines with leading spaces.\n"
        f"- End with: 'Type your answer, ask a question, or type practice when ready.'"
    )


def build_followup_prompt(topic: str, subtopic: str, user_question: str, chat_history: list) -> str:
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
        f"MODE: CHECK / CLARIFY\n"
        f"Topic: **{topic}**\n\n"
        f"Current concept: **{subtopic}**\n\n"
        f"{FOLLOWUP_SCOPE_RULES}\n"
        f"Conversation so far:\n{history_str}\n\n"
        f"Student's input: {user_question}\n\n"
        f"CRITICAL MONGODB RULES:\n"
        f"- Answer strictly according to official MongoDB behavior. If you are unsure, say so plainly.\n"
        f"- If a field is an array, querying `{{field: 'value'}}` DOES match documents whose array contains 'value'. Do NOT claim they must use `{{field: ['value']}}` unless they want an exact array match.\n"
        f"{language_rule}\n\n"
        f"RESPONSE BEHAVIOR:\n"
        f"- If the student is answering your Micro-Challenge, first state what they got right, then state the exact gap, code-smell, or casing trap, explain the database engine impact when relevant (for example COLLSCAN penalties or AttributeErrors), and then give the corrected answer in clean, exam-ready syntax.\n"
        f"- If the student asks a question, answer directly with technical precision, then tie it back to the exam signal or common trap.\n"
        f"- If the student asks for more examples, give no more than two and keep them inside the current concept.\n"
        f"- If the student asks about a later topic, refuse to teach it here and briefly defer it to the relevant syllabus node.\n"
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
    """Strict-but-friendly local AI coach."""


    def __init__(self):
        try:
            self._llm = ChatOllama(
                model=MODEL,
                base_url=LOCAL_LLM_URL,
                temperature=0.7,
                num_ctx=STUDY_NUM_CTX,
                reasoning=STUDY_REASONING,
            )
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


    def handle_followup(self, topic: str, subtopic: str, user_question: str, chat_history: list) -> str:
        return self._call(build_followup_prompt(topic, subtopic, user_question, chat_history), temperature=0.5)


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
