"""Sidebar UI component for LLM provider selection and user profile inputs."""

import streamlit as st
from typing import Tuple, Optional
from config import (
    PROVIDER_GEMINI,
    PROVIDER_GROQ,
    SUPPORTED_PROVIDERS,
    get_gemini_model_names,
    get_gemini_model_id,
    is_gemini_configured,
    get_groq_model_names,
    get_groq_model_id,
    is_groq_configured,
    DEFAULT_ROLES,
    DEFAULT_ROLE,
    EXPERIENCE_LEVELS,
    DEFAULT_EXPERIENCE,
    DIFFICULTY_LEVELS,
    DEFAULT_DIFFICULTY,
    ALL_CATEGORIES,
    SCENARIO_CATEGORIES_GROUPED,
)
from llm import test_provider_connection
from models import UserProfile


def render_sidebar() -> Tuple[str, str, UserProfile, bool]:
    """
    Render the sidebar interface.

    Returns:
        tuple: (selected_provider, selected_model_id, user_profile, generate_clicked)
    """
    with st.sidebar:
        st.markdown("## ⚙️ AI Configuration")

        # 1. AI Provider Selector
        st.markdown("### AI Provider")
        provider_index = (
            0
            if st.session_state.get("selected_provider", PROVIDER_GEMINI)
            == PROVIDER_GEMINI
            else 1
        )
        selected_provider = st.radio(
            "Select Provider",
            options=SUPPORTED_PROVIDERS,
            index=provider_index,
            label_visibility="collapsed",
        )
        st.session_state.selected_provider = selected_provider

        # 2. Dynamic Model Selector & Status
        if selected_provider == PROVIDER_GEMINI:
            gemini_models = get_gemini_model_names()
            curr_gemini_model = st.session_state.get(
                "selected_gemini_model_name", "Gemini 3.6 Flash"
            )
            g_idx = (
                gemini_models.index(curr_gemini_model)
                if curr_gemini_model in gemini_models
                else 0
            )

            selected_model_name = st.selectbox(
                "Gemini Model",
                options=gemini_models,
                index=g_idx,
            )
            st.session_state.selected_gemini_model_name = selected_model_name
            selected_model_id = get_gemini_model_id(selected_model_name)

            st.caption(f"Model ID: `{selected_model_id}`")
            if is_gemini_configured():
                st.success("API Key: Configured", icon="✅")
            else:
                st.warning("API Key missing in `.env` (`GEMINI_API_KEY`)", icon="⚠️")

        else:
            groq_models = get_groq_model_names()
            curr_groq_model = st.session_state.get(
                "selected_groq_model_name", "GPT OSS 120B"
            )
            gr_idx = (
                groq_models.index(curr_groq_model)
                if curr_groq_model in groq_models
                else 0
            )

            selected_model_name = st.selectbox(
                "Groq Model",
                options=groq_models,
                index=gr_idx,
            )
            st.session_state.selected_groq_model_name = selected_model_name
            selected_model_id = get_groq_model_id(selected_model_name)

            st.caption(f"Model ID: `{selected_model_id}`")
            if is_groq_configured():
                st.success("API Key: Configured", icon="✅")
            else:
                st.warning("API Key missing in `.env` (`GROQ_API_KEY`)", icon="⚠️")

        st.session_state.selected_model_id = selected_model_id

        # Connection Test Button
        if st.button("⚡ Test API Connection", use_container_width=True):
            with st.spinner(f"Testing {selected_provider} connection..."):
                ok, msg = test_provider_connection(selected_provider, selected_model_id)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

        st.divider()

        # 3. User Profile & Personalization Inputs
        st.markdown("## 👤 User Profile")

        # Role
        role_choice = st.selectbox(
            "Target Role",
            options=DEFAULT_ROLES,
            index=DEFAULT_ROLES.index(DEFAULT_ROLE)
            if DEFAULT_ROLE in DEFAULT_ROLES
            else 0,
        )
        if role_choice == "Other (Custom Role)":
            custom_role = st.text_input("Enter custom role:", value="Tech Lead")
            final_role = custom_role.strip() or "Professional"
        else:
            final_role = role_choice

        # Experience Level
        experience = st.selectbox(
            "Experience Level",
            options=EXPERIENCE_LEVELS,
            index=EXPERIENCE_LEVELS.index(DEFAULT_EXPERIENCE),
        )

        # Category
        # Display categorized list
        category = st.selectbox(
            "Scenario Category",
            options=ALL_CATEGORIES,
            index=0,
            help="Choose from Interview or Workplace Decision Making categories",
        )

        # Difficulty Level (with adaptive indicator if changed)
        current_diff = st.session_state.get("adaptive_difficulty", DEFAULT_DIFFICULTY)
        diff_idx = (
            DIFFICULTY_LEVELS.index(current_diff)
            if current_diff in DIFFICULTY_LEVELS
            else 1
        )
        difficulty = st.select_slider(
            "Difficulty",
            options=DIFFICULTY_LEVELS,
            value=current_diff,
        )

        # Skills / Focus Areas
        skills = st.text_input(
            "Skills / Keywords (Optional)",
            value="",
            placeholder="e.g., Python, System Design, Stakeholder Mgmt",
        )

        user_profile = UserProfile(
            role=final_role,
            experience=experience,
            category=category,
            difficulty=difficulty,
            skills=skills,
        )
        st.session_state.user_profile = user_profile

        st.divider()

        # 4. Action Buttons
        generate_clicked = st.button(
            "🚀 Generate Scenario",
            type="primary",
            use_container_width=True,
        )

        # Session reset button
        if st.button("🔄 Reset Session", use_container_width=True):
            st.session_state.history = []
            st.session_state.current_scenario = None
            st.session_state.current_evaluation = None
            st.session_state.app_state = "idle"
            st.rerun()

        # Session stats in sidebar
        history = st.session_state.get("history", [])
        st.markdown(f"**Completed Scenarios:** `{len(history)}`")

        return selected_provider, selected_model_id, user_profile, generate_clicked
