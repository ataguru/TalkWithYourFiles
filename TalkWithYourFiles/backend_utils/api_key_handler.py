import os
from dotenv import load_dotenv

class ApiKeyHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiKeyHandler, cls).__new__(cls)
            load_dotenv()
            cls._instance.env_api_key = os.getenv("OPENAI_API_KEY")
        return cls._instance

    def get_api_key(self, input_api_key=None):
        # If input_api_key is not None and not empty, use it
        if input_api_key:
            return input_api_key
        # Otherwise, use the API key from the .env file
        else:
            return self.env_api_key
    
    def set_api_key_environment_variable(self, openai_api_key):
        # Set the environment variable
        os.environ["OPENAI_API_KEY"] = openai_api_key