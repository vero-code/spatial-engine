import sys
import os
import base64
from PIL import Image
import io

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from my_agent.physics_engine import overlay_heatmap_on_image

def test_overlay_generation():
    print("Testing overlay generation...")
    
    # Create a dummy dark image
    img = Image.new('RGB', (800, 600), color = (50, 50, 50))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    img_bytes = buf.getvalue()
    
    # Define lamp positions (relative)
    lamps = [(0.2, 0.2), (0.8, 0.8), (0.5, 0.5)]
    
    # Generate overlay
    result_b64 = overlay_heatmap_on_image(img_bytes, lamp_positions=lamps)
    
    if result_b64:
        print("Success: Overlay generated (base64 string returned).")
        
        # Decode and save for manual inspection if needed
        with open("debug_overlay_test.png", "wb") as f:
            f.write(base64.b64decode(result_b64))
        print("Saved 'debug_overlay_test.png' for inspection.")
    else:
        print("Error: Overlay generation returned empty string.")

if __name__ == "__main__":
    test_overlay_generation()
