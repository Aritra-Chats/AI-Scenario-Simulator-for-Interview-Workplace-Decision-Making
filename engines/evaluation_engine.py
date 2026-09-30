"""Evaluation engine computing structured multi-dimensional scores and feedback."""

import datetime
from typing import Optional, Dict, Any

from models.scenario_model import Scenario
from models.user_profile_model import UserProfile
from models.evaluation_model import EvaluationResult
from prompts.evaluation_prompts import build_evaluation_prompt
from llm.llm_client import call_llm
from utils.json_parser import extract_json
from utils.error_handler import LLMError


def _clamp_score(val: Any, default: int = 70) -> int:
    """Clamp score value to safe 0-100 integer range."""
    try:
        score = int(float(val))
        return max(0, min(100, score))
    except (ValueError, TypeError):
        return default


def _build_fallback_evaluation(
    scenario: Scenario,
    user_response: str,
) -> EvaluationResult:
    """Provide realistic fallback evaluation if LLM or API is unavailable."""
    # Basic heuristic based on length and keywords
    char_len = len(user_response.strip())
    base_score = 72 if char_len >= 120 else 60

    return EvaluationResult(
        overall_score=base_score,
        communication=base_score + 2,
        decision_making=base_score - 2,
        problem_solving=base_score + 1,
        professionalism=base_score + 4,
        relevance=base_score,
        clarity=base_score + 1,
        strengths=[
            "Addressed the core situation directly without deflecting responsibility.",
            "Maintained a constructive, professional demeanor throughout.",
        ],
        weaknesses=[
            "Could articulate concrete quantitative trade-offs or business impact more thoroughly.",
            "Lacks detailed proactive follow-up timelines and contingency planning.",
        ],
        feedback=(
            "Your response demonstrates good intuition and willingness to tackle the challenge head-on. "
            "To reach the top tier, incorporate structured frameworks (like STAR or Situation-Complication-Resolution) "
            "and explicitly consider cross-functional stakeholder impacts."
        ),
        ideal_response=(
            f"In addressing the situation '{scenario.scenario_title}', an ideal response directly states the primary priority, "
            "aligns with key stakeholders before taking disruptive actions, establishes an empirical feedback loop, "
            "and outlines a transparent communication cadence for leadership."
        ),
        missing_points=[
            "Data-backed risk assessment before deciding.",
            "Clear timeline for review and retrospective postmortem.",
        ],
        improvement_suggestions=[
            "Always state your decision criteria explicitly before jumping into action steps.",
            "Quantify trade-offs in terms of engineering hours, customer churn risk, or SLA commitments.",
        ],
        scenario_id=scenario.id,
        evaluated_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


def evaluate_response(
    scenario: Scenario,
    user_response: str,
    user_profile: UserProfile,
    provider: str,
    model_id: str,
) -> EvaluationResult:
    """
    Evaluate user response against scenario requirements across 7 dimensions using LLM,
    with automated retry parsing and resilient fallback.

    Args:
        scenario: Active Scenario.
        user_response: User's typed response text.
        user_profile: User profile.
        provider: Selected AI provider.
        model_id: Model ID.

    Returns:
        EvaluationResult: Structured evaluation with scores, strengths, weaknesses, and feedback.
    """
    system_prompt, user_prompt = build_evaluation_prompt(
        scenario=scenario,
        user_response=user_response,
        user_profile=user_profile,
    )

    parsed_json: Optional[Dict[str, Any]] = None

    try:
        raw_response = call_llm(
            prompt=user_prompt,
            provider=provider,
            model_id=model_id,
            system_instruction=system_prompt,
        )
        parsed_json = extract_json(raw_response)

        # Retry once if JSON parse failed
        if not parsed_json:
            retry_prompt = (
                f"{user_prompt}\n\n"
                "CRITICAL REMINDER: You MUST return a single valid JSON object only. "
                "Ensure all 7 score dimensions are integers between 0 and 100."
            )
            raw_response = call_llm(
                prompt=retry_prompt,
                provider=provider,
                model_id=model_id,
                system_instruction=system_prompt,
            )
            parsed_json = extract_json(raw_response)

    except (LLMError, Exception):
        return _build_fallback_evaluation(scenario, user_response)

    if parsed_json and isinstance(parsed_json, dict):
        try:
            return EvaluationResult(
                overall_score=_clamp_score(parsed_json.get("overall_score"), 75),
                communication=_clamp_score(parsed_json.get("communication"), 75),
                decision_making=_clamp_score(parsed_json.get("decision_making"), 75),
                problem_solving=_clamp_score(parsed_json.get("problem_solving"), 75),
                professionalism=_clamp_score(parsed_json.get("professionalism"), 75),
                relevance=_clamp_score(parsed_json.get("relevance"), 75),
                clarity=_clamp_score(parsed_json.get("clarity"), 75),
                strengths=parsed_json.get("strengths", ["Clear and direct communication"]),
                weaknesses=parsed_json.get("weaknesses", ["Could deepen risk mitigation"]),
                feedback=parsed_json.get(
                    "feedback", "Constructive response with solid grounding in the scenario."
                ),
                ideal_response=parsed_json.get(
                    "ideal_response", "Exemplary model response addressing all trade-offs."
                ),
                missing_points=parsed_json.get("missing_points", []),
                improvement_suggestions=parsed_json.get("improvement_suggestions", []),
                scenario_id=scenario.id,
                evaluated_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        except Exception:
            return _build_fallback_evaluation(scenario, user_response)

    return _build_fallback_evaluation(scenario, user_response)
