"""Script to patch the Micro-Challenge section of the find() lesson."""
from certcoach.core import database

def main():
    database.check_connection()
    art = database.get_lesson_artifact(3, "find()")
    if not art:
        print("Lesson 'find()' not found.")
        return
        
    old_md = art["lesson_markdown"]
    
    target_str = "### 5. Micro-Challenge\n- A) Double"
    replacement_str = """### 5. Micro-Challenge
A developer needs to store a monetary value such as a product price in a document. Which BSON type is the correct choice to guarantee exact decimal representation and avoid floating-point rounding errors?

A) Double
B) Int32
C) Decimal128
D) String"""
    
    if target_str in old_md:
        new_md = old_md.replace(target_str, replacement_str)
    else:
        # Try with double newline or single newline
        target_str_alt = "### 5. Micro-Challenge\n- A) Double"
        if target_str_alt in old_md:
            new_md = old_md.replace(target_str_alt, replacement_str)
        else:
            print("Could not find the target Micro-Challenge section to replace.")
            return
            
    # Also clean up duplicate options if they are still there
    new_md = new_md.replace("- B) Int32\n- C) Decimal128\n- D) String\n", "")
    new_md = new_md.replace("- B) Int32\n- C) Decimal128\n- D) String", "")
    
    art["lesson_markdown"] = new_md
    database.upsert_lesson_artifact(art)
    print("[+] Successfully patched the find() lesson in MongoDB.")

if __name__ == "__main__":
    main()
