import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: API Key not found.")
    exit()

client = genai.Client(api_key=api_key)

def run_search_demo():
    print("--- Spatial Engine: Grounding with Google Search ---")

    prompt = """
    Generate a color palette with hex codes for the Dark Academia style.
    Return the output as Python code that I can run.
    Only return the code.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ]
            )
        )

        print("🤖 Gemini:", response.text)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_search_demo()
