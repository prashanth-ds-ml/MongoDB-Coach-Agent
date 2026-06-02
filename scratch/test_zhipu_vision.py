import os
import sys
import base64
from zhipuai import ZhipuAI

# Load Environment Variables from Global Config
GLOBAL_CONFIG_DIR = os.path.expanduser("~/.certcoach")
ENV_PATH = os.path.join(GLOBAL_CONFIG_DIR, ".env")
from dotenv import load_dotenv
load_dotenv(ENV_PATH)

OLLAMA_CLOUD_API_KEY = os.getenv("OLLAMA_CLOUD_API_KEY")
if not OLLAMA_CLOUD_API_KEY:
    print("Error: OLLAMA_CLOUD_API_KEY not found.")
    sys.exit(1)

# Connect via official SDK
client = ZhipuAI(api_key=OLLAMA_CLOUD_API_KEY)

# Target image
_HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.abspath(os.path.join(_HERE, "../src/certcoach/data/pics_qa/Screenshot 2025-12-14 090435.png"))

if not os.path.exists(IMAGE_PATH):
    print(f"Error: Image not found at {IMAGE_PATH}")
    sys.exit(1)

# Encode image to base64
with open(IMAGE_PATH, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

print("Sending request to Zhipu AI GLM-4V...")
try:
    response = client.chat.completions.create(
        model="glm-4v",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "content": "Analyze this screenshot. It contains a multiple choice question about MongoDB. Extract the question text, the options, and if visible or implied, the correct answer and a brief explanation. Return the extracted content as a structured JSON object matching the standard MCQ schema with fields: topic, difficulty, question, options (list of strings), correct_answer, and explanation."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0.1
    )
    print("\nResponse Received successfully:")
    # Use standard UTF-8 stream to avoid cp1252 print errors on Windows terminal
    sys.stdout.buffer.write(response.choices[0].message.content.encode('utf-8'))
    print()
except Exception as e:
    print(f"Error calling GLM-4V: {e}")
