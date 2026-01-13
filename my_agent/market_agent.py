# my_agent/market_agent.py
import os
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
Find real-world lighting products, prices, and electricity rates.

INSTRUCTIONS:
1. When asked for a product (e.g., "LED bulb 1500 lumens"), use `Google Search` to find:
   - Specific model names.
   - Current prices in USD.
   - Retailers (Amazon, Home Depot, etc.).
2. Always return the data in a clean summary format: "Product: [Name], Price: $[X], Link: [URL]".
3. If searching for electricity rates, look for "average electricity rate in [Location] 2025".

You are purely factual. Do not guess prices.
"""

# --- MARKET AGENT ---
market_agent_core = Agent(
    name="market_agent",
    model="gemini-3-pro-preview",
    description="An agent that searches the web for products and prices.",
    instruction=MARKET_PROMPT,
    tools=[google_search]
)

def search_market_sync(query: str) -> str:
    """
    Synchronous wrapper to call the Market Agent.
    Used by the main agent as a tool.
    """
    try:
        return asyncio.run(_run_market_search(query))
    except Exception as e:
        return f"Market Agent Error: {str(e)}"

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

if __name__ == "__main__":
    print("Testing Market Agent...")
    result = asyncio.run(_run_market_search("Find price for 1500 lumen LED bulb Philips"))
    print(f"RESULT:\n{result}")