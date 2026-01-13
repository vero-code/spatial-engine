# my_agent/market_agent.py
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
import asyncio

APP_NAME = "market_search_service"
USER_ID = "spatial_engine_core"
SESSION_ID = "market_session_v1"

# --- MARKET AGENT PROMPT ---
MARKET_PROMPT = """
You are the Market Procurement Agent for the Spatial Engine system.

YOUR GOAL:
Search for the requested lighting product and return technical/financial data in STRICT JSON format.

INSTRUCTIONS:
1. Use `Google Search` to find the product.
2. Extract:
   - "name": Product title.
   - "price_usd": Price for ONE unit (calculate if pack). Type: Float.
   - "lumens": Brightness. Type: Int.
   - "watts": Power consumption. Type: Float.
   - "link": URL to retailer.
3. OUTPUT FORMAT:
   Return ONLY a valid JSON object. No markdown formatting, no conversational text.
   
Example:
{
  "name": "Philips LED A19",
  "price_usd": 6.99,
  "lumens": 1500,
  "watts": 14.5,
  "link": "https://amazon.com/..."
}
"""

# --- MARKET AGENT ---
market_agent_core = Agent(
    name="market_agent",
    model="gemini-3-pro-preview",
    description="An agent that searches the web for products and prices, and returns product data in JSON.",
    instruction=MARKET_PROMPT,
    tools=[google_search]
)

def clean_json_string(text: str) -> dict:
    """Helper to extract JSON from Markdown blocks"""
    try:
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            json_str = text
            
        return json.loads(json_str)
    except Exception as e:
        print(f"[Parser Error] Could not parse JSON: {text}")
        return {"error": "Failed to parse market data", "raw_text": text}

async def _run_market_search(query: str):
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=market_agent_core, app_name=APP_NAME, session_service=session_service)
    
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    
    final_text = ""
    async for event in events:
         if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_text += part.text
    
    return final_text

def search_product_data(query: str) -> dict:
    """
    Returns a Dictionary with product data (price, lumens, etc).
    """
    try:
        raw_text = asyncio.run(_run_market_search(query))
        return clean_json_string(raw_text)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Testing Market Agent (JSON Parser)...")
    
    # Test 1: Lamp
    data = search_product_data("Find best price for 1500 lumen LED bulb Philips")
    print("\n--- LAMP DATA (DICT) ---")
    print(data)
    print(f"Type: {type(data)}")
    
    # Test 2: Access fields
    if "price_usd" in data:
        print(f"\nCalculated Cost for 10 bulbs: ${data['price_usd'] * 10}")