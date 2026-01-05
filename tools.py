import ast
import operator as op
import requests
from datetime import date, timedelta

from langchain_core.tools import tool

from cred import weather_api_key

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
    if isinstance(node, ast.Constant):
        return node.n
    if isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            _eval_expr(node.left),
            _eval_expr(node.right)
        )
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
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_expr(tree.body)
        return f"Result: {result}"
    except Exception as e:
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

        return {
            "word_count": len(words),
            "character_count": char_count,
            "sentiment": sentiment
        }

    except Exception as e:
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
    try:
        if days is None:
            raise ValueError("Days is None.")
        if not isinstance(days, int):
            raise TypeError("Days must be an integer.")
        return (date.today() + timedelta(days=days)).isoformat()
    except Exception as e:
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
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={weather_api_key}&units=metric"
        )
        response = requests.get(url)
        data = response.json()

        return {
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"]
        }
    except Exception as e:
        return {"error": str(e)}
