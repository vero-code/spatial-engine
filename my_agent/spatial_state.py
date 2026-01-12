# spatial_state.py
from typing import List, Dict
import json

class SpatialState:
    def __init__(self, area_sqm: float = 0.0, wall_reflection: float = 0.5):
        """
        area_sqm: Room area in sqm.
        wall_reflection: 0.1 (dark walls) to 0.9 (white walls). Default 0.5.
        """
        self.area_sqm = area_sqm
        self.wall_reflection = wall_reflection
        # List of dictionaries: [{'name': 'Ceiling Lamp', 'lumens': 800}, ...]
        self.light_sources: List[Dict] = [] 

    def update_geometry(self, area: float):
        """Update room area"""
        self.area_sqm = area
        print(f"[State Update] Room area set to {self.area_sqm} sqm")

    def add_light_source(self, name: str, lumens: float):
        """Add a light source (lamp or window)"""
        self.light_sources.append({"name": name, "lumens": lumens})
        print(f"[State Update] Added source: {name} ({lumens} lm)")

    def calculate_current_lux(self) -> float:
        """
        Simple physics engine (simplified):
        Lux = (Total Lumens * Reflection_Factor) / Area
        """
        if self.area_sqm <= 0:
            return 0.0
        
        total_lumens = sum(src['lumens'] for src in self.light_sources)
        
        # Simple formula with reflection factor (Room Cavity Ratio simplified)
        # If walls are white, more light.
        effective_lumens = total_lumens * (1 + self.wall_reflection * 0.5)
        
        lux = effective_lumens / self.area_sqm
        return round(lux, 2)

    def get_summary(self) -> str:
        """Generate text description for AI Agent"""
        lux = self.calculate_current_lux()
        sources_desc = ", ".join([f"{s['name']} ({s['lumens']}lm)" for s in self.light_sources])
        if not sources_desc:
            sources_desc = "None"
            
        return (
            f"--- ROOM STATE ---\n"
            f"Area: {self.area_sqm} sqm\n"
            f"Wall Reflection: {self.wall_reflection}\n"
            f"Active Sources: {sources_desc}\n"
            f"Current Light Level: {lux} LUX\n"
            f"------------------"
        )

# Small test, runs only if file is executed directly
if __name__ == "__main__":
    # 1. Initialize empty room
    room = SpatialState(area_sqm=20, wall_reflection=0.7) # White walls
    
    # 2. Add one lamp
    room.add_light_source("Main Chandelier", 1500)
    print(room.get_summary())
    
    # 3. Add desk lamp
    room.add_light_source("Desk Lamp", 800)
    print(room.get_summary())