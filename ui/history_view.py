"""History view component for browsing previous scenarios and scores."""

import streamlit as st
from typing import List, Dict, Any


def render_history_view(history: List[Dict[str, Any]]):
    """
    Render past simulation runs in a clean, chronological timeline.
    """
    if not history:
        st.info("📜 No scenarios completed in this session yet. Completed sessions will be recorded here.")
        return

    st.markdown(f"### 📜 Session History ({len(history)} Completed)")

    for i, item in enumerate(reversed(history), 1):
        scenario = item.get("scenario")
        evaluation = item.get("evaluation")
        user_response = item.get("user_response", "")

        title = scenario.scenario_title if scenario else f"Scenario #{len(history) - i + 1}"
        overall_score = evaluation.overall_score if evaluation else "N/A"
        category = scenario.category if scenario else "General"
        difficulty = scenario.difficulty if scenario else "Intermediate"

        with st.expander(f"#{len(history) - i + 1} — {title} | Score: {overall_score}/100 [{difficulty}]"):
            st.markdown(f"**Category:** `{category}` | **Difficulty:** `{difficulty}`")
            if scenario:
                st.caption(f"**Challenge:** {scenario.specific_challenge}")
            
            st.markdown("**Your Response:**")
            st.text(user_response or "No response recorded.")

            if evaluation:
                st.markdown(f"**Overall Score:** `{evaluation.overall_score}/100`")
                st.markdown(f"**Feedback:** {evaluation.feedback}")
                if evaluation.strengths:
                    st.markdown(f"**Strengths:** {', '.join(evaluation.strengths[:2])}")
                if evaluation.weaknesses:
                    st.markdown(f"**Weaknesses:** {', '.join(evaluation.weaknesses[:2])}")
