"""AI Scenario Simulator for Interview & Workplace Decision Making
Main Streamlit Application Entry Point.
"""

import streamlit as st
from config import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_ICON,
    APP_VERSION,
    PROVIDER_GEMINI,
    DEFAULT_DIFFICULTY,
)
from ui import (
    render_sidebar,
    render_scenario_view,
    render_response_view,
    render_evaluation_view,
    render_history_view,
    render_report_view,
)
from engines import (
    generate_scenario,
    generate_followup_scenario,
    evaluate_response,
    determine_next_difficulty,
    add_to_history,
    generate_performance_report,
)
from utils.validators import validate_user_response


def init_session_state():
    """Initialize all Streamlit session state keys with default values."""
    defaults = {
        "history": [],
        "user_profile": None,
        "current_scenario": None,
        "current_user_response": None,
        "current_evaluation": None,
        "final_report": None,
        "selected_provider": PROVIDER_GEMINI,
        "selected_gemini_model_name": "Gemini 3.6 Flash",
        "selected_groq_model_name": "GPT OSS 120B",
        "selected_model_id": "gemini-3.6-flash",
        "adaptive_difficulty": DEFAULT_DIFFICULTY,
        "app_state": "idle",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()

    # Render Sidebar and retrieve current inputs
    provider, model_id, user_profile, generate_clicked = render_sidebar()

    # Main Area Header
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.caption(f"{APP_SUBTITLE} • Version {APP_VERSION}")

    # Active Configuration Status Bar
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Active Provider", provider)
    with col2:
        st.metric("Model", model_id.split("/")[-1])
    with col3:
        st.metric("Target Role", user_profile.role)
    with col4:
        st.metric("Experience", user_profile.experience)
    with col5:
        st.metric("Difficulty", user_profile.difficulty)

    st.markdown("---")

    # Handle Scenario Generation Trigger from Sidebar
    if generate_clicked:
        with st.spinner(f"Generating realistic {user_profile.category} scenario with {provider}..."):
            scenario = generate_scenario(
                user_profile=user_profile,
                provider=provider,
                model_id=model_id,
                history=st.session_state.history,
            )
            st.session_state.current_scenario = scenario
            st.session_state.current_user_response = None
            st.session_state.current_evaluation = None
            st.session_state.app_state = "scenario_active"
            st.toast(f"New scenario ready: '{scenario.scenario_title}'", icon="🎯")

    # Main Interface Tabs
    tab_sim, tab_eval, tab_history, tab_report = st.tabs(
        [
            "🎯 Active Simulation",
            "📊 Response Evaluation",
            "📜 Session History",
            "📈 Performance Analytics",
        ]
    )

    # -------------------------------------------------------------
    # TAB 1: ACTIVE SIMULATION
    # -------------------------------------------------------------
    with tab_sim:
        # Check and notify on adaptive difficulty progression
        if len(st.session_state.history) >= 2:
            new_diff, diff_reason = determine_next_difficulty(
                st.session_state.history, current_difficulty=user_profile.difficulty
            )
            if new_diff != user_profile.difficulty:
                st.info(f"⚡ **Adaptive Difficulty Update:** {diff_reason}", icon="📈")

        # Render Scenario View component
        render_scenario_view(st.session_state.current_scenario)

        # Response and Evaluation Flow
        if st.session_state.current_scenario is not None:
            st.markdown("---")
            is_evaluated = st.session_state.current_evaluation is not None
            response_text, submitted = render_response_view(disabled=is_evaluated)

            if submitted and response_text and not is_evaluated:
                is_valid, val_msg = validate_user_response(response_text)
                if not is_valid:
                    st.warning(val_msg, icon="⚠️")
                else:
                    st.session_state.current_user_response = response_text
                    with st.spinner(f"🤖 AI Evaluator analyzing response across 7 dimensions using {provider}..."):
                        evaluation = evaluate_response(
                            scenario=st.session_state.current_scenario,
                            user_response=response_text,
                            user_profile=user_profile,
                            provider=provider,
                            model_id=model_id,
                        )
                        st.session_state.current_evaluation = evaluation

                        # Save into Session History
                        add_to_history(
                            history=st.session_state.history,
                            scenario=st.session_state.current_scenario,
                            user_response=response_text,
                            evaluation=evaluation,
                        )
                        st.session_state.app_state = "evaluated"
                        # Invalidate previous report cache since new session was completed
                        st.session_state.final_report = None

                    st.success(
                        f"🎉 **Evaluation Complete! Overall Score: {evaluation.overall_score}/100.** "
                        "Check the **'📊 Response Evaluation'** tab to review your detailed feedback!",
                        icon="✅",
                    )
                    st.rerun()

            if is_evaluated:
                st.success("✅ This scenario has been completed and evaluated. See the Evaluation tab for details.")

    # -------------------------------------------------------------
    # TAB 2: RESPONSE EVALUATION & ACTION CONTROLS
    # -------------------------------------------------------------
    with tab_eval:
        if st.session_state.current_evaluation is not None:
            render_evaluation_view(st.session_state.current_evaluation)

            st.markdown("---")
            st.markdown("### 🚀 Next Steps")
            col_act1, col_act2 = st.columns(2)

            with col_act1:
                if st.button("⚡ Generate Follow-Up Scenario (Target Weaknesses)", type="primary", use_container_width=True):
                    with st.spinner("Generating follow-up complication tailored to your weak areas..."):
                        followup = generate_followup_scenario(
                            previous_scenario=st.session_state.current_scenario,
                            evaluation=st.session_state.current_evaluation,
                            user_profile=user_profile,
                            provider=provider,
                            model_id=model_id,
                        )
                        st.session_state.current_scenario = followup
                        st.session_state.current_user_response = None
                        st.session_state.current_evaluation = None
                        st.session_state.app_state = "scenario_active"
                        st.toast("Follow-up scenario generated!", icon="⚡")
                        st.rerun()

            with col_act2:
                if st.button("🎯 Generate New Scenario (Adaptive Difficulty)", use_container_width=True):
                    with st.spinner("Generating next scenario with adaptive difficulty..."):
                        next_scen = generate_scenario(
                            user_profile=user_profile,
                            provider=provider,
                            model_id=model_id,
                            history=st.session_state.history,
                        )
                        st.session_state.current_scenario = next_scen
                        st.session_state.current_user_response = None
                        st.session_state.current_evaluation = None
                        st.session_state.app_state = "scenario_active"
                        st.toast("Next scenario loaded!", icon="🎯")
                        st.rerun()
        else:
            render_evaluation_view(None)

    # -------------------------------------------------------------
    # TAB 3: SESSION HISTORY
    # -------------------------------------------------------------
    with tab_history:
        render_history_view(st.session_state.history)

    # -------------------------------------------------------------
    # TAB 4: PERFORMANCE ANALYTICS & FINAL REPORT
    # -------------------------------------------------------------
    with tab_report:
        if len(st.session_state.history) < 2:
            st.info(
                f"📈 **Unlock Comprehensive Performance Analytics**\n\n"
                f"You have completed **{len(st.session_state.history)}/2** required scenarios. "
                "Complete at least 2 scenarios to generate your executive performance report and personalized growth roadmap."
            )
        else:
            if st.button("📑 Generate / Refresh Final Performance Report", type="primary"):
                with st.spinner(f"Synthesizing complete session history with {provider}..."):
                    report = generate_performance_report(
                        history=st.session_state.history,
                        user_profile=user_profile,
                        provider=provider,
                        model_id=model_id,
                    )
                    st.session_state.final_report = report
                    st.toast("Performance report generated!", icon="📈")

            # Render report if generated, or generate on first view
            if st.session_state.final_report is None:
                report = generate_performance_report(
                    history=st.session_state.history,
                    user_profile=user_profile,
                    provider=provider,
                    model_id=model_id,
                )
                st.session_state.final_report = report

            render_report_view(st.session_state.final_report, st.session_state.history)


if __name__ == "__main__":
    main()
