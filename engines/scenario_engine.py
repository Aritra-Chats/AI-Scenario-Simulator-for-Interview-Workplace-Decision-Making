"""Scenario engine orchestrating personalized generation, retry parsing, and follow-ups."""

from typing import Optional, List, Dict, Any
import uuid
import datetime

from models.scenario_model import Scenario
from models.user_profile_model import UserProfile
from models.evaluation_model import EvaluationResult
from prompts.scenario_prompts import build_scenario_prompt
from prompts.followup_prompts import build_followup_prompt
from llm.llm_client import call_llm
from utils.json_parser import extract_json
from utils.error_handler import LLMError, LLMErrorCategory
from engines.difficulty_engine import (
    determine_next_difficulty,
    extract_history_performance_summary,
)


def _build_fallback_scenario(user_profile: UserProfile) -> Scenario:
    """Provide a realistic fallback scenario if LLM or API is unavailable."""
    is_interview = "interview" in user_profile.category.lower()
    scenario_type = "Interview" if is_interview else "Workplace"

    if is_interview:
        title = f"High-Stakes Technical Architecture Discussion ({user_profile.role})"
        context = (
            f"You are interviewing for a {user_profile.experience} {user_profile.role} position at a fast-growing tech company. "
            "The engineering director and principal architect are conducting a deep-dive situational interview."
        )
        description = (
            "The team is experiencing intermittent database connection pooling timeouts during peak traffic bursts, "
            "causing 504 Gateway errors for approximately 6% of active users. Two senior engineers disagree on the root cause: "
            "one advocates adding more read replicas immediately, while the other wants to refactor the core ORM query caching layer."
        )
        challenge = (
            "How do you approach investigating this issue, mediating the technical disagreement between the engineers, "
            "and deciding on the short-term vs long-term resolution?"
        )
        considerations = [
            "User impact during live peak traffic",
            "Cost and complexity of adding replicas vs query refactoring",
            "Team alignment and objective data-driven decision making",
        ]
        expected_skills = ["System Architecture", "Root Cause Analysis", "Stakeholder Communication"]
    else:
        title = f"Navigating Critical Deadline vs Technical Debt ({user_profile.role})"
        context = (
            f"You are working as a {user_profile.experience} {user_profile.role} on an agile delivery team. "
            "A major enterprise client launch is scheduled in 72 hours, committed at the VP level."
        )
        description = (
            "During final integration testing, your team discovers a critical data synchronization race condition. "
            "Fixing it properly requires architectural refactoring that will delay the launch by 5 business days. "
            "The Product Manager is urging the team to apply a fragile temporary patch and ship on time."
        )
        challenge = (
            "How do you handle this dilemma with the Product Manager, engineering team, and executive stakeholders?"
        )
        considerations = [
            "Risk of production data corruption versus client contract penalties",
            "Transparency with non-technical leadership",
            "Pragmatic mitigation strategies and contingency planning",
        ]
        expected_skills = ["Risk Management", "Ethical Decision Making", "Cross-functional Negotiation"]

    return Scenario(
        id=str(uuid.uuid4())[:8],
        scenario_title=title,
        scenario_type=scenario_type,
        category=user_profile.category,
        context=context,
        scenario_description=description,
        specific_challenge=challenge,
        key_considerations=considerations,
        difficulty=user_profile.difficulty,
        expected_skills=expected_skills,
        target_role=user_profile.role,
        created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


def generate_scenario(
    user_profile: UserProfile,
    provider: str,
    model_id: str,
    history: Optional[List[Dict[str, Any]]] = None,
) -> Scenario:
    """
    Generate a personalized scenario using the LLM with adaptive difficulty,
    history performance context, structured JSON parsing, and retry recovery.

    Args:
        user_profile: The user profile parameters.
        provider: Selected AI provider ('Google Gemini' or 'Groq').
        model_id: Selected model identifier.
        history: Optional session history for adaptation.

    Returns:
        Scenario: Fully parsed and validated Scenario object.
    """
    # 1. Apply Adaptive Difficulty if history exists
    effective_profile = user_profile.model_copy()
    if history and len(history) >= 2:
        new_diff, _ = determine_next_difficulty(history, current_difficulty=user_profile.difficulty)
        effective_profile.difficulty = new_diff

    # 2. Extract History Performance Context
    history_summary = extract_history_performance_summary(history or [])

    # 3. Build Prompt
    system_prompt, user_prompt = build_scenario_prompt(
        effective_profile, history_summary=history_summary
    )

    # 4. Invoke LLM with Retry Protection
    raw_response = ""
    parsed_json = None

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
                "CRITICAL REMINDER: Your previous response was not valid JSON. "
                "You MUST output raw parseable JSON only, starting with '{' and ending with '}'."
            )
            raw_response = call_llm(
                prompt=retry_prompt,
                provider=provider,
                model_id=model_id,
                system_instruction=system_prompt,
            )
            parsed_json = extract_json(raw_response)

    except LLMError:
        # Fall back gracefully on API or auth error
        return _build_fallback_scenario(effective_profile)
    except Exception:
        return _build_fallback_scenario(effective_profile)

    # 5. Construct Scenario Object
    if parsed_json and isinstance(parsed_json, dict):
        try:
            return Scenario(
                id=str(uuid.uuid4())[:8],
                scenario_title=parsed_json.get("scenario_title", f"{effective_profile.category} Scenario"),
                scenario_type=parsed_json.get("scenario_type", "Workplace"),
                category=parsed_json.get("category", effective_profile.category),
                context=parsed_json.get("context", "Context provided during simulation."),
                scenario_description=parsed_json.get("scenario_description", raw_response),
                specific_challenge=parsed_json.get(
                    "specific_challenge", "What is your immediate response to this situation?"
                ),
                key_considerations=parsed_json.get("key_considerations", []),
                difficulty=parsed_json.get("difficulty", effective_profile.difficulty),
                expected_skills=parsed_json.get("expected_skills", []),
                target_role=parsed_json.get("target_role", effective_profile.role),
                created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        except Exception:
            return _build_fallback_scenario(effective_profile)

    # If parsing completely failed, use calibrated fallback
    return _build_fallback_scenario(effective_profile)


def generate_followup_scenario(
    previous_scenario: Scenario,
    evaluation: EvaluationResult,
    user_profile: UserProfile,
    provider: str,
    model_id: str,
) -> Scenario:
    """
    Generate a continuation/stage-2 scenario targeting previously revealed weaknesses.

    Args:
        previous_scenario: Prior Scenario object.
        evaluation: Prior EvaluationResult object.
        user_profile: User profile.
        provider: AI Provider.
        model_id: Model ID.

    Returns:
        Scenario: Follow-up Scenario object.
    """
    system_prompt, user_prompt = build_followup_prompt(
        previous_scenario=previous_scenario,
        evaluation=evaluation,
        user_profile=user_profile,
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
            return Scenario(
                id=str(uuid.uuid4())[:8],
                scenario_title=parsed_json.get("scenario_title", f"Follow-up: {previous_scenario.scenario_title}"),
                scenario_type=previous_scenario.scenario_type,
                category=previous_scenario.category,
                context=parsed_json.get("context", previous_scenario.context),
                scenario_description=parsed_json.get("scenario_description", "The situation continues to evolve."),
                specific_challenge=parsed_json.get("specific_challenge", "How do you respond to this new development?"),
                key_considerations=parsed_json.get("key_considerations", []),
                difficulty=user_profile.difficulty,
                expected_skills=parsed_json.get("expected_skills", previous_scenario.expected_skills),
                target_role=user_profile.role,
                created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
    except Exception:
        pass

    # Curated Follow-up Fallback
    return Scenario(
        id=str(uuid.uuid4())[:8],
        scenario_title=f"Follow-up Complication: {previous_scenario.scenario_title}",
        scenario_type=previous_scenario.scenario_type,
        category=previous_scenario.category,
        context=f"Following your initial decision on '{previous_scenario.scenario_title}', the team took immediate action.",
        scenario_description=(
            "While your initial decision addressed the urgent symptoms, an unforeseen side effect has emerged: "
            "a key stakeholder expresses frustration about communication gaps and questions the trade-offs made."
        ),
        specific_challenge="How do you handle this pushback, justify your rationale, and maintain stakeholder trust?",
        key_considerations=[
            "Addressing stakeholder sentiment constructively",
            "Clarifying trade-offs without becoming defensive",
            "Setting up preventative governance for the future",
        ],
        difficulty=user_profile.difficulty,
        expected_skills=["Stakeholder Diplomacy", "Defensive De-escalation", "Accountability"],
        target_role=user_profile.role,
        created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
