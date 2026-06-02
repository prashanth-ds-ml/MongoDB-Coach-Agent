import os

path = r"data/Primary_Exam_Guide.md"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    print(f"File size: {len(content)} characters")
    
    # Search for BSON or BSON Data Types
    lines = content.splitlines()
    matches = []
    for idx, line in enumerate(lines, 1):
        if "bson" in line.lower() or "type" in line.lower() or "document" in line.lower():
            matches.append((idx, line))
            
    print(f"Found {len(matches)} matches. Sample matches:")
    for idx, line in matches[:30]:
        print(f"  Line {idx}: {line[:120]}")
else:
    print("Primary_Exam_Guide.md not found")
