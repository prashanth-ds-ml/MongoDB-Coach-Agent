import sys
import os
from unittest.mock import patch

# Set PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Ensure stdout is reconfigured to utf-8 if needed
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from certcoach.cli import main_menu

# Patch Prompt.ask to raise KeyboardInterrupt immediately to capture the menu printout
print("--- RUNNING CERTCOACH MAIN MENU RENDER ---")
with patch("certcoach.cli.Prompt.ask", side_effect=KeyboardInterrupt()):
    try:
        main_menu()
    except (KeyboardInterrupt, SystemExit):
        print("\n--- CLI RENDER COMPLETED ---")
