import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('src/certcoach/cli.py', encoding='utf-8') as f:
    lines = f.readlines()

print("Searching for Settings Menu / Main Menu:")
for i, line in enumerate(lines):
    if "def show_" in line or "def run_" in line or "def main_" in line or "def settings" in line or "Option 3" in line or "casing" in line.lower():
        print(f"Line {i+1}: {line.strip()}")
