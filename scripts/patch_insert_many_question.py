"""Script to patch the Micro-Challenge section of the insertMany() lesson."""
from certcoach.core import database

def main():
    database.check_connection()
    art = database.get_lesson_artifact(2, "insertMany()")
    if not art:
        print("Lesson 'insertMany()' not found.")
        return
        
    old_md = art["lesson_markdown"]
    
    target_str = "### 5. Micro-Challenge\n\nA. Double"
    replacement_str = """### 5. Micro-Challenge
A developer is designing a schema for a sales platform. They need to store an exact financial amount representing a document's price. Which BSON representation is the correct choice to prevent rounding errors during calculations?

A. Double
B. Int32 (NumberInt)
C. Int64 (NumberLong)
D. Decimal128 (NumberDecimal)"""
    
    if target_str in old_md:
        new_md = old_md.replace(target_str, replacement_str)
    else:
        # Try with double newline or single newline
        target_str_alt = "### 5. Micro-Challenge\nA. Double"
        if target_str_alt in old_md:
            new_md = old_md.replace(target_str_alt, replacement_str)
        else:
            print("Could not find the target Micro-Challenge section to replace.")
            return
            
    # Also clean up duplicate options if they are still there
    new_md = new_md.replace("B. Int32 (NumberInt)\nC. Int64 (NumberLong)\nD. Decimal128 (NumberDecimal)\n", "")
    new_md = new_md.replace("B. Int32 (NumberInt)\nC. Int64 (NumberLong)\nD. Decimal128 (NumberDecimal)", "")
    
    art["lesson_markdown"] = new_md
    database.upsert_lesson_artifact(art)
    print("[+] Successfully patched the insertMany() lesson in MongoDB.")

if __name__ == "__main__":
    main()
