import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
log_path = r"C:\Users\prash\.gemini\antigravity-cli\brain\73cf2dc7-90e0-44e8-8daa-22cac5d7254e\.system_generated\tasks\task-1905.log"
if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        lines = content.splitlines()
        if lines:
            # print the last 15 lines with safe printable characters
            for line in lines[-15:]:
                safe_line = "".join(c if ord(c) < 128 else "?" for c in line)
                print(safe_line)
        else:
            print("Log file empty")
else:
    print("Log file not found")
