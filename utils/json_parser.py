"""Robust JSON extraction and parsing utilities for LLM structured outputs."""

import json
import re
from typing import Any, Dict, Optional


def extract_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Safely extract and parse a JSON dictionary from LLM text response.
    Handles markdown code blocks, backticks, leading/trailing prose, and minor formatting errors.

    Args:
        text: Raw text string returned by LLM.

    Returns:
        Parsed dict if successful, None if parsing fails.
    """
    if not text or not isinstance(text, str):
        return None

    cleaned = text.strip()

    # Strategy 1: Try direct JSON parse
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except (json.JSONDecodeError, ValueError):
        pass

    # Strategy 2: Extract code block ```json ... ``` or ``` ... ```
    code_block_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    matches = re.findall(code_block_pattern, cleaned, re.IGNORECASE)
    for match in matches:
        try:
            data = json.loads(match.strip())
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, ValueError):
            continue

    # Strategy 3: Find outermost curly braces { ... }
    start_idx = cleaned.find("{")
    end_idx = cleaned.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        candidate = cleaned[start_idx : end_idx + 1]
        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, ValueError):
            pass

        # Strategy 4: Clean up common LLM trailing comma issues before brackets
        cleaned_candidate = re.sub(r",\s*([\]}])", r"\1", candidate)
        try:
            data = json.loads(cleaned_candidate)
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, ValueError):
            pass

    return None


def safe_json_loads(text: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Parse JSON with fallback to default dictionary if extraction fails."""
    parsed = extract_json(text)
    if parsed is not None:
        return parsed
    return default or {}
