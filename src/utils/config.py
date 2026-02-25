import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Central configuration class mapping env variables."""
    
    BASE_UI_URL = os.getenv("BASE_UI_URL", "https://practicesoftwaretesting.com")
    BASE_API_URL = os.getenv("BASE_API_URL", "https://api.practicesoftwaretesting.com")
    
    TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "customer@practicesoftwaretesting.com")
    TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "welcome01")
    
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
