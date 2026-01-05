"""
cred.py
--------
This file is responsible for loading and validating
all sensitive credentials (API keys).

Best Practice:
- Credentials are NOT hardcoded
- Values are loaded from environment variables
"""

import os
from dotenv import load_dotenv
from logger_config import setup_logger

# Initialize logger for this module
logger = setup_logger(__name__)

logger.info("Starting credential loading process")

# Load variables from .env file into environment
load_dotenv()
logger.debug(".env file loaded successfully")

# Read Gemini API key from environment
gemini_api_key = os.getenv("GEMINI_API_KEY", "")
logger.debug(f"GEMINI_API_KEY present: {bool(gemini_api_key)}")

# Read weather api key from environment
weather_api_key = os.getenv('WEATHER_API_KEY', "")
logger.debug(f"WEATHER_API_KEY present: {bool(weather_api_key)}")

# Validate API key existence
if not gemini_api_key:
    logger.critical("GEMINI_API_KEY not found in .env file")
    raise EnvironmentError("GEMINI_API_KEY not found in .env file")

if not weather_api_key:
    logger.critical("WEATHER_API_KEY not found in .env file")
    raise EnvironmentError("WEATHER_API_KEY not found in .env file")

logger.info("All required API keys validated successfully")
