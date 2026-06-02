import os
import sys
from dotenv import load_dotenv

# Add src to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import List

# Load env
GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")
load_dotenv(ENV_PATH)

MODEL = os.getenv("MODEL", "qwen2.5-coder:7b")
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")

class CertCoachMCQ(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    feedbacks: List[str]
    trap_analysis: str
    six_part_explanation: str
    citation_source: str

print(f"Testing ChatOllama directly...")
print(f"Model: {MODEL}")
print(f"URL: {LOCAL_LLM_URL}")

llm = ChatOllama(model=MODEL, base_url=LOCAL_LLM_URL, temperature=0.5, timeout=120.0, num_ctx=4096)
structured_llm = llm.with_structured_output(CertCoachMCQ)

prompt = "Generate a multiple choice question about MongoDB BSON Data Types."

try:
    print("Invoking structured LLM...")
    res = structured_llm.invoke(prompt)
    print("SUCCESS!")
    print(f"Response: {res}")
except Exception as e:
    print(f"FAILED WITH EXCEPTION: {e}")
    import traceback
    traceback.print_exc()
