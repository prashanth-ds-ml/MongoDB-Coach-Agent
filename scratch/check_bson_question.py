import certcoach.core.database as db

db.check_connection()
# Try searching for Number or integers
questions = list(db.questions_col.find({"question_text": {"$regex": "Number", "$options": "i"}}))
if not questions:
    questions = list(db.questions_col.find().limit(5))
print(f"Found {len(questions)} matching questions:")
for idx, q in enumerate(questions, 1):
    print(f"\nQuestion {idx}: {q.get('question_text')[:100]}...")
    print("Options:")
    for opt in q.get("options", []):
        print(f"  Option {opt.get('option_letter')}: code={opt.get('code_snippet')}, is_correct={opt.get('is_correct')}, is_trap={opt.get('is_trap')}, feedback='{opt.get('feedback')}'")
