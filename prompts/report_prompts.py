"""Prompt templates for cumulative performance reporting and personalized career growth roadmaps."""

from typing import Tuple, List, Dict, Any
from models.user_profile_model import UserProfile


def build_report_prompt(
    history: List[Dict[str, Any]],
    user_profile: UserProfile,
    average_scores: Dict[str, float],
) -> Tuple[str, str]:
    """
    Construct system and user prompts to generate a holistic performance synthesis report.

    Args:
        history: Complete session history.
        user_profile: User profile.
        average_scores: Pre-calculated average scores dictionary.

    Returns:
        tuple: (system_prompt, user_prompt)
    """
    system_prompt = (
        "You are a Chief Talent Officer and Principal Leadership Assessor.\n"
        "Your task is to synthesize a comprehensive performance report for a professional who has completed "
        "multiple high-stakes interview and workplace simulation scenarios.\n\n"
        "STANDARDS:\n"
        "1. Evidence-Based Synthesis: Rely on the historical scores, recurring strengths, and persistent weaknesses.\n"
        "2. Actionable Coaching: Provide concrete, actionable improvement recommendations tailored directly to their role.\n"
        "3. Output format: Return ONLY a valid, parseable JSON object matching the requested schema."
    )

    # Format history records
    history_bullets = []
    for i, item in enumerate(history, 1):
        scen = item.get("scenario")
        ev = item.get("evaluation")
        title = scen.scenario_title if scen else f"Scenario {i}"
        cat = scen.category if scen else "General"
        score = ev.overall_score if ev else "N/A"
        weaknesses = ", ".join(ev.weaknesses[:2]) if ev and ev.weaknesses else "None"
        history_bullets.append(f"- Scenario {i} ('{title}', {cat}): Score {score}/100 | Weaknesses: {weaknesses}")

    history_text = "\n".join(history_bullets)
    scores_text = "\n".join([f"  - {k}: {v:.1f}/100" for k, v in average_scores.items()])

    user_prompt = f"""Generate a comprehensive performance evaluation report based on the candidate's simulation history:

CANDIDATE PROFILE:
- Target Role: {user_profile.role}
- Experience Level: {user_profile.experience}
- Total Scenarios Completed: {len(history)}

HISTORICAL PERFORMANCE DATA:
Calculated Dimension Averages:
{scores_text}

Session Chronology:
{history_text}

OUTPUT REQUIREMENTS:
Produce a single JSON object with the following schema:
{{
  "overall_average_score": {average_scores.get('overall_score', 75.0)},
  "average_scores": {{
    "communication": {average_scores.get('communication', 75.0)},
    "decision_making": {average_scores.get('decision_making', 75.0)},
    "problem_solving": {average_scores.get('problem_solving', 75.0)},
    "professionalism": {average_scores.get('professionalism', 75.0)},
    "relevance": {average_scores.get('relevance', 75.0)},
    "clarity": {average_scores.get('clarity', 75.0)}
  }},
  "strongest_areas": [
    "Most prominent behavioral or technical strength observed across sessions",
    "Second prominent strength"
  ],
  "weakest_areas": [
    "Most persistent vulnerability or blindspot",
    "Second persistent weakness"
  ],
  "recurring_mistakes": [
    "Primary recurring mistake or omitted perspective across multiple challenges",
    "Secondary recurring oversight"
  ],
  "personalized_recommendations": [
    "High-impact, role-specific coaching action item #1",
    "High-impact coaching action item #2",
    "High-impact coaching action item #3"
  ],
  "suggested_practice_areas": [
    "Suggested scenario category #1 for subsequent practice",
    "Suggested scenario category #2",
    "Suggested scenario category #3"
  ],
  "overall_assessment": "3-4 sentence holistic executive summary of the candidate's trajectory, readiness, and growth potential."
}}

Respond with valid JSON only.
"""
    return system_prompt, user_prompt
