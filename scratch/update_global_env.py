import os

path = os.path.expanduser("~/.certcoach/.env")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace MODEL
    new_content = content.replace('MODEL="gemma4:e4b"', 'MODEL="qwen2.5:7b"')
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Global .env model updated to qwen2.5:7b")
else:
    print("Global .env file not found")
