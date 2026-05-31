import os
import shutil

root_dir = "."
src_data_dir = os.path.join("src", "certcoach", "data")
root_data_dir = "data"

# 1. Sync syllabus.json
shutil.copy2(
    os.path.join(root_data_dir, "syllabus.json"),
    os.path.join(src_data_dir, "syllabus.json")
)
print("Synced syllabus.json")

# 2. Sync raw_markdowns
src_raw_dir = os.path.join(src_data_dir, "raw_markdowns")
root_raw_dir = os.path.join(root_data_dir, "raw_markdowns")

# Remove old files in src_raw_dir first to avoid mixing old and new naming schemes
if os.path.exists(src_raw_dir):
    shutil.rmtree(src_raw_dir)
os.makedirs(src_raw_dir, exist_ok=True)

for fname in os.listdir(root_raw_dir):
    if fname.endswith(".md"):
        shutil.copy2(
            os.path.join(root_raw_dir, fname),
            os.path.join(src_raw_dir, fname)
        )
print("Synced raw_markdowns")

# 3. Sync cleaned_markdowns
src_clean_dir = os.path.join(src_data_dir, "cleaned_markdowns")
root_clean_dir = os.path.join(root_data_dir, "cleaned_markdowns")

if os.path.exists(src_clean_dir):
    shutil.rmtree(src_clean_dir)
os.makedirs(src_clean_dir, exist_ok=True)

for fname in os.listdir(root_clean_dir):
    if fname.endswith(".md"):
        shutil.copy2(
            os.path.join(root_clean_dir, fname),
            os.path.join(src_clean_dir, fname)
        )
print("Synced cleaned_markdowns")
