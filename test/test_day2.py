import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""Verification test for Day 2 configuration and UI modules."""

from config.gemini_config import (
    GEMINI_MODELS,
    get_gemini_model_names,
    get_gemini_model_id,
    is_gemini_configured,
)
from config.groq_config import (
    GROQ_MODELS,
    get_groq_model_names,
    get_groq_model_id,
    is_groq_configured,
)
from ui.sidebar import render_sidebar


def test_day2():
    print("Testing Day 2 components...")

    # Verify requested Gemini models
    required_gemini_models = {
        "Gemini 3.6 Flash": "gemini-3.6-flash",
        "Gemini 3.5 Flash": "gemini-3.5-flash",
        "Gemini 3.5 Flash Lite": "gemini-3.5-flash-lite",
        "Gemini 3 Flash (Preview)": "gemini-3-flash-preview",
        "Gemini 2.5 Flash": "gemini-2.5-flash",
        "Gemini 2.5 Flash Lite": "gemini-2.5-flash-lite",
        "Gemini 2.5 Pro": "gemini-2.5-pro",
    }

    for name, model_id in required_gemini_models.items():
        assert name in GEMINI_MODELS, f"Missing {name} in GEMINI_MODELS"
        assert (
            get_gemini_model_id(name) == model_id
        ), f"ID mismatch for {name}: expected {model_id}, got {get_gemini_model_id(name)}"
        print(f"  [OK] Gemini Model: {name} -> {model_id}")

    # Ensure deprecated 2.0 models are excluded
    assert "gemini-2.0-flash" not in GEMINI_MODELS.values()
    assert "gemini-2.0-flash-lite" not in GEMINI_MODELS.values()
    print("  [OK] Deprecated 2.0 models excluded as required.")

    # Verify Groq models
    groq_models = get_groq_model_names()
    assert len(groq_models) >= 4, "Groq models list too short"
    for gm in groq_models:
        mid = get_groq_model_id(gm)
        print(f"  [OK] Groq Model: {gm} -> {mid}")

    # Verify sidebar function is callable
    assert callable(render_sidebar)
    print("  [OK] render_sidebar component verified.")

    print("ALL DAY 2 VERIFICATIONS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_day2()
