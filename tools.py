# tools.py
from __future__ import annotations

import ast
import json
import operator as op
import re
import urllib.parse
import urllib.request
from datetime import date, timedelta
from typing import Optional

from langchain_core.tools import tool


# =============================================================================
# 1) Math Tool (safe arithmetic eval)
# =============================================================================
_ALLOWED_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}
_ALLOWED_UNARY_OPS = {ast.UAdd: op.pos, ast.USub: op.neg}


def _safe_eval_math(expr: str) -> float:
    expr = expr.strip()
    if not expr:
        raise ValueError("Expression is empty.")

    expr = expr.replace("×", "*").replace("÷", "/")
    node = ast.parse(expr, mode="eval")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)

        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return float(n.value)

        if isinstance(n, ast.UnaryOp) and type(n.op) in _ALLOWED_UNARY_OPS:
            return _ALLOWED_UNARY_OPS[type(n.op)](_eval(n.operand))

        if isinstance(n, ast.BinOp) and type(n.op) in _ALLOWED_BIN_OPS:
            return _ALLOWED_BIN_OPS[type(n.op)](_eval(n.left), _eval(n.right))

        raise ValueError("Unsupported expression. Use only numbers and + - * / // % ** ( ).")

    return _eval(node)


@tool("math_tool")
def math_tool(expression: str) -> str:
    """
    Evaluate an arithmetic expression and return the result.

    Input:
      expression: arithmetic expression as a string (example: "(234*12)+98")
    Output:
      result as a string
    """
    try:
        result = _safe_eval_math(expression)
        if abs(result - int(result)) < 1e-12:
            return str(int(result))
        return str(result)
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"


# =============================================================================
# 2) Text Analyzer Tool
# =============================================================================
_POS_WORDS = {"good", "great", "awesome", "amazing", "love", "excellent", "happy", "nice", "fantastic", "positive"}
_NEG_WORDS = {"bad", "terrible", "awful", "hate", "poor", "sad", "angry", "worst", "negative", "horrible"}


@tool("text_analyzer_tool")
def text_analyzer_tool(text: str) -> dict:
    """
    Analyze text and return word count, character count, and simple rule-based sentiment.

    Input:
      text: any string
    Output (dict):
      word_count, character_count, sentiment, sentiment_reason
    """
    try:
        if text is None:
            raise ValueError("Text is None.")
        cleaned = text.strip()
        if not cleaned:
            raise ValueError("Text is empty.")

        tokens = re.findall(r"\b\w+\b", cleaned)
        word_count = len(tokens)
        character_count = len(text)

        lower_tokens = [t.lower() for t in tokens]
        pos_hits = sum(1 for t in lower_tokens if t in _POS_WORDS)
        neg_hits = sum(1 for t in lower_tokens if t in _NEG_WORDS)

        if pos_hits > neg_hits:
            sentiment = "positive"
            reason = f"More positive keywords ({pos_hits}) than negative keywords ({neg_hits})."
        elif neg_hits > pos_hits:
            sentiment = "negative"
            reason = f"More negative keywords ({neg_hits}) than positive keywords ({neg_hits})."
        else:
            sentiment = "neutral"
            reason = f"Equal/zero keyword hits (pos={pos_hits}, neg={neg_hits})."

        return {
            "word_count": word_count,
            "character_count": character_count,
            "sentiment": sentiment,
            "sentiment_reason": reason,
        }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


# =============================================================================
# 3) Date Utility Tool
# =============================================================================
@tool("date_utility_tool")
def date_utility_tool(days: int) -> str:
    """
    Return the calendar date after N days from today.

    Input:
      days: integer number of days
    Output:
      ISO date string YYYY-MM-DD
    """
    try:
        if days is None:
            raise ValueError("Days is None.")
        if not isinstance(days, int):
            raise TypeError("Days must be an integer.")
        return (date.today() + timedelta(days=days)).isoformat()
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"


# =============================================================================
# 4) Weather API Tool (Open-Meteo)
# =============================================================================
def _http_get_json(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "langchain-weatherstack-tool/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


@tool("weather_api_tool")
def weather_api_tool(city: str, country: Optional[str] = None) -> dict:
    """
    Fetch live current weather for a city using Weatherstack.

    Input:
      city: city name (e.g., "Chandigarh")
      country: optional country hint (e.g., "India")
    Output (dict):
      location, current (temperature, weather_descriptions, wind_speed, humidity, feelslike, observation_time)
    """
    try:
        if not city or not city.strip():
            raise ValueError("City is required.")

        # Prefer env var; fallback to hardcoded key ONLY if you insist.
        api_key = os.getenv("WEATHERSTACK_API_KEY") or "4d1d8ae207a8c845a52df8a67bf3623e"

        query = f"{city}, {country}" if country else city

        base = "https://api.weatherstack.com/current"
        url = base + "?" + urllib.parse.urlencode({"access_key": api_key, "query": query})

        data = _http_get_json(url)

        # Weatherstack returns errors in an "error" object.
        if isinstance(data, dict) and data.get("error"):
            return {"error": data["error"]}

        location = data.get("location")
        current = data.get("current")
        if not location or not current:
            return {"error": "Unexpected Weatherstack response (missing 'location' or 'current')."}

        # Keep only the fields the agent needs for interpretation.
        return {
            "location": {
                "name": location.get("name"),
                "region": location.get("region"),
                "country": location.get("country"),
                "localtime": location.get("localtime"),
            },
            "current": {
                "observation_time": current.get("observation_time"),
                "temperature": current.get("temperature"),
                "feelslike": current.get("feelslike"),
                "weather_descriptions": current.get("weather_descriptions"),
                "wind_speed": current.get("wind_speed"),
                "wind_dir": current.get("wind_dir"),
                "humidity": current.get("humidity"),
            },
        }

    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}