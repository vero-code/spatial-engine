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

def run_combo_demo():
    print("--- Spatial Engine: Search + Code Execution ---")
    
    # The Task:
    # 1. FIND the text of "The Tell-Tale Heart" (Search).
    # 2. COUNT sentences, words, syllables (Code).
    # 3. CALCULATE the Flesch–Kincaid formula (Code).
    prompt = (
        "Calculate the Flesch–Kincaid Grade Level of Edgar Allan Poe's "
        "short story 'The Tell-Tale Heart'."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    ),
                    types.Tool(
                        code_execution=types.ToolCodeExecution()
                    ),
                ]
            )
        )

        print("🤖 Gemini:", response.text)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_combo_demo()
