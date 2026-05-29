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

GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")
load_dotenv(ENV_PATH)

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

    def explain_topic(self, topic: str, subtopic: str, md_context: str = "") -> str:
        if not md_context.strip():
            md_context = "CRITICAL: No official reference material is loaded for this topic in the syllabus."

        context_section = (
            f"\n\nReference material (use for accuracy):\n```\n{md_context[:2500]}\n```"
            if md_context else ""
        )
        return self._call(
            f"You are CertCoach — an expert MongoDB Certification Instructor.\n\n"
            f"Today's topic: **{topic}**\n"
            f"Current subtopic: **{subtopic}**\n"
            f"{context_section}\n\n"
            f"Teach this specific subtopic to a developer preparing for the MongoDB Associate Developer Exam.\n\n"
            f"Keep it bite-sized. Structure your response exactly like this:\n"
            f"1. **Concept**: A concise explanation (2-3 sentences).\n"
            f"2. **Example**: A brief MongoDB Shell code example.\n"
            f"3. **Micro-Challenge**: Ask a quick 1-question challenge related to this specific subtopic that they can answer in the chat.\n\n"
            f"CRITICAL RULES:\n"
            f"- You MUST answer STRICTLY based on the Reference material provided above. Do NOT use external web search.\n"
            f"- If the Reference material is missing or does not cover the concept, state: 'This is not covered in my official docs.' and do not make up any content.\n"
            f"- Be conversational and focused. No padding.\n"
            f"- End with: 'Type your answer or ask any questions.'",
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
            f"- You MUST answer STRICTLY based on official MongoDB best practices. If you don't know, say so.\n"
            f"- If a field is an array, querying `{{field: 'value'}}` DOES return documents where the array contains 'value'. Do NOT tell the student they need to wrap it in an array like `{{field: ['value']}}` unless they are looking for an exact array match.\n\n"
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
