import pandas as pd
import json
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create absolute path to the Excel file
file_path = os.path.join(script_dir, 'buildingNumtoName.xlsx')

print(f"Looking for file at: {file_path}")  # Debug print

# Load the Excel file
try:
    data = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"File not found at {file_path}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir(os.getcwd())}")
    raise

# Create dictionary with building number as key and both names
building_dict = {}
for _, row in data.iterrows():
    building_num = str(row['Building #'])  # Convert to string to ensure it works as a JSON key
    building_dict[building_num] = {
        'full_name': row['Building Name'],
        'short_name': row['Building Name - Short']
    }

# Create absolute path to the API directory (one level up and into API)
api_dir = os.path.join(os.path.dirname(script_dir), 'API')

# Ensure the API directory exists
if not os.path.exists(api_dir):
    print(f"Warning: API directory not found at {api_dir}")
    print("Creating API directory...")
    os.makedirs(api_dir)

# Save the extracted data to a JSON file in the API directory
json_file_path = os.path.join(api_dir, 'buildings_import.json')
with open(json_file_path, 'w') as json_file:
    json.dump(building_dict, json_file, indent=4)

print(f"Data exported to {json_file_path}.")
