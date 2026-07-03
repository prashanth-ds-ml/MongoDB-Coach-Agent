"""Script to patch the Micro-Challenge section of the BSON Data Types lesson."""
from certcoach.core import database

def main():
    database.check_connection()
    art = database.get_lesson_artifact(1, "BSON Data Types")
    if not art:
        print("Lesson BSON Data Types not found.")
        return
        
    old_md = art["lesson_markdown"]
    
    target_str = "### 5. Micro-Challenge\n\nA) Double"
    replacement_str = """### 5. Micro-Challenge
A developer is designing a schema for financial ledger entries where arithmetic rounding errors are unacceptable. Which BSON numeric representation MUST be used to store transaction amounts?

A) Double
B) Int32
C) Int64
D) Decimal128"""
    
    if target_str in old_md:
        new_md = old_md.replace(target_str, replacement_str)
    else:
        # Try without the double newline
        target_str_alt = "### 5. Micro-Challenge\nA) Double"
        if target_str_alt in old_md:
            new_md = old_md.replace(target_str_alt, replacement_str)
        else:
            print("Could not find the target Micro-Challenge section to replace.")
            return
            
    art["lesson_markdown"] = new_md
    database.upsert_lesson_artifact(art)
    print("[+] Successfully patched the Micro-Challenge section in MongoDB.")

if __name__ == "__main__":
    main()
