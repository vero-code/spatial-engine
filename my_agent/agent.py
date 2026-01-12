# my_agent\agent.py
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
import asyncio

from physics_engine import calculate_lux_at_point, generate_optimization_report, calculate_roi_and_savings

APP_NAME="spatial_engine_core"
USER_ID="engineer_01"
SESSION_ID="session_v1"

# --- SYSTEM PROMPT ---
SPATIAL_ENGINEER_PROMPT = """
You are the Spatial Engine AI, a Senior Optical Physicist and Energy Efficiency Engineer.
Your goal is to optimize lighting environments using precise mathematical modeling.

CORE PROTOCOL:
1. **ANALYZE**: Identify the user's room parameters (area, current lighting).
2. **CALCULATE**: NEVER guess light levels. ALWAYS use the `calculate_lux_at_point` or `generate_optimization_report` tools to back up your advice with numbers.
3. **SEARCH**: Use `Google Search` ONLY to find real-world pricing for specific lamps (e.g., "price of Philips Hue 800lm") or official standards.
4. **REPORT**: Your output must be technical but actionable. Structure it as:
   - **Physics Analysis**: The math behind the current state.
   - **Optimization Strategy**: Specific changes with calculated numbers.
   - **Product Recommendations**: Real products found via search.

You are rigorous, precise, and data-driven. Do not be chatty—be professional.
"""

# --- AGENT ---
root_agent = Agent(
    name="spatial_engine_agent",
    model="gemini-3-pro-preview",
    description="An autonomous agent for spatial light reasoning and energy calculation.",
    instruction=SPATIAL_ENGINEER_PROMPT,
    tools=[calculate_lux_at_point, generate_optimization_report, calculate_roi_and_savings]
)

# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

# Agent Interaction
async def call_agent_async(query):
    print(f"User Query: {query}\n" + "-"*50)
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    print("Thinking...", end="", flush=True)

    async for event in events:
        print("\r", end="")
        try:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"\n🗣️ Agent: {part.text}")
                    if part.function_call:
                        print(f"\n🛠️ TOOL CALL: {part.function_call.name}")
                        print(f"   Args: {part.function_call.args}")
        except Exception as e:
            print(f"\n[Log]: Event processing detail: {e}")

    print("\n" + "="*50)
    print("🏁 Session Finished")
                

if __name__ == "__main__":
    # test_query = "I have a 20 sqm home office with only one 800 lumen bulb. It feels too dark for working. Calculate exactly how many lumens I am missing for standard office work (500 lux) and find me a suitable lamp on amazon."
    test_query = "I plan to replace ten 60W incandescent bulbs with 9W LEDs. They are on for 5 hours a day. Electricity costs $0.20 per kWh. Calculate my exact annual savings in dollars and CO2 reduction."
    
    asyncio.run(call_agent_async(test_query))