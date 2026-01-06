"""
client.py

Initializes a Google Gemini chat model client for use with LangChain. This module
creates a `ChatGoogleGenerativeAI` instance configured for low-variance responses
and a capped output length, and exports it as `model` for reuse across the app.

Configuration notes:
- `temperature`, `top_p`, and `top_k` control sampling/creativity.
- `max_output_tokens` caps the maximum tokens in the model's response.

Security:
- Store the API key outside source control (for example via environment variables
  or a separate secrets/credentials file that is not committed).
"""
from langchain_google_genai import ChatGoogleGenerativeAI

from cred import gemini_api_key
from logger_config import setup_logger

# Initialize logger for this module
logger = setup_logger(__name__)

logger.info("Initializing Gemini chat model client")

try:
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        api_key=gemini_api_key,
        temperature=0.2,
        top_p=0.9,
        top_k=40,
        max_output_tokens=512,   # output length cap
    )
    logger.info("Gemini model initialized successfully")
    logger.debug(f"Model config: model=gemini-2.5-flash, temp=0.2, top_p=0.9, top_k=40, max_tokens=512")
except Exception as e:
    logger.error(f"Failed to initialize Gemini model: {str(e)}", exc_info=True)
    raise
