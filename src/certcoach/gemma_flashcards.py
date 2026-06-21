import os
import sys
import re
import json
import random
import threading
import urllib.request
import urllib.error
import tkinter as tk
from tkinter import ttk, messagebox

# Fallback config loaders if imported outside the certcoach package context
try:
    from certcoach.core import database, planner
    from certcoach.core.config import get_local_llm_url, get_population_model
    from certcoach.core.bank_state import canonical_status
    HAS_CERTCOACH = True
except ImportError:
    HAS_CERTCOACH = False
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

SYLLABUS_TOPICS = [
    "Topic 1: MongoDB Overview & The Document Model",
    "Topic 2: CRUD Operations - Create",
    "Topic 3: CRUD Operations - Read",
    "Topic 4: CRUD Operations - Update",
    "Topic 5: CRUD Operations - Delete",
    "Topic 6: Query Operators & MQL",
    "Topic 7: Querying Arrays & Embedded Documents",
    "Topic 8: Aggregation Framework",
    "Topic 9: Indexes & Performance",
    "Topic 10: Data Modeling",
    "Topic 11: MongoDB Drivers & PyMongo",
    "Topic 12: Tools, Tooling & Atlas Search"
]

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
        self.root.title("🧠 MongoGemma Flashcards & Study Companion")
        self.root.geometry("900x700")
        self.root.minsize(750, 550)
        
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
        
        # DB Bank State
        self.db_questions = []
        self.seen_db_ids = set()
        
        # Setup Styles & Notebook
        self.setup_styles()
        self.build_tabs()
        
        # Initial Loads
        self.detect_ollama_and_models()
        self.load_cheat_sheet_by_domain()

    def setup_styles(self):
        self.style = ttk.Style(master=self.root)
        self.style.theme_use("clam")
        
        # Configure frames and elements
        self.style.configure(".", background=self.bg_color, foreground=self.text_color)
        self.style.configure("TFrame", background=self.bg_color)
        
        # Notebook Tab Styling
        self.style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.border_color, foreground=self.text_color, font=("Segoe UI", 9, "bold"), padding=(15, 5))
        self.style.map("TNotebook.Tab", background=[("selected", self.card_bg)], foreground=[("selected", self.accent_cyan)])
        
        # ComboBox Styling
        self.style.configure("TCombobox", fieldbackground=self.card_bg, background=self.border_color, foreground=self.text_color)
        
        # Buttons Styling
        self.style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), background=self.border_color, foreground=self.text_color)
        self.style.map("Action.TButton",
            background=[("active", "#585b70"), ("disabled", "#313244")],
            foreground=[("disabled", "#585b70")]
        )

    def build_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        # Tab 1: Flashcards
        self.flashcard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.flashcard_tab, text="🃏 Flashcards Review")
        self.build_flashcard_ui(self.flashcard_tab)
        
        # Tab 2: Cheat Sheets
        self.cheatsheet_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cheatsheet_tab, text="📖 Study Guide & Traps")
        self.build_cheatsheet_ui(self.cheatsheet_tab)
        
        # Status Bar
        self.status_lbl = tk.Label(
            self.root, 
            text="Status: Initializing...", 
            font=("Segoe UI", 9, "italic"), 
            bg=self.bg_color, 
            fg=self.status_dim, 
            anchor="w"
        )
        self.status_lbl.pack(fill=tk.X, side=tk.BOTTOM, padx=25, pady=(5, 5))

    def build_flashcard_ui(self, parent):
        # Top Config Bar
        config_frame = ttk.Frame(parent, padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Domain Selector
        domain_lbl = ttk.Label(config_frame, text="Domain:", font=("Segoe UI", 10, "bold"), background=self.bg_color, foreground=self.accent_cyan)
        domain_lbl.pack(side=tk.LEFT, padx=5)
        
        self.domain_var = tk.StringVar(master=self.root, value="All Domains Combined (Default)")
        self.domain_combo = ttk.Combobox(
            config_frame, 
            textvariable=self.domain_var, 
            values=list(DOMAINS.keys()), 
            state="readonly",
            width=35
        )
        self.domain_combo.pack(side=tk.LEFT, padx=5)
        self.domain_combo.bind("<<ComboboxSelected>>", self.on_domain_changed)
        
        # Source Selector
        source_lbl = ttk.Label(config_frame, text="Source:", font=("Segoe UI", 10, "bold"), background=self.bg_color, foreground=self.accent_cyan)
        source_lbl.pack(side=tk.LEFT, padx=(15, 5))
        
        self.source_var = tk.StringVar(master=self.root, value="CertCoach Database (Default)" if HAS_CERTCOACH else "Local LLM Generator")
        self.source_combo = ttk.Combobox(
            config_frame,
            textvariable=self.source_var,
            values=["CertCoach Database (Default)", "Local LLM Generator"] if HAS_CERTCOACH else ["Local LLM Generator"],
            state="readonly",
            width=23
        )
        self.source_combo.pack(side=tk.LEFT, padx=5)
        self.source_combo.bind("<<ComboboxSelected>>", self.on_source_changed)
        
        # Model Selector
        self.model_lbl = ttk.Label(config_frame, text="Model:", font=("Segoe UI", 10, "bold"), background=self.bg_color, foreground=self.accent_cyan)
        self.model_lbl.pack(side=tk.LEFT, padx=(15, 5))
        
        self.model_var = tk.StringVar(master=self.root, value=self.configured_model)
        self.model_combo = ttk.Combobox(
            config_frame,
            textvariable=self.model_var,
            state="readonly",
            width=12
        )
        self.model_combo.pack(side=tk.LEFT, padx=5)
        
        # Flashcard Area
        self.card_frame = tk.Frame(parent, bg=self.card_bg, bd=1, relief="solid", highlightbackground=self.border_color, highlightcolor=self.border_color)
        self.card_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Category label inside card
        self.category_lbl = tk.Label(
            self.card_frame, 
            text="[Choose a Domain and click Next Card]", 
            font=("Segoe UI", 11, "bold"), 
            bg=self.card_bg, 
            fg=self.accent_cyan,
            anchor="w"
        )
        self.category_lbl.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        # Question Text Area
        q_frame = tk.Frame(self.card_frame, bg=self.card_bg)
        q_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        q_title = tk.Label(q_frame, text="QUESTION CARD", font=("Segoe UI", 9, "bold"), bg=self.card_bg, fg=self.status_dim, anchor="w")
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
        self.sep_line.pack(fill=tk.X, padx=15, pady=5)
        
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
        self.q_text.insert(tk.END, "Your flashcard question will appear here when you click Next Card.")
        self.q_text.configure(state=tk.DISABLED)
        self.a_text.configure(state=tk.DISABLED)
        
        # Controls Frame
        controls_frame = ttk.Frame(parent, padding=10)
        controls_frame.pack(fill=tk.X, padx=15, pady=5)
        
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
        
        # Trigger source change update
        self.on_source_changed(None)

    def build_cheatsheet_ui(self, parent):
        # Top toolbar
        toolbar = ttk.Frame(parent, padding=10)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        topic_lbl = ttk.Label(toolbar, text="Select Syllabus Topic:", font=("Segoe UI", 10, "bold"), background=self.bg_color, foreground=self.accent_cyan)
        topic_lbl.pack(side=tk.LEFT, padx=5)
        
        self.topic_var = tk.StringVar(master=self.root, value=SYLLABUS_TOPICS[0])
        self.topic_combo = ttk.Combobox(
            toolbar,
            textvariable=self.topic_var,
            values=SYLLABUS_TOPICS,
            state="readonly",
            width=50
        )
        self.topic_combo.pack(side=tk.LEFT, padx=5)
        self.topic_combo.bind("<<ComboboxSelected>>", self.on_topic_combo_changed)
        
        # Content Box
        cs_frame = tk.Frame(parent, bg=self.card_bg, bd=1, relief="solid", highlightbackground=self.border_color, highlightcolor=self.border_color)
        cs_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        self.cs_text = tk.Text(
            cs_frame,
            bg=self.card_bg,
            fg=self.text_color,
            insertbackground=self.accent_cyan,
            font=("Consolas", 11),
            bd=0,
            highlightthickness=0,
            wrap=tk.WORD
        )
        self.cs_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        cs_scroll = ttk.Scrollbar(cs_frame, command=self.cs_text.yview)
        cs_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.cs_text.configure(yscrollcommand=cs_scroll.set)

    def on_source_changed(self, event):
        source = self.source_var.get()
        if "Database" in source:
            self.model_combo.configure(state="disabled")
        else:
            self.model_combo.configure(state="readonly")

    def on_domain_changed(self, event):
        self.load_cheat_sheet_by_domain()

    def on_topic_combo_changed(self, event):
        # Manually load the selected topic cheat sheet
        topic_str = self.topic_var.get()
        match = re.match(r"^Topic (\d+)", topic_str)
        if match:
            topic_id = int(match.group(1))
            self.display_cheat_sheet_file(topic_id)

    def load_cheat_sheet_by_domain(self):
        domain = self.domain_var.get()
        
        # Maps domain choices to representative Topic IDs for Cheat Sheets
        domain_to_topic = {
            "All Domains Combined (Default)": 1,
            "CRUD Operations & PyMongo Syntax": 2,
            "Indexing & Performance (ESR, COLLSCAN vs IXSCAN)": 9,
            "Aggregation Framework Pipelines": 8,
            "Data Modeling Patterns & Limits": 10
        }
        
        topic_id = domain_to_topic.get(domain, 1)
        # Select matching topic in dropdown
        for topic_str in SYLLABUS_TOPICS:
            if topic_str.startswith(f"Topic {topic_id}:"):
                self.topic_var.set(topic_str)
                break
                
        self.display_cheat_sheet_file(topic_id)

    def display_cheat_sheet_file(self, topic_id):
        self.cs_text.configure(state=tk.NORMAL)
        self.cs_text.delete("1.0", tk.END)
        
        if not HAS_CERTCOACH:
            self.cs_text.insert(tk.END, "Syllabus files are only available when running inside the CertCoach project environment.")
            self.cs_text.configure(state=tk.DISABLED)
            return
            
        filename = f"topic_{topic_id:02d}_benchmark.md"
        filepath = os.path.join(planner.MEMORY_DIR, filename)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.cs_text.insert(tk.END, content)
            except Exception as e:
                self.cs_text.insert(tk.END, f"Error loading cheat sheet file: {e}")
        else:
            self.cs_text.insert(tk.END, f"Cheat sheet record not found at: {filepath}\n\nMake sure the topic benchmark has been generated.")
            
        self.cs_text.configure(state=tk.DISABLED)
        # Scroll to top
        self.cs_text.see("1.0")

    def detect_ollama_and_models(self):
        def task():
            self.update_status("Detecting local Ollama service...")
            try:
                req = urllib.request.Request(f"{self.ollama_url}/api/tags")
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode("utf-8"))
                    self.models_list = [m["name"] for m in data.get("models", [])]
                    
                if self.models_list:
                    self.model_combo.configure(values=self.models_list)
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
            except Exception:
                self.update_status("Status: Connected (Local DB only, LLM offline).")
        
        threading.Thread(target=task, daemon=True).start()

    def update_status(self, text):
        self.root.after(0, lambda: self.status_lbl.configure(text=text))

    def set_loading_state(self, is_loading):
        self.loading = is_loading
        if is_loading:
            self.next_btn.configure(state=tk.DISABLED, bg=self.border_color)
            self.show_btn.configure(state=tk.DISABLED)
            self.domain_combo.configure(state="disabled")
            self.source_combo.configure(state="disabled")
            self.model_combo.configure(state="disabled")
        else:
            self.next_btn.configure(state=tk.NORMAL, bg=self.green_btn)
            self.domain_combo.configure(state="readonly")
            self.source_combo.configure(state="readonly")
            self.on_source_changed(None)

    def fetch_next_card(self):
        if self.loading:
            return
            
        source = self.source_var.get()
        domain = self.domain_var.get()
        
        self.set_loading_state(True)
        
        # Clear fields
        self.category_lbl.configure(text="[Loading next card...]")
        self.q_text.configure(state=tk.NORMAL)
        self.q_text.delete("1.0", tk.END)
        self.q_text.insert(tk.END, "Retrieving/Generating card details...")
        self.q_text.configure(state=tk.DISABLED)
        
        self.a_text.configure(state=tk.NORMAL)
        self.a_text.delete("1.0", tk.END)
        self.a_text.configure(state=tk.DISABLED)
        self.a_title.configure(text="ANSWER & EXPLANATION (HIDDEN)")

        if "Database" in source:
            self.update_status(f"Loading question from CertCoach database for '{domain}'...")
            threading.Thread(target=self.task_load_db_card, args=(domain,), daemon=True).start()
        else:
            model = self.model_var.get()
            self.update_status(f"[Gemma is thinking...] Generating card for '{domain}'...")
            threading.Thread(target=self.task_generate_llm_card, args=(domain, model), daemon=True).start()

    def task_load_db_card(self, domain):
        try:
            if not HAS_CERTCOACH:
                raise ImportError("CertCoach environment not loaded.")
                
            database.check_connection()
            all_questions = list(database.questions_col.find({}))
            active_questions = [q for q in all_questions if canonical_status(q) == "active"]
            
            # Filter based on domain selection
            if domain == "CRUD Operations & PyMongo Syntax":
                active_questions = [q for q in active_questions if q.get("metadata", {}).get("topic_id") in {2, 3, 4, 5, 11}]
            elif domain == "Indexing & Performance (ESR, COLLSCAN vs IXSCAN)":
                active_questions = [q for q in active_questions if q.get("metadata", {}).get("topic_id") == 9]
            elif domain == "Aggregation Framework Pipelines":
                active_questions = [q for q in active_questions if q.get("metadata", {}).get("topic_id") == 8]
            elif domain == "Data Modeling Patterns & Limits":
                active_questions = [q for q in active_questions if q.get("metadata", {}).get("topic_id") == 10]
                
            if not active_questions:
                self.update_status("Status: No active questions in domain.")
                self.root.after(0, lambda: messagebox.showwarning(
                    "Database Study Gate",
                    f"No active questions found in the '{domain}' domain.\n"
                    "Please run repair or population runs to make this topic ready."
                ))
                self.root.after(0, self.on_card_failed)
                return
                
            # Filter out seen questions
            unseen = [q for q in active_questions if q["_id"] not in self.seen_db_ids]
            if not unseen:
                # Loop seen questions if all have been viewed
                self.seen_db_ids.clear()
                unseen = active_questions
                
            selected = random.choice(unseen)
            self.seen_db_ids.add(selected["_id"])
            
            # Format to Card JSON contract
            meta = selected.get("metadata", {})
            cat_label = f"Topic {meta.get('topic_id')} | {meta.get('concept')} ({meta.get('difficulty')})"
            
            # Format Options
            options_text = []
            correct_text = ""
            for opt in selected.get("options", []):
                letter = opt.get("option_letter")
                snippet = opt.get("code_snippet", "")
                text = opt.get("text", "")
                val = f"{snippet} {text}".strip()
                options_text.append(f"  {letter}) {val}")
                
                if opt.get("is_correct"):
                    correct_text = f"{letter}) {val}"
            
            q_formatted = selected.get("question_text", "")
            if options_text:
                q_formatted += "\n\nOptions:\n" + "\n".join(options_text)
                
            a_formatted = f"Correct Answer: {correct_text}\n\nExplanation:\n{selected.get('explanation', '')}"
            
            self.current_card = {
                "category": cat_label,
                "question": q_formatted,
                "answer": a_formatted
            }
            self.root.after(0, self.on_card_loaded)
        except Exception as e:
            self.update_status("Status: DB connection error.")
            self.root.after(0, lambda: messagebox.showerror(
                "Database Offline",
                f"Failed to query MongoDB: {e}\n\nVerify connection string in ~/.certcoach/.env."
            ))
            self.root.after(0, self.on_card_failed)

    def task_generate_llm_card(self, domain, model):
        domain_desc = DOMAINS.get(domain, "")
        prompt = PROMPT_TEMPLATE.format(domain_focus=domain, domain_desc=domain_desc)
        
        data = {
            "model": model,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.6}
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
                
                card = json.loads(raw_response)
                if not isinstance(card, dict) or "question" not in card or "answer" not in card:
                    raise ValueError("JSON response missing required keys.")
                    
                self.current_card = card
                self.root.after(0, self.on_card_loaded)
        except Exception as e:
            self.update_status("Status: LLM Generation failed.")
            self.root.after(0, lambda: self.on_generation_fallback(e))
            self.root.after(0, self.on_card_failed)

    def on_card_loaded(self):
        self.set_loading_state(False)
        self.update_status("[Card Loaded] Ready for study review.")
        
        card = self.current_card
        self.category_lbl.configure(text=f"📂 {card.get('category', 'Syllabus Topic')}")
        
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
        fallback_card = {
            "category": "Parsing Fail / Fallback",
            "question": f"Ollama model generated a malformed JSON response or failed to respond. \n\nDetails:\n{error}\n\nPlease click [Next Card] to generate a new card.",
            "answer": "Make sure your Ollama service is functioning and has the model pulled."
        }
        self.current_card = fallback_card
        self.on_card_loaded()

    def show_answer(self):
        if not self.current_card:
            return
        
        # Show text
        self.a_title.configure(text="ANSWER & EXPLANATION")
        self.a_text.configure(state=tk.NORMAL)
        self.a_text.see("1.0")
        
        # Disable show button
        self.show_btn.configure(state=tk.DISABLED, bg=self.border_color, fg=self.text_color)
        self.update_status("[Answer Revealed] Done. Click Next Card to load another card.")

def main():
    root = tk.Tk()
    app = FlashcardsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
