import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""Comprehensive test suite for Day 3: Common LLM Interface & API Testing (Parts A-E)."""

import os
from unittest.mock import patch, MagicMock
from utils.error_handler import LLMError, LLMErrorCategory, handle_llm_error
from utils.json_parser import extract_json, safe_json_loads
from utils.validators import validate_user_response, validate_user_profile, sanitize_user_input
from llm.gemini_provider import call_gemini
from llm.groq_provider import call_groq
from llm.llm_client import call_llm, test_provider_connection
from config.settings import PROVIDER_GEMINI, PROVIDER_GROQ
from models.user_profile_model import UserProfile


def test_part_a_gemini_provider():
    print("\n[DAY 3 - PART A] Testing Gemini Provider...")

    # 1. Missing Key Check
    with patch("llm.gemini_provider.get_gemini_api_key", return_value=None):
        try:
            call_gemini("Hello", "gemini-2.5-flash")
            assert False, "Should have raised LLMError for missing key"
        except LLMError as e:
            assert e.category == LLMErrorCategory.MISSING_API_KEY
            assert "GEMINI_API_KEY" in e.message
            print("  [OK] Gemini raises MISSING_API_KEY when key is absent")

    # 2. Successful Call Mock
    with patch("llm.gemini_provider.get_gemini_api_key", return_value="fake_gemini_key"):
        with patch("google.generativeai.configure") as mock_conf:
            with patch("google.generativeai.GenerativeModel") as mock_model_cls:
                mock_model_instance = MagicMock()
                mock_model_instance.generate_content.return_value = MagicMock(text="Gemini Mock Response")
                mock_model_cls.return_value = mock_model_instance

                res = call_gemini("Test Prompt", "gemini-3.6-flash", system_instruction="Be concise")
                assert res == "Gemini Mock Response"
                mock_conf.assert_called_once_with(api_key="fake_gemini_key")
                mock_model_cls.assert_called_once_with(model_name="gemini-3.6-flash", system_instruction="Be concise")
                print("  [OK] Gemini provider executes and returns raw text correctly")


def test_part_b_groq_provider():
    print("\n[DAY 3 - PART B] Testing Groq Provider...")

    # 1. Missing Key Check
    with patch("llm.groq_provider.get_groq_api_key", return_value=None):
        try:
            call_groq("Hello", "llama-3.3-70b-versatile")
            assert False, "Should have raised LLMError for missing key"
        except LLMError as e:
            assert e.category == LLMErrorCategory.MISSING_API_KEY
            assert "GROQ_API_KEY" in e.message
            print("  [OK] Groq raises MISSING_API_KEY when key is absent")

    # 2. Successful Call Mock
    with patch("llm.groq_provider.get_groq_api_key", return_value="fake_groq_key"):
        with patch("groq.Groq") as mock_groq_cls:
            mock_client = MagicMock()
            mock_choice = MagicMock()
            mock_choice.message.content = "Groq Mock Response"
            mock_response = MagicMock(choices=[mock_choice])
            mock_client.chat.completions.create.return_value = mock_response
            mock_groq_cls.return_value = mock_client

            res = call_groq("Test Prompt", "llama-3.3-70b-versatile", system_instruction="Be helpful")
            assert res == "Groq Mock Response"
            mock_client.chat.completions.create.assert_called_once()
            print("  [OK] Groq provider executes and returns raw text correctly")


def test_part_c_common_llm_interface():
    print("\n[DAY 3 - PART C] Testing Common LLM Interface (call_llm)...")

    # 1. Routing to Gemini
    with patch("llm.llm_client.call_gemini", return_value="Gemini Routed Output") as mock_g:
        out = call_llm("Ping", provider=PROVIDER_GEMINI, model_id="gemini-2.5-flash")
        assert out == "Gemini Routed Output"
        mock_g.assert_called_once_with(prompt="Ping", model_id="gemini-2.5-flash", system_instruction=None)
        print("  [OK] call_llm routes 'Google Gemini' to call_gemini")

    # 2. Routing to Groq
    with patch("llm.llm_client.call_groq", return_value="Groq Routed Output") as mock_gr:
        out = call_llm("Ping", provider=PROVIDER_GROQ, model_id="llama-3.3-70b-versatile")
        assert out == "Groq Routed Output"
        mock_gr.assert_called_once_with(prompt="Ping", model_id="llama-3.3-70b-versatile", system_instruction=None)
        print("  [OK] call_llm routes 'Groq' to call_groq")

    # 3. Unsupported Provider
    try:
        call_llm("Ping", provider="UnsupportedProvider", model_id="xyz")
        assert False, "Should raise error for unsupported provider"
    except LLMError as e:
        assert "Unsupported AI Provider" in e.message
        print("  [OK] call_llm raises LLMError for unsupported provider")


def test_part_d_utilities():
    print("\n[DAY 3 - PART D] Testing Utilities (JSON Parser, Validators, Error Handler)...")

    # 1. JSON Parser - Direct JSON
    d1 = extract_json('{"score": 90, "feedback": "Great job"}')
    assert d1 == {"score": 90, "feedback": "Great job"}
    print("  [OK] JSON parser parses direct JSON string")

    # 2. JSON Parser - Markdown fenced block
    fenced = 'Here is your evaluation:\n```json\n{"strengths": ["Clear communication"], "score": 85}\n```\nHope this helps!'
    d2 = extract_json(fenced)
    assert d2 == {"strengths": ["Clear communication"], "score": 85}
    print("  [OK] JSON parser extracts from markdown code fences")

    # 3. JSON Parser - Embedded in text with trailing comma
    embedded = 'Result: {"decision": "Approve", "items": [1, 2, ], }'
    d3 = extract_json(embedded)
    assert d3 == {"decision": "Approve", "items": [1, 2]}
    print("  [OK] JSON parser cleans trailing commas and parses embedded dict")

    # 4. JSON Parser - Invalid text returns None or default
    assert extract_json("Not a JSON object at all") is None
    assert safe_json_loads("Not json", default={"default": True}) == {"default": True}
    print("  [OK] JSON parser handles invalid text with safe fallback")

    # 5. Validators - User Response
    valid_ok, _ = validate_user_response("This is a detailed response explaining my steps to resolve the outage.", min_length=30)
    assert valid_ok is True
    short_ok, short_msg = validate_user_response("Too short", min_length=30)
    assert short_ok is False
    assert "too short" in short_msg.lower()
    empty_ok, empty_msg = validate_user_response("   ")
    assert empty_ok is False
    assert "empty" in empty_msg.lower()
    print("  [OK] User response validator enforces non-empty and minimum length requirements")

    # 6. Validators - User Profile
    good_prof = UserProfile(role="Backend Engineer", experience="Junior", category="Technical interview", difficulty="Intermediate")
    p_ok, _ = validate_user_profile(good_prof)
    assert p_ok is True
    bad_prof = {"role": "", "experience": "Junior", "category": "Technical interview", "difficulty": "Intermediate"}
    bad_ok, _ = validate_user_profile(bad_prof)
    assert bad_ok is False
    print("  [OK] User profile validator validates role, category, and difficulty")

    # 7. Error Handler Messages
    err_missing = LLMError("No key", provider="Google Gemini", model_id="gemini-2.5-flash", category=LLMErrorCategory.MISSING_API_KEY)
    assert "GEMINI_API_KEY" in err_missing.user_friendly_message()
    err_rate = LLMError("Rate limit", provider="Groq", model_id="llama-3.3-70b-versatile", category=LLMErrorCategory.RATE_LIMIT)
    assert "Rate Limit Exceeded" in err_rate.user_friendly_message()
    print("  [OK] Error handler provides user-friendly actionable guidance")


def test_part_e_live_connection_and_fallback():
    print("\n[DAY 3 - PART E] Testing Live API Connection & Fallback...")

    # Test live connection with active models
    ok_gem, msg_gem = test_provider_connection(PROVIDER_GEMINI, "gemini-3.6-flash")
    print(f"  [OK] Gemini connection test result: success={ok_gem} ({msg_gem[:50]})")
    assert ok_gem is True or "API Key" in msg_gem

    ok_groq, msg_groq = test_provider_connection(PROVIDER_GROQ, "openai/gpt-oss-120b")
    print(f"  [OK] Groq connection test result: success={ok_groq} ({msg_groq[:50]})")
    assert ok_groq is True or "API Key" in msg_groq

    # Test with mocked active connection
    with patch("llm.llm_client.call_llm", return_value="READY"):
        ok_mock, msg_mock = test_provider_connection(PROVIDER_GEMINI, "gemini-3.6-flash")
        assert ok_mock is True
        assert "verified" in msg_mock.lower()
        print("  [OK] test_provider_connection verifies live responses successfully")


def main():
    print("==========================================================")
    print("STARTING DAY 3 COMPREHENSIVE VERIFICATION (PARTS A - E)")
    print("==========================================================")
    test_part_a_gemini_provider()
    test_part_b_groq_provider()
    test_part_c_common_llm_interface()
    test_part_d_utilities()
    test_part_e_live_connection_and_fallback()
    print("\n==========================================================")
    print("ALL DAY 3 SUB-PARTS (PARTS A TO E) PASSED 100%!")
    print("==========================================================")


if __name__ == "__main__":
    main()
