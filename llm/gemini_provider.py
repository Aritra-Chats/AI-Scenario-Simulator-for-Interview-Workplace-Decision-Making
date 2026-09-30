"""Google Gemini API Provider implementation."""

from typing import Optional
import google.generativeai as genai
from google.api_core.exceptions import (
    InvalidArgument,
    PermissionDenied,
    ResourceExhausted,
    NotFound,
    GoogleAPIError,
)
from config.gemini_config import get_gemini_api_key
from utils.error_handler import LLMError, LLMErrorCategory


def call_gemini(
    prompt: str,
    model_id: str = "gemini-2.5-flash",
    system_instruction: Optional[str] = None,
) -> str:
    """
    Execute a prompt against Google Gemini API using the official SDK.

    Args:
        prompt: The user or task prompt.
        model_id: Gemini model identifier (e.g., 'gemini-3.6-flash', 'gemini-2.5-flash').
        system_instruction: Optional system-level prompt guiding model persona/behavior.

    Returns:
        Raw text output from the model.

    Raises:
        LLMError: Standardized exception wrapping any provider or network failure.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        raise LLMError(
            message="Gemini API Key is not configured. Add GEMINI_API_KEY to your .env file.",
            provider="Google Gemini",
            model_id=model_id,
            category=LLMErrorCategory.MISSING_API_KEY,
        )

    try:
        genai.configure(api_key=api_key)

        model_kwargs = {"model_name": model_id}
        if system_instruction:
            model_kwargs["system_instruction"] = system_instruction

        model = genai.GenerativeModel(**model_kwargs)
        response = model.generate_content(prompt)

        if not response.text:
            raise LLMError(
                message="Received empty text response from Gemini API.",
                provider="Google Gemini",
                model_id=model_id,
                category=LLMErrorCategory.UNKNOWN,
            )

        return response.text

    except (PermissionDenied, InvalidArgument) as e:
        raise LLMError(
            message=f"Authentication or argument failed: {str(e)}",
            provider="Google Gemini",
            model_id=model_id,
            category=LLMErrorCategory.INVALID_API_KEY,
            original_exception=e,
        )
    except ResourceExhausted as e:
        raise LLMError(
            message=f"Quota exceeded or rate limited: {str(e)}",
            provider="Google Gemini",
            model_id=model_id,
            category=LLMErrorCategory.RATE_LIMIT,
            original_exception=e,
        )
    except NotFound as e:
        raise LLMError(
            message=f"Model not found: {model_id}. Error: {str(e)}",
            provider="Google Gemini",
            model_id=model_id,
            category=LLMErrorCategory.MODEL_NOT_FOUND,
            original_exception=e,
        )
    except GoogleAPIError as e:
        raise LLMError(
            message=f"Google Gemini API error: {str(e)}",
            provider="Google Gemini",
            model_id=model_id,
            category=LLMErrorCategory.CONNECTION_ERROR,
            original_exception=e,
        )
    except Exception as e:
        if isinstance(e, LLMError):
            raise e
        raise LLMError(
            message=f"Unexpected error calling Gemini API: {str(e)}",
            provider="Google Gemini",
            model_id=model_id,
            category=LLMErrorCategory.UNKNOWN,
            original_exception=e,
        )
