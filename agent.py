from __future__ import annotations

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from prompts import AGENT_PROMPT
from tools import math_tool, text_analyzer_tool, date_utility_tool, weather_api_tool


def build_agent_executor(
    model: str = "gemini-1.5-flash",
    temperature: float = 0.2,
) -> AgentExecutor:
    tools = [math_tool, text_analyzer_tool, date_utility_tool, weather_api_tool]

    llm = ChatGoogleGenerativeAI(model=model, temperature=temperature)
    agent = create_tool_calling_agent(llm, tools, AGENT_PROMPT)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )
