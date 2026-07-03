"""Script to patch the Micro-Challenge section of the Collections vs Tables lesson."""
from certcoach.core import database

def main():
    database.check_connection()
    art = database.get_lesson_artifact(1, "Collections vs Tables")
    if not art:
        print("Lesson 'Collections vs Tables' not found.")
        return
        
    old_md = art["lesson_markdown"]
    
    target_str = "### 5. Micro-Challenge\n\nWhich BSON representation is the correct choice for these two fields?"
    replacement_str = """### 5. Micro-Challenge
A developer is designing a schema for a sales platform. They need to store a ledger document containing a `sales_amount` (exact decimal precision required) and a unique `sequence_id` (a monotonically increasing counter exceeding 2^53).

Which BSON representation is the correct choice for these two fields?

A) `sales_amount: Double`, `sequence_id: Int32`
B) `sales_amount: Decimal128`, `sequence_id: Int32`
C) `sales_amount: Double`, `sequence_id: Int64`
D) `sales_amount: Decimal128`, `sequence_id: Int64`"""
    
    if target_str in old_md:
        new_md = old_md.replace(target_str, replacement_str)
    else:
        # Try without the double newline or different matching
        target_str_alt = "### 5. Micro-Challenge\nWhich BSON representation is the correct choice for these two fields?"
        if target_str_alt in old_md:
            new_md = old_md.replace(target_str_alt, replacement_str)
        else:
            print("Could not find the target Micro-Challenge section to replace.")
            return
            
    # Also clean up the original options if they are still there
    new_md = new_md.replace("A) `write operation_amount: Double`, `sequence_id: Int32`\nB) `write operation_amount: Decimal128`, `sequence_id: Int32`\nC) `write operation_amount: Double`, `sequence_id: Int64`\nD) `write operation_amount: Decimal128`, `sequence_id: Int64`", "")
    new_md = new_md.replace("A) `write operation_amount: Double`, `sequence_id: Int32`\nB) `write operation_amount: Decimal128`, `sequence_id: Int32`\nC) `write operation_amount: Double`, `sequence_id: Int64`\nD) `write operation_amount: Decimal128`, `sequence_id: Int64`\n", "")
    
    art["lesson_markdown"] = new_md
    database.upsert_lesson_artifact(art)
    print("[+] Successfully patched the Collections vs Tables lesson in MongoDB.")

if __name__ == "__main__":
    main()
