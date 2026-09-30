"""Response input component for capturing and validating user responses."""

import streamlit as st
from typing import Tuple, Optional


def render_response_view(disabled: bool = False) -> Tuple[Optional[str], bool]:
    """
    Render the user response text area and submit button.

    Returns:
        tuple: (response_text, submitted)
    """
    st.markdown("### ✍️ Your Response")
    st.caption("Formulate your structured, professional response addressing the situation and trade-offs.")

    response_text = st.text_area(
        "Response input",
        height=220,
        placeholder="Type your response here... (Aim for structured thinking, professional tone, and concrete action steps)",
        disabled=disabled,
        label_visibility="collapsed",
        key="user_response_input",
    )

    char_count = len(response_text.strip())
    col1, col2 = st.columns([4, 1])

    with col1:
        if char_count == 0:
            st.caption("Character count: 0 | Recommended minimum: 60 characters")
        elif char_count < 60:
            st.caption(f"⚠️ Character count: {char_count} (A bit brief — consider adding reasoning and next steps)")
        else:
            st.caption(f"✅ Character count: {char_count} (Good detail)")

    with col2:
        submit_clicked = st.button(
            "📤 Submit Response",
            type="primary",
            use_container_width=True,
            disabled=disabled or char_count < 10,
        )

    return (response_text.strip() if response_text else None), submit_clicked
