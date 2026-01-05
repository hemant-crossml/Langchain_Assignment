"""
llm_client.py

Initializes a Google Gemini chat model client for use with LangChain. This module
creates a `ChatGoogleGenerativeAI` instance configured for low-variance responses
and a capped output length, and exports it as `model` for reuse across the app. [web:1]

Configuration notes:
- `temperature`, `top_p`, and `top_k` control sampling/creativity. [web:1]
- `max_output_tokens` caps the maximum tokens in the model’s response. [web:1]

Security:
- Store the API key outside source control (for example via environment variables
  or a separate secrets/credentials file that is not committed). [web:1]
"""
from langchain_google_genai import ChatGoogleGenerativeAI

from cred import gemini_api_key


model= ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=gemini_api_key,
    temperature=0.2,
    top_p=0.9,
    top_k=40,
    max_output_tokens=512,   # output length cap
)