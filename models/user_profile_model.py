"""Data model for user profile and scenario personalization parameters."""

from typing import Optional
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """User profile used to personalize scenario generation and evaluation."""

    role: str = Field(
        default="Software Engineer",
        description="Target job title or workplace role of the user.",
    )
    experience: str = Field(
        default="Fresher",
        description="Experience level: Fresher, Junior, Mid-level, or Senior.",
    )
    category: str = Field(
        default="Technical interview",
        description="Selected scenario category (interview subtype or workplace scenario).",
    )
    difficulty: str = Field(
        default="Intermediate",
        description="Current difficulty level: Beginner, Intermediate, or Advanced.",
    )
    skills: Optional[str] = Field(
        default="",
        description="Specific skills, tech stack, or domain focus (e.g., Python, System Design, Stakeholder Management).",
    )

    class Config:
        frozen = False
