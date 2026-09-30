"""Scenario view component for displaying interview and workplace scenarios."""

import streamlit as st
from typing import Optional
from models.scenario_model import Scenario


def render_scenario_view(scenario: Optional[Scenario] = None):
    """
    Render the active scenario with clear visual hierarchy, badges, and challenge context.
    """
    if not scenario:
        st.info(
            "👈 Select your profile, provider, and scenario category in the sidebar, "
            "then click **'🚀 Generate Scenario'** to begin your simulation."
        )
        return

    st.subheader(f"📋 {scenario.scenario_title}")

    # Badges and metadata row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"**Type:** `{scenario.scenario_type}`")
    with col2:
        st.markdown(f"**Category:** `{scenario.category}`")
    with col3:
        st.markdown(f"**Difficulty:** `{scenario.difficulty}`")
    with col4:
        st.markdown(f"**Target Role:** `{scenario.target_role or 'General'}`")

    st.markdown("---")

    # Context & Scenario Description
    st.markdown("### 🏢 Background Context")
    st.info(scenario.context)

    st.markdown("### ⚡ The Situation")
    st.write(scenario.scenario_description)

    # Key Considerations
    if scenario.key_considerations:
        st.markdown("### 🎯 Key Considerations")
        for point in scenario.key_considerations:
            st.markdown(f"- {point}")

    # Expected Competencies/Skills
    if scenario.expected_skills:
        st.markdown("### 🧠 Competencies Evaluated")
        skills_pills = " ".join([f"`{skill}`" for skill in scenario.expected_skills])
        st.markdown(skills_pills)

    st.markdown("---")

    # Specific Challenge Callout
    st.warning(f"**Your Immediate Challenge:**\n\n{scenario.specific_challenge}", icon="❓")
