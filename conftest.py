import pytest
from dotenv import load_dotenv
import os

@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Fixture to load environment variables from .env file."""
    load_dotenv()  # This will automatically look for a .env file in the current directory
    # Optionally, you can specify the path explicitly:
    # load_dotenv(dotenv_path="path/to/your/.env")
    
    # Check if environment variables are loaded (for debugging purposes)
    assert os.getenv("API_URL_METEO") is not None, "DATABASE_URL is not set"
    assert os.getenv("SECRET_KEY") is not None, "SECRET_KEY is not set"