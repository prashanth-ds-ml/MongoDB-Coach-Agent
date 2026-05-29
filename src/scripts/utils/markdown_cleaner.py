import os
import re
from pathlib import Path

def clean_markdown_files(directory_path):
    print(f"--- Cleaning Markdown files in {directory_path} ---")
    data_dir = Path(directory_path)
    md_files = list(data_dir.rglob("*.md"))
    
    # Text blocks that appear from scraping the language tabs on mongodb docs
    language_tabs = [
        "MongoDB Shell", "Compass", "C", "C#", "Go", "Java (Async)", 
        "Java (Sync)", "Kotlin (Coroutine)", "Motor", "Node.js", "PHP", 
        "Python", "Ruby", "Scala", "PyMongo", "Motor"
    ]
    
    # Create a regex that aggressively matches these standalone lines
    tab_re = re.compile(r'^\s*(' + '|'.join(re.escape(lang) for lang in language_tabs) + r')\s*$', re.IGNORECASE)

    files_modified = 0

    for file_path in md_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            cleaned_lines = []
            skip_count = 0
            
            for line in lines:
                # Remove scraping noise (Language tab lists)
                if tab_re.match(line):
                    skip_count += 1
                    continue
                    
                # Fix weird "---" under code blocks to clean it up slightly if needed
                # For now just keep it as it might be valid yaml or seperators
                
                cleaned_lines.append(line)
                
            # Rejoin and fix excessive newlines
            content = "".join(cleaned_lines)
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            # Write back
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            if skip_count > 0:
                files_modified += 1
                
        except Exception as e:
            print(f"Error cleaning {file_path.name}: {e}")

    print(f"Cleaning complete. Modified {files_modified} files to remove scraping noise.")
    
    # Run the profiler to generate the post-clean JSON
    from markdown_profiler import profile_markdown_files
    profile_markdown_files(directory_path)
    
    # Rename the output to distinguish it
    import os
    raw_prof = os.path.join(directory_path, "raw_profile.json")
    clean_prof = os.path.join(directory_path, "cleaned_profile.json")
    if os.path.exists(raw_prof):
        if os.path.exists(clean_prof):
            os.remove(clean_prof)
        os.rename(raw_prof, clean_prof)
        print(f"Cleaned profile saved to {clean_prof}")

if __name__ == "__main__":
    clean_markdown_files("data")
