"""Data model representing a generated scenario."""

from typing import List, Optional
from pydantic import BaseModel, Field
import uuid
import datetime


class Scenario(BaseModel):
    """Structured representation of a generated interview or workplace scenario."""

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4())[:8],
        description="Unique identifier for the scenario instance.",
    )
    scenario_title: str = Field(
        ...,
        description="Concise, realistic title of the scenario.",
    )
    scenario_type: str = Field(
        default="Workplace",
        description="High-level category: 'Interview' or 'Workplace'.",
    )
    category: str = Field(
        ...,
        description="Specific scenario subcategory (e.g., Technical interview, Team conflict).",
    )
    context: str = Field(
        ...,
        description="Background company setting, team dynamics, or project environment.",
    )
    scenario_description: str = Field(
        ...,
        description="Detailed scenario unfolding the tension, question, or dilemma.",
    )
    specific_challenge: str = Field(
        ...,
        description="Direct question or action required from the user.",
    )
    key_considerations: List[str] = Field(
        default_factory=list,
        description="Nuances, constraints, or stakes to consider.",
    )
    difficulty: str = Field(
        default="Intermediate",
        description="Difficulty level: Beginner, Intermediate, or Advanced.",
    )
    expected_skills: List[str] = Field(
        default_factory=list,
        description="Key skills/competencies being evaluated in this scenario.",
    )
    target_role: Optional[str] = Field(
        default="",
        description="Role for which this scenario was tailored.",
    )
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp of when the scenario was generated.",
    )

    class Config:
        frozen = False
