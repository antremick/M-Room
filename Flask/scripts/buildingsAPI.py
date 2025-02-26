import os
import json
from dotenv import load_dotenv
import sys

# Add API directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'API'))

import api_functions
import requests

def main():
    """Main function for getting building data"""
    # Load environment variables
    load_dotenv()
    
    # Get API keys from environment
    publicKey = os.getenv("BUILDINGS_KEY")
    privateKey = os.getenv("BUILDINGS_SECRET")

    
    # Change scope from "classrooms" to "buildings"
    auth_header = api_functions.generate_token(publicKey, privateKey, "buildings")
    
    # Make the API call
    try:
        response = requests.get("https://gw.api.it.umich.edu/um/bf/Buildings/v2/BuildingInfo", 
                              headers=auth_header, 
                              timeout=30)
        
        if response.ok:
            data = response.json()
            # Save the data
            with open('buildings.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print("Successfully saved building data to buildings.json")
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Error making request: {str(e)}")

if __name__ == "__main__":
    main()
