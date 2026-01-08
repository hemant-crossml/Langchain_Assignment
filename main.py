"""
main.py
-------
Interactive chat loop with Mem0 memory integration.
Demonstrates agent invocation with persistent memory across conversations.
"""
import traceback
from langchain.messages import HumanMessage

from agent import invoke_agent_with_memory
from cred import USER_ID
from prompt import system_prompt, user_query_1,user_query_2,user_query_3
from logger_config import setup_logger

logger = setup_logger(__name__)


def interactive_chat(user_id: str = USER_ID):
    """
    Run interactive chat loop with Mem0 memory persistence.
    
    Args:
        user_id (str): Unique identifier for memory isolation
    
    Features:
        - Continuous conversation with memory
        - Graceful error handling
        - Clean exit commands
        - Full logging for debugging
    """
    logger.info("="*70)
    logger.info("INTERACTIVE CHAT MODE STARTED")
    logger.info(f"User ID: {user_id}")
    logger.info("="*70)
    
    # Welcome message
    print("\n" + "="*70)
    print("🤖 AI Agent with Memory - Interactive Chat")
    print("="*70)
    print("\nAvailable commands:")
    print("  - Type your question normally to chat")
    print("  - 'exit', 'quit', 'bye' - End the conversation")
    print("  - 'clear' - View your conversation history")
    print("\nTools available: Math Calculator, Date Utility, Weather, Text Analysis")
    print("-"*70 + "\n")
    
    conversation_count = 0
    
    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for empty input
            if not user_input:
                print("⚠️  Please enter a message.\n")
                continue
            
            # Handle exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                print("\n👋 Thanks for chatting! Your conversation has been saved to memory.")
                logger.info(f"User ended conversation. Total turns: {conversation_count}")
                break
            
            # Handle special commands
            if user_input.lower() == 'clear':
                print(f"\n📊 You've had {conversation_count} conversation turns in this session.\n")
                continue
            
            # Log the user query
            logger.info(f"[Turn {conversation_count + 1}] User query: {user_input}")
            
            # Prepare message structure
            messages = {
                "messages": [
                    system_prompt,
                    HumanMessage(content=user_input)
                ]
            }
            
            # Show typing indicator
            print("\n🤔 Agent is thinking...", end="\r")
            
            # Invoke agent with memory
            response = invoke_agent_with_memory(messages, user_id)
            
            # Extract and display response
            assistant_response = response["messages"][-1].content
            print("\r" + " "*30 + "\r", end="")  # Clear typing indicator
            print(f"Agent: {assistant_response}\n")
            
            conversation_count += 1
            logger.info(f"[Turn {conversation_count}] Agent response delivered successfully")
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully_
            print("\n\n⚠️  Interrupted by user (Ctrl+C)")
            print("👋 Exiting chat. Your conversation has been saved.\n")
            logger.warning("Chat interrupted by KeyboardInterrupt (Ctrl+C)")
            break
            
        except KeyError as e:
            logger.error(f"[ERROR] KeyError - missing expected key: {e}", exc_info=True)
            print(f"\n❌ Error: Missing data in response - {e}")
            print("Please try rephrasing your question.\n")
            
        except Exception as e:
            logger.error(f"[ERROR] Unexpected error: {str(e)}", exc_info=True)
            logger.debug(f"Full traceback:\n{traceback.format_exc()}")
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again or type 'exit' to quit.\n")
    
    # Cleanup and final log
    logger.info("="*70)
    logger.info("INTERACTIVE CHAT SESSION ENDED")
    logger.info(f"Total conversation turns: {conversation_count}")
    logger.info("="*70)


def run_example_queries():
    """
    Run predefined example queries (original functionality).
    Useful for testing and demonstration.
    """
    
    logger.info("="*70)
    logger.info("RUNNING EXAMPLE QUERIES WITH MEMORY")
    logger.info("="*70)
    
    examples = [
        ("Math Calculation", user_query_1),
        ("Multi-Tool Usage", user_query_2),
        ("Weather API", user_query_3)
    ]
    
    for idx, (title, query) in enumerate(examples, 1):
        try:
            logger.info(f"\n[EXAMPLE {idx}] Starting: {title}")
            logger.info(f"[EXAMPLE {idx}] Query: {query.content}")
            
            messages = {"messages": [system_prompt, query]}
            response = invoke_agent_with_memory(messages, user_id=USER_ID)
            
            print(f"\n--- Example {idx}: {title} ---")
            print(response["messages"][-1].content[0]['text'])
            
            logger.info(f"[EXAMPLE {idx}] Completed successfully")
            
        except Exception as e:
            logger.error(f"[EXAMPLE {idx}] Failed: {str(e)}", exc_info=True)
            print(f"\n--- Example {idx} FAILED ---")
            print(f"Error: {e}\n")
    
    logger.info("="*70)
    logger.info("ALL EXAMPLE QUERIES COMPLETED")
    logger.info("="*70)


if __name__ == "__main__":
    # Choose mode: interactive or examples
    print("\n🚀 LangChain Agent with Mem0")
    print("Select mode:")
    print("  1. Interactive Chat (recommended)")
    print("  2. Run Example Queries")
    
    try:
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            interactive_chat(USER_ID)
        elif choice == "2":
            run_example_queries()
        else:
            print("❌ Invalid choice. Running interactive chat by default.")
            interactive_chat(USER_ID)
            
    except KeyboardInterrupt:
        print("\n\n👋 Exiting application.")
        logger.info("Application terminated by user")
