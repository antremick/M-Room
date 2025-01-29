import pandas as pd
import json

# Load the Excel file
file_path = 'buildingNumtoName.xlsx'  # Replace with the actual file path
data = pd.read_excel(file_path)

# Extract the columns "Building #" and "Building Name"
building_dict = data[['Building #', 'Building Name', 'Building Name - Short']].set_index('Building #').to_dict()['Building Name']

# Save the extracted data to a JSON file
json_file_path = 'buildings.json'  # Replace with desired output file path
with open(json_file_path, 'w') as json_file:
    json.dump(building_dict, json_file, indent=4)

print(f"Data exported to {json_file_path}.")
