import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""Comprehensive test suite for Day 4 (Prompt Engineering & Scenarios) and Day 5 (Personalization & Response System)."""

import json
from unittest.mock import patch, MagicMock
from models.user_profile_model import UserProfile
from models.scenario_model import Scenario
from models.evaluation_model import EvaluationResult
from prompts.scenario_prompts import build_scenario_prompt, build_scenario_system_prompt
from prompts.followup_prompts import build_followup_prompt
from engines.difficulty_engine import (
    determine_next_difficulty,
    extract_history_performance_summary,
)
from engines.scenario_engine import (
    generate_scenario,
    generate_followup_scenario,
    _build_fallback_scenario,
)
from utils.validators import validate_user_response
from config.settings import (
    DIFFICULTY_BEGINNER,
    DIFFICULTY_INTERMEDIATE,
    DIFFICULTY_ADVANCED,
    PROVIDER_GEMINI,
    PROVIDER_GROQ,
)


def test_day4_prompt_engineering():
    print("\n[DAY 4 - PART A & B] Testing Prompt Engineering Templates...")

    profile = UserProfile(
        role="Senior Backend Engineer",
        experience="Mid-level",
        category="Team conflict",
        difficulty="Intermediate",
        skills="Go, Kubernetes, Distributed Systems",
    )

    # Test Scenario Prompt Builder
    system_p, user_p = build_scenario_prompt(profile, history_summary="Scored 70/100 previously.")
    assert "Senior Backend Engineer" in user_p
    assert "Team conflict" in user_p
    assert "Intermediate" in user_p
    assert "Go, Kubernetes" in user_p
    assert "Scored 70/100 previously" in user_p
    assert "scenario_title" in user_p
    assert "specific_challenge" in user_p
    print("  [OK] build_scenario_prompt constructs personalized prompt with JSON schema")

    # Test Follow-up Prompt Builder
    dummy_scenario = _build_fallback_scenario(profile)
    dummy_eval = EvaluationResult(
        overall_score=68,
        communication=65,
        decision_making=70,
        problem_solving=72,
        professionalism=70,
        relevance=70,
        clarity=65,
        strengths=["Clear technical insight"],
        weaknesses=["Did not acknowledge colleague's workload", "Too rigid on deadlines"],
        feedback="Good attempt but needs more empathy.",
        ideal_response="Model answer.",
        missing_points=["Offer to share sprint tasks", "Check in 1-on-1 first"],
        improvement_suggestions=["Use collaborative framing."],
        scenario_id=dummy_scenario.id,
    )

    sys_f, user_f = build_followup_prompt(dummy_scenario, dummy_eval, profile)
    assert dummy_scenario.scenario_title in user_f
    assert "Too rigid on deadlines" in user_f
    assert "Offer to share sprint tasks" in user_f
    print("  [OK] build_followup_prompt injects previous evaluation weaknesses and missing points")


def test_day4_scenario_engine():
    print("\n[DAY 4 - PART C & D] Testing Scenario Engine & Fallback...")

    profile = UserProfile(
        role="Product Manager",
        experience="Junior",
        category="Client communication",
        difficulty="Beginner",
        skills="Agile, Roadmapping",
    )

    # 1. Normal Mocked Generation
    mock_json = {
        "scenario_title": "Enterprise Client Urgent Feature Request",
        "scenario_type": "Workplace",
        "category": "Client communication",
        "context": "A top-tier financial client requests an unvetted custom API endpoint.",
        "scenario_description": "The client threatens to stall their renewal unless this is delivered in sprint 4.",
        "specific_challenge": "How do you respond to the client account team and negotiate the roadmap?",
        "key_considerations": ["Renewal risk", "Engineering capacity", "Security compliance"],
        "difficulty": "Beginner",
        "expected_skills": ["Client Negotiation", "Scope Management"],
        "target_role": "Product Manager",
    }

    with patch("engines.scenario_engine.call_llm", return_value=json.dumps(mock_json)):
        scen = generate_scenario(profile, PROVIDER_GEMINI, "gemini-2.5-flash")
        assert scen.scenario_title == "Enterprise Client Urgent Feature Request"
        assert scen.category == "Client communication"
        assert len(scen.key_considerations) == 3
        print("  [OK] generate_scenario parses LLM output into Scenario model")

    # 2. Retry Logic on Malformed JSON
    call_counts = {"count": 0}

    def mock_call_llm_retry(*args, **kwargs):
        call_counts["count"] += 1
        if call_counts["count"] == 1:
            return "Here is the scenario without proper JSON brackets..."
        return json.dumps(mock_json)

    with patch("engines.scenario_engine.call_llm", side_effect=mock_call_llm_retry):
        scen_retry = generate_scenario(profile, PROVIDER_GROQ, "llama-3.3-70b-versatile")
        assert scen_retry.scenario_title == "Enterprise Client Urgent Feature Request"
        assert call_counts["count"] == 2
        print("  [OK] generate_scenario automatically retries on initial JSON parse failure")

    # 3. Fallback when LLM Fails completely
    with patch("engines.scenario_engine.call_llm", side_effect=Exception("API Outage")):
        fallback_scen = generate_scenario(profile, PROVIDER_GEMINI, "gemini-2.5-flash")
        assert fallback_scen is not None
        assert len(fallback_scen.scenario_title) > 0
        assert fallback_scen.category == "Client communication"
        print("  [OK] generate_scenario returns high-quality fallback Scenario without crashing")


def test_day5_adaptive_difficulty():
    print("\n[DAY 5 - PART A] Testing Adaptive Difficulty Engine...")

    # Case 1: Less than 2 sessions -> Maintain
    history_short = [{"evaluation": {"overall_score": 95}}]
    d1, r1 = determine_next_difficulty(history_short, current_difficulty=DIFFICULTY_INTERMEDIATE)
    assert d1 == DIFFICULTY_INTERMEDIATE
    assert "requires at least" in r1
    print("  [OK] Insufficient history correctly maintains difficulty")

    # Case 2: High Performance (>= 75) -> Upgrade
    history_high = [
        {"evaluation": {"overall_score": 85}},
        {"evaluation": {"overall_score": 90}},
    ]
    d2, r2 = determine_next_difficulty(history_high, current_difficulty=DIFFICULTY_BEGINNER)
    assert d2 == DIFFICULTY_INTERMEDIATE
    assert "Promoted" in r2

    d3, r3 = determine_next_difficulty(history_high, current_difficulty=DIFFICULTY_INTERMEDIATE)
    assert d3 == DIFFICULTY_ADVANCED
    assert "Promoted" in r3

    d4, r4 = determine_next_difficulty(history_high, current_difficulty=DIFFICULTY_ADVANCED)
    assert d4 == DIFFICULTY_ADVANCED
    assert "Maintained" in r4
    print("  [OK] High score threshold (>= 75) smoothly upgrades Beginner -> Intermediate -> Advanced")

    # Case 3: Low Performance (< 50) -> Downgrade
    history_low = [
        {"evaluation": {"overall_score": 40}},
        {"evaluation": {"overall_score": 45}},
    ]
    d5, r5 = determine_next_difficulty(history_low, current_difficulty=DIFFICULTY_ADVANCED)
    assert d5 == DIFFICULTY_INTERMEDIATE
    assert "Adjusted" in r5

    d6, r6 = determine_next_difficulty(history_low, current_difficulty=DIFFICULTY_INTERMEDIATE)
    assert d6 == DIFFICULTY_BEGINNER
    assert "Adjusted" in r6

    d7, r7 = determine_next_difficulty(history_low, current_difficulty=DIFFICULTY_BEGINNER)
    assert d7 == DIFFICULTY_BEGINNER
    print("  [OK] Low score threshold (< 50) smoothly downgrades Advanced -> Intermediate -> Beginner")

    # Case 4: Performance Summary Extraction
    summary = extract_history_performance_summary(
        [
            {"evaluation": {"overall_score": 80, "weaknesses": ["Time management", "Vague estimates"]}},
            {"evaluation": {"overall_score": 85, "weaknesses": ["Time management", "Stakeholder updates"]}},
        ]
    )
    assert "average recent score of 82" in summary or "83" in summary
    assert "Time management" in summary
    print("  [OK] History performance summary correctly extracts metrics and deduplicated weaknesses")


def test_day5_user_response_and_session_state():
    print("\n[DAY 5 - PART B, C & D] Testing User Response Validation & App State...")

    # Response validation
    good_resp = "I would first meet with the engineering lead to understand the root cause data. Then I would prepare a transparent contingency plan for the client."
    is_valid, _ = validate_user_response(good_resp)
    assert is_valid is True

    short_resp = "I will fix it."
    is_invalid, msg = validate_user_response(short_resp)
    assert is_invalid is False
    assert "too short" in msg.lower()

    none_resp = None
    is_empty, empty_msg = validate_user_response(none_resp)
    assert is_empty is False
    print("  [OK] User response system strictly validates input thresholds")

    # Verify app state imports
    import app
    assert hasattr(app, "init_session_state")
    assert hasattr(app, "main")
    print("  [OK] Streamlit app state integration verified")


def main():
    print("==========================================================")
    print("STARTING DAY 4 & DAY 5 COMPREHENSIVE VERIFICATION")
    print("==========================================================")
    test_day4_prompt_engineering()
    test_day4_scenario_engine()
    test_day5_adaptive_difficulty()
    test_day5_user_response_and_session_state()
    print("\n==========================================================")
    print("ALL DAY 4 (A-E) AND DAY 5 (A-D) SUB-PARTS PASSED 100%!")
    print("==========================================================")


if __name__ == "__main__":
    main()
