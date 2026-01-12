# my_agent\agent.py
import os
import sys
from pathlib import Path
import pypdf

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from spatial_state import SpatialState

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

room_state = SpatialState()

def set_room_parameters(area_sqm: float, wall_reflection: float):
    """
    Sets the room's physical parameters in the state.
    area_sqm: Estimated floor area in square meters.
    wall_reflection: 0.2 (Brick/Dark) to 0.8 (White/Mirrors). Default is 0.5.
    """
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

def read_pdf_file(file_path: str) -> str:
    """Reads a PDF file from the given path and returns its text content."""
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

# --- SYSTEM PROMPT ---
SPATIAL_ENGINEER_PROMPT = """
You are the Spatial Engine AI, a Senior Optical Physicist.

CORE PROTOCOL:

1. **VISUAL AUDIT (Step-by-Step)**:
   - **Grid Analysis**: Mentally divide the image into a 3x3 grid.
   - **Materials**: Identify wall reflection (High: White paint=0.8 / Low: Brick=0.2).
   - **Geometry**: Estimate floor area (sqm) based on standard furniture scale.
   
   >>> **CRITICAL ACTION**: Immediately call `set_room_parameters(area_sqm, wall_reflection)` to SAVE these findings.

2. **LIGHT SOURCE AUDIT**:
   - Identify windows or lamps.
   - For each source, estimate lumens (Window=1000-5000, Bulb=800).
   
   >>> **CRITICAL ACTION**: Call `add_light_to_room(name, lumens)` for EACH source found.

3. **DOCUMENT ANALYSIS** (If PDF provided):
   - Use `read_pdf_file`. If a new lamp is found, call `add_light_to_room` to simulate installing it.

4. **PHYSICS VERIFICATION**:
   - Call `get_room_state` to retrieve the mathematically accurate Lux level.
   - DO NOT calculate manually. Trust the State Tool.

5. **REPORTING**:
   - Start with "Visual Scan Results" (Grid, Materials).
   - Provide the "Physics Report" from the State.
   - If Lux < 500, recommend solutions.
"""

# --- AGENT ---
root_agent = Agent(
    name="spatial_engine_agent",
    model="gemini-3-pro-preview",
    description="An autonomous agent for spatial light reasoning, energy calculation, and document analysis.",
    instruction=SPATIAL_ENGINEER_PROMPT,
    tools=[
        calculate_lux_at_point, 
        generate_optimization_report, 
        calculate_roi_and_savings, 
        read_pdf_file,
        set_room_parameters,
        add_light_to_room,
        get_room_state
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
            print(f"📎 Attaching image: {image_path} ({path.stat().st_size} bytes)")
            image_data = path.read_bytes()
            parts.append(types.Part(
                inline_data=types.Blob(
                    mime_type="image/jpeg",
                    data=image_data
                )
            ))
        else:
            print(f"⚠️ Error: Image file '{image_path}' not found!")

    print("="*50)

    content = types.Content(role='user', parts=parts)
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
    pdf_file = "data/datasheet.pdf"
    
    query = f"""
    I have a dark room (approx 15 sqm, white walls) with no lights currently.
    I am considering buying the lamp from {pdf_file}.
    
    Please:
    1. Set up the room parameters (Area and Material).
    2. Read the PDF and add that lamp to the room state.
    3. Tell me the final Lux level from the state and if it is good for reading (needs 300+ Lux).
    """

    if os.path.exists(pdf_file):
        asyncio.run(call_agent_async(query))
    else:
        print("⚠️ File not found, run create_pdf.py first!")