from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, Response
from typing import Optional
import json
import os
import sys

# Ensure my_agent is in the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_agent.physics_engine import (
    calculate_lux_at_point, 
    generate_optimization_report, 
    calculate_roi_and_savings, 
    check_health_compliance,
    generate_light_distribution_heatmap,
    generate_roi_chart,
    generate_consumption_chart,
    overlay_heatmap_on_image
)

app = FastAPI(title="Spatial Engine AI API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def read_root():
#     return {"status": "Spatial Engine API Online", "version": "1.0.4"}

@app.post("/api/lux-calculation")
def api_calculate_lux(lumens: float, distance: float, angle: float = 120.0):
    """Calculates Lux using the Physics Engine."""
    result = calculate_lux_at_point(lumens, distance, angle)
    heatmap = generate_light_distribution_heatmap(lumens, distance, angle)
    return {"lux": float(result), "heatmap_image": heatmap}

@app.post("/api/optimization-report")
def api_optimization_report(area: float, target_lux: int, current_lumens: int):
    """Generates an optimization strategy report."""
    report_json = generate_optimization_report(area, target_lux, current_lumens)
    return json.loads(report_json)

@app.post("/api/roi-analysis")
def api_roi_analysis(
    old_watts: float, 
    new_watts: float, 
    price: float, 
    hours: float, 
    rate: float,
    count: int = 1
):
    """Calculates ROI and energy savings."""
    roi_json = calculate_roi_and_savings(
        old_watts=old_watts,
        new_watts=new_watts,
        new_bulb_price=price,
        hours_per_day=hours,
        kwh_cost_usd=rate,
        count=count
    )
    roi_data = json.loads(roi_json)
    
    # Generate Chart
    chart = generate_roi_chart(old_watts, new_watts, price, hours, rate)
    roi_data["roi_chart_image"] = chart
    
    # Generate Consumption Chart
    consumption_chart = generate_consumption_chart(old_watts, new_watts, hours)
    roi_data["consumption_chart_image"] = consumption_chart
    
    return roi_data

@app.post("/api/health-compliance")
def api_health_check(lux: float, room_type: str = "office"):
    """Checks if the lighting meets ISO/SanPiN health standards."""
    verdict = check_health_compliance(lux, room_type)
    return {"verdict": verdict, "compliant": "PASS" in verdict}

@app.post("/api/spatial-audit")
async def api_spatial_audit(file: UploadFile = File(...)):
    """
    Simulates a multimodal spatial audit.
    In a real implementation, this would call the Gemini vision model.
    """
    # Read file for processing
    contents = await file.read()
    
    # Generate Overlay
    # Mocking Agent Decision: Placing lamps at logical points
    # Randomized to simulate "Recalculate" feature
    import random
    num_lamps = random.randint(2, 4)
    mock_lamp_decisions = [(random.uniform(0.2, 0.8), random.uniform(0.2, 0.8)) for _ in range(num_lamps)]
    
    overlay_b64 = overlay_heatmap_on_image(contents, lamp_positions=mock_lamp_decisions)

    # Mock response mirroring the script.js logic for now
    return {
        "status": "success",
        "area_sqm": 18.5,
        "reflection": 0.45,
        "vision_data": {
            "sectors": "3x3 Grid Analysis complete",
            "material": "Dark Oak / Paint",
            "reference_object": "Door Frame",
            "heatmap_overlay": overlay_b64
        }
    }

from backend.report_generator import ReportRequest, generate_html_report
from fastapi.responses import HTMLResponse, Response
from backend.pdf_generator import generate_pdf_report

@app.post("/api/export-report")
def api_export_report(request: ReportRequest):
    """Generates a downloadable HTML Engineering Report."""
    html_content = generate_html_report(request)
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/api/export-pdf")
def api_export_pdf(request: ReportRequest):
    """Generates a downloadable PDF Engineering Report."""
    pdf_bytes = generate_pdf_report(request)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Engineering_Report.pdf"}
    )

# --- FRONTEND SERVING ---
if os.path.exists("frontend/dist/assets"):
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    file_path = os.path.join("frontend/dist", full_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    return FileResponse("frontend/dist/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
