"""
CertCoach Persona
==================
Single model: gemma4:e4b — used for all teaching, feedback, and Q&A tasks.
"""
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL", "gemma4:e4b")
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")


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

    def explain_topic(self, topic: str, subtopics: list, md_context: str = "") -> str:
        subtopics_str = "\n".join(f"  - {s}" for s in subtopics)
        context_section = (
            f"\n\nReference material (use for accuracy):\n```\n{md_context[:25000]}\n```"
            if md_context else ""
        )
        return self._call(
            f"You are CertCoach — an expert MongoDB Certification Instructor.\n\n"
            f"Today's topic: **{topic}**\n"
            f"Key subtopics:\n{subtopics_str}"
            f"{context_section}\n\n"
            f"Teach this to a developer preparing for the MongoDB Associate Developer Exam.\n\n"
            f"Structure:\n"
            f"Please separate each of the following sections with exactly '---CHUNK---' on its own line.\n"
            f"1. **Core Concept & Importance** — 2 sentences on why it matters and what it is.\n"
            f"---CHUNK---\n"
            f"2. **Scenarios & Examples** — Provide 2 distinct real-world scenarios with MongoDB Shell code blocks and detailed explanations for each.\n"
            f"---CHUNK---\n"
            f"3. **Exam Traps** — 1-2 common gotchas candidates fall for.\n"
            f"---CHUNK---\n"
            f"4. **Interactive Practice Question** — Ask an open-ended mini-scenario question for the student to solve right now in the chat. End with: 'Type your answer, ask any questions, or type practice when you are ready for MCQs.'\n\n"
            f"CRITICAL RULES:\n"
            f"- Do not hallucinate array queries. In MongoDB, querying `{{tags: 'tech'}}` DOES match arrays containing 'tech'. Querying `{{tags: ['tech']}}` matches an exact array of just 'tech'.\n"
            f"Be conversational and focused. No padding.",
            temperature=0.4
        )

    def handle_followup(self, topic: str, user_question: str, chat_history: list) -> str:
        history_str = "\n".join(
            f"{'Student' if m['role'] == 'user' else 'CertCoach'}: {m['content']}"
            for m in chat_history[-6:]
        )
        return self._call(
            f"You are CertCoach — a strict-but-warm MongoDB Certification Instructor.\n"
            f"Topic: **{topic}**\n\n"
            f"Conversation so far:\n{history_str}\n\n"
            f"Student's input: {user_question}\n\n"
            f"CRITICAL MONGODB RULES:\n"
            f"- If a field is an array, querying `{{field: 'value'}}` DOES return documents where the array contains 'value'. Do NOT tell the student they need to wrap it in an array like `{{field: ['value']}}` unless they are looking for an exact array match.\n\n"
            f"If the student is answering your interactive practice question, evaluate their MongoDB syntax, correct them if needed, and praise them if right.\n"
            f"If they ask a question, answer clearly and concisely.\n"
            f"End with a short follow-up like 'Does that clear it up?' or ask if they are ready to type 'practice' for the MCQs.",
            temperature=0.5
        )

    def handle_free_chat(self, user_input: str, chat_history: list) -> str:
        history_str = "\n".join(
            f"{'Student' if m['role'] == 'user' else 'CertCoach'}: {m['content']}"
            for m in chat_history[-6:]
        )
        return self._call(
            f"You are CertCoach — a strict-but-warm MongoDB Certification Instructor.\n"
            f"The student is chatting with you in an open-ended session.\n\n"
            f"Conversation so far:\n{history_str}\n\n"
            f"Student says: {user_input}\n\n"
            f"Respond conversationally. If they ask a MongoDB question, answer it. "
            f"If they ask for study advice, give it. Be concise, use markdown.",
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
            f"Firm and constructive — never harsh.",
            temperature=0.6
        )
