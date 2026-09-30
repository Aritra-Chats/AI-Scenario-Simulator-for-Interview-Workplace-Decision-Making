"""Prompt templates for in-depth comparative analysis and ideal response generation."""

from typing import Tuple
from models.scenario_model import Scenario
from models.evaluation_model import EvaluationResult


def build_ideal_response_prompt(
    scenario: Scenario,
    user_response: str,
    evaluation: EvaluationResult,
) -> Tuple[str, str]:
    """
    Construct prompt for generating a deeper comparative analysis between the user's
    response and an exemplary benchmark answer.

    Returns:
        tuple: (system_prompt, user_prompt)
    """
    system_prompt = (
        "You are an Executive Communication Coach. Your goal is to dissect a candidate's answer "
        "and produce an exemplary model answer alongside a point-by-point comparative delta."
    )

    user_prompt = f"""Perform a comparative analysis for this scenario:

SCENARIO: {scenario.scenario_title}
CHALLENGE: {scenario.specific_challenge}
CANDIDATE'S ANSWER:
{user_response}

CURRENT EVALUATION:
Score: {evaluation.overall_score}/100
Weaknesses: {', '.join(evaluation.weaknesses)}

OUTPUT REQUIREMENTS:
Return valid JSON:
{{
  "ideal_response": "Polished, highly professional benchmark response.",
  "key_differentiators": [
    "Difference in framing or structure",
    "Difference in risk mitigation depth",
    "Difference in executive tone"
  ],
  "coaching_takeaway": "Single most impactful piece of advice for this scenario."
}}
"""
    return system_prompt, user_prompt
