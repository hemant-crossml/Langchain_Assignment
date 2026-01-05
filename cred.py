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


# Load variables from .env file into environment
load_dotenv()

# Read Gemini API key from environment
gemini_api_key = os.getenv("GEMINI_API_KEY","")

# Read weather api key from environment
weather_api_key=os.getenv('WEATHER_API_KEY',"")

# Validate API key existence
if not gemini_api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in .env file")

if not weather_api_key:
    raise EnvironmentError("WEATHER_API_KEY not found in .env file")
