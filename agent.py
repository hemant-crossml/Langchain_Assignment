"""
agent.py

Creates a LangChain agent (LangGraph-backed) that can call a set of tools in a loop
until it produces a final answer (or hits a stop/iteration limit). [web:1][web:5]

This module wires together:
- A Google Gemini chat model (provided by `client.model`).
- A system prompt (from `prompt.system_prompt`) that defines agent behavior.
- A list of tools (from `tools.*`) that the agent is allowed to call. [web:1][web:5]

Usage:
    from agent import agent

    # Typical invocation shape (LangChain v1 agents expect "messages" state):
    result = agent.invoke({
        "messages": [{"role": "user", "content": "What's the weather in Gurugram?"}]
    })

Notes:
- Ensure each tool has type hints and a concise docstring; the agent/model uses
  thos

"""
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from client import model
from prompt import system_prompt
from tools import math_calculator, date_utility_tool, get_weather, analyze_text


llm = model

tools = [math_calculator, date_utility_tool, get_weather,analyze_text]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)
