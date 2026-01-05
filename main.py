"""
run_examples.py

Runs multiple end-to-end examples against the preconfigured LangChain agent and
logs results to both the console and a file for easy debugging and repeatable demos. 

What this script does:
- Configures Python logging with two handlers:
  - `FileHandler("agent_execution.log")` to persist logs to disk. [web:24]
  - `StreamHandler()` to also show logs in the terminal (defaults to stderr). [web:21][web:24]
- Invokes the agent using the LangGraph agent API via `agent.invoke({"messages": [...]})`. [web:1]
- Wraps each example in `try/except` so one failing example doesn’t stop the rest. [web:24]

How to run:
    python run_examples.py

Expected inputs/outputs:
- Inputs are chat-style `messages` dicts (role/content) compatible with LangChain’s
  message dictionary format. [web:30]
- The agent result includes a `messages` list; the last entry is typically the final
  assistant message, which is logged. [web:1]
"""


import logging
from agent import agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('agent_execution.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Example 1: Math Calculation
    logger.info("\n" + "="*50)
    logger.info("Example 1: Math Calculation")
    logger.info("="*50)
    
    try:
        math_response = agent.invoke({
            "messages": [
                {"role": "user", "content": "What is (234 * 12) + 98?"}
            ]
        })
        logger.info(f"Math Response: {math_response['messages'][-1].content}")
    except Exception as e:
        logger.error(f"Error in Math Calculation: {e}", exc_info=True)

    # Example 2: Multi Tool Example
    logger.info("\n" + "="*50)
    logger.info("Multi Tool Example")
    logger.info("="*50)
    
    try:
        multi_response = agent.invoke({
            "messages": [
                {"role": "user",
                 "content": "Calculate the total cost if I buy 3 items priced at 499 each and tell me the delivery date if shipping takes 7 days."}
            ]
        })
        logger.info(f"Multi Tool Response: {multi_response['messages'][-1].content}")
    except Exception as e:
        logger.error(f"Error in Multi Tool Example: {e}", exc_info=True)

    # Example 3: Real API Tool (Weather)
    logger.info("\n" + "="*50)
    logger.info("Real API Tool Example: Weather Query")
    logger.info("="*50)
    
    try:
        api_response = agent.invoke({
            "messages": [
                {"role": "user",
                 "content": "What is today's weather in Chandigarh and suggest clothing accordingly?"}
            ]
        })
        logger.info(f"Weather Response: {api_response['messages'][-1].content}")
    except Exception as e:
        logger.error(f"Error in Weather API Call: {e}", exc_info=True)

    logger.info("\n" + "="*50)
    logger.info("All examples completed")
    logger.info("="*50)