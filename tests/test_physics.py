import unittest
import json
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.join(parent_dir, 'my_agent'))

from physics_engine import calculate_lux_at_point, generate_optimization_report, calculate_roi_and_savings

class TestSpatialPhysics(unittest.TestCase):
    
    # Test 1: Lux calculation
    def test_lux_calculation_basic(self):
        """Check: 800 lm at 1 meter should yield ~254 lux."""
        # Formula: 800 / (2*pi*(1-cos(60))) / 1^2
        result = float(calculate_lux_at_point(800, 1.0))
        # Check if result is within expected range (250-260)
        self.assertTrue(250 < result < 260, f"Expected ~254 lux, got {result}")

    # Test 2: Zero distance protection
    def test_lux_zero_distance(self):
        """Check: division by zero should return '0.0', not an error."""
        result = calculate_lux_at_point(800, 0)
        self.assertEqual(result, "0.0")

    # Test 3: ROI calculation
    def test_roi_calculation_logic(self):
        """Check: does replacing 60W with 9W save money?"""
        # Manually calculate for one bulb:
        # Difference 51 W. 5 hours per day. 365 days. $0.20 per kWh
        # 0.051 kW * 5 * 365 * 0.20 = $18.615
        
        response = calculate_roi_and_savings(60, 9, hours_per_day=5, kwh_cost_usd=0.20)
        data = json.loads(response)
        
        print(f"\n[TEST INFO] Calculated Savings: ${data['annual_savings_usd']}")
        
        # Check if program calculated around $18.62
        self.assertAlmostEqual(data['annual_savings_usd'], 18.62, delta=0.1)

    # Test 4: Report structure
    def test_optimization_report_structure(self):
        """Check: function returns valid JSON with recommendations."""
        response = generate_optimization_report(20, 500, 800)
        data = json.loads(response)
        
        # Check if response contains key fields
        self.assertIn("engineering_recommendation", data)
        self.assertIn("deficiency_lumens", data)
        # For 20m2 and 500 lux, 10000 lumens are needed. There are 800. Deficit should be > 0
        self.assertTrue(data["deficiency_lumens"] > 0)

if __name__ == '__main__':
    unittest.main()