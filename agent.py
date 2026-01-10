"""
agent.py

Creates a LangChain agent (LangGraph-backed) that can call a set of tools in a loop
until it produces a final answer (or hits a stop/iteration limit).

This module wires together:
- A Google Gemini chat model (provided by `client.model`).
- A system prompt (from `prompt.system_prompt`) that defines agent behavior.
- A list of tools (from `tools.*`) that the agent is allowed to call.

Usage:
    from agent import agent

    # Typical invocation shape (LangChain v1 agents expect "messages" state):
    result = agent.invoke({
        "messages": [{"role": "user", "content": "What's the weather in Gurugram?"}]
    })

Notes:
- Ensure each tool has type hints and a concise docstring; the agent/model uses those
"""
from langchain.agents import create_agent

from client import model

from tools import math_calculator, date_utility_tool, get_weather, analyze_text
from logger_config import setup_logger

# Initialize logger for this module
logger = setup_logger(__name__)

logger.info("Initializing LangChain agent")


tools = [math_calculator, date_utility_tool, get_weather, analyze_text]

logger.debug(f"Registered tools: {[tool.name for tool in tools]}")

try:
    agent = create_agent(
        model=model,
        tools=tools,
    )
    logger.info("Agent created successfully")
except Exception as e:
    logger.error(f"Failed to create agent: {str(e)}", exc_info=True)
    raise
