"""
agent.py

LangChain agent with Mem0 memory integration for personalized responses.
"""
from typing import Dict, List
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from client import model, mem0
from prompt import system_prompt
from tools import math_calculator, date_utility_tool, get_weather, analyze_text
from logger_config import setup_logger

logger = setup_logger(__name__)

logger.info("Initializing LangChain agent with Mem0 memory")

tools = [math_calculator, date_utility_tool, get_weather, analyze_text]
logger.debug(f"Registered tools: {[tool.name for tool in tools]}")


def retrieve_memories(query: str, user_id: str) -> List[str]:
    """
    Summary:
        Retrieve relevant memories from Mem0 for context enrichment.
    
    Searches the Mem0 database for memories associated with the specified user
    that are relevant to the provided query. Skips memory retrieval for short
    queries (less than 3 words) to optimize performance.
    
    Args:
        query (str): The user's input query to search for relevant memories.
        user_id (str): Unique identifier for the user whose memories to retrieve.
    
    Returns:
        str: Serialized string of relevant memories, one per line with bullet points.
             Returns empty string if no memories found or query is too short.
    """
    logger.info(f"Retrieving memories for user: {user_id}")

    # Skip memory search for greetings / short input
    if len(query.strip().split()) < 3:
        return ""

    try:
        memories = mem0.search(
            query=query,
            filters={ "user_id":user_id},
            limit=5
        )

        memory_list = memories.get("results", [])

        if not memory_list:
            return ""

        serialized = "\n".join(
            f"- {mem['memory']}" for mem in memory_list
        )
        logger.info(f"Retrieved {len(memory_list)} memories")
        return serialized

    except Exception as e:
        logger.error(f"Error retrieving memories: {str(e)}", exc_info=True)
        return ""


def save_interaction(user_id: str, user_input: str, assistant_response: str):
    """
    Summary:
        Save the conversation turn to Mem0 for future context.
    
    Stores both the user's message and the assistant's response in the Mem0
    database, enabling persistent memory across sessions.
    
    Args:
        user_id (str): Unique identifier for the user.
        user_input (str): The user's message content.
        assistant_response (str): The agent's generated response.
    
    Returns:
        None
    """
    logger.info(f"Saving interaction to Mem0 for user: {user_id}")
    try:
        interaction = [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": assistant_response}
        ]
        result = mem0.add(interaction, user_id=user_id)
        #breakpoint()
        logger.info(f"Memory saved successfully: {len(result.get('results', []))} memories added")
    except Exception as e:
        logger.error(f"Error saving interaction to Mem0: {str(e)}", exc_info=True)


def invoke_agent_with_memory(messages: Dict, user_id: str = "default_user") -> Dict:
    """
    Summary:
        Invoke agent with memory-enhanced context for personalized responses.
    
    Retrieves relevant memories for the user, enhances the system prompt with
    memory context, invokes the LangChain agent, and saves the interaction back
    to Mem0.
    
    Args:
        messages (Dict): Message dictionary containing a 'messages' key with
                        conversation history as list of message objects.
        user_id (str, optional): Unique user identifier for memory persistence.
                                Defaults to "default_user".
    
    Returns:
        Dict: Agent response containing updated messages with the assistant's reply.
    
    """
    logger.info(f"Agent invocation with memory for user: {user_id}")
    
    # Get the last user message
    last_message = messages["messages"][-1]
    user_query = last_message.content if hasattr(last_message, 'content') else str(last_message)
    
    # Retrieve relevant memories
    memory_context = retrieve_memories(user_query, user_id)
    
    # Enhance system prompt with memory context

    enhanced_system_prompt = SystemMessage(
        content=f"""{system_prompt.content}

    ## MEMORY CONTEXT
    {memory_context}

    Rules:
    - Use memory facts if available
    - If user's name is known, use it
    - Do NOT say you lack personal info if memory exists
    """
    )
    
    # Replace system prompt with enhanced version
    enhanced_messages = {"messages": [enhanced_system_prompt] + messages["messages"][1:]}
    
    # Invoke agent
    try:
        response = agent.invoke(enhanced_messages)
        
        # Extract assistant response
        assistant_response = response["messages"][-1].content
        
        # Save interaction to memory
        save_interaction(user_id, user_query, assistant_response)
        
        logger.info("Agent invocation with memory completed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Failed to invoke agent with memory: {str(e)}", exc_info=True)
        raise

# Initialize agent at module level (single initialization)
try:
    agent = create_agent(model=model, tools=tools)
    logger.info("Agent created successfully")
except Exception as e:
    logger.error(f"Failed to create agent: {str(e)}", exc_info=True)
    raise
