"""Script to export BSON Data Types lesson markdown from MongoDB."""
from certcoach.core import database

def main():
    database.check_connection()
    art = database.get_lesson_artifact(1, "BSON Data Types")
    if art:
        out_path = "memory/bson_data_types_lesson.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(art["lesson_markdown"])
        print(f"Exported lesson to: {out_path}")
    else:
        print("Lesson BSON Data Types not found in database.")

if __name__ == "__main__":
    main()
