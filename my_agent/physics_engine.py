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

def generate_light_distribution_heatmap(lumens: float, distance_meters: float, beam_angle_degrees: float) -> str:
    """
    Generates a visual heatmap of the light distribution on the floor.
    Returns: Base64 encoded PNG string.
    """
    import matplotlib
    matplotlib.use('Agg') # Non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np
    import io
    import base64

    print(f"[PHYSICS ENGINE]: Generating Heatmap for {lumens}lm...")

    # Grid setup (Floor area 6x6 meters)
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    
    # Calculate distance from center (0,0) on the floor
    # We assume the light is at (0,0, distance_meters)
    # Distance from light point to grid point (x,y,0)
    # d = sqrt(x^2 + y^2 + h^2)
    # But for lux simply: E = I / d^2 * cos(theta)
    # approximate spot logic:
    
    R_floor = np.sqrt(X**2 + Y**2) # Distance from center on floor
    D_light = np.sqrt(R_floor**2 + distance_meters**2) # Slant range
    
    # Cosine of angle of incidence (theta)
    # cos(theta) = adjacent / hypotenuse = distance_meters / D_light
    cos_theta = distance_meters / D_light
    
    # Beam angle cutoff
    # If angle of point > beam_angle/2, intensity drops (simplified)
    # angle_of_point = arccos(cos_theta)
    angle_of_point_rad = np.arccos(cos_theta)
    beam_cutoff_rad = np.radians(beam_angle_degrees / 2)
    
    # Intensity (Candela) distribution (Simplified Lambertian-ish within beam)
    # I = I0 * cos(angle_of_point) ?? Generic approximation
    # Let's assume uniform intensity I within beam for simplicity, or slightly peaked.
    # Solid Angle = 2pi(1 - cos(beam/2))
    solid_angle = 2 * np.pi * (1 - np.cos(beam_cutoff_rad))
    I_avg = lumens / solid_angle
    
    # Simple falloff model: E = (I / D^2) * cos(theta)
    # Only if angle_of_point < beam_cutoff
    
    Illuminance = (I_avg / (D_light**2)) * cos_theta
    
    # Apply cutoff
    start_fade = beam_cutoff_rad * 0.8
    # Soft mask
    mask = np.clip((beam_cutoff_rad - angle_of_point_rad) / (beam_cutoff_rad - start_fade), 0, 1)
    Illuminance = Illuminance * mask

    # Plotting
    fig, ax = plt.subplots(figsize=(6, 5), facecolor='black')
    ax.set_facecolor('black')
    
    # Countourf
    levels = np.linspace(0, np.max(Illuminance), 20)
    if np.max(Illuminance) == 0: levels = 10 # avoid error
    
    contour = ax.contourf(X, Y, Illuminance, levels=levels, cmap='plasma')
    
    # Styling
    ax.set_title(f"Light Distribution ({int(lumens)} lm @ {distance_meters}m)", color='white', pad=20)
    ax.set_xlabel("Meters (X)", color='gray')
    ax.set_ylabel("Meters (Y)", color='gray')
    ax.spines['bottom'].set_color('gray')
    ax.spines['left'].set_color('gray')
    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')
    ax.grid(color='white', alpha=0.1, linestyle='--')
    
    # Colorbar
    cbar = plt.colorbar(contour)
    cbar.set_label('Illuminance (Lux)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return img_str

def generate_roi_chart(old_watts: float, new_watts: float, price: float, hours: float, rate: float) -> str:
    """
    Generates a cumulative cost comparison chart (ROI Payback).
    Returns: Base64 encoded PNG string.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import io
    import base64
    
    print(f"[PHYSICS ENGINE]: Generating ROI Chart...")
    
    # Timeline: 3 years (36 months)
    months = np.arange(0, 37, 1)
    
    # Monthly cost calculation
    # Energy (kWh) per month = (Watts * Hours * 30) / 1000
    kwh_month_old = (old_watts * hours * 30) / 1000
    cost_month_old = kwh_month_old * rate
    
    kwh_month_new = (new_watts * hours * 30) / 1000
    cost_month_new = kwh_month_new * rate
    
    # Cumulative Costs
    # Old: Start at 0 (already own it), accum cost
    cum_cost_old = months * cost_month_old
    
    # New: Start at Price (Initial Investment), accum cost
    cum_cost_new = price + (months * cost_month_new)
    
    # Plotting
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='#0d1117')
    ax.set_facecolor('#0d1117')
    
    ax.plot(months, cum_cost_old, color='#ff4d4d', linestyle='--', label='Current Bulbs (Inefficient)')
    ax.plot(months, cum_cost_new, color='#00ff9d', linewidth=2, label='Upgrade (Efficient)')
    
    # Highlight Intersection (Payback Point)
    # Find where New < Old
    idx = np.argwhere(cum_cost_new < cum_cost_old)
    if len(idx) > 0:
        payback_month = months[idx[0][0]]
        payback_cost = cum_cost_new[idx[0][0]]
        ax.plot(payback_month, payback_cost, 'wo', markersize=8)
        ax.annotate(f'Payback: {payback_month} mo', 
                    xy=(payback_month, payback_cost), 
                    xytext=(payback_month + 2, payback_cost - 10),
                    color='white',
                    arrowprops=dict(arrowstyle='->', color='white'))
        
        # Fill area between curves to show savings
        ax.fill_between(months, cum_cost_old, cum_cost_new, where=(months >= payback_month), interpolate=True, color='#00ff9d', alpha=0.1)

    # Styling
    ax.set_title("Return on Investment (ROI) Timeline", color='white', pad=15)
    ax.set_xlabel("Months", color='gray')
    ax.set_ylabel("Cumulative Cost ($)", color='gray')
    
    ax.spines['bottom'].set_color('gray')
    ax.spines['left'].set_color('gray')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.tick_params(axis='x', colors='gray')
    ax.tick_params(axis='y', colors='gray')
    ax.grid(color='white', alpha=0.05, linestyle='--')
    
    legend = ax.legend(loc='upper left', facecolor='#0d1117', edgecolor='gray')
    plt.setp(legend.get_texts(), color='gray')
    
    # Save
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    
    return base64.b64encode(buf.read()).decode('utf-8')

def generate_consumption_chart(old_watts: float, new_watts: float, hours_per_day: float = 5.0) -> str:
    """
    Generates a bar chart comparing annual energy consumption (kWh).
    Returns: Base64 encoded PNG string.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import io
    import base64

    print(f"[PHYSICS ENGINE]: Generating Consumption Chart...")

    # Calculate Annual kWh
    kwh_old = (old_watts * hours_per_day * 365) / 1000
    kwh_new = (new_watts * hours_per_day * 365) / 1000
    
    # Data
    labels = ['Before (Legacy)', 'After (Upgrade)']
    values = [kwh_old, kwh_new]
    colors = ['#ff4d4d', '#00ff9d'] # Red for bad, Green for good

    # Plotting
    fig, ax = plt.subplots(figsize=(5, 4), facecolor='#0d1117')
    ax.set_facecolor('#0d1117')
    
    # Create Bars
    bars = ax.bar(labels, values, color=colors, width=0.5)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + (max(values)*0.02),
                f'{int(height)} kWh',
                ha='center', va='bottom', color='white', fontweight='bold')

    # Styling
    ax.set_title("Annual Energy Consumption", color='white', pad=15)
    ax.set_ylabel("Energy (kWh / Year)", color='gray')
    
    ax.spines['bottom'].set_color('gray')
    ax.spines['left'].set_color('gray')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='gray')
    
    # Y limit padding
    ax.set_ylim(0, max(values) * 1.2)
    
    # Save
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    
    return base64.b64encode(buf.read()).decode('utf-8')

def overlay_heatmap_on_image(image_bytes: bytes, lamp_positions: list = None) -> str:
    """
    Overlays a light distribution heatmap AND a technical measurement grid.
    Matches the style of a CAD/Engineering interface.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import io
    import base64
    from PIL import Image

    print(f"[PHYSICS ENGINE]: Processing Vision Audit - Overlaying Heatmap & Tech Grid...")

    try:
        # Load Image
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        w, h = img.size
        
        # Create figure matching image aspect ratio
        # DPI = 100 ensures readable font size relative to image
        dpi = 100
        fig, ax = plt.subplots(figsize=(w/dpi, h/dpi), dpi=dpi)
        
        # --- 1. Draw Background Image ---
        # extent sets the coordinate system [left, right, bottom, top]
        # We invert Y (h, 0) to match image coordinates (0,0 is top-left)
        ax.imshow(img, extent=[0, w, h, 0])
        
        # --- 2. Generate Heatmap Logic ---
        y_indices, x_indices = np.mgrid[0:h, 0:w]
        cy, cx = h // 2, w // 2
        dist_sq = (x_indices - cx)**2 + (y_indices - cy)**2
        sigma = min(w, h) / 3 
        heatmap_data = np.exp(-dist_sq / (2 * sigma**2))
        
        # Overlay Heatmap (Transparent)
        ax.imshow(heatmap_data, cmap='plasma', alpha=0.35, extent=[0, w, h, 0])

        # Add Contour Lines (Isolux Contour Map)
        # "Isolux" means lines of equal illuminance
        levels = np.linspace(0.1, 1.0, 10) 
        CS = ax.contour(heatmap_data, levels=levels, extent=[0, w, h, 0], 
                   colors='white', alpha=0.3, linewidths=0.5)
        ax.clabel(CS, inline=True, fontsize=6, fmt='%.1f', colors='white')
        
        # --- 2.1 Draw "Decided" Lamp Positions ---
        if lamp_positions:
            # lamp_positions is expected to be a list of (x, y) tuples
            # If values are <= 1.0, treat as relative coordinates.
            # If > 1.0, treat as pixel coordinates.
            
            lx_coords = []
            ly_coords = []
            
            for (lx, ly) in lamp_positions:
                if lx <= 1.0 and ly <= 1.0:
                    lx_coords.append(lx * w)
                    ly_coords.append(ly * h)
                else:
                    lx_coords.append(lx)
                    ly_coords.append(ly)
            
            # Draw markers
            # 'x' marker, yellow color, with a slight glow effect (halo)
            # Halo
            ax.scatter(lx_coords, ly_coords, s=150, c='black', marker='x', linewidths=3, alpha=0.5)
            # Core
            ax.scatter(lx_coords, ly_coords, s=100, c='#FFD700', marker='x', linewidths=2, label='Proposed Lamp')
            
            # Add labels
            for i, (lx, ly) in enumerate(zip(lx_coords, ly_coords)):
                ax.text(lx + 15, ly - 15, f"LAMP {i+1}", color='#FFD700', fontsize=8, fontweight='bold')
        
        # --- 3. Engineering Grid Styling (The "Tech" Look) ---
        
        # Enable Grid
        # alpha=0.2 makes it barely visible (Clean Look)
        ax.grid(True, which='both', color='white', linestyle='-', linewidth=0.5, alpha=0.2)
        
        # Configure Ticks (The Numbers)
        ax.tick_params(axis='both', which='both', colors='white', labelsize=6, direction='in')
        
        # Configure Spines (The Border Box)
        for spine in ax.spines.values():
            spine.set_edgecolor('white')
            spine.set_linewidth(0.5)
            spine.set_alpha(0.5) # Semi-transparent border
            
        # Optional: Add Label Units
        ax.set_xlabel("X Coordinates (px)", color='white', fontsize=6, alpha=0.5)
        ax.set_ylabel("Y Coordinates (px)", color='white', fontsize=6, alpha=0.5)
        
        # Ensure tight layout to remove extra whitespace around the plot
        plt.tight_layout(pad=0.5)

        # Save to buffer
        buf = io.BytesIO()
        # transparent=False is important here to keep the black/dark theme of the plot if needed, 
        # but transparent=True is better for overlaying on UI. 
        # Let's keep transparent=True so only the content is saved.
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        plt.close(fig)
        buf.seek(0)
        
        return base64.b64encode(buf.read()).decode('utf-8')

    except Exception as e:
        print(f"[PHYSICS ENGINE]: Error in overlay - {e}")
        return ""

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

def calculate_roi_and_savings(
    old_watts: float,
    new_watts: float,
    new_bulb_price: float = 0.0,
    hours_per_day: float = 5.0,
    kwh_cost_usd: float = 0.17,
    count: int = 1
) -> str:
    """
    Calculates energy savings and ROI for switching to efficient lighting for multiple bulbs.
    Now includes Payback Period and count support.

    Args:
        old_watts: Wattage of the current bulb (e.g., 60W incandescent).
        new_watts: Wattage of the replacement bulb (e.g., 9W LED).
        new_bulb_price: Price of ONE replacement bulb.
        hours_per_day: Average usage hours.
        kwh_cost_usd: Cost of electricity per kWh (default $0.17).
        count: Number of bulbs to replace.
        
    Returns:
        JSON string with annual savings and ROI analysis.
    """
    print(f"\n[PHYSICS ENGINE]: Calculating ROI (Old: {old_watts}W vs New: {new_watts}W, Count: {count})...")
    
    # Calculate the difference in consumption (kW) for ONE bulb
    watts_saved_per_bulb = old_watts - new_watts
    kwh_saved_daily_per_bulb = (watts_saved_per_bulb * hours_per_day) / 1000
    kwh_saved_annual_total = kwh_saved_daily_per_bulb * 365 * count
    
    # Calculate the money
    money_saved_annual_total = kwh_saved_annual_total * kwh_cost_usd
    total_investment = new_bulb_price * count

    co2_saved_kg_total = kwh_saved_annual_total * 0.385  # Average emission coefficient
    
    # Payback Period (remains same if both cost and savings scale linearly)
    payback_months = 0.0
    if total_investment > 0 and money_saved_annual_total > 0:
        years_to_payback = total_investment / money_saved_annual_total
        payback_months = round(years_to_payback * 12, 1)

    data = {
        "annual_savings_usd": round(money_saved_annual_total, 2),
        "payback_period_months": payback_months,
        "kwh_saved_year": round(kwh_saved_annual_total, 1),
        "co2_reduction_kg": round(co2_saved_kg_total, 1),
        "lamp_count": count,
        "total_investment": round(total_investment, 2),
        "message": f"Replacing {count} bulbs saves ${round(money_saved_annual_total, 2)} per year and reduces CO2 by {round(co2_saved_kg_total, 1)}kg."
    }
    
    print(f"[PHYSICS ENGINE]: ROI Calculated for {count} bulbs. Payback: {payback_months} months.")
    return json.dumps(data)

def check_health_compliance(lux_level: float, room_type: str = "office") -> str:
    """
    Verifies if the lighting meets ISO/SanPiN health standards.
    room_type: 'office', 'living_room', 'corridor', 'kitchen'.
    Returns a PASS/FAIL verdict with specific deficit calculation.
    """
    standards = {
        "office": 500,
        "kitchen": 300,
        "living_room": 150,
        "corridor": 100,
        "bedroom": 150
    }
    
    r_type = room_type.lower()
    if "office" in r_type or "work" in r_type: target = 500
    elif "living" in r_type: target = 150
    else: target = standards.get(r_type, 300)
    
    if lux_level >= target:
        return f"✅ PASS: {lux_level:.1f} Lux meets the standard for {room_type} (Target: {target} Lux)."
    else:
        deficit = target - lux_level
        return f"⚠️ FAIL: {lux_level:.1f} Lux is unsafe for {room_type}. Target is {target} Lux. You need +{deficit:.1f} Lux to avoid eye strain."

if __name__ == "__main__":
    print("--- TESTING ROI CALCULATOR ---")
    result = calculate_roi_and_savings(
        old_watts=100,
        new_watts=14,
        new_bulb_price=4.99
    )
    print(result)