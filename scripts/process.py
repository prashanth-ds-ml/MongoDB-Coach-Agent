import os
import json

def main():
    stage = os.environ.get("STAGE", "development")
    print(f"Running process.py in STAGE: {stage}")

    # The mount is at /app/data inside the container, or ./data locally
    data_dir = "/app/data" if os.path.exists("/app/data") else "./data"
    os.makedirs(data_dir, exist_ok=True)
    
    output_path = os.path.join(data_dir, "output.json")
    
    result = {
        "status": "success",
        "stage": stage,
        "message": "Hello from the Antigravity workflow!"
    }
    
    with open(output_path, "w") as f:
        json.dump(result, f, indent=4)
        
    print(f"Successfully processed data and wrote to {output_path}")

if __name__ == "__main__":
    main()
