import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: Key not found. Check your .env file.")
    exit()

client = genai.Client(api_key=api_key)

prompt = """Classify the following 5 items into either 'Fruit' or 'Vegetable'.
Format your answer as a simple, comma-separated list of pairs (Item: Category).
Avocado
Carrot
Tomato
Apple
Zucchini"""

try:
    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel.LOW
            )
        )
    )
    print("\n🤖 Gemini:\n", response.text)
except Exception as e:
    print("\n⚠️ Error:", e)