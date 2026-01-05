from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import requests

from cred import gemini_api_key

search_tool = DuckDuckGoSearchRun()

model= ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=gemini_api_key,
    temperature=0.2,
    top_p=0.9,
    top_k=40,
    max_output_tokens=512,   # output length cap
)