"""Script to patch the Micro-Challenge section of the Document structure lesson."""
from certcoach.core import database

def main():
    database.check_connection()
    art = database.get_lesson_artifact(1, "Document structure")
    if not art:
        print("Lesson 'Document structure' not found.")
        return
        
    old_md = art["lesson_markdown"]
    
    target_str = "### 5. Micro-Challenge\nA) `Double`"
    replacement_str = """### 5. Micro-Challenge
A developer is designing a document schema for a finance application. Which BSON data type must be used to store monetary values to prevent rounding errors during calculations?

A) `Double`
B) `Int32`
C) `Decimal128`
D) `String`"""
    
    if target_str in old_md:
        new_md = old_md.replace(target_str, replacement_str)
    else:
        # Try with double newline or different markdown ticks
        target_str_alt = "### 5. Micro-Challenge\n\nA) `Double`"
        if target_str_alt in old_md:
            new_md = old_md.replace(target_str_alt, replacement_str)
        else:
            print("Could not find the target Micro-Challenge section to replace.")
            return
            
    art["lesson_markdown"] = new_md
    database.upsert_lesson_artifact(art)
    print("[+] Successfully patched the Document structure lesson in MongoDB.")

if __name__ == "__main__":
    main()
