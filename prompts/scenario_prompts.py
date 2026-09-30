"""Prompt templates for realistic interview and workplace scenario generation."""

from typing import Tuple, Optional
from models.user_profile_model import UserProfile


def build_scenario_system_prompt() -> str:
    """System prompt establishing persona and JSON output constraints."""
    return (
        "You are an elite Executive Interviewer, Organizational Psychologist, and Workplace Simulation Designer.\n"
        "Your role is to craft deeply realistic, immersive, and nuanced workplace or interview scenarios "
        "tailored precisely to a candidate's specific job role, experience level, scenario category, and difficulty.\n\n"
        "CORE DIRECTIVES:\n"
        "1. Realism: Create authentic situations with competing priorities, realistic team dynamics, constraints, or technical hurdles.\n"
        "2. No Generic Questions: Do NOT ask standard cliché questions like 'tell me about a time you failed' or 'what is polymorphism'. "
        "Instead, frame an active dilemma or technical hurdle where the user must take ownership, make decisions, or communicate under pressure.\n"
        "3. Calibration: Ensure the complexity matches the specified experience level and difficulty.\n"
        "4. Output format: You MUST return ONLY a valid, parseable JSON object matching the exact requested schema. "
        "Do not include any greeting, explanation, or conversational commentary."
    )


def build_scenario_prompt(
    user_profile: UserProfile,
    history_summary: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Construct the system and user prompts for generating a personalized scenario.

    Args:
        user_profile: UserProfile containing role, experience, category, difficulty, skills.
        history_summary: Optional performance string from previous scenarios.

    Returns:
        tuple: (system_prompt, user_prompt)
    """
    system_prompt = build_scenario_system_prompt()

    # Determine scenario type based on category
    scenario_type = "Interview" if "interview" in user_profile.category.lower() else "Workplace"

    history_injection = ""
    if history_summary:
        history_injection = (
            f"\nPREVIOUS PERFORMANCE INSIGHTS:\n"
            f"{history_summary}\n"
            f"Use this context to subtly test or address their previously identified weak spots."
        )

    skills_focus = f"Focus Skills/Keywords: {user_profile.skills}" if user_profile.skills else "Skills: Core competencies for this role"

    user_prompt = f"""Generate a highly realistic simulation scenario based on the following candidate profile:

CANDIDATE PROFILE:
- Target Role: {user_profile.role}
- Experience Level: {user_profile.experience}
- Scenario Type: {scenario_type}
- Specific Category: {user_profile.category}
- Difficulty Level: {user_profile.difficulty}
- {skills_focus}
{history_injection}

OUTPUT REQUIREMENTS:
Produce a single JSON object with the following schema:
{{
  "scenario_title": "A concise, engaging title for this scenario",
  "scenario_type": "{scenario_type}",
  "category": "{user_profile.category}",
  "context": "Rich 2-3 sentence background context (company setting, team structure, current project state, stakes)",
  "scenario_description": "Detailed 3-5 sentence narrative of the exact situation, dilemma, or technical breakdown that has just happened",
  "specific_challenge": "The exact question, decision, or action required from the user right now (1-2 sentences)",
  "key_considerations": [
    "First critical trade-off or nuance to keep in mind",
    "Second constraint (e.g. deadline, stakeholder sentiment, technical limitation)",
    "Third consideration (e.g. business impact, ethics, communication risk)"
  ],
  "difficulty": "{user_profile.difficulty}",
  "expected_skills": [
    "Primary skill evaluated (e.g. Conflict De-escalation, Incident Triage)",
    "Secondary skill evaluated",
    "Tertiary skill evaluated"
  ],
  "target_role": "{user_profile.role}"
}}

Respond with valid JSON only. Do not include markdown code block tags if possible, or wrap in ```json ... ```.
"""
    return system_prompt, user_prompt
