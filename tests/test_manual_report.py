import requests
import base64
import json

def test_export_report():
    url = "http://localhost:8000/api/export-report"
    
    # Mock Data
    mock_data = {
        "project_name": "Test Project",
        "timestamp": "2023-10-27 10:00:00",
        "area_sqm": 20.0,
        "lux_level": 450.5,
        "target_lux": 500.0,
        "energy_savings_annual": 120.50,
        "co2_reduction": 50.2,
        "payback_months": 8.5,
        "physics_heatmap_image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
        "vision_heatmap_image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
        "roi_chart_image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    }
    
    try:
        response = requests.post(url, json=mock_data)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response Headers:", response.headers['content-type'])
            content_preview = response.text[:100]
            print(f"Content Preview: {content_preview}")
            
            if "<!DOCTYPE html>" in response.text and "Visual Light Analysis" in response.text:
                print("✅ TEST PASSED: Valid HTML received.")
            else:
                print("❌ TEST FAILED: Response does not look like the expected HTML.")
        else:
            print(f"❌ TEST FAILED: Backend returned {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ TEST FAILED: Could not connect to localhost:8000. Is the backend running?")

if __name__ == "__main__":
    test_export_report()
