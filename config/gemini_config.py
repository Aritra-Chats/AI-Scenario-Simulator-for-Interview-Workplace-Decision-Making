"""Centralized configuration and model registry for Google Gemini API."""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Active Google Gemini Models (display name -> model ID)
# Note: Deprecated/shut down models (gemini-2.0-flash, gemini-2.0-flash-lite) are excluded.
GEMINI_MODELS: Dict[str, str] = {
    "Gemini 3.6 Flash": "gemini-3.6-flash",
    "Gemini 3.5 Flash": "gemini-3.5-flash",
    "Gemini 3.5 Flash Lite": "gemini-3.5-flash-lite",
    "Gemini 3 Flash (Preview)": "gemini-3-flash-preview",
    "Gemini 2.5 Flash": "gemini-2.5-flash",
    "Gemini 2.5 Flash Lite": "gemini-2.5-flash-lite",
    "Gemini 2.5 Pro": "gemini-2.5-pro",
}

DEFAULT_GEMINI_MODEL: str = "Gemini 3.6 Flash"


def get_gemini_model_names() -> List[str]:
    """Return list of user-facing Gemini model display names."""
    return list(GEMINI_MODELS.keys())


def get_gemini_model_id(display_name: str) -> str:
    """Resolve display name to Google Gemini API model ID."""
    return GEMINI_MODELS.get(display_name, GEMINI_MODELS[DEFAULT_GEMINI_MODEL])


def get_gemini_api_key() -> Optional[str]:
    """Retrieve the Gemini API key from the environment."""
    return os.getenv("GEMINI_API_KEY", "").strip() or None


def is_gemini_configured() -> bool:
    """Check if a non-empty Gemini API key is configured."""
    key = get_gemini_api_key()
    return bool(key and key != "your_gemini_api_key_here")
