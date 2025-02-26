import os
from dotenv import load_dotenv, find_dotenv

# Print the path of the .env file being loaded
env_path = find_dotenv()
print(f"Loading .env from: {env_path}")

# Load and print environment variables for debugging
load_dotenv()
print(f"API_ENDPOINT value: {os.getenv('API_ENDPOINT')}")
print(f"Current working directory: {os.getcwd()}")

class DataLoader:
    def __init__(self):
        self.api_url = os.getenv('API_ENDPOINT', 'https://mroom-api-c7aef75a74b0.herokuapp.com') + "/import_data"
        print(f"Using API URL: {self.api_url}")