import ast
import operator as op
import requests
from datetime import date, timedelta

from langchain_core.tools import tool

from cred import weather_api_key
from logger_config import setup_logger

# Initialize logger for this module
logger = setup_logger(__name__)

# Math tool (safe case)
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
}


def _eval_expr(node):
    """
    Summary:
        Recursively evaluates a restricted Python AST node representing an arithmetic expression.

    Args:
        node: An AST node (e.g., ast.Constant, ast.BinOp) produced by parsing an expression.

    Returns:
        The numeric result of evaluating the AST node.
    """
    logger.debug(f"Evaluating AST node: {type(node).__name__}")
    if isinstance(node, ast.Constant):
        return node.n
    if isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            _eval_expr(node.left),
            _eval_expr(node.right)
        )
    logger.error(f"Invalid expression node type: {type(node).__name__}")
    raise ValueError("Invalid expression")


@tool
def math_calculator(expression: str) -> str:
    """
    Summary:
        Safely evaluates a basic arithmetic expression using AST parsing (no eval).

    Args:
        expression (str): Arithmetic expression like "(234 * 12) + 98".

    Returns:
        str: A string containing either the computed result (e.g., "Result: 2906")
        or an error message if evaluation fails.
    """
    logger.info(f"[TOOL CALL] math_calculator invoked with expression: {expression}")
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_expr(tree.body)
        logger.info(f"[TOOL SUCCESS] Math calculation result: {result}")
        return f"Result: {result}"
    except Exception as e:
        logger.error(f"[TOOL ERROR] Math calculation failed: {str(e)}", exc_info=True)
        return f"Error evaluating expression: {str(e)}"


@tool
def analyze_text(text: str) -> dict:
    """
    Summary:
        Analyzes a text string to compute word count, character count, and a simple sentiment label.

    Args:
        text (str): The input text to analyze.

    Returns:
        dict: A dictionary containing:
            - word_count (int): Number of whitespace-separated tokens.
            - character_count (int): Total number of characters in the text.
            - sentiment (str): "Positive", "Negative", or "Neutral".
        If an error occurs, returns {"error": "<message>"}.
    """
    logger.info(f"[TOOL CALL] analyze_text invoked with text length: {len(text)}")
    logger.debug(f"Text preview: {text[:100]}...")
    
    try:
        words = text.split()
        char_count = len(text)

        positive_words = ["good", "great", "excellent", "happy", "love"]
        negative_words = ["bad", "poor", "sad", "hate", "terrible"]

        sentiment_score = 0
        for word in words:
            if word.lower() in positive_words:
                sentiment_score += 1
            elif word.lower() in negative_words:
                sentiment_score -= 1

        sentiment = "Neutral"
        if sentiment_score > 0:
            sentiment = "Positive"
        elif sentiment_score < 0:
            sentiment = "Negative"

        result = {
            "word_count": len(words),
            "character_count": char_count,
            "sentiment": sentiment
        }
        
        logger.info(f"[TOOL SUCCESS] Text analysis complete: {result}")
        return result

    except Exception as e:
        logger.error(f"[TOOL ERROR] Text analysis failed: {str(e)}", exc_info=True)
        return {"error": str(e)}


@tool("date_utility_tool")
def date_utility_tool(days: int) -> str:
    """
    Summary:
        Returns the calendar date after N days from today (local system date).

    Args:
        days (int): Number of days to add to today's date.

    Returns:
        str: ISO date string in the format "YYYY-MM-DD".
        If validation or computation fails, returns an error string like:
        "ERROR: TypeError: Days must be an integer."
    """
    logger.info(f"[TOOL CALL] date_utility_tool invoked with days: {days}")
    
    try:
        if days is None:
            logger.warning("Days parameter is None")
            raise ValueError("Days is None.")
        if not isinstance(days, int):
            logger.warning(f"Days parameter has wrong type: {type(days)}")
            raise TypeError("Days must be an integer.")
        
        result_date = (date.today() + timedelta(days=days)).isoformat()
        logger.info(f"[TOOL SUCCESS] Calculated date: {result_date}")
        return result_date
    except Exception as e:
        logger.error(f"[TOOL ERROR] Date calculation failed: {str(e)}", exc_info=True)
        return f"ERROR: {type(e).__name__}: {e}"


@tool
def get_weather(city: str) -> dict:
    """
    Summary:
        Fetches live weather data for a given city using the OpenWeatherMap current weather API.

    Args:
        city (str): City name (e.g., "Chandigarh").

    Returns:
        dict: On success, returns:
            - temperature (float): Current temperature in Celsius.
            - condition (str): Weather description (e.g., "clear sky").
        On failure, returns {"error": "<message>"}.
    """
    logger.info(f"[TOOL CALL] get_weather invoked for city: {city}")
    
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={weather_api_key}&units=metric"
        )
        logger.debug(f"Making API request to OpenWeatherMap for city: {city}")
        
        response = requests.get(url, timeout=10)
        logger.debug(f"API response status code: {response.status_code}")
        
        response.raise_for_status()  # Raise exception for bad status codes
        data = response.json()
        
        result = {
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"]
        }
        
        logger.info(f"[TOOL SUCCESS] Weather data retrieved: temp={result['temperature']}°C, condition={result['condition']}")
        return result
        
    except requests.exceptions.Timeout:
        logger.error(f"[TOOL ERROR] Weather API request timed out for city: {city}")
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        logger.error(f"[TOOL ERROR] Weather API request failed: {str(e)}", exc_info=True)
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"[TOOL ERROR] Unexpected error in get_weather: {str(e)}", exc_info=True)
        return {"error": str(e)}
