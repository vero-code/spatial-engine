# my_agent\agent.py
import os
import sys
import json
from pathlib import Path
import pypdf
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from spatial_state import SpatialState

from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from physics_engine import calculate_lux_at_point, generate_optimization_report, calculate_roi_and_savings
from market_agent import search_product_data

APP_NAME="spatial_engine_core"
USER_ID="engineer_01"
SESSION_ID="session_v1"

room_state = SpatialState()

# --- STATE TOOLS ---
def set_room_parameters(area_sqm: float, wall_reflection: float):
    """Sets room geometry. Reflection: 0.2 (Brick/Dark) to 0.8 (White/Mirrors)."""
    room_state.area_sqm = area_sqm
    room_state.wall_reflection = wall_reflection
    room_state.update_geometry(area_sqm)
    return f"State Updated: Area={area_sqm} sqm, Reflection={wall_reflection}."

def add_light_to_room(name: str, lumens: float):
    """Adds a light source to the internal spatial state."""
    room_state.add_light_source(name, lumens)
    return f"State Updated: Added {name} ({lumens} lm)."

def get_room_state():
    """Returns the current summary of the room: area, sources, and total lux."""
    return room_state.get_summary()

def search_market_tool(query: str):
    """
    Multipurpose Market Tool.
    1. Search for products: "Price of Philips LED 1500lm"
    2. Search for rates: "Electricity rate in New York"
    
    Returns JSON string with data.
    """
    print(f"\n[MAIN AGENT] 🛒 Market Request: '{query}'...")
    data = search_product_data(query)
    if "error" in data:
        return f"Market Error: {data['error']}"
    return json.dumps(data, indent=2)

def read_pdf_file(file_path: str) -> str:
    """Reads a PDF file from the given path."""
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."
        reader = pypdf.PdfReader(file_path)
        text = f"--- Content of {file_path} ---\n"
        for i, page in enumerate(reader.pages):
            text += f"[Page {i+1}]\n{page.extract_text()}\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def consult_standards_kb(topic: str) -> str:
    """
    Reads the Smart Home Standards Knowledge Base.
    Use this when user asks about Zigbee, Matter, Hubs, or compatibility.
    """
    kb_path = "data/smart_home_standards.md"
    try:
        if not os.path.exists(kb_path):
            return "Error: Knowledge Base file not found at data/smart_home_standards.md"
        
        print(f"\n[MAIN AGENT] 📖 Reading Standards for: '{topic}'...")
        with open(kb_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"--- KNOWLEDGE BASE ({topic}) ---\n{content}"
    except Exception as e:
        return f"Error reading KB: {str(e)}"

def generate_scenarios_config(room_name: str) -> str:
    """
    Generates a JSON configuration for Smart Home Hubs (Home Assistant/HomeKit).
    Creates presets: Focus, Relax, Movie.
    """
    lights = [src['name'] for src in room_state.light_sources]
    if not lights:
        lights = ["Main Ceiling Light"] # Fallback

    config = {
        "room": room_name,
        "generated_by": "Spatial Engine AI",
        "devices": lights,
        "scenes": {
            "morning_focus": {
                "brightness_pct": 100,
                "color_temp_kelvin": 4500,
                "description": "High blue-light content for wakefulness"
            },
            "work_day": {
                "brightness_pct": 80,
                "color_temp_kelvin": 4000,
                "description": "Neutral white for standard tasks"
            },
            "evening_relax": {
                "brightness_pct": 50,
                "color_temp_kelvin": 2700,
                "description": "Warm white to simulate sunset"
            },
            "night_movie": {
                "brightness_pct": 20,
                "color_temp_kelvin": 2000,
                "description": "Very warm, dim light to preserve melatonin"
            }
        }
    }
    
    return json.dumps(config, indent=2)

# --- SYSTEM PROMPT ---
SPATIAL_ENGINEER_PROMPT = """
You are the Spatial Engine AI. You combine Optical Physics, Economics, Smart Home Standards, and Configuration Logic.

CORE PROTOCOL:

1. **VISUAL/STATE AUDIT**: 
   - Analyze the room (Area, Materials).
   - CALL `set_room_parameters`.
   - CALL `get_room_state` to check Lux levels.

2. **COMPATIBILITY CHECK**:
   - If recommending smart lights (Hue, Zigbee, Matter), CALL `consult_standards_kb`.
   - Verify: Does the user need a Hub? Is the dimmer compatible?
   - Warn the user strictly if extra hardware is needed.

3. **PROCUREMENT**:
   - **Step A (Product)**: Find a suitable lamp. Query example: "Price of 1600 lumen LED bulb Philips".
     - Extract `price_usd` and `watts`.
   - **Step B (Rates)**: Find local electricity cost. Query example: "Electricity rate in New York".
     - Extract `rate_usd_kwh`.

4. **FINANCIAL ANALYSIS**:
   - CALL `calculate_roi_and_savings`.
   - Inputs:
     - `old_watts`: Assume 60W or 100W if replacing old bulbs.
     - `new_watts`: From Step A.
     - `new_bulb_price`: From Step A.
     - `kwh_cost_usd`: From Step B (default 0.17 if search fails).

5. **CONFIGURATION**:
   - If the user asks for "setup", "scenes", "config", or "JSON", CALL `generate_scenarios_config`.
   - Output the JSON block clearly.

6. **REPORTING**:
   - Summarize Physics (Lux).
   - Summarize Economics (ROI).
   - Summarize Compatibility (Hubs).
   - Provide Config if requested.
"""

# --- AGENT ---
root_agent = Agent(
    name="spatial_engine_agent",
    model="gemini-3-pro-preview",
    description="Spatial AI with Physics, Market Logic, and Standards Knowledge.",
    instruction=SPATIAL_ENGINEER_PROMPT,
    tools=[
        calculate_lux_at_point,
        generate_optimization_report,
        calculate_roi_and_savings,
        set_room_parameters,
        add_light_to_room,
        get_room_state,
        read_pdf_file,
        search_market_tool,
        consult_standards_kb,
        generate_scenarios_config
    ]
)

# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

# Agent Interaction
async def call_agent_async(query, image_path=None):
    print(f"User Query: {query}\n" + "="*50)
    parts = [types.Part(text=query)]
    if image_path:
        path = Path(image_path)
        if path.exists():
            image_data = path.read_bytes()
            parts.append(types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_data)))
    
    content = types.Content(role='user', parts=parts)
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    print("Thinking...", end="", flush=True)
    async for event in events:
        print("\r", end="")
        try:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text: print(f"\n🗣️ Agent: {part.text}")
                    if part.function_call:
                        print(f"\n🛠️ TOOL CALL: {part.function_call.name}")
                        print(f"   Args: {part.function_call.args}")
        except Exception as e:
            print(f"\n[Log]: Event error: {e}")
    print("\n" + "="*50)

if __name__ == "__main__":
    # test_query = "I have a 20 sqm home office with only one 800 lumen bulb. It feels too dark for working. Calculate exactly how many lumens I am missing for standard office work (500 lux) and find me a suitable lamp on amazon."
    # test_query = "I plan to replace ten 60W incandescent bulbs with 9W LEDs. They are on for 5 hours a day. Electricity costs $0.20 per kWh. Calculate my exact annual savings in dollars and CO2 reduction."

    # asyncio.run(call_agent_async(test_query))
    
    # Image Test
    # test_image = "test_room.png"
    
    # query = """
    # Look at this image.
    # 1. Estimate the room area (sqm).
    # 2. Identify the wall material.
    # 3. Calculate the lumen deficit for a standard Home Office (500 lux), assuming current lighting is 0.
    # """

    # if os.path.exists(test_image):
    #     asyncio.run(call_agent_async(query, image_path=test_image))
    # else:
    #     print("⚠️ Image not found, running text test...")
    #     asyncio.run(call_agent_async("Calculate ROI for switching 60W to 9W LEDs."))

    # PDF Test
    # pdf_file = "data/datasheet.pdf"
    
    # query = f"""
    # Read the technical specs from {pdf_file}.
    # Based on the 'Luminous Flux' found in the file, would one such lamp be enough 
    # to light up a 10 sqm room to a level of 300 lux? 
    # Calculate and explain.
    # """

    # if os.path.exists(pdf_file):
    #     asyncio.run(call_agent_async(query))
    # else:
    #     print("⚠️ PDF file not found!")

    # Comprehensive loop logic test
    # pdf_file = "data/datasheet.pdf"
    
    # query = f"""
    # I have a dark room (approx 15 sqm, white walls) with no lights currently.
    # I am considering buying the lamp from {pdf_file}.
    
    # Please:
    # 1. Set up the room parameters (Area and Material).
    # 2. Read the PDF and add that lamp to the room state.
    # 3. Tell me the final Lux level from the state and if it is good for reading (needs 300+ Lux).
    # """

    # if os.path.exists(pdf_file):
    #     asyncio.run(call_agent_async(query))
    # else:
    #     print("⚠️ File not found, run create_pdf.py first!")

    # INTEGRATION TEST
    # query = """
    # I have a dark 15 sqm room with white walls and one old 100W bulb.
    
    # Please:
    # 1. Update the room state.
    # 2. Find a Philips LED bulb (1500+ lumens) and the current electricity rate in New York.
    # 3. Calculate the ROI if I switch to this new bulb using the specific New York rate.
    # """

    # asyncio.run(call_agent_async(query))

    # TEST TASK 24: Verification of standards
    # query = """
    # I want to buy Philips Hue bulbs for my home office. 
    # 1. Do I need extra hardware for them to work reliably?
    # 2. Can I use my existing wall dimmer switch?
    # Check your knowledge base for standards.
    # """
    # asyncio.run(call_agent_async(query))

    # TEST TASK 25: Generate Smart Home config
    query = """
    I have updated my room with a Philips Hue bulb.
    Please generate a JSON configuration file for my Home Assistant 
    with scenes for working, relaxing, and watching movies.
    """
    asyncio.run(call_agent_async(query))