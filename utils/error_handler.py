"""Centralized error handling and unified exception classes for LLM interactions."""

from typing import Optional


class LLMErrorCategory:
    """Error categories for granular diagnosis and UI messaging."""
    MISSING_API_KEY = "missing_api_key"
    INVALID_API_KEY = "invalid_api_key"
    RATE_LIMIT = "rate_limit"
    MODEL_NOT_FOUND = "model_not_found"
    CONNECTION_ERROR = "connection_error"
    JSON_PARSE_ERROR = "json_parse_error"
    UNKNOWN = "unknown"


class LLMError(Exception):
    """Unified exception raised by common LLM layer across all providers."""

    def __init__(
        self,
        message: str,
        provider: str = "Unknown",
        model_id: str = "Unknown",
        category: str = LLMErrorCategory.UNKNOWN,
        original_exception: Optional[Exception] = None,
    ):
        super().__init__(message)
        self.message = message
        self.provider = provider
        self.model_id = model_id
        self.category = category
        self.original_exception = original_exception

    def user_friendly_message(self) -> str:
        """Provide clear, actionable advice suitable for display in the UI."""
        if self.category == LLMErrorCategory.MISSING_API_KEY:
            if "Gemini" in self.provider:
                return (
                    "⚠️ **Gemini API Key Missing**\n\n"
                    "Please set `GEMINI_API_KEY=your_key_here` in your local `.env` file and restart/reload the app."
                )
            else:
                return (
                    "⚠️ **Groq API Key Missing**\n\n"
                    "Please set `GROQ_API_KEY=your_key_here` in your local `.env` file and restart/reload the app."
                )

        if self.category == LLMErrorCategory.INVALID_API_KEY:
            return (
                f"🚫 **Invalid API Key for {self.provider}**\n\n"
                f"The provided API key was rejected by the {self.provider} service. Please check your credentials in `.env`."
            )

        if self.category == LLMErrorCategory.RATE_LIMIT:
            return (
                f"⏳ **Rate Limit Exceeded ({self.provider})**\n\n"
                f"You have hit the request quota for `{self.model_id}`. Please wait a moment before trying again or switch models in the sidebar."
            )

        if self.category == LLMErrorCategory.MODEL_NOT_FOUND:
            return (
                f"🔍 **Model Not Available (`{self.model_id}`)**\n\n"
                f"The selected model `{self.model_id}` was not found or has been retired. Please select another active model from the sidebar."
            )

        if self.category == LLMErrorCategory.CONNECTION_ERROR:
            return (
                f"🌐 **Network / Connection Error**\n\n"
                f"Failed to connect to {self.provider} API. Please check your internet connection and try again."
            )

        if self.category == LLMErrorCategory.JSON_PARSE_ERROR:
            return (
                "🧩 **Structured Output Parse Error**\n\n"
                "The model response could not be parsed into valid structured JSON. Retrying or choosing a more capable model is recommended."
            )

        return f"❌ **{self.provider} Error:** {self.message}"


def handle_llm_error(error: Exception, provider: str = "", model_id: str = "") -> str:
    """Format an exception into a user-friendly UI message string."""
    if isinstance(error, LLMError):
        return error.user_friendly_message()
    return f"❌ Unexpected error while communicating with {provider or 'AI service'}: {str(error)}"
