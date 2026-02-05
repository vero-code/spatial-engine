import requests
import base64
import os
import sys
from datetime import datetime

# URL of the running API
API_URL = "http://localhost:8000/api/export-pdf"

def test_pdf_export():
    print("Testing PDF Export API...")

    # Create dummy base64 image (1x1 pixel red dot)
    # This acts as a placeholder for heatmaps/charts
    dummy_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

    payload = {
        "project_name": "Test PDF Project",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "area_sqm": 50.0,
        "lux_level": 450.0,
        "target_lux": 500.0,
        "energy_savings_annual": 1200.50,
        "co2_reduction": 500.25,
        "payback_months": 8.5,
        "physics_heatmap_image": dummy_image,
        "vision_heatmap_image": dummy_image,
        "roi_chart_image": dummy_image,
        "consumption_chart_image": dummy_image
    }

    try:
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            print("✅ API returned 200 OK")
            
            content_type = response.headers.get("Content-Type")
            if content_type == "application/pdf":
                print("✅ Content-Type is application/pdf")
            else:
                print(f"❌ Unexpected Content-Type: {content_type}")

            # Save the file
            output_file = "test_output_report.pdf"
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            file_size = os.path.getsize(output_file)
            if file_size > 0:
                 print(f"✅ PDF file saved successfully ({file_size} bytes)")
            else:
                 print("❌ Saved PDF file is empty")
                 
        else:
            print(f"❌ API Request Failed. Status: {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Is the server running on port 8000?")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    test_pdf_export()
