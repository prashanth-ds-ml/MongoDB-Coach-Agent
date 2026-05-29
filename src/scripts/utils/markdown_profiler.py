import os
import re
from pathlib import Path

def profile_markdown_files(directory_path):
    print(f"--- Profiling Markdown files in {directory_path} ---")
    data_dir = Path(directory_path)
    md_files = list(data_dir.rglob("*.md"))
    
    if not md_files:
        print("No markdown files found.")
        return
        
    total_files = len(md_files)
    total_lines = 0
    total_empty_lines = 0
    total_code_blocks = 0
    total_tables = 0
    anomalous_files = []

    for file_path in md_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            lines = content.split('\n')
            num_lines = len(lines)
            empty_lines = sum(1 for line in lines if not line.strip())
            
            # Count code blocks (pairs of ```)
            code_blocks = len(re.findall(r'```', content)) // 2
            
            # Rough estimate of tables (lines starting with | and containing -|- )
            has_table = bool(re.search(r'\|.*-.*\|', content))
            if has_table:
                total_tables += 1
                
            total_lines += num_lines
            total_empty_lines += empty_lines
            total_code_blocks += code_blocks

            # Detect anomalies
            if num_lines == 0:
                anomalous_files.append((file_path.name, "Empty file"))
            elif (empty_lines / max(1, num_lines)) > 0.4:
                anomalous_files.append((file_path.name, f"High empty line ratio: {empty_lines}/{num_lines}"))
                
        except Exception as e:
            print(f"Error reading {file_path.name}: {e}")

    import json
    
    profile_data = {
        "summary": {
            "total_files": total_files,
            "total_lines": total_lines,
            "total_empty_lines": total_empty_lines,
            "empty_line_ratio": round((total_empty_lines/max(1,total_lines))*100, 2),
            "code_blocks_detected": total_code_blocks,
            "files_with_tables": total_tables
        },
        "anomalies": [{"file": fname, "issue": issue} for fname, issue in anomalous_files]
    }
    
    out_file = os.path.join(directory_path, "raw_profile.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=4)
        
    print(f"\n--- Profiling Summary ---")
    print(f"Total Files Analyzed: {total_files}")
    print(f"Total Lines: {total_lines}")
    print(f"Empty Lines: {total_empty_lines} ({(total_empty_lines/max(1,total_lines))*100:.1f}%)")
    print(f"Code Blocks Detected: {total_code_blocks}")
    print(f"Files containing Tables: {total_tables}")
    
    print(f"\n--- Anomalies ---")
    if anomalous_files:
        for fname, issue in anomalous_files:
            print(f"Warning - {fname}: {issue}")
    else:
        print("OK - No critical anomalies detected.")
        
    print(f"Profile saved to {out_file}")

if __name__ == "__main__":
    profile_markdown_files("data")
