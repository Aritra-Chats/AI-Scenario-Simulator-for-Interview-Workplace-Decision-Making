"""Prompt templates for multi-dimensional AI response evaluation and scoring."""

from typing import Tuple
from models.scenario_model import Scenario
from models.user_profile_model import UserProfile


def build_evaluation_system_prompt() -> str:
    """System prompt establishing the evaluator persona and assessment standards."""
    return (
        "You are a Senior Executive Talent Assessor, Leadership Coach, and Technical Interview Evaluator.\n"
        "Your role is to rigorously evaluate a candidate's response to an interview or workplace simulation scenario.\n\n"
        "EVALUATION STANDARDS:\n"
        "1. Multi-Dimensional Scoring: Grade each dimension objectively between 0 and 100 based on standard industry expectations:\n"
        "   - 90-100: Exceptional, executive-level nuance, anticipates second-order consequences.\n"
        "   - 75-89: Strong, competent, practical, and well-reasoned.\n"
        "   - 55-74: Adequate, but lacks depth, missed key trade-offs, or somewhat generic.\n"
        "   - 0-54: Weak, inappropriate, evasive, or failed to address the core dilemma.\n"
        "2. Concrete Strengths & Weaknesses: Avoid vague praise. Pinpoint exact phrasing, decisions, or omissions.\n"
        "3. Missing Nuances: Identify critical considerations, business implications, or stakeholder perspectives they missed.\n"
        "4. Exemplary Ideal Response: Provide a polished, realistic model answer demonstrating how a top 1% professional would answer.\n"
        "5. Output Constraint: Return ONLY a valid, parseable JSON object matching the exact requested schema."
    )


def build_evaluation_prompt(
    scenario: Scenario,
    user_response: str,
    user_profile: UserProfile,
) -> Tuple[str, str]:
    """
    Construct evaluation prompts to analyze a user's scenario response.

    Args:
        scenario: The active Scenario object.
        user_response: The raw response text entered by the candidate.
        user_profile: The user profile.

    Returns:
        tuple: (system_prompt, user_prompt)
    """
    system_prompt = build_evaluation_system_prompt()

    user_prompt = f"""Evaluate the following candidate response to the simulation scenario:

SCENARIO CONTEXT:
- Title: {scenario.scenario_title}
- Category: {scenario.category}
- Target Role: {scenario.target_role or user_profile.role}
- Experience Level: {user_profile.experience}
- Difficulty Level: {scenario.difficulty}
- Background Context: {scenario.context}
- Situation Description: {scenario.scenario_description}
- Specific Challenge Asked: {scenario.specific_challenge}
- Key Considerations: {', '.join(scenario.key_considerations)}
- Expected Competencies: {', '.join(scenario.expected_skills)}

CANDIDATE'S SUBMITTED RESPONSE:
\"\"\"
{user_response}
\"\"\"

OUTPUT REQUIREMENTS:
Produce a single JSON object with the following schema:
{{
  "overall_score": 0-100 (integer composite score),
  "communication": 0-100 (clarity, persuasion, tone, diplomacy),
  "decision_making": 0-100 (sound judgment, prioritization, trade-off awareness),
  "problem_solving": 0-100 (practicality, structured thinking, root-cause resolution),
  "professionalism": 0-100 (emotional intelligence, demeanor, composure, ethics),
  "relevance": 0-100 (directly addressing the prompt without evasion or fluff),
  "clarity": 0-100 (conciseness, structure, articulate expression),
  "strengths": [
    "First specific strength with reference to their response",
    "Second specific strength"
  ],
  "weaknesses": [
    "First specific shortcoming or missed opportunity",
    "Second specific shortcoming"
  ],
  "feedback": "Comprehensive 3-4 sentence evaluation highlighting what worked well and what compromised the response.",
  "ideal_response": "A detailed, first-person exemplary model response showing how an elite candidate would answer this exact challenge.",
  "missing_points": [
    "Crucial perspective or contingency the user omitted",
    "Important metric, framework, or follow-up step missed"
  ],
  "improvement_suggestions": [
    "First actionable tip for future similar scenarios",
    "Second actionable tip"
  ]
}}

Respond with valid JSON only.
"""
    return system_prompt, user_prompt
