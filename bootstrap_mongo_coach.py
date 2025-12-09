import os
from pathlib import Path
import textwrap
import json

BASE_DIR = Path("mongo-coach")

def write_file(path: Path, content: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"Created: {path}")
    else:
        print(f"Exists (skipped): {path}")

def main():
    # --- Top level files ---
    write_file(
        BASE_DIR / "README.md",
        textwrap.dedent(
            """
            # MongoCoach – MongoDB Associate Developer (Python) Coach 🧠

            MongoCoach is an AI + RAG powered coach that helps you prepare for the
            **MongoDB Associate Developer – Python** certification.

            This repo will eventually include:
            - A Scraper Agent to ingest MongoDB docs into JSON and MongoDB
            - Question bank + Tutor Agent for personalized practice
            - Curriculum Planner + Analytics for tracking exam readiness

            ## Quick Start (Dev)

            ```bash
            git clone <this-repo>
            cd mongo-coach
            python -m venv .venv
            source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
            pip install -r requirements.txt
            python app.py
            ```

            For Hugging Face Spaces, `app.py` is the main entrypoint.
            """
        ),
    )

    write_file(
        BASE_DIR / ".gitignore",
        """
        .venv/
        __pycache__/
        .DS_Store
        .env
        .idea/
        .vscode/
        .pytest_cache/
        data/raw/
        data/processed/
        logs/
        """
    )

    write_file(
        BASE_DIR / "requirements.txt",
        """
        gradio>=4.0.0
        requests
        beautifulsoup4
        python-dotenv
        """
    )

    write_file(
        BASE_DIR / ".env.example",
        """
        # Copy this file to .env and fill in values for local dev.
        # On Hugging Face Spaces, set these in the "Secrets" panel instead.

        MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>/<db>?retryWrites=true&w=majority
        HF_TOKEN=your_huggingface_token_here
        """
    )

    # Minimal app for Spaces – just a placeholder UI
    write_file(
        BASE_DIR / "app.py",
        textwrap.dedent(
            """
            import gradio as gr

            def home():
                return (
                    "👋 Welcome to MongoCoach!\\n\\n"
                    "The backend agents (scraper, tutor, planner, analytics) "
                    "are under active development. This Space currently exposes "
                    "only a simple placeholder interface."
                )

            with gr.Blocks() as demo:
                gr.Markdown("# MongoCoach – MongoDB Associate Developer (Python)")
                gr.Markdown(
                    "This Space will become an AI-powered exam coach using MongoDB, RAG, and agents."
                )
                btn = gr.Button("Say hi")
                out = gr.Textbox(label="Status")

                btn.click(fn=lambda: home(), outputs=out)

            if __name__ == "__main__":
                demo.launch()
            """
        ),
    )

    # --- config ---
    seed_path = BASE_DIR / "config" / "sources_seed_associate_python.json"
    seed_content = {
        "exam_code": "ASSOC_DEV_PY",
        "root_docs": [
            "https://www.mongodb.com/docs/manual/crud/",
            "https://www.mongodb.com/docs/manual/aggregation/",
            "https://www.mongodb.com/docs/manual/indexes/",
            "https://www.mongodb.com/docs/manual/core/transactions/"
        ],
        "python_docs": [
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/get-started/",
            "https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/"
        ],
        "methods": [
            "https://www.mongodb.com/docs/manual/reference/method/db.collection.insertOne/",
            "https://www.mongodb.com/docs/manual/reference/method/db.collection.find/",
            "https://www.mongodb.com/docs/manual/reference/method/db.collection.updateOne/"
        ]
    }
    seed_path.parent.mkdir(parents=True, exist_ok=True)
    if not seed_path.exists():
        seed_path.write_text(json.dumps(seed_content, indent=2), encoding="utf-8")
        print(f"Created: {seed_path}")
    else:
        print(f"Exists (skipped): {seed_path}")

    write_file(
        BASE_DIR / "config" / "settings.toml",
        """
        [paths]
        raw_data_dir = "data/raw"
        processed_data_dir = "data/processed"
        catalog_dir = "data/catalog"

        [scraper]
        user_agent = "MongoCoachScraper/0.1"
        """
    )

    # --- data dirs (empty placeholders) ---
    (BASE_DIR / "data" / "raw").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "data" / "processed").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "data" / "catalog").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "logs").mkdir(parents=True, exist_ok=True)
    print("Ensured data/ and logs/ directories exist")

    # --- docs ---
    write_file(
        BASE_DIR / "docs" / "scraper_agent_plan.md",
        textwrap.dedent(
            """
            # Scraper Agent – Design (v1)

            Goal: Given a MongoDB docs URL, fetch the page, extract the main
            documentation content (title, sections, subsections, code blocks)
            into a structured JSON file under `data/raw/`.

            Modes (planned):
            - `single_url`: scrape one URL (e.g. db.collection.insertOne).
            - `associate_python_full`: use a catalog + seed config to scrape
              all relevant URLs for the Associate Dev (Python) exam.

            Output schema (high-level):

            ```jsonc
            {
              "url": "...",
              "doc_type": "mongodb_docs_method",
              "method_name": "db.collection.insertOne",
              "title": "db.collection.insertOne() (mongosh method)",
              "version": "8.2",
              "breadcrumbs": [...],
              "sections": [
                {
                  "section_id": "definition",
                  "heading": "Definition",
                  "heading_level": 2,
                  "content": "Text...",
                  "code_blocks": [],
                  "subsections": []
                }
              ],
              "fetched_at": "ISO-8601 timestamp"
            }
            ```
            """
        ),
    )

    write_file(
        BASE_DIR / "docs" / "mongocoach_design.md",
        textwrap.dedent(
            """
            # MongoCoach – Overall Design

            ## Goal

            Build an AI-powered coach to help users clear the
            **MongoDB Associate Developer – Python** certification on the first attempt.

            ## Agents

            1. Scraper & Indexer Agent
            2. Question Generator & Reviewer Agent
            3. Tutor / Coach Agent
            4. Curriculum Planner Agent
            5. Analytics & Insights Agent

            ## Data Model (MongoDB – planned)

            - `sources`: raw scraped pages with metadata
            - `docs_chunks`: RAG-ready text chunks + embeddings
            - `exam_objectives`: official objectives for ASSOC_DEV_PY
            - `questions_bank`: curated + generated questions
            - `users`: learner profiles
            - `user_progress`: per-user mastery tracking
            - `practice_sessions`: logs of question attempts

            This document is a living spec to guide implementation.
            """
        ),
    )

    # --- src package ---
    write_file(BASE_DIR / "src" / "__init__.py", "")

    # config loader
    write_file(
        BASE_DIR / "src" / "config" / "__init__.py",
        ""
    )
    write_file(
        BASE_DIR / "src" / "config" / "settings.py",
        textwrap.dedent(
            """
            import os
            from pathlib import Path

            BASE_DIR = Path(__file__).resolve().parents[2]

            RAW_DATA_DIR = BASE_DIR / "data" / "raw"
            PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
            CATALOG_DIR = BASE_DIR / "data" / "catalog"

            MONGODB_URI = os.environ.get("MONGODB_URI")
            HF_TOKEN = os.environ.get("HF_TOKEN")
            """
        ),
    )

    # core utilities
    write_file(
        BASE_DIR / "src" / "core" / "__init__.py",
        ""
    )
    write_file(
        BASE_DIR / "src" / "core" / "file_utils.py",
        textwrap.dedent(
            """
            import json
            from pathlib import Path
            from typing import Any, Dict

            def read_json(path: Path) -> Dict[str, Any]:
                with path.open("r", encoding="utf-8") as f:
                    return json.load(f)

            def write_json(path: Path, data: Dict[str, Any]) -> None:
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            """
        ),
    )
    write_file(
        BASE_DIR / "src" / "core" / "logging_utils.py",
        textwrap.dedent(
            """
            import datetime as _dt

            def log(msg: str) -> None:
                ts = _dt.datetime.utcnow().isoformat()
                print(f"[{ts}] {msg}")
            """
        ),
    )

    # models
    write_file(
        BASE_DIR / "src" / "models" / "__init__.py",
        ""
    )
    write_file(
        BASE_DIR / "src" / "models" / "scraper_types.py",
        textwrap.dedent(
            """
            from typing import List, Optional, Dict, Any
            from dataclasses import dataclass, field

            @dataclass
            class Section:
                section_id: str
                heading: str
                heading_level: int
                content: str = ""
                code_blocks: List[str] = field(default_factory=list)
                subsections: List[Dict[str, Any]] = field(default_factory=list)

            @dataclass
            class ScrapedDoc:
                url: str
                doc_type: str
                method_name: Optional[str]
                title: str
                version: Optional[str]
                breadcrumbs: List[str]
                sections: List[Section]
                fetched_at: str
            """
        ),
    )

    # agents
    write_file(
        BASE_DIR / "src" / "agents" / "__init__.py",
        ""
    )
    write_file(
        BASE_DIR / "src" / "agents" / "scraper_agent.py",
        textwrap.dedent(
            """
            \"\"\"Scraper Agent v1 – skeleton.

            - scrape_single_url(url): fetch & parse one MongoDB docs page
            - save_scrape_to_file(scraped): write JSON into data/raw/
            \"\"\"

            import datetime as dt
            from pathlib import Path
            from typing import Dict, Any

            import requests
            from bs4 import BeautifulSoup  # type: ignore

            from src.core.file_utils import write_json
            from src.core.logging_utils import log
            from src.config.settings import RAW_DATA_DIR


            class ScraperAgent:
                def __init__(self, user_agent: str = "MongoCoachScraper/0.1") -> None:
                    self.user_agent = user_agent

                def scrape_single_url(self, url: str) -> Dict[str, Any]:
                    log(f"Scraping URL: {url}")
                    headers = {"User-Agent": self.user_agent}
                    resp = requests.get(url, headers=headers, timeout=20)
                    resp.raise_for_status()

                    soup = BeautifulSoup(resp.text, "html.parser")

                    # Very minimal v1 parsing: title + all h2 sections with their text.
                    h1 = soup.find("h1")
                    title = h1.get_text(strip=True) if h1 else url

                    sections = []
                    for h2 in soup.find_all("h2"):
                        heading = h2.get_text(strip=True)
                        # Collect sibling text until next h2
                        content_parts = []
                        for sib in h2.next_siblings:
                            if getattr(sib, "name", None) == "h2":
                                break
                            if getattr(sib, "name", None) in {"p", "ul", "ol"}:
                                content_parts.append(sib.get_text(" ", strip=True))
                        sections.append(
                            {
                                "section_id": heading.lower().replace(" ", "-"),
                                "heading": heading,
                                "heading_level": 2,
                                "content": "\\n".join(content_parts),
                                "code_blocks": [],
                                "subsections": [],
                            }
                        )

                    scraped = {
                        "url": url,
                        "doc_type": "mongodb_docs_method",
                        "method_name": url.rstrip("/").split("/")[-1],
                        "title": title,
                        "version": None,
                        "breadcrumbs": [],
                        "sections": sections,
                        "fetched_at": dt.datetime.utcnow().isoformat(),
                    }
                    return scraped

                def save_scrape_to_file(self, scraped: Dict[str, Any]) -> Path:
                    method_name = scraped.get("method_name", "unknown")
                    filename = f"docs_{method_name}.json"
                    path = RAW_DATA_DIR / filename
                    write_json(path, scraped)
                    log(f"Saved scraped doc to: {path}")
                    return path
            """
        ),
    )

    # tests dir
    (BASE_DIR / "tests").mkdir(parents=True, exist_ok=True)
    write_file(
        BASE_DIR / "tests" / "test_scraper_agent.py",
        textwrap.dedent(
            """
            from src.agents.scraper_agent import ScraperAgent

            def test_scraper_agent_smoke():
                agent = ScraperAgent()
                assert agent is not None
            """
        ),
    )

    print("\n✅ Repo skeleton created under ./mongo-coach")

if __name__ == "__main__":
    main()
