import os
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import json
import requests
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

# LangChain structured execution
from langchain_ollama import ChatOllama
from retriever import CertCoachRetriever

# Load configs
load_dotenv()

# Single model for all tasks
MODEL = os.getenv("MODEL", "gemma4:e4b")
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")


# 1. Define strict output schema using Pydantic
class CertCoachMCQ(BaseModel):
    question: str = Field(description="The multiple choice question based strictly on the provided context.")
    options: List[str] = Field(description="List of 4 possible answers. Include at least one 'gotcha' trap option.")
    correct_answer: str = Field(description="The matching correct string from the options list.")
    explanation: str = Field(description="Why the answer is correct and why the others are wrong.")
    trap_analysis: str = Field(description="Explicitly explain which option is the 'trap' and why a student might fall for it.", default="No specific trap.")
    citation_source: str = Field(description="The exact source file name provided in the context metadata.")

def _call_ollama_cloud(prompt: str) -> Optional[str]:
    """Calls the Ollama Cloud API directly using requests + Bearer auth."""
    headers = {
        "Authorization": f"Bearer {OLLAMA_CLOUD_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build strict JSON generation prompt
    schema_hint = json.dumps({
        "question": "string",
        "options": ["string", "string", "string", "string"],
        "correct_answer": "string",
        "explanation": "string",
        "trap_analysis": "string",
        "citation_source": "string"
    }, indent=2)
    
    full_prompt = f"""{prompt}

You MUST respond with ONLY a valid JSON object matching this exact schema (no markdown, no extra text):
{schema_hint}
"""
    

def _parse_mcq_from_text(raw_text: str) -> Optional[CertCoachMCQ]:
    """Attempts to extract a valid CertCoachMCQ from raw LLM text."""
    # Strip any markdown fencing
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    
    # Find JSON object boundaries
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        return None
    
    try:
        data = json.loads(text[start:end])
        return CertCoachMCQ(**data)
    except Exception:
        return None

def generate_quiz_for_topic(topic: str) -> Optional[CertCoachMCQ]:
    print(f"--- Generating CertCoach MCQ for: {topic} ---")
    
    # 2. Retrieve Vector context
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../chroma_db"))
    retriever = CertCoachRetriever(db_path)
    
    raw_chunks = retriever.retrieve_chunks(topic, k=10)
    top_chunks = retriever.openrouter_rerank(topic, raw_chunks, top_n=3)
    
    if not top_chunks:
        print("❌ Error: No context retrieved from Vector Database.")
        return None

    # Build context prompt
    context_body = ""
    for idx, c in enumerate(top_chunks):
        context_body += f"\n[Source: {c['source']}]\n{c['content']}\n"

    prompt = f"""You are an expert MongoDB Certification Instructor. Based ONLY on the following 
MongoDB documentation Context, generate a hyper-accurate Multiple Choice Question 
for the "MongoDB Associate Python Developer" exam.

Constraints:
1. NEVER make up answers not found in the context.
2. Ensure the citation_source exactly matches the [Source: ...] tag above the text you used.
3. Intentionally generate at least one "gotcha" or "trap" option that looks very similar to the correct answer but has a subtle syntax or logic error common in MongoDB.
4. Fill out the `trap_analysis` field explaining exactly why that trap option is tricky.

CONTEXT:
{context_body}"""

    # Use gemma4:e4b for structured question generation
    print(f"🧠 Generating with local {MODEL}...")
    try:
        llm = ChatOllama(model=MODEL, base_url=LOCAL_LLM_URL, temperature=0.2)
        structured_llm = llm.with_structured_output(CertCoachMCQ)
        mcq_result = structured_llm.invoke(prompt)
        print("✅ Question generated successfully.")
        return mcq_result
    except Exception as e:
        print(f"❌ Question generation failed: {e}")
        return None

if __name__ == "__main__":
    res = generate_quiz_for_topic("MongoDB CRUD Insert Operations")
    if res:
        print(f"\n✅ Success! Q: {res.question}")
