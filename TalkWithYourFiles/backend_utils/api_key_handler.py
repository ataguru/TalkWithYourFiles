import os
from dotenv import load_dotenv
import requests

class ApiKeyHandler:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiKeyHandler, cls).__new__(cls)
        return cls._instance
    
    def set_api_key_environment_variable(self, openai_api_key):
        # Set the environment variable
        os.environ["OPENAI_API_KEY"] = openai_api_key

    def validate_key(self, openai_api_key):
        response = requests.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {openai_api_key}"})
        if response.status_code == 200:
            return True
        else:
            return False