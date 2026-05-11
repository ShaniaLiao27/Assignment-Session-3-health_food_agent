import os
from google import genai
from dotenv import load_dotenv

load_dotenv("health_food_agent/.env")
client = genai.Client()

print("Available Models:")
try:
    for m in client.models.list():
        if "gemini" in m.name:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
