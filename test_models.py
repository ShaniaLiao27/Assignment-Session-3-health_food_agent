import os
from google import genai
from dotenv import load_dotenv

load_dotenv("health_food_agent/.env")
client = genai.Client()

models_to_test = [
    "gemini-2.5-pro",
    "gemini-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash-001"
]

for model in models_to_test:
    print(f"Testing {model}...")
    try:
        response = client.models.generate_content(
            model=model,
            contents="Say hi"
        )
        print(f"SUCCESS: {model} -> {response.text}")
    except Exception as e:
        print(f"FAILED: {model} -> {e}")
