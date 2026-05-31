import certcoach.core.database as db

db.check_connection()
attempts = db.get_user_attempts('local_user_1')
print(f"Attempts count: {len(attempts)}")
for idx, a in enumerate(attempts, 1):
    print(f"  {idx}: Topic='{a.get('topic')}' Correct={a.get('is_correct')} Confidence='{a.get('confidence_level')}'")
