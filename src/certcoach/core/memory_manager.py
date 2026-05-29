import os
import json
from datetime import datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(_HERE, "../data"))
CHAT_LOGS_DIR = os.path.join(DATA_DIR, "chat_logs")
BRAIN_FILE = os.path.join(CHAT_LOGS_DIR, "MongoDB_Brain.md")
HISTORY_FILE = os.path.join(CHAT_LOGS_DIR, "active_history.json")

# Keep the last 15 messages (user + assistant) in active context to avoid overflowing LLM limits.
MAX_ACTIVE_MESSAGES = 15

def init_memory():
    if not os.path.exists(CHAT_LOGS_DIR):
        os.makedirs(CHAT_LOGS_DIR)
        
    if not os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, "w", encoding="utf-8") as f:
            f.write("# 🧠 MongoDB Brain\n\n")
            f.write("This document contains your entire conversation history with CertCoach. "
                    "Use it to review past explanations, questions, and insights.\n\n---\n")

def log_interaction(role: str, content: str):
    """
    Appends to the Markdown Brain and updates the rolling JSON history.
    role: 'user' or 'assistant'
    """
    init_memory()
    
    # 1. Append to Markdown Brain
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(BRAIN_FILE, "a", encoding="utf-8") as f:
        if role == "user":
            f.write(f"\n### 🧑 You ({timestamp})\n")
            f.write(f"{content}\n")
        else:
            f.write(f"\n### 🤖 CertCoach ({timestamp})\n")
            f.write(f"{content}\n")
            f.write("\n---\n")

    # 2. Update Active JSON History
    history = load_active_history()
    history.append({"role": role, "content": content})
    
    # Enforce rolling window
    if len(history) > MAX_ACTIVE_MESSAGES:
        # Keep the most recent MAX_ACTIVE_MESSAGES
        history = history[-MAX_ACTIVE_MESSAGES:]
        
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def load_active_history() -> list:
    """Returns the rolling window of the last N messages."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []
