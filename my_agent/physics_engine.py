# my_agent\physics_engine.py
import math
import json

def calculate_lux_at_point(light_lumens: float, distance_meters: float, beam_angle_degrees: float = 120) -> str:
    """
    Calculates Illuminance (Lux) at a specific point based on Inverse Square Law.
    
    Args:
        light_lumens: The total luminous flux of the light source (e.g., 800 for a standard LED).
        distance_meters: Distance from light source to the surface.
        beam_angle_degrees: The angle of the light beam (default 120 for standard bulbs).
        
    Returns:
        float: Lux level at the target surface.
    """
    print(f"\n[PHYSICS ENGINE]: Calculating Lux for {light_lumens}lm at {distance_meters}m...")

    if distance_meters <= 0:
        return "0.0"
    
    # 1. Calculate Candelas (Intensity) based on Beam Angle
    # Formula approximation for Lambertian source
    solid_angle = 2 * math.pi * (1 - math.cos(math.radians(beam_angle_degrees) / 2))
    candela = light_lumens / solid_angle
    
    # 2. Apply Inverse Square Law (E = I / d^2)
    lux = candela / (distance_meters ** 2)
    
    result = round(lux, 2)
    print(f"[PHYSICS ENGINE]: Result = {result} lux")
    return str(result)

def generate_optimization_report(room_area_sqm: float, target_lux: int, current_lumens: int) -> str:
    """
    Analyzes the gap between current lighting and required standards.
    Returns a structured dictionary for the engineering report.
    """
    print(f"\n[PHYSICS ENGINE]: Generating Report for {room_area_sqm}m2, Target: {target_lux} lux...")

    required_total_lumens = room_area_sqm * target_lux
    deficiency = required_total_lumens - current_lumens
    
    # How many more 800lm bulbs do we need?
    bulbs_needed = math.ceil(max(0, deficiency) / 800)
    
    data = {
        "status": "Optimization Required" if deficiency > 0 else "Optimal",
        "analysis": {
             "current_lux_avg": round(current_lumens / room_area_sqm, 1),
             "target_lux": target_lux,
             "room_area": room_area_sqm
        },
        "deficiency_lumens": round(max(0, deficiency), 1),
        "engineering_recommendation": f"CRITICAL DEFICIT. You need {bulbs_needed} more light sources (approx 800lm each) to reach safe working standards."
    }

    print(f"[PHYSICS ENGINE]: Report Generated. Deficit: {deficiency}")
    return json.dumps(data)