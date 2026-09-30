"""Common LLM Interface providing a unified, provider-agnostic abstraction."""

from typing import Optional, Tuple
from config.settings import PROVIDER_GEMINI, PROVIDER_GROQ
from llm.gemini_provider import call_gemini
from llm.groq_provider import call_groq
from utils.error_handler import LLMError, LLMErrorCategory, handle_llm_error


def call_llm(
    prompt: str,
    provider: str = PROVIDER_GEMINI,
    model_id: str = "gemini-2.5-flash",
    system_instruction: Optional[str] = None,
) -> str:
    """
    Unified entry point for all LLM calls across the application.
    Abstracts away differences between Google Gemini and Groq APIs.

    Args:
        prompt: The main user prompt or instruction.
        provider: Provider name ('Google Gemini' or 'Groq').
        model_id: Model ID for the selected provider.
        system_instruction: Optional system instruction guiding model persona/behavior.

    Returns:
        Raw text output from the selected model.

    Raises:
        LLMError: Standardized exception raised if any provider fails.
    """
    norm_provider = provider.strip().lower()

    if "gemini" in norm_provider or norm_provider == "google":
        return call_gemini(
            prompt=prompt,
            model_id=model_id,
            system_instruction=system_instruction,
        )
    elif "groq" in norm_provider:
        return call_groq(
            prompt=prompt,
            model_id=model_id,
            system_instruction=system_instruction,
        )
    else:
        raise LLMError(
            message=f"Unsupported AI Provider '{provider}'. Supported options: {PROVIDER_GEMINI}, {PROVIDER_GROQ}.",
            provider=provider,
            model_id=model_id,
            category=LLMErrorCategory.UNKNOWN,
        )


def test_provider_connection(provider: str, model_id: str) -> Tuple[bool, str]:
    """
    Test live connectivity and authentication with the specified provider and model.

    Returns:
        tuple (success: bool, message: str)
    """
    ping_prompt = "Hello! Please respond with the single word: READY."
    try:
        response = call_llm(
            prompt=ping_prompt,
            provider=provider,
            model_id=model_id,
            system_instruction="You are a ping test agent. Keep answers minimal.",
        )
        if response and len(response.strip()) > 0:
            return True, f"Connection verified with {provider} ({model_id})."
        return False, "Received empty response during connectivity test."
    except LLMError as e:
        return False, e.user_friendly_message()
    except Exception as e:
        return False, handle_llm_error(e, provider=provider, model_id=model_id)
