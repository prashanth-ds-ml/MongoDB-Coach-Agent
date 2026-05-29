import os
import sys
import json
import random

# Ensure we use utf-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

console = Console()
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
JSON_FILE = os.path.join(PROJECT_ROOT, "data", "extracted_questions.json")

def run_test_quiz():
    if not os.path.exists(JSON_FILE):
        console.print(f"[red]Error: Could not find {JSON_FILE}[/red]")
        return
        
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    console.print(f"[bold green]✅ Loaded {len(questions)} official questions from JSON![/bold green]\n")
    
    # Shuffle so they get different questions every time
    random.shuffle(questions)
    
    for idx, q in enumerate(questions[:5]): # Test just 5 questions
        console.clear()
        
        meta = q.get("metadata", {})
        context = q.get("context", {})
        
        header = f"[bold cyan]Topic: {meta.get('topic', 'Unknown')}[/bold cyan] | Difficulty: {meta.get('difficulty', 'Unknown')}"
        console.print(Panel(header))
        
        # Print Context if exists
        if context.get("scenario_description"):
            console.print(f"[dim]Scenario:[/dim] {context.get('scenario_description')}")
        if context.get("database_info"):
            console.print(f"[dim]Data:[/dim] {context.get('database_info')}\n")
            
        # Print Question
        console.print(f"[bold]{q.get('question_text')}[/bold]\n")
        
        # Print Options
        valid_options = []
        for opt in q.get("options", []):
            letter = opt.get("option_letter", "?")
            valid_options.append(letter.upper())
            snippet = opt.get("code_snippet", "")
            console.print(f"[bold yellow]{letter})[/bold yellow] {snippet}")
            
        print("\n")
        ans = Prompt.ask("Your Answer", choices=valid_options).upper()
        
        # Check correctness
        correct_option = None
        user_feedback = ""
        is_correct = False
        
        for opt in q.get("options", []):
            if opt.get("is_correct"):
                correct_option = opt
            if opt.get("option_letter", "").upper() == ans:
                user_feedback = opt.get("feedback", "No specific feedback provided.")
                is_correct = opt.get("is_correct", False)
                
        if is_correct:
            console.print(f"\n[bold green]✅ Correct![/bold green]")
        else:
            console.print(f"\n[bold red]❌ Incorrect.[/bold red]")
            if correct_option:
                console.print(f"[bold white]The correct answer was: {correct_option.get('option_letter')}[/bold white]")
                
        console.print(Panel(user_feedback, title="Official Feedback 🪤", border_style="yellow"))
        
        if idx < 4:
            Prompt.ask("\nPress Enter for the next question...")
            
    console.print("\n[bold green]Test Complete! You just tested 5 official exam questions.[/bold green]")

if __name__ == "__main__":
    try:
        run_test_quiz()
    except KeyboardInterrupt:
        print("\nExiting...")
