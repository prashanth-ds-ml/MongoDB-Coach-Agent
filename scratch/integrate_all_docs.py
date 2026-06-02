import os
import json
import re
import shutil
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(".").resolve()
DATA_DIR = PROJECT_ROOT / "data"
SRC_DATA_DIR = PROJECT_ROOT / "src" / "certcoach" / "data"
MAPPED_DIR = DATA_DIR / "mongodb_docs" / "syllabus_mapped" / "associate_python_developer"

# Define output directories
RAW_DIRS = [DATA_DIR / "raw_markdowns", SRC_DATA_DIR / "raw_markdowns"]
CLEAN_DIRS = [DATA_DIR / "cleaned_markdowns", SRC_DATA_DIR / "cleaned_markdowns"]

# Create output directories
for d in RAW_DIRS + CLEAN_DIRS:
    d.mkdir(parents=True, exist_ok=True)

# Markdown cleaning helpers from clean_markdown.py
def clean_markdown_tables(text):
    def repl_table(match):
        table_html = match.group(0)
        trs = re.findall(r'<tr.*?>(.*?)</tr>', table_html, re.DOTALL | re.IGNORECASE)
        if not trs: 
            return table_html
        
        md_lines = []
        for i, tr in enumerate(trs):
            cells = re.findall(r'<(th|td).*?>(.*?)</\1>', tr, re.DOTALL | re.IGNORECASE)
            row_data = []
            for tag, content in cells:
                cleaned = re.sub(r'\s+', ' ', content).strip()
                row_data.append(cleaned)
                
            if row_data:
                md_lines.append('| ' + ' | '.join(row_data) + ' |')
                if i == 0:
                    md_lines.append('| ' + ' | '.join(['---'] * len(row_data)) + ' |')
                
        return '\n'.join(md_lines) + '\n'
    return re.sub(r'<table.*?>.*?</table>', repl_table, text, flags=re.DOTALL | re.IGNORECASE)

def clean_content(text):
    text = re.sub(r'This page documents a \[.*?\]\(.*?\) method\. To see the equivalent method in a MongoDB driver, see the corresponding page for your programming language:', '', text, flags=re.DOTALL)
    text = re.sub(r'## Compatibility.*?## Syntax', '## Syntax', text, flags=re.DOTALL)
    text = re.sub(r'## Learn More.*', '', text, flags=re.DOTALL)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = clean_markdown_tables(text)
    text = re.sub(r'(\w\(\))([A-Z])', r'\1 \2', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'

def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")

# Load syllabus
syllabus_path = DATA_DIR / "syllabus.json"
with open(syllabus_path, "r", encoding="utf-8") as f:
    syllabus = json.load(f)

# Clear existing raw/clean markdown dirs under package to avoid mixing old names
for d in [SRC_DATA_DIR / "raw_markdowns", SRC_DATA_DIR / "cleaned_markdowns", DATA_DIR / "raw_markdowns", DATA_DIR / "cleaned_markdowns"]:
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True, exist_ok=True)

# Iterate over syllabus topics
for topic_item in syllabus:
    topic_id = topic_item["id"]
    topic_name = topic_item["topic"]
    
    topic_folder_name = f"{topic_id:02d}_{slugify(topic_name)}"
    topic_mapped_dir = MAPPED_DIR / topic_folder_name
    
    print(f"\nProcessing Topic #{topic_id}: {topic_name}")
    
    if not topic_mapped_dir.exists():
        print(f"  Warning: Mapped directory {topic_mapped_dir} does not exist.")
        topic_item["md_files"] = []
        continue
        
    md_files_list = []
    # Find all mapped markdown files
    for md_file in sorted(topic_mapped_dir.glob("*.md")):
        if md_file.name == "topic_mapping_manifest.json" or md_file.name == "mapping_summary.json":
            continue
            
        # Build new filename: e.g. topic_01_introduction__abcdef.md
        original_name = md_file.name
        # clean prefix like "00_existing_" or "00_resolved_" or "01_" if mapped ranks them
        clean_name = re.sub(r"^\d+_(existing_|resolved_)?", "", original_name)
        new_filename = f"topic_{topic_id:02d}_{clean_name}"
        
        # Read raw content
        with open(md_file, "r", encoding="utf-8", errors="replace") as f:
            raw_text = f.read()
            
        # Clean content
        cleaned_text = clean_content(raw_text)
        
        # Write raw files
        for rd in RAW_DIRS:
            with open(rd / new_filename, "w", encoding="utf-8") as f:
                f.write(raw_text)
                
        # Write cleaned files
        for cd in CLEAN_DIRS:
            with open(cd / new_filename, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
                
        md_files_list.append(new_filename)
        print(f"  Mapped & Cleaned: {original_name} -> {new_filename}")
        
    topic_item["md_files"] = md_files_list
    print(f"  Topic #{topic_id} now has {len(md_files_list)} mapped markdown files.")

# Save syllabus files
with open(DATA_DIR / "syllabus.json", "w", encoding="utf-8") as f:
    json.dump(syllabus, f, indent=4, ensure_ascii=False)

with open(SRC_DATA_DIR / "syllabus.json", "w", encoding="utf-8") as f:
    json.dump(syllabus, f, indent=4, ensure_ascii=False)

print("\nSuccessfully integrated all mapped syllabus documents and updated syllabus.json!")
