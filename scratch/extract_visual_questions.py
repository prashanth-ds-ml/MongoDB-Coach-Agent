import os
import sys

# Ensure import paths work
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, "..")))

from src.certcoach.core.image_extractor import process_pics_qa

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CertCoach Visual Question Bank Processor")
    parser.add_argument("--limit", type=int, help="Limit number of images to process in this run")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without calling LLM or writing to DB")
    args = parser.parse_args()
    
    print("=" * 60)
    print("      CertCoach Visual Question Extractor: pics_qa Pipeline")
    print("=" * 60)
    
    process_pics_qa(limit=args.limit, dry_run=args.dry_run)
