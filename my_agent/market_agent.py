# my_agent/market_agent.py
import os
import json
import re
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types

APP_NAME = "market_search_service"
USER_ID = "spatial_engine_core"
SESSION_ID = "market_session_v1"

# --- MARKET AGENT PROMPT ---
MARKET_PROMPT = """
You are the Market Procurement Agent.

YOUR GOAL:
Search for (1) Lighting products OR (2) Electricity rates, and return STRICT JSON.

INSTRUCTIONS:

--- MODE A: PRODUCT SEARCH ---
If the user asks for a lamp/bulb:
1. Find basic specs: "price_usd" (float), "watts" (float), "lumens" (int), "name" (string).
2. **VERIFY CRITICAL FEATURES**:
   - Check if it is explicitly "dimmable" or "non-dimmable".
   - Check connectivity (Zigbee, WiFi, Bluetooth, or None).
3. JSON Format:
   {
     "type": "product",
     "name": "Philips LED A19",
     "price_usd": 6.99,
     "lumens": 1500,
     "watts": 14.5,
     "is_dimmable": true,
     "protocol": "Zigbee",
     "link": "http..."
   }

--- MODE B: RATE FINDER ---
If the user asks for "electricity rate" in a location:
1. Search for "residential electricity rate kwh [Location] 2024 2025".
2. Extract the average price per kWh in USD.
3. JSON Format:
   {
     "type": "rate",
     "location": "California",
     "rate_usd_kwh": 0.28,
     "source": "bls.gov or local provider"
   }

--- RULES ---
1. RETURN ONLY JSON. No markdown texts.
2. If exact rate is unknown, use the latest regional average.
3. If "dimmable" is not mentioned in the product page, assume "false".
"""

# --- MARKET AGENT ---
market_agent_core = Agent(
    name="market_agent",
    model="gemini-3-pro-preview",
    description="Searches for products, rates, and verifies technical specs (dimmable, protocol).",
    instruction=MARKET_PROMPT,
    tools=[google_search]
)

def clean_json_string(text: str) -> dict:
    """Helper to extract JSON from Markdown blocks or raw text"""
    try:
        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            json_str = match.group(1)
            return json.loads(json_str)
        else:
            return json.loads(text)
    except Exception as e:
        return {"error": "Failed to parse JSON", "raw_text": text}

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

def _run_in_thread(query: str):
    """Internal helper to run asyncio.run in a separate thread"""
    return asyncio.run(_run_market_search(query))

def search_product_data(query: str) -> dict:
    """
    Universal entry point for Market Agent.
    Uses ThreadPoolExecutor to isolate the async loop from the main agent.
    """
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_in_thread, query)
            raw_text = future.result()
            
        return clean_json_string(raw_text)
    except Exception as e:
        return {"error": f"Thread Error: {str(e)}"}

if __name__ == "__main__":
    # print("Testing Rate Finder...")
    
    # location = "New York"
    # query = f"What is the average electricity rate price per kwh in {location}?"
    
    # data = search_product_data(query)
    
    # print(f"\n--- RATE DATA FOR {location} ---")
    # print(data)
    
    # if "rate_usd_kwh" in data:
    #     print(f"✅ Success! Found rate: ${data['rate_usd_kwh']}/kWh")
    # else:
    #     print("❌ Failed to find rate.")

    print("Testing Feature Verification (Task 28)...")
    # Test: Searching for a dimmable bulb
    data = search_product_data("Price of dimmable Philips Hue A19 bulb")
    print(data)
    
    if data.get("is_dimmable") is True:
        print("✅ SUCCESS: Recognized as dimmable.")
    else:
        print("⚠️ WARNING: Verification failed or product is not dimmable.")