"""Prompt templates for follow-up scenario generation targeting identified weaknesses."""

from typing import Tuple, Optional
from models.scenario_model import Scenario
from models.evaluation_model import EvaluationResult
from models.user_profile_model import UserProfile


def build_followup_prompt(
    previous_scenario: Scenario,
    evaluation: EvaluationResult,
    user_profile: UserProfile,
) -> Tuple[str, str]:
    """
    Construct system and user prompts to generate a follow-up scenario directly responding
    to the user's previous decisions, specifically targeting areas of weakness or missed nuances.

    Args:
        previous_scenario: The scenario just completed.
        evaluation: The evaluation result of the user's response.
        user_profile: The user profile.

    Returns:
        tuple: (system_prompt, user_prompt)
    """
    system_prompt = (
        "You are an expert Simulation Assessor conducting a multi-stage simulation.\n"
        "Your task is to generate a realistic follow-up scenario (Stage 2) that naturally evolves from "
        "the previous scenario and directly tests the candidate on the weaknesses or blindspots they displayed in their earlier response.\n\n"
        "DIRECTIVES:\n"
        "1. Continuity: Acknowledge the aftermath or reaction to their previous actions.\n"
        "2. Targeted Pressure: Intentionally introduce a complication that addresses their specific weaknesses or missing points.\n"
        "3. Realism: Keep the workplace/interview environment authentic and grounded.\n"
        "4. Format: Output MUST be valid JSON only matching the exact requested schema."
    )

    weaknesses_str = "\n".join([f"- {w}" for w in evaluation.weaknesses]) if evaluation.weaknesses else "- General depth and trade-off analysis"
    missing_str = "\n".join([f"- {m}" for m in evaluation.missing_points]) if evaluation.missing_points else "- Deeper risk mitigation"

    user_prompt = f"""Generate a Stage 2 Follow-Up scenario based on the following previous interaction:

PREVIOUS SCENARIO:
- Title: {previous_scenario.scenario_title}
- Category: {previous_scenario.category}
- Context: {previous_scenario.context}
- Previous Challenge: {previous_scenario.specific_challenge}

PREVIOUS EVALUATION (AREAS TO TARGET):
- Overall Score: {evaluation.overall_score}/100
- Weaknesses identified:
{weaknesses_str}
- Critical considerations omitted:
{missing_str}

CANDIDATE PROFILE:
- Role: {user_profile.role}
- Experience: {user_profile.experience}
- Difficulty: {user_profile.difficulty}

OUTPUT REQUIREMENTS:
Produce a single JSON object with the following schema:
{{
  "scenario_title": "Follow-up: [Descriptive title of the evolving situation]",
  "scenario_type": "{previous_scenario.scenario_type}",
  "category": "{previous_scenario.category}",
  "context": "Context describing how the situation has evolved following the initial response (2-3 sentences)",
  "scenario_description": "New complication or unexpected pushback arising from the initial outcome that directly challenges their identified weak spots (3-4 sentences)",
  "specific_challenge": "The immediate question, negotiation, or decision required from the user right now (1-2 sentences)",
  "key_considerations": [
    "Complication arising from earlier decision",
    "Stakeholder reaction or technical consequence",
    "Balancing immediate fix with long-term strategy"
  ],
  "difficulty": "{user_profile.difficulty}",
  "expected_skills": [
    "Adaptive Communication",
    "Crisis Management",
    "Negotiation under Pushback"
  ],
  "target_role": "{user_profile.role}"
}}

Respond with valid JSON only.
"""
    return system_prompt, user_prompt
