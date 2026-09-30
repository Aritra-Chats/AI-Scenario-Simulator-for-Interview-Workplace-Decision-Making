"""Input validation and sanitization utilities for user profiles and responses."""

from typing import Tuple, Any, Optional
from config.settings import ALL_CATEGORIES, DIFFICULTY_LEVELS, EXPERIENCE_LEVELS


def validate_user_response(text: Optional[str], min_length: int = 40) -> Tuple[bool, str]:
    """
    Validate user response text before sending for AI evaluation.

    Args:
        text: The response string typed by user.
        min_length: Minimum character threshold for a meaningful answer.

    Returns:
        tuple (is_valid, validation_message)
    """
    if not text or not text.strip():
        return False, "Response cannot be empty. Please enter your answer to the scenario."

    cleaned = text.strip()
    if len(cleaned) < min_length:
        return (
            False,
            f"Response is too short ({len(cleaned)} characters). Please provide at least {min_length} characters to allow a comprehensive multi-dimensional evaluation.",
        )

    return True, "Valid response."


def validate_user_profile(profile: Any) -> Tuple[bool, str]:
    """
    Validate that user profile has required fields and recognized categories.

    Args:
        profile: UserProfile instance or dictionary.

    Returns:
        tuple (is_valid, validation_message)
    """
    if profile is None:
        return False, "User profile is required."

    role = getattr(profile, "role", None) or (profile.get("role") if isinstance(profile, dict) else None)
    if not role or not str(role).strip():
        return False, "Target role cannot be blank."

    experience = getattr(profile, "experience", None) or (profile.get("experience") if isinstance(profile, dict) else None)
    if experience not in EXPERIENCE_LEVELS:
        return False, f"Invalid experience level: {experience}."

    category = getattr(profile, "category", None) or (profile.get("category") if isinstance(profile, dict) else None)
    if category not in ALL_CATEGORIES:
        return False, f"Invalid category: {category}."

    difficulty = getattr(profile, "difficulty", None) or (profile.get("difficulty") if isinstance(profile, dict) else None)
    if difficulty not in DIFFICULTY_LEVELS:
        return False, f"Invalid difficulty: {difficulty}."

    return True, "Valid profile."


def sanitize_user_input(text: Optional[str], max_length: int = 4000) -> str:
    """
    Sanitize and clamp user response text to avoid prompt injection or overflow.
    """
    if not text:
        return ""
    cleaned = text.strip()
    # Normalize excessive newlines
    import re
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    # Clamp length
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned
