"""
main.py
-------
Run all examples from one file.
Demonstrates agent invocation with comprehensive logging for debugging.
"""
import traceback

from agent import agent
from logger_config import setup_logger
from prompt import system_prompt, user_query_1,user_query_2,user_query_3


# Initialize logger for main module
logger = setup_logger(__name__)

# Message structure for Example 1: Simple math calculation query
message1 = {
    "messages": [
        system_prompt,
        user_query_1
    ]
}

# Message structure for Example 2: Multi-tool usage (math + date operations)
message2 = {
    "messages": [
        system_prompt,
        user_query_2
    ]
}

# Message structure for Example 3: Weather API query with clothing recommendations
message3 = {
    "messages": [
        system_prompt,
        user_query_3
    ]
}

if __name__ == "__main__":
    logger.info("="*70)
    logger.info("APPLICATION STARTED")
    logger.info("="*70)
    
    # ==================== Example 1: Math Calculation ====================
    try:
        logger.info("\n[EXAMPLE 1] Starting math calculation example")
        
        logger.info(f"[EXAMPLE 1] User query: {user_query_1}")
        
        math_response = agent.invoke(message1)
        
        logger.info(f"[EXAMPLE 1] Agent invocation completed successfully")
        logger.debug(f"[EXAMPLE 1] Response messages count: {len(math_response['messages'])}")
        logger.debug(f"[EXAMPLE 1] Final message type: {type(math_response['messages'][-1])}")
        
        print("\n--- Example 1 ---")
        print(math_response["messages"][-1].content)
        
        logger.info(f"[EXAMPLE 1] Output displayed to user")
        
    except KeyError as e:
        logger.error(f"[EXAMPLE 1] KeyError - missing expected key in response: {e}", exc_info=True)
        print(f"\n--- Example 1 FAILED ---")
        print(f"Error: Missing expected data in response - {e}")
        
    except Exception as e:
        logger.error(f"[EXAMPLE 1] Unexpected error occurred: {e}", exc_info=True)
        logger.debug(f"[EXAMPLE 1] Full traceback:\n{traceback.format_exc()}")
        print(f"\n--- Example 1 FAILED ---")
        print(f"Error: {e}")
    
    # Example 2: Multi-Tool Usage
    try:
        logger.info("\n[EXAMPLE 2] Starting multi-tool example")
        
        logger.info(f"[EXAMPLE 2] User query: {user_query_2}")

        multi_response = agent.invoke(message2)
        
        logger.info(f"[EXAMPLE 2] Agent invocation completed successfully")
        logger.debug(f"[EXAMPLE 2] Response messages count: {len(multi_response['messages'])}")
        
        print("\n--- Multi Tool Example ---")
        print(multi_response["messages"][-1].content)
        
        logger.info(f"[EXAMPLE 2] Output displayed to user")
        
    except KeyError as e:
        logger.error(f"[EXAMPLE 2] KeyError - missing expected key in response: {e}", exc_info=True)
        print(f"\n--- Multi Tool Example FAILED ---")
        print(f"Error: Missing expected data in response - {e}")
        
    except Exception as e:
        logger.error(f"[EXAMPLE 2] Unexpected error occurred: {e}", exc_info=True)
        logger.debug(f"[EXAMPLE 2] Full traceback:\n{traceback.format_exc()}")
        print(f"\n--- Multi Tool Example FAILED ---")
        print(f"Error: {e}")
    
    # Example 3: Weather API 
    try:
        logger.info("\n[EXAMPLE 3] Starting weather API example")
        logger.info(f"[EXAMPLE 3] User query: {user_query_3}")
        
        api_response = agent.invoke(message3)
        
        logger.info(f"[EXAMPLE 3] Agent invocation completed successfully")
        logger.debug(f"[EXAMPLE 3] Response messages count: {len(api_response['messages'])}")
        
        print("\n--- Real API Tool Example ---")
        print(api_response["messages"][-1].content)
        
        logger.info(f"[EXAMPLE 3] Output displayed to user")
        
    except KeyError as e:
        logger.error(f"[EXAMPLE 3] KeyError - missing expected key in response: {e}", exc_info=True)
        print(f"\n--- Real API Tool Example FAILED ---")
        print(f"Error: Missing expected data in response - {e}")
        
    except Exception as e:
        logger.error(f"[EXAMPLE 3] Unexpected error occurred: {e}", exc_info=True)
        logger.debug(f"[EXAMPLE 3] Full traceback:\n{traceback.format_exc()}")
        print(f"\n--- Real API Tool Example FAILED ---")
        print(f"Error: {e}")
    
    logger.info("="*70)
    logger.info("ALL EXAMPLES COMPLETED")
    logger.info("="*70)
