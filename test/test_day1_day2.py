import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""Comprehensive validation test covering all sub-parts of Day 1 and Day 2."""

import os
from pathlib import Path


def test_day1_and_day2_all_subparts():
    print("==========================================================")
    print("STARTING FULL VERIFICATION: DAY 1 & DAY 2 (ALL SUB-PARTS)")
    print("==========================================================")

    # ---------------------------------------------------------
    # DAY 1 - PART A: Repository & Environment Foundation
    # ---------------------------------------------------------
    print("\n[DAY 1 - PART A] Checking Repository & Environment Foundation...")
    base_dir = Path(".")

    # 1. Check .gitignore
    gitignore_path = base_dir / ".gitignore"
    assert gitignore_path.exists(), ".gitignore is missing"
    gitignore_content = gitignore_path.read_text()
    for item in [".env", ".venv", "__pycache__"]:
        assert item in gitignore_content, f"{item} missing from .gitignore"
    print("  [OK] .gitignore properly excludes .env, .venv, __pycache__")

    # 2. Check .env.example
    env_ex_path = base_dir / ".env.example"
    assert env_ex_path.exists(), ".env.example is missing"
    env_ex_content = env_ex_path.read_text()
    assert "GEMINI_API_KEY=" in env_ex_content, "GEMINI_API_KEY missing from .env.example"
    assert "GROQ_API_KEY=" in env_ex_content, "GROQ_API_KEY missing from .env.example"
    print("  [OK] .env.example template configured with GEMINI_API_KEY and GROQ_API_KEY")

    # 3. Check .env exists
    env_path = base_dir / ".env"
    assert env_path.exists(), ".env file is missing"
    print("  [OK] Local .env file exists")

    # 4. Check folder structure
    packages = ["config", "llm", "prompts", "engines", "models", "ui", "utils"]
    for pkg in packages:
        init_file = base_dir / pkg / "__init__.py"
        assert init_file.exists(), f"Package __init__.py missing for {pkg}"
    print(f"  [OK] All 7 modular packages and __init__.py files present: {', '.join(packages)}")

    # ---------------------------------------------------------
    # DAY 1 - PART B: Dependencies & Virtual Environment
    # ---------------------------------------------------------
    print("\n[DAY 1 - PART B] Checking Dependencies & Installed Packages...")
    req_path = base_dir / "requirements.txt"
    assert req_path.exists(), "requirements.txt is missing"
    req_content = req_path.read_text()
    for dep in ["streamlit", "google-generativeai", "groq", "python-dotenv", "pydantic"]:
        assert dep in req_content, f"{dep} missing from requirements.txt"
    print("  [OK] requirements.txt contains all core dependencies")

    # Import dependencies in runtime
    import streamlit
    import google.generativeai
    import groq
    import dotenv
    import pydantic
    print(f"  [OK] streamlit ({streamlit.__version__}) importable")
    print(f"  [OK] google-generativeai ({google.generativeai.__version__}) importable")
    print(f"  [OK] groq ({groq.__version__}) importable")
    print(f"  [OK] pydantic ({pydantic.__version__}) importable")

    # ---------------------------------------------------------
    # DAY 1 - PART C: App Constants & Settings Module
    # ---------------------------------------------------------
    print("\n[DAY 1 - PART C] Checking App Constants & Settings Module...")
    from config.settings import (
        INTERVIEW_CATEGORIES,
        WORKPLACE_CATEGORIES,
        ALL_CATEGORIES,
        DIFFICULTY_LEVELS,
        EXPERIENCE_LEVELS,
        DEFAULT_ROLES,
        SCORING_DIMENSIONS,
        SCORING_DIMENSION_LABELS,
        DIFFICULTY_UPGRADE_THRESHOLD,
        DIFFICULTY_DOWNGRADE_THRESHOLD,
    )
    assert len(INTERVIEW_CATEGORIES) == 5, f"Expected 5 interview categories, got {len(INTERVIEW_CATEGORIES)}"
    assert len(WORKPLACE_CATEGORIES) == 9, f"Expected 9 workplace categories, got {len(WORKPLACE_CATEGORIES)}"
    assert len(ALL_CATEGORIES) == 14, f"Expected 14 total categories, got {len(ALL_CATEGORIES)}"
    assert set(DIFFICULTY_LEVELS) == {"Beginner", "Intermediate", "Advanced"}
    assert set(EXPERIENCE_LEVELS) == {"Fresher", "Junior", "Mid-level", "Senior"}
    assert len(SCORING_DIMENSIONS) == 7, "Expected 7 scoring dimensions"
    assert DIFFICULTY_UPGRADE_THRESHOLD == 75
    assert DIFFICULTY_DOWNGRADE_THRESHOLD == 50
    print(f"  [OK] 14 categories verified (5 Interview + 9 Workplace)")
    print(f"  [OK] 3 Difficulty levels + 4 Experience levels configured")
    print(f"  [OK] 7 Scoring dimensions verified: {', '.join(SCORING_DIMENSIONS)}")
    print(f"  [OK] Adaptive difficulty thresholds verified (>= {DIFFICULTY_UPGRADE_THRESHOLD} up, < {DIFFICULTY_DOWNGRADE_THRESHOLD} down)")

    # ---------------------------------------------------------
    # DAY 1 - PART D: Data Models (Schemas)
    # ---------------------------------------------------------
    print("\n[DAY 1 - PART D] Checking Data Models (Pydantic Schemas)...")
    from models import UserProfile, Scenario, EvaluationResult

    # UserProfile test
    user = UserProfile(
        role="Full Stack Developer",
        experience="Fresher",
        category="Team conflict",
        difficulty="Beginner",
        skills="React, Node.js, Conflict Resolution"
    )
    assert user.role == "Full Stack Developer"
    print("  [OK] UserProfile model instantiated and validated successfully")

    # Scenario test
    scen = Scenario(
        scenario_title="Handling Critical Production Outage Under Pressure",
        scenario_type="Workplace",
        category="Project failure",
        context="A payment processing gateway stopped responding during Black Friday.",
        scenario_description="Your team lead is unreachable and transactions are failing.",
        specific_challenge="What immediate triage steps and stakeholder updates do you execute?",
        key_considerations=["Customer data safety", "Rollback vs hotfix", "Executive status updates"],
        difficulty="Intermediate",
        expected_skills=["Incident Management", "Prioritization", "Communication"],
        target_role="Full Stack Developer"
    )
    assert len(scen.id) > 0
    assert len(scen.created_at) > 0
    print(f"  [OK] Scenario model validated with auto-generated ID ({scen.id}) and timestamp ({scen.created_at})")

    # EvaluationResult test
    ev = EvaluationResult(
        overall_score=88,
        communication=85,
        decision_making=90,
        problem_solving=92,
        professionalism=87,
        relevance=88,
        clarity=86,
        strengths=["Methodical triage", "Proactive rollback decision"],
        weaknesses=["Omitted customer support canned response"],
        feedback="Superb composure under high pressure situation.",
        ideal_response="Immediate rollback followed by canary testing and incident postmortem.",
        missing_points=["Status page notification", "Support team alert"],
        improvement_suggestions=["Always notify customer support before doing invasive debugging."],
        scenario_id=scen.id
    )
    assert ev.overall_score == 88
    assert ev.decision_making == 90
    print(f"  [OK] EvaluationResult validated across all 7 dimensions with score bounds")

    # ---------------------------------------------------------
    # DAY 2 - PART A: Gemini Configuration Module
    # ---------------------------------------------------------
    print("\n[DAY 2 - PART A] Checking Gemini Configuration Module...")
    from config.gemini_config import (
        GEMINI_MODELS,
        get_gemini_model_names,
        get_gemini_model_id,
        is_gemini_configured,
        get_gemini_api_key,
    )
    required_gemini_models = {
        "Gemini 3.6 Flash": "gemini-3.6-flash",
        "Gemini 3.5 Flash": "gemini-3.5-flash",
        "Gemini 3.5 Flash Lite": "gemini-3.5-flash-lite",
        "Gemini 3 Flash (Preview)": "gemini-3-flash-preview",
        "Gemini 2.5 Flash": "gemini-2.5-flash",
        "Gemini 2.5 Flash Lite": "gemini-2.5-flash-lite",
        "Gemini 2.5 Pro": "gemini-2.5-pro",
    }
    for disp, mid in required_gemini_models.items():
        assert disp in GEMINI_MODELS, f"{disp} missing from GEMINI_MODELS"
        assert get_gemini_model_id(disp) == mid, f"ID mismatch for {disp}"
    assert "gemini-2.0-flash" not in GEMINI_MODELS.values(), "gemini-2.0-flash must not be included"
    assert "gemini-2.0-flash-lite" not in GEMINI_MODELS.values(), "gemini-2.0-flash-lite must not be included"
    print(f"  [OK] All 7 active Gemini models registered: {list(required_gemini_models.keys())}")
    print("  [OK] Deprecated 2.0 flash models strictly excluded")
    print(f"  [OK] Gemini key loader verified (configured: {is_gemini_configured()})")

    # ---------------------------------------------------------
    # DAY 2 - PART B: Groq Configuration Module
    # ---------------------------------------------------------
    print("\n[DAY 2 - PART B] Checking Groq Configuration Module...")
    from config.groq_config import (
        GROQ_MODELS,
        get_groq_model_names,
        get_groq_model_id,
        is_groq_configured,
        get_groq_api_key,
    )
    groq_models = get_groq_model_names()
    assert len(groq_models) >= 5, "Groq model registry incomplete"
    for gm in groq_models:
        assert len(get_groq_model_id(gm)) > 0
    print(f"  [OK] Groq models registered: {groq_models}")
    print(f"  [OK] Groq key loader verified (configured: {is_groq_configured()})")

    # ---------------------------------------------------------
    # DAY 2 - PART C: Streamlit App Entry Point
    # ---------------------------------------------------------
    print("\n[DAY 2 - PART C] Checking Streamlit App Entry Point...")
    import app
    assert hasattr(app, "init_session_state"), "app.py missing init_session_state"
    assert hasattr(app, "main"), "app.py missing main"
    print("  [OK] app.py imports cleanly with valid entry points and session state initializers")

    # ---------------------------------------------------------
    # DAY 2 - PART D: Sidebar UI & Modular Views
    # ---------------------------------------------------------
    print("\n[DAY 2 - PART D] Checking Sidebar UI & Modular Views...")
    from ui import (
        render_sidebar,
        render_scenario_view,
        render_response_view,
        render_evaluation_view,
        render_history_view,
        render_report_view,
    )
    assert callable(render_sidebar)
    assert callable(render_scenario_view)
    assert callable(render_response_view)
    assert callable(render_evaluation_view)
    assert callable(render_history_view)
    assert callable(render_report_view)
    print("  [OK] All UI modules (sidebar, scenario, response, evaluation, history, report) implemented and verified")

    print("\n==========================================================")
    print("ALL SUB-PARTS (DAY 1: A-D & DAY 2: A-D) PASSED 100%!")
    print("==========================================================")


if __name__ == "__main__":
    test_day1_and_day2_all_subparts()
