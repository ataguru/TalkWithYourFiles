import os
from dotenv import load_dotenv

class ApiKeyHandler:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiKeyHandler, cls).__new__(cls)
        return cls._instance
    
    def set_api_key_environment_variable(self, openai_api_key):
        # Set the environment variable
        os.environ["OPENAI_API_KEY"] = openai_api_key