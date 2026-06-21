import os
import sys
import re
import json
import threading
import urllib.request
import urllib.error
import tkinter as tk
from tkinter import ttk, messagebox

# Fallback config loaders if imported outside the certcoach package context
try:
    from certcoach.core.config import get_local_llm_url, get_population_model
except ImportError:
    def get_local_llm_url():
        return os.getenv("LOCAL_LLM_URL", "http://localhost:11434")
    def get_population_model():
        return os.getenv("POPULATION_MODEL", "gemma4")

DOMAINS = {
    "All Domains Combined (Default)": "All C100DEV certification domains including CRUD, indexing, PyMongo, aggregation, and data modeling",
    "CRUD Operations & PyMongo Syntax": "PyMongo connection, MongoClient, CRUD methods (insertOne, insertMany, find, updateOne, updateMany, deleteOne, deleteMany), query operators, and casing rules",
    "Indexing & Performance (ESR, COLLSCAN vs IXSCAN)": "Single field, compound, multikey indexes, Index selection rules (Equality, Sort, Range), explain() output, COLLSCAN vs IXSCAN, executionStats, and index limits",
    "Aggregation Framework Pipelines": "Aggregation pipeline stages ($match, $group, $project, $sort, $limit, $lookup, $out, $unwind, $addFields) and aggregation syntax in PyMongo",
    "Data Modeling Patterns & Limits": "Document schema design, embedding vs referencing, one-to-many patterns, anti-patterns (unbounded arrays), 16MB document limit, and schema flexibility benefits"
}

PROMPT_TEMPLATE = """
You are an expert MongoDB Certification Lead preparer (C100DEV).
Generate one high-signal, exam-grade study flashcard for the MongoDB Certified Professional Python Developer Associate exam.
Target Exam Domain: {domain_focus}
Detailed guidelines: {domain_desc}

You MUST return a JSON object with exactly the following keys, and nothing else (no wrapping, no text before or after the JSON):
{{
  "category": "The target exam domain classification",
  "question": "A clear, technically accurate question or scenario targeting a common exam trap, syntax rule, or performance behavior. Include code blocks where helpful.",
  "answer": "The correct answer, clean PyMongo/mongosh code blocks, and a detailed explanation of the rules, traps, and performance details."
}}

Guidelines:
1. Focus heavily on Python / PyMongo syntax, correct casing (camelCase vs snake_case), indexing rules (ESR, COLLSCAN), aggregation pipeline stages ($match, $group), or data modeling patterns.
2. Ensure all code blocks in the question and answer are clearly written.
3. Be 100% technically correct. Do not invent syntax or options.
4. Keep the question challenging and exam-relevant.
"""

class FlashcardsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 MongoGemma Flashcards")
        self.root.geometry("850x650")
        self.root.minsize(700, 500)
        
        # Colors
        self.bg_color = "#1e1e2e"
        self.card_bg = "#252538"
        self.text_color = "#cdd6f4"
        self.accent_cyan = "#89dceb"
        self.green_btn = "#a6e3a1"
        self.red_btn = "#f38ba8"
        self.border_color = "#45475a"
        self.status_dim = "#7f849c"
        
        self.root.configure(bg=self.bg_color)
        
        # App State
        self.ollama_url = get_local_llm_url()
        self.configured_model = get_population_model()
        self.models_list = []
        self.current_card = None
        self.loading = False
        
        # Setup Styles
        self.setup_styles()
        
        # Build UI
        self.build_ui()
        
        # Check Ollama and fetch models
        self.detect_ollama_and_models()

    def setup_styles(self):
        self.style = ttk.Style(master=self.root)
        self.style.theme_use("clam")
        
        # Configure frames and elements
        self.style.configure(".", background=self.bg_color, foreground=self.text_color)
        self.style.configure("TFrame", background=self.bg_color)
        
        # Card Frame Style
        self.style.configure("Card.TFrame", background=self.card_bg, borderwidth=1, relief="solid")
        
        # ComboBox Styling
        self.style.configure("TCombobox", fieldbackground=self.card_bg, background=self.border_color, foreground=self.text_color)
        
        # Buttons Styling
        self.style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), background=self.border_color, foreground=self.text_color)
        self.style.map("Action.TButton",
            background=[("active", "#585b70"), ("disabled", "#313244")],
            foreground=[("disabled", "#585b70")]
        )

    def build_ui(self):
        # Top Config Bar
        config_frame = ttk.Frame(self.root, padding=10)
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Domain Selector
        domain_lbl = ttk.Label(config_frame, text="Select Domain:", font=("Segoe UI", 10, "bold"), background=self.bg_color, foreground=self.accent_cyan)
        domain_lbl.pack(side=tk.LEFT, padx=5)
        
        self.domain_var = tk.StringVar(master=self.root, value="All Domains Combined (Default)")
        self.domain_combo = ttk.Combobox(
            config_frame, 
            textvariable=self.domain_var, 
            values=list(DOMAINS.keys()), 
            state="readonly",
            width=40
        )
        self.domain_combo.pack(side=tk.LEFT, padx=5)
        
        # Model Selector
        model_lbl = ttk.Label(config_frame, text="Model:", font=("Segoe UI", 10, "bold"), background=self.bg_color, foreground=self.accent_cyan)
        model_lbl.pack(side=tk.LEFT, padx=(20, 5))
        
        self.model_var = tk.StringVar(master=self.root, value=self.configured_model)
        self.model_combo = ttk.Combobox(
            config_frame,
            textvariable=self.model_var,
            state="normal",
            width=15
        )
        self.model_combo.pack(side=tk.LEFT, padx=5)
        
        # Flashcard Area
        self.card_frame = tk.Frame(self.root, bg=self.card_bg, bd=1, relief="solid", highlightbackground=self.border_color, highlightcolor=self.border_color)
        self.card_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        
        # Category label inside card
        self.category_lbl = tk.Label(
            self.card_frame, 
            text="[Select a domain and click Next Card]", 
            font=("Segoe UI", 11, "bold"), 
            bg=self.card_bg, 
            fg=self.accent_cyan,
            anchor="w"
        )
        self.category_lbl.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        # Question Text Area
        q_frame = tk.Frame(self.card_frame, bg=self.card_bg)
        q_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        q_title = tk.Label(q_frame, text="QUESTION", font=("Segoe UI", 9, "bold"), bg=self.card_bg, fg=self.status_dim, anchor="w")
        q_title.pack(fill=tk.X)
        
        self.q_text = tk.Text(
            q_frame, 
            bg=self.card_bg, 
            fg=self.text_color, 
            insertbackground=self.accent_cyan,
            font=("Consolas", 11),
            bd=0,
            highlightthickness=0,
            wrap=tk.WORD
        )
        self.q_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        
        q_scroll = ttk.Scrollbar(q_frame, command=self.q_text.yview)
        q_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.q_text.configure(yscrollcommand=q_scroll.set)
        
        # Separator line
        self.sep_line = tk.Frame(self.card_frame, height=2, bg=self.border_color)
        self.sep_line.pack(fill=tk.X, padx=15, pady=10)
        
        # Answer Text Area
        a_frame = tk.Frame(self.card_frame, bg=self.card_bg)
        a_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        self.a_title = tk.Label(a_frame, text="ANSWER & EXPLANATION (HIDDEN)", font=("Segoe UI", 9, "bold"), bg=self.card_bg, fg=self.status_dim, anchor="w")
        self.a_title.pack(fill=tk.X)
        
        self.a_text = tk.Text(
            a_frame, 
            bg=self.card_bg, 
            fg=self.text_color, 
            insertbackground=self.accent_cyan,
            font=("Consolas", 11),
            bd=0,
            highlightthickness=0,
            wrap=tk.WORD
        )
        self.a_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        
        a_scroll = ttk.Scrollbar(a_frame, command=self.a_text.yview)
        a_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.a_text.configure(yscrollcommand=a_scroll.set)
        
        # Initial states
        self.q_text.insert(tk.END, "Your generated question will appear here...")
        self.q_text.configure(state=tk.DISABLED)
        self.a_text.configure(state=tk.DISABLED)
        
        # Controls Frame
        controls_frame = ttk.Frame(self.root, padding=10)
        controls_frame.pack(fill=tk.X, padx=25, pady=10)
        
        # Show Answer Button
        self.show_btn = tk.Button(
            controls_frame, 
            text="👁️ Show Answer", 
            font=("Segoe UI", 10, "bold"), 
            bg=self.border_color, 
            fg=self.text_color,
            activebackground="#585b70",
            activeforeground=self.text_color,
            bd=1,
            relief="flat",
            command=self.show_answer,
            state=tk.DISABLED
        )
        self.show_btn.pack(side=tk.LEFT, padx=5, ipady=5, ipadx=10)
        
        # Next Card Button
        self.next_btn = tk.Button(
            controls_frame, 
            text="➡️ Next Card", 
            font=("Segoe UI", 10, "bold"), 
            bg=self.green_btn, 
            fg=self.bg_color,
            activebackground="#8ef288",
            activeforeground=self.bg_color,
            bd=0,
            command=self.fetch_next_card,
        )
        self.next_btn.pack(side=tk.RIGHT, padx=5, ipady=6, ipadx=15)
        
        # Status Bar
        self.status_lbl = tk.Label(
            self.root, 
            text="Status: Initializing...", 
            font=("Segoe UI", 9, "italic"), 
            bg=self.bg_color, 
            fg=self.status_dim, 
            anchor="w"
        )
        self.status_lbl.pack(fill=tk.X, side=tk.BOTTOM, padx=25, pady=(0, 5))

    def detect_ollama_and_models(self):
        def task():
            self.update_status("Detecting local Ollama service...")
            try:
                # Query tags
                req = urllib.request.Request(f"{self.ollama_url}/api/tags")
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode("utf-8"))
                    self.models_list = [m["name"] for m in data.get("models", [])]
                    
                if self.models_list:
                    self.model_combo.configure(values=self.models_list)
                    # Try to select the gemma4 or configured model
                    default_choice = self.configured_model
                    if default_choice not in self.models_list:
                        gemma_models = [m for m in self.models_list if "gemma" in m]
                        if gemma_models:
                            default_choice = gemma_models[0]
                        else:
                            default_choice = self.models_list[0]
                    
                    self.model_var.set(default_choice)
                    self.update_status("Status: Connected to Ollama.")
                else:
                    self.update_status("Status: Connected, but no models found.")
                    self.root.after(0, lambda: messagebox.showwarning(
                        "Ollama Config Warning",
                        "Connected to Ollama, but no local models are installed.\n"
                        "Please run `ollama pull gemma4` to fetch a compatible study model."
                    ))
            except Exception as e:
                self.update_status("Status: Ollama service offline.")
                self.root.after(0, lambda: messagebox.showerror(
                    "Ollama Connection Error",
                    f"Could not connect to the local Ollama service at {self.ollama_url}.\n\n"
                    "Please verify that the service is running. Run `ollama serve` in your terminal."
                ))
        
        threading.Thread(target=task, daemon=True).start()

    def update_status(self, text):
        self.root.after(0, lambda: self.status_lbl.configure(text=text))

    def set_loading_state(self, is_loading):
        self.loading = is_loading
        if is_loading:
            self.next_btn.configure(state=tk.DISABLED, bg=self.border_color)
            self.show_btn.configure(state=tk.DISABLED)
            self.domain_combo.configure(state="disabled")
            self.model_combo.configure(state="disabled")
        else:
            self.next_btn.configure(state=tk.NORMAL, bg=self.green_btn)
            self.domain_combo.configure(state="readonly")
            self.model_combo.configure(state="normal")

    def fetch_next_card(self):
        if self.loading:
            return
        
        domain = self.domain_var.get()
        model = self.model_var.get()
        
        if not model:
            messagebox.showwarning("Config Warning", "Please select or type an Ollama model name.")
            return
            
        self.set_loading_state(True)
        self.update_status(f"[Gemma is thinking...] Generating question for '{domain}'...")
        
        # Clear fields
        self.category_lbl.configure(text="[Loading next card...]")
        self.q_text.configure(state=tk.NORMAL)
        self.q_text.delete("1.0", tk.END)
        self.q_text.insert(tk.END, "Generating flashcard text, please wait...")
        self.q_text.configure(state=tk.DISABLED)
        
        self.a_text.configure(state=tk.NORMAL)
        self.a_text.delete("1.0", tk.END)
        self.a_text.configure(state=tk.DISABLED)
        self.a_title.configure(text="ANSWER & EXPLANATION (HIDDEN)")
        
        def task():
            domain_desc = DOMAINS.get(domain, "")
            prompt = PROMPT_TEMPLATE.format(domain_focus=domain, domain_desc=domain_desc)
            
            data = {
                "model": model,
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": 0.6
                }
            }
            
            req_body = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                f"{self.ollama_url}/api/generate",
                data=req_body,
                headers={"Content-Type": "application/json"}
            )
            
            try:
                with urllib.request.urlopen(req, timeout=120) as response:
                    resp_body = response.read().decode("utf-8")
                    resp_json = json.loads(resp_body)
                    raw_response = resp_json.get("response", "").strip()
                    
                    # Parse internal JSON
                    card = json.loads(raw_response)
                    
                    if not isinstance(card, dict) or "question" not in card or "answer" not in card:
                        raise ValueError("Ollama response did not contain required JSON fields.")
                        
                    self.current_card = card
                    self.root.after(0, self.on_card_loaded)
            except urllib.error.URLError:
                self.update_status("Status: Connection to Ollama failed.")
                self.root.after(0, lambda: messagebox.showerror(
                    "Ollama Offline",
                    f"Ollama server went offline or failed to respond.\n"
                    "Verify `ollama serve` is running on your computer."
                ))
                self.root.after(0, self.on_card_failed)
            except Exception as e:
                self.update_status("Status: Generation error.")
                self.root.after(0, lambda: self.on_generation_fallback(e))
                self.root.after(0, self.on_card_failed)

        threading.Thread(target=task, daemon=True).start()

    def on_card_loaded(self):
        self.set_loading_state(False)
        self.update_status("[Question Ready] Ready for your answer.")
        
        card = self.current_card
        self.category_lbl.configure(text=f"📂 Category: {card.get('category', 'Syllabus Topic')}")
        
        # Populate question
        self.q_text.configure(state=tk.NORMAL)
        self.q_text.delete("1.0", tk.END)
        self.q_text.insert(tk.END, card.get("question", ""))
        self.q_text.configure(state=tk.DISABLED)
        
        # Prepare hidden answer
        self.a_text.configure(state=tk.NORMAL)
        self.a_text.delete("1.0", tk.END)
        self.a_text.insert(tk.END, card.get("answer", ""))
        self.a_text.configure(state=tk.DISABLED)
        
        # Toggle buttons
        self.show_btn.configure(state=tk.NORMAL, bg=self.accent_cyan, fg=self.bg_color)

    def on_card_failed(self):
        self.set_loading_state(False)
        self.category_lbl.configure(text="[Failed to load card]")
        self.show_btn.configure(state=tk.DISABLED, bg=self.border_color, fg=self.text_color)

    def on_generation_fallback(self, error):
        # Displays a safe fallback warning card
        fallback_card = {
            "category": "Parsing Fail / Fallback",
            "question": f"Ollama model generated a malformed JSON response or failed to respond. \n\nDetails:\n{error}\n\nPlease click [Next Card] to generate a new card.",
            "answer": "Make sure your Ollama service has gemma4 loaded, and is functioning correctly under standard load."
        }
        self.current_card = fallback_card
        self.on_card_loaded()

    def show_answer(self):
        if not self.current_card:
            return
        
        # Show text
        self.a_title.configure(text="ANSWER & EXPLANATION")
        self.a_text.configure(state=tk.NORMAL)
        
        # Apply visual focus/scroll
        self.a_text.see("1.0")
        
        # Disable show button
        self.show_btn.configure(state=tk.DISABLED, bg=self.border_color, fg=self.text_color)
        self.update_status("[Answer Revealed] Done. Click Next Card to generate a new topic.")

def main():
    root = tk.Tk()
    app = FlashcardsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
