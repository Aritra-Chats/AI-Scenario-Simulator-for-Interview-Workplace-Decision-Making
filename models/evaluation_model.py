"""Data model representing structured evaluation results for a user response."""

from typing import List, Optional
from pydantic import BaseModel, Field
import datetime


class EvaluationResult(BaseModel):
    """Multi-dimensional evaluation results and structured feedback for a user's response."""

    overall_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Overall composite score between 0 and 100.",
    )
    communication: int = Field(
        ...,
        ge=0,
        le=100,
        description="Communication effectiveness and articulation score (0-100).",
    )
    decision_making: int = Field(
        ...,
        ge=0,
        le=100,
        description="Quality of judgment, prioritization, and trade-off balance (0-100).",
    )
    problem_solving: int = Field(
        ...,
        ge=0,
        le=100,
        description="Analytical thinking, solution practicality, and structure (0-100).",
    )
    professionalism: int = Field(
        ...,
        ge=0,
        le=100,
        description="Emotional intelligence, demeanor, tact, and ethics (0-100).",
    )
    relevance: int = Field(
        ...,
        ge=0,
        le=100,
        description="Directness in addressing core challenge without drifting (0-100).",
    )
    clarity: int = Field(
        ...,
        ge=0,
        le=100,
        description="Precision, conciseness, and structured flow (0-100).",
    )
    strengths: List[str] = Field(
        default_factory=list,
        description="Key strengths demonstrated in the user's response.",
    )
    weaknesses: List[str] = Field(
        default_factory=list,
        description="Specific shortcomings or missed opportunities in the response.",
    )
    feedback: str = Field(
        ...,
        description="Detailed narrative feedback explaining the assessment.",
    )
    ideal_response: str = Field(
        ...,
        description="Exemplary model response demonstrating best practices for this scenario.",
    )
    missing_points: List[str] = Field(
        default_factory=list,
        description="Critical points, frameworks, or considerations the user omitted.",
    )
    improvement_suggestions: List[str] = Field(
        default_factory=list,
        description="Concrete, actionable recommendations for future responses.",
    )
    scenario_id: Optional[str] = Field(
        default="",
        description="ID of the scenario evaluated.",
    )
    evaluated_at: Optional[str] = Field(
        default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        description="Timestamp of evaluation generation.",
    )

    class Config:
        frozen = False
