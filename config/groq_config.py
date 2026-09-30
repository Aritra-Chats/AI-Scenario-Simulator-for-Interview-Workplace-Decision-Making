"""Centralized configuration and model registry for Groq API."""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Active Groq Models (display name -> model ID)
GROQ_MODELS: Dict[str, str] = {
    "GPT OSS 120B": "openai/gpt-oss-120b",
    "GPT OSS 20B": "openai/gpt-oss-20b",
    "Qwen 3.8 27B": "qwen/qwen3.8-27b",
    "Groq Compound": "groq/compound",
    "Groq Compound Mini": "groq/compound-mini",
    "LLaMA 3.3 70B Versatile": "llama-3.3-70b-versatile",
    "LLaMA 3.1 8B Instant": "llama-3.1-8b-instant",
}

DEFAULT_GROQ_MODEL: str = "GPT OSS 120B"


def get_groq_model_names() -> List[str]:
    """Return list of user-facing Groq model display names."""
    return list(GROQ_MODELS.keys())


def get_groq_model_id(display_name: str) -> str:
    """Resolve display name to Groq API model ID."""
    return GROQ_MODELS.get(display_name, GROQ_MODELS[DEFAULT_GROQ_MODEL])


def get_groq_api_key() -> Optional[str]:
    """Retrieve the Groq API key from the environment."""
    return os.getenv("GROQ_API_KEY", "").strip() or None


def is_groq_configured() -> bool:
    """Check if a non-empty Groq API key is configured."""
    key = get_groq_api_key()
    return bool(key and key != "your_groq_api_key_here")
