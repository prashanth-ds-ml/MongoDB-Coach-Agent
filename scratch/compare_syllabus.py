import json

with open("data/syllabus.json", "r", encoding="utf-8") as f:
    s1 = json.load(f)

with open("src/certcoach/data/syllabus.json", "r", encoding="utf-8") as f:
    s2 = json.load(f)

print(f"Are syllabus files identical? {s1 == s2}")
if s1 != s2:
    for idx, (t1, t2) in enumerate(zip(s1, s2)):
        if t1 != t2:
            print(f"\nDiff at topic {t1.get('id')} - {t1.get('topic')}:")
            print("  Root:", t1)
            print("  Src: ", t2)
