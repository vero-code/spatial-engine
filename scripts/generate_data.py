import csv
import os

# Ensure the 'data' directory exists
os.makedirs("data", exist_ok=True)

# Data transcribed from the video screenshot
data = [
    ["Date", "Customer_ID", "Customer_Name", "Plan_Tier", "MRR", "Region", "Churn_Status", "Churn_Date"],
    ["2024-01-03", "1001", "Apex Solutions", "Enterprise", "499", "North America", "No", ""],
    ["2024-01-05", "1002", "BetaWave", "Basic", "29", "Europe", "No", ""],
    ["2024-01-08", "1003", "CloudSphere", "Pro", "99", "Asia", "No", ""],
    ["2024-01-12", "1004", "Delta Dynamics", "Basic", "29", "North America", "Yes", "2024-04-15"],
    ["2024-01-15", "1005", "Echo Logic", "Enterprise", "499", "Europe", "No", ""],
    ["2024-01-19", "1006", "Falcon Systems", "Pro", "99", "South America", "No", ""],
    ["2024-01-22", "1007", "GridLock Inc", "Basic", "29", "North America", "No", ""],
    ["2024-01-25", "1008", "HyperLoop Tech", "Basic", "29", "Asia", "Yes", "2024-03-10"],
    ["2024-01-28", "1009", "Ion Innovation", "Pro", "99", "Europe", "No", ""],
    ["2024-02-01", "1010", "JumpStart Co", "Enterprise", "499", "North America", "No", ""],
    ["2024-02-04", "1011", "Kinetix", "Basic", "29", "North America", "No", ""],
    ["2024-02-07", "1012", "Lunar Media", "Basic", "29", "Europe", "Yes", "2024-05-20"],
    ["2024-02-11", "1013", "MicroNet", "Pro", "99", "Asia", "No", ""],
    ["2024-02-14", "1014", "NanoSoft", "Enterprise", "499", "North America", "No", ""],
    ["2024-02-18", "1015", "OmniGroup", "Pro", "99", "Europe", "No", ""],
    ["2024-02-21", "1016", "Pulse Digital", "Basic", "29", "North America", "No", ""],
    ["2024-02-25", "1017", "Quantum Leap", "Basic", "29", "South America", "Yes", "2024-04-05"],
    ["2024-02-28", "1018", "RedShift", "Enterprise", "499", "North America", "No", ""],
    ["2024-03-02", "1019", "SolarFlare", "Pro", "99", "Europe", "No", ""],
    ["2024-03-05", "1020", "TerraFirm", "Basic", "29", "North America", "No", ""],
    ["2024-03-09", "1021", "UltraVibe", "Basic", "29", "Asia", "No", ""],
    ["2024-03-12", "1022", "Velocity Labs", "Pro", "99", "North America", "No", ""],
    ["2024-03-16", "1023", "WarpSpeed", "Enterprise", "499", "Europe", "No", ""],
    ["2024-03-19", "1024", "Xenon Tech", "Basic", "29", "North America", "No", ""],
    ["2024-03-23", "1025", "Yellow Brick", "Basic", "29", "South America", "Yes", "2024-06-15"],
    ["2024-03-26", "1026", "Zenith Corp", "Pro", "99", "North America", "No", ""],
    ["2024-03-30", "1027", "AlphaStream", "Enterprise", "499", "Asia", "No", ""],
    ["2024-04-02", "1028", "BlueSky", "Basic", "29", "Europe", "No", ""],
    ["2024-04-06", "1029", "CyberCore", "Basic", "29", "North America", "Yes", "2024-07-12"],
    ["2024-04-09", "1030", "DeepDive", "Pro", "99", "North America", "No", ""]
]

file_path = os.path.join("data", "sales_data.csv")

with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"✅ CSV file generated successfully at: {file_path}")