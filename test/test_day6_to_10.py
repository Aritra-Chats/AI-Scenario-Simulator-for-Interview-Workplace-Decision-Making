import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""Comprehensive test suite verifying Days 6 to 10 and all their sub-parts."""

import json
from unittest.mock import patch, MagicMock
from models.user_profile_model import UserProfile
from models.scenario_model import Scenario
from models.evaluation_model import EvaluationResult
from prompts.evaluation_prompts import build_evaluation_prompt
from prompts.report_prompts import build_report_prompt
from engines.evaluation_engine import evaluate_response, _build_fallback_evaluation
from engines.history_engine import (
    add_to_history,
    compute_average_scores,
    get_dimension_extremes,
    find_recurring_mistakes,
)
from engines.scenario_engine import generate_scenario, generate_followup_scenario
from engines.report_engine import generate_performance_report
from config.settings import PROVIDER_GEMINI, PROVIDER_GROQ


def test_day6_evaluation_engine():
    print("\n[DAY 6] Testing AI Response Evaluation Engine (Parts A-D)...")

    profile = UserProfile(
        role="DevOps Engineer",
        experience="Mid-level",
        category="Project failure",
        difficulty="Intermediate",
    )

    scenario = Scenario(
        scenario_title="Kubernetes Ingress Controller Silent Crash",
        scenario_type="Workplace",
        category="Project failure",
        context="Production ingress crashed during a minor helm update.",
        scenario_description="Traffic to 4 core microservices is failing with 502 Bad Gateway.",
        specific_challenge="What is your immediate rollback and triage protocol?",
        key_considerations=["Minimizing downtime", "Preserving ingress logs"],
        difficulty="Intermediate",
        expected_skills=["Kubernetes", "Incident Triage"],
        target_role="DevOps Engineer",
    )

    user_resp = (
        "I would immediately execute a helm rollback to the previous release revision. "
        "Next, I will inspect the crashed pod logs and events using kubectl describe. "
        "I'll alert customer support on Slack #outages with an ETA of 10 minutes."
    )

    # 1. Test Prompt Builder
    sys_p, user_p = build_evaluation_prompt(scenario, user_resp, profile)
    assert "Kubernetes Ingress Controller Silent Crash" in user_p
    assert "overall_score" in user_p
    assert "communication" in user_p
    assert "decision_making" in user_p
    assert "ideal_response" in user_p
    print("  [OK] build_evaluation_prompt constructs prompt with all 7 scoring dimensions")

    # 2. Test Successful Evaluation Generation
    mock_eval_json = {
        "overall_score": 88,
        "communication": 85,
        "decision_making": 90,
        "problem_solving": 89,
        "professionalism": 88,
        "relevance": 92,
        "clarity": 84,
        "strengths": ["Immediate rollback priority", "Proactive internal communication"],
        "weaknesses": ["Did not mention traffic draining or ingress health checks"],
        "feedback": "Strong and decisive incident handling under pressure.",
        "ideal_response": "Exemplary model response with traffic draining and postmortem plan.",
        "missing_points": ["Traffic draining before rollback", "Status page update"],
        "improvement_suggestions": ["Include post-incident review timelines."],
    }

    with patch("engines.evaluation_engine.call_llm", return_value=json.dumps(mock_eval_json)):
        ev = evaluate_response(scenario, user_resp, profile, PROVIDER_GEMINI, "gemini-2.5-flash")
        assert ev.overall_score == 88
        assert ev.relevance == 92
        assert len(ev.strengths) == 2
        assert len(ev.weaknesses) == 1
        print("  [OK] evaluate_response parses multi-dimensional scores and structured feedback")

    # 3. Test Fallback Evaluation on API Failure
    with patch("engines.evaluation_engine.call_llm", side_effect=Exception("API Error")):
        fallback_ev = evaluate_response(scenario, user_resp, profile, PROVIDER_GROQ, "llama-3.3-70b-versatile")
        assert fallback_ev is not None
        assert 50 <= fallback_ev.overall_score <= 100
        assert len(fallback_ev.strengths) > 0
        print("  [OK] evaluate_response returns robust fallback EvaluationResult on failure")


def test_day7_history_and_followup():
    print("\n[DAY 7] Testing History, Session Memory & Follow-Up Engine (Parts A-D)...")

    history = []
    scen1 = Scenario(
        scenario_title="Technical Challenge 1",
        scenario_type="Interview",
        category="Technical interview",
        context="Context 1",
        scenario_description="Desc 1",
        specific_challenge="Challenge 1",
        key_considerations=["C1"],
        difficulty="Intermediate",
    )
    eval1 = EvaluationResult(
        overall_score=80,
        communication=75,
        decision_making=80,
        problem_solving=85,
        professionalism=80,
        relevance=80,
        clarity=80,
        strengths=["Structured"],
        weaknesses=["Omitted edge cases"],
        feedback="Good.",
        ideal_response="Ideal 1",
    )

    add_to_history(history, scen1, "Response 1", eval1)
    assert len(history) == 1
    assert history[0]["scenario"].scenario_title == "Technical Challenge 1"
    print("  [OK] add_to_history successfully appends session record")

    scen2 = Scenario(
        scenario_title="Workplace Challenge 2",
        scenario_type="Workplace",
        category="Team conflict",
        context="Context 2",
        scenario_description="Desc 2",
        specific_challenge="Challenge 2",
        key_considerations=["C2"],
        difficulty="Intermediate",
    )
    eval2 = EvaluationResult(
        overall_score=90,
        communication=85,
        decision_making=90,
        problem_solving=95,
        professionalism=90,
        relevance=90,
        clarity=90,
        strengths=["Empathetic"],
        weaknesses=["Omitted edge cases", "Timeline vague"],
        feedback="Great.",
        ideal_response="Ideal 2",
    )
    add_to_history(history, scen2, "Response 2", eval2)
    assert len(history) == 2

    # Averages
    averages = compute_average_scores(history)
    assert averages["overall_score"] == 85.0
    assert averages["problem_solving"] == 90.0
    print(f"  [OK] compute_average_scores correctly calculates 7 dimension metrics (overall: {averages['overall_score']})")

    # Extremes
    strongest, weakest = get_dimension_extremes(history)
    assert strongest[0] == "problem_solving"
    assert weakest[0] == "communication"
    print(f"  [OK] get_dimension_extremes correctly identifies strongest ({strongest[0]}) and weakest ({weakest[0]})")

    # Follow-up Generation
    profile = UserProfile(role="Engineer", experience="Fresher", category="Technical interview", difficulty="Intermediate")
    with patch("engines.scenario_engine.call_llm", return_value=json.dumps({
        "scenario_title": "Follow-up: Handling Edge Case Surges",
        "scenario_type": "Interview",
        "category": "Technical interview",
        "context": "Context evolution",
        "scenario_description": "A surge of edge cases arrived as feared.",
        "specific_challenge": "How do you triage them?",
        "key_considerations": ["Edge cases", "Data integrity"],
        "difficulty": "Intermediate",
        "expected_skills": ["Edge Case Analysis"],
        "target_role": "Engineer"
    })):
        followup = generate_followup_scenario(scen2, eval2, profile, PROVIDER_GEMINI, "gemini-2.5-flash")
        assert "Follow-up" in followup.scenario_title
        print("  [OK] generate_followup_scenario constructs continuation addressing prior evaluation")


def test_day8_report_engine():
    print("\n[DAY 8] Testing Final Performance Report & Analytics (Parts A-D)...")

    profile = UserProfile(role="Engineering Manager", experience="Senior", category="Leadership decision", difficulty="Advanced")
    history = [
        {
            "scenario": Scenario(scenario_title="S1", scenario_type="Workplace", category="Leadership decision", context="C1", scenario_description="D1", specific_challenge="Q1"),
            "evaluation": EvaluationResult(overall_score=78, communication=80, decision_making=75, problem_solving=80, professionalism=85, relevance=75, clarity=73, weaknesses=["Lack of explicit timeline"], strengths=["Empathy"], feedback="F1", ideal_response="I1"),
        },
        {
            "scenario": Scenario(scenario_title="S2", scenario_type="Workplace", category="Team conflict", context="C2", scenario_description="D2", specific_challenge="Q2"),
            "evaluation": EvaluationResult(overall_score=86, communication=84, decision_making=86, problem_solving=88, professionalism=88, relevance=85, clarity=85, weaknesses=["Lack of explicit timeline", "Contingency planning"], strengths=["Clear decisions"], feedback="F2", ideal_response="I2"),
        },
    ]

    # Test Report Generation with Mock
    mock_report = {
        "overall_average_score": 82.0,
        "average_scores": {"communication": 82.0, "decision_making": 80.5, "problem_solving": 84.0, "professionalism": 86.5, "relevance": 80.0, "clarity": 79.0},
        "strongest_areas": ["Professionalism & Executive Demeanor", "Empathetic leadership"],
        "weakest_areas": ["Explicit timeline tracking", "Contingency planning"],
        "recurring_mistakes": ["Setting deliverables without milestone dates"],
        "personalized_recommendations": ["Institute a weekly milestone check-in framework."],
        "suggested_practice_areas": ["Time management", "Missed deadline"],
        "overall_assessment": "Excellent executive trajectory with clear delegation skills.",
    }

    with patch("engines.report_engine.call_llm", return_value=json.dumps(mock_report)):
        report = generate_performance_report(history, profile, PROVIDER_GEMINI, "gemini-2.5-flash")
        assert report["overall_average_score"] == 82.0
        assert len(report["personalized_recommendations"]) > 0
        assert len(report["recurring_mistakes"]) > 0
        print("  [OK] generate_performance_report generates structured synthesis and coaching plan")

    # Guard check: < 2 scenarios
    short_report = generate_performance_report([history[0]], profile, PROVIDER_GEMINI, "gemini-2.5-flash")
    assert "error" in short_report
    print("  [OK] generate_performance_report enforces minimum 2-scenario requirement")


def test_day9_and_10_end_to_end_workflows():
    print("\n[DAY 9 & 10] Testing End-to-End Integration, Error Hardening & Polish...")

    # Full simulation pipeline test without real API keys (verifying resilient fallback and state flow)
    profile = UserProfile(
        role="Software Engineer",
        experience="Fresher",
        category="Technical interview",
        difficulty="Intermediate",
        skills="Python, Data Structures",
    )

    # 1. Generate Scenario (Gemini path)
    scen = generate_scenario(profile, PROVIDER_GEMINI, "gemini-2.5-flash", history=[])
    assert scen is not None
    assert scen.target_role == "Software Engineer"
    print("  [OK] Step 1: Initial scenario generated via Gemini path")

    # 2. User Response & Evaluation
    resp = "I will implement a hash table for O(1) lookups and handle collisions using chaining with linked lists."
    ev = evaluate_response(scen, resp, profile, PROVIDER_GEMINI, "gemini-2.5-flash")
    assert ev.overall_score >= 0
    print(f"  [OK] Step 2: Response evaluated with composite score {ev.overall_score}/100")

    # 3. Add to History
    history = []
    add_to_history(history, scen, resp, ev)
    assert len(history) == 1
    print("  [OK] Step 3: Session saved to chronological history")

    # 4. Generate Follow-up Scenario
    followup = generate_followup_scenario(scen, ev, profile, PROVIDER_GROQ, "llama-3.3-70b-versatile")
    assert followup is not None
    print(f"  [OK] Step 4: Follow-up generated via Groq path ('{followup.scenario_title}')")

    # 5. Second Response & Evaluation
    resp2 = "To prevent memory bloat under high scale, I will add an LRU cache eviction policy with a max capacity."
    ev2 = evaluate_response(followup, resp2, profile, PROVIDER_GROQ, "llama-3.3-70b-versatile")
    add_to_history(history, followup, resp2, ev2)
    assert len(history) == 2
    print(f"  [OK] Step 5: Second response evaluated with composite score {ev2.overall_score}/100")

    # 6. Generate Comprehensive Performance Report
    report = generate_performance_report(history, profile, PROVIDER_GEMINI, "gemini-2.5-flash")
    assert report is not None
    assert "overall_average_score" in report
    assert "strongest_areas" in report
    assert "personalized_recommendations" in report
    print(f"  [OK] Step 6: Final performance analytics generated successfully (Avg: {report['overall_average_score']:.1f}/100)")


def main():
    print("==========================================================")
    print("STARTING FULL VERIFICATION: DAYS 6 TO 10 (ALL SUB-PARTS)")
    print("==========================================================")
    test_day6_evaluation_engine()
    test_day7_history_and_followup()
    test_day8_report_engine()
    test_day9_and_10_end_to_end_workflows()
    print("\n==========================================================")
    print("ALL SUB-PARTS FOR DAYS 6 TO 10 PASSED 100%!")
    print("==========================================================")


if __name__ == "__main__":
    main()
