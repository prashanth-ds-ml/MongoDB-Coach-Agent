import argparse
import sys
import os
import yaml
from pathlib import Path
from .engine import execute_workflow

def init_cmd(args):
    os.makedirs(".antigravity", exist_ok=True)
    config_path = Path(".antigravity/config.yaml")
    if not config_path.exists():
        with open(config_path, "w") as f:
            f.write("engine: docker\ndefault_stage: development\n")
        print("Initialized .antigravity/config.yaml")
    else:
        print("Config already exists.")

def lint_cmd(args):
    file_path = args.file
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        sys.exit(1)
        
    try:
        with open(file_path, "r") as f:
            content = yaml.safe_load(f)
    except Exception as e:
        print(f"YAML parsing error: {e}")
        sys.exit(1)
        
    required_keys = ["version", "project", "tasks"]
    for k in required_keys:
        if k not in content:
            print(f"Lint Error: Missing required key '{k}' in {file_path}")
            sys.exit(1)
            
    # Check tasks format
    for i, t in enumerate(content.get("tasks", [])):
        if "name" not in t or "image" not in t:
            print(f"Lint Error: Task {i} is missing 'name' or 'image'")
            sys.exit(1)
    
    print(f"Syntax OK for {file_path}")

def run_cmd(args):
    file_path = args.file
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        sys.exit(1)
        
    try:
        execute_workflow(file_path)
    except Exception as e:
        print(f"Execution Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Antigravity Workflow Engine")
    subparsers = parser.add_subparsers(dest="command")

    # init
    parser_init = subparsers.add_parser("init", help="Initialize antigravity config")
    
    # lint
    parser_lint = subparsers.add_parser("lint", help="Lint a workflow YAML file")
    parser_lint.add_argument("file", help="Path to workflow YAML")

    # run
    parser_run = subparsers.add_parser("run", help="Execute a workflow YAML file")
    parser_run.add_argument("file", help="Path to workflow YAML")

    args = parser.parse_args()

    if getattr(args, "command", None) == "init":
        init_cmd(args)
    elif getattr(args, "command", None) == "lint":
        lint_cmd(args)
    elif getattr(args, "command", None) == "run":
        run_cmd(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
