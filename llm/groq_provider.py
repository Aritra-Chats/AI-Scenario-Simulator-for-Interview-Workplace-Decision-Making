"""Groq API Provider implementation."""

from typing import Optional
import groq
from groq import (
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    APIConnectionError,
    APIError,
)
from config.groq_config import get_groq_api_key
from utils.error_handler import LLMError, LLMErrorCategory


def call_groq(
    prompt: str,
    model_id: str = "llama-3.3-70b-versatile",
    system_instruction: Optional[str] = None,
) -> str:
    """
    Execute a prompt against Groq API using the official SDK.

    Args:
        prompt: The user or task prompt.
        model_id: Groq model identifier (e.g., 'llama-3.3-70b-versatile').
        system_instruction: Optional system instruction guiding model persona/behavior.

    Returns:
        Raw text output from the model.

    Raises:
        LLMError: Standardized exception wrapping any provider or network failure.
    """
    api_key = get_groq_api_key()
    if not api_key:
        raise LLMError(
            message="Groq API Key is not configured. Add GROQ_API_KEY to your .env file.",
            provider="Groq",
            model_id=model_id,
            category=LLMErrorCategory.MISSING_API_KEY,
        )

    try:
        client = groq.Groq(api_key=api_key)

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=0.7,
        )

        if not response.choices or not response.choices[0].message.content:
            raise LLMError(
                message="Received empty response choices from Groq API.",
                provider="Groq",
                model_id=model_id,
                category=LLMErrorCategory.UNKNOWN,
            )

        return response.choices[0].message.content

    except AuthenticationError as e:
        raise LLMError(
            message=f"Groq authentication failed: {str(e)}",
            provider="Groq",
            model_id=model_id,
            category=LLMErrorCategory.INVALID_API_KEY,
            original_exception=e,
        )
    except RateLimitError as e:
        raise LLMError(
            message=f"Groq rate limit exceeded: {str(e)}",
            provider="Groq",
            model_id=model_id,
            category=LLMErrorCategory.RATE_LIMIT,
            original_exception=e,
        )
    except NotFoundError as e:
        raise LLMError(
            message=f"Groq model not found: {model_id}. Error: {str(e)}",
            provider="Groq",
            model_id=model_id,
            category=LLMErrorCategory.MODEL_NOT_FOUND,
            original_exception=e,
        )
    except APIConnectionError as e:
        raise LLMError(
            message=f"Failed to connect to Groq API: {str(e)}",
            provider="Groq",
            model_id=model_id,
            category=LLMErrorCategory.CONNECTION_ERROR,
            original_exception=e,
        )
    except APIError as e:
        raise LLMError(
            message=f"Groq API error: {str(e)}",
            provider="Groq",
            model_id=model_id,
            category=LLMErrorCategory.UNKNOWN,
            original_exception=e,
        )
    except Exception as e:
        if isinstance(e, LLMError):
            raise e
        raise LLMError(
            message=f"Unexpected error calling Groq API: {str(e)}",
            provider="Groq",
            model_id=model_id,
            category=LLMErrorCategory.UNKNOWN,
            original_exception=e,
        )
