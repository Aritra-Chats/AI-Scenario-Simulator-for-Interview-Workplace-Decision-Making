"""Report engine generating comprehensive multi-session performance analytics and growth roadmaps."""

from typing import List, Dict, Any
from models.user_profile_model import UserProfile
from engines.history_engine import (
    compute_average_scores,
    get_dimension_extremes,
    get_all_strengths,
    get_all_weaknesses,
    find_recurring_mistakes,
)
from prompts.report_prompts import build_report_prompt
from llm.llm_client import call_llm
from utils.json_parser import extract_json
from utils.error_handler import LLMError


def _build_fallback_report(
    history: List[Dict[str, Any]],
    user_profile: UserProfile,
    average_scores: Dict[str, float],
) -> Dict[str, Any]:
    """Analytical fallback report synthesized directly from history without LLM."""
    strongest_dim, weakest_dim = get_dimension_extremes(history)
    strong_text = f"Consistent performance in {strongest_dim[0].replace('_', ' ').title()} ({strongest_dim[1]:.0f}/100)" if strongest_dim else "Solid baseline communication"
    weak_text = f"Opportunity for growth in {weakest_dim[0].replace('_', ' ').title()} ({weakest_dim[1]:.0f}/100)" if weakest_dim else "Balancing speed with thoroughness"

    recurring = find_recurring_mistakes(history)
    strengths = get_all_strengths(history)

    return {
        "overall_average_score": average_scores.get("overall_score", 75.0),
        "average_scores": {k: v for k, v in average_scores.items() if k != "overall_score"},
        "strongest_areas": strengths[:3] if strengths else [strong_text, "Professional composure"],
        "weakest_areas": [weak_text, "Deeper quantitative trade-off evaluation"],
        "recurring_mistakes": recurring if recurring else ["Omission of secondary stakeholder notifications."],
        "personalized_recommendations": [
            f"Tailor communication for {user_profile.role} by establishing explicit decision criteria before proposing actions.",
            "Incorporate structured risk mitigation timelines for all technical or interpersonal choices.",
            "Proactively anticipate client and cross-functional team reactions during high-stress dilemmas.",
        ],
        "suggested_practice_areas": [
            "Leadership decision",
            "Technical interview",
            "Team conflict",
        ],
        "overall_assessment": (
            f"Over {len(history)} simulated scenarios, candidate demonstrated dependable professional instincts "
            f"with an overall average score of {average_scores.get('overall_score', 75.0):.1f}/100. "
            "Focused deliberate practice in quantitative decision modeling will prepare them for senior workplace challenges."
        ),
    }


def generate_performance_report(
    history: List[Dict[str, Any]],
    user_profile: UserProfile,
    provider: str,
    model_id: str,
) -> Dict[str, Any]:
    """
    Synthesize complete simulation history into a final performance report using LLM,
    with analytical fallback guarantee.

    Args:
        history: Session history list (requires at least 2 entries).
        user_profile: Active UserProfile.
        provider: AI Provider.
        model_id: Model ID.

    Returns:
        dict: Complete structured performance report.
    """
    if not history or len(history) < 2:
        return {
            "error": "At least 2 completed scenarios are required to generate a comprehensive performance report.",
            "overall_average_score": 0.0,
            "average_scores": {},
            "strongest_areas": [],
            "weakest_areas": [],
            "recurring_mistakes": [],
            "personalized_recommendations": [],
            "suggested_practice_areas": [],
            "overall_assessment": "Complete more scenarios to unlock performance analytics.",
        }

    average_scores = compute_average_scores(history)
    system_prompt, user_prompt = build_report_prompt(
        history=history,
        user_profile=user_profile,
        average_scores=average_scores,
    )

    try:
        raw_response = call_llm(
            prompt=user_prompt,
            provider=provider,
            model_id=model_id,
            system_instruction=system_prompt,
        )
        parsed_json = extract_json(raw_response)

        if parsed_json and isinstance(parsed_json, dict):
            # Ensure required keys
            parsed_json.setdefault("overall_average_score", average_scores.get("overall_score", 75.0))
            parsed_json.setdefault("average_scores", {k: v for k, v in average_scores.items() if k != "overall_score"})
            parsed_json.setdefault("strongest_areas", ["Structured approach", "Professional tone"])
            parsed_json.setdefault("weakest_areas", ["Quantifying impact", "Contingency planning"])
            parsed_json.setdefault("recurring_mistakes", ["Missing root cause focus"])
            parsed_json.setdefault("personalized_recommendations", ["Structure answers clearly"])
            parsed_json.setdefault("suggested_practice_areas", ["Team conflict", "Leadership decision"])
            parsed_json.setdefault("overall_assessment", "Solid progress demonstrated.")
            return parsed_json

    except (LLMError, Exception):
        pass

    return _build_fallback_report(history, user_profile, average_scores)
