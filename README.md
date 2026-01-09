# LangChain Agent with Mem0 Memory

A production-style LangChain + Gemini agent that uses multiple tools (math, dates, weather, text analysis) and integrates **Mem0** as a long-term memory layer to provide personalized, context-aware conversations.

---
## Features

- **Google Gemini** chat model as the core LLM.
- **LangChain agent** that can call tools in a loop until it reaches a final answer.
- **Tools**:
  - Math calculator (safe AST-based evaluation).
  - Date utility (compute future dates).
  - Weather fetch (via OpenWeatherMap API).
  - Text analysis (word/char count + simple sentiment).
- **Mem0 integration**:
  - Stores key interaction snippets as long-term memory.
  - Retrieves relevant memories based on the current query and `user_id`.
  - Injects memory context into the system prompt to personalize responses.
- **Rich logging**:
  - File + console logging with rotation.
  - Per-module loggers for easier debugging.
- **Interactive chat loop**:
  - CLI chat with memory.
  - Also supports predefined example runs.
---
## Project Objective
The goal of this assignment is to:
- Understand **LangChain Agents**
- Implement **custom tools**
- Explore **single-tool and multi-tool agents**
- Integrate **external APIs** with LLMs
- Learn practical **agent orchestration** using Google Gemini
---
## :brain: Agents Implemented
### :one: Single Tool Agent
- Uses **one tool only**
- Suitable for focused tasks like calculations
### :two: Multi Tool Agent
- Uses **multiple tools**
- LLM decides which tool to call based on user intent
### :three: API Agent
- Integrates **external APIs**
- Example: Weather information retrieval
---
## Tech Stack
- **Language:** Python 3.10+
- **Framework:** LangChain
- **LLM:** Google Gemini
  - `gemini-2.5-flash`
  - `gemini-2.5-flash-lite`
- **Environment:** Virtual Environment (`venv`)
- **API:** OpenWeatherMap,
- A Mem0 API key 
---
yaml
Copy code
---
## Installation & Setup
### :one: Clone the Repository
            git clone https://github.com/hemant-crossml/Langchain_Assignment.git
            cd Langchain_Assignment
### :two: Create & Activate Virtual Environment
      python -m venv venv
      source venv/bin/activate     # Linux / macOS
      myenv\Scripts\activate        # Windows
### :closed_lock_with_key: API Key Configuration
Add your Gemini API Key in cred.py:
    gemini_api_key = "YOUR_GEMINI_API_KEY"
    weather_api_key= "YOUR_WEATHER_API_KEY"
    mem0_api_key= "YOUR_MEM0_API_KEY"
### :warning: Important:
Do not commit your real API key to GitHub.
Use .env and environment variables for production projects.
### How to Run
Run the main application:
    python main.py
The agent will:
- Understand the user query
- Select the appropriate tool
- Execute the tool
- Return the final response
### Example Use Cases
- Solve mathematical calculations
- Find future dates
- Analyze text content
- Fetch weather information
- Dynamically choose tools based on query intent
### Learning Outcomes
- Understand how to wire up a Gemini-powered LangChain agent with custom tools and a centralized system prompt.
- Learn how to design and register tools for math, dates, weather, and text analysis in a reusable, production-style way.
- Gain hands-on experience integrating a long-term memory layer (Mem0) into an agent, including:
  - Storing structured interactions as memories.
  - Retrieving and serializing memories per user_id.
  - Injecting memory context into prompts to personalize responses.
- Practice building an interactive CLI chat loop that maintains context across turns and sessions.
- Improve your understanding of logging, error handling, and environment-based configuration for real-world AI applications.
