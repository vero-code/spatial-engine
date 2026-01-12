# create_pdf.py
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'Technical Specification: UltraLED 5000', border=False, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(10)

pdf = PDF()
pdf.add_page()
pdf.set_font("helvetica", size=12)

# Text imitating real datasheet
text = """
Product Data Sheet
-----------------------------------
Model Name: UltraLED WorkLight Pro
Manufacturer: SpatialLighting Corp.

Electrical Characteristics:
- Power Consumption: 12 Watts
- Input Voltage: 220-240V
- Frequency: 50/60 Hz

Photometric Data:
- Luminous Flux: 1500 lumens
- Color Temperature: 4000K (Neutral White)
- Beam Angle: 120 degrees
- Color Rendering Index (CRI): >80

Application Notes:
Suitable for home offices, garages, and study rooms.
Replaces standard 100W incandescent bulb.
"""

pdf.multi_cell(0, 10, text)
pdf.output("data/datasheet.pdf")

print("✅ File datasheet.pdf successfully created!")