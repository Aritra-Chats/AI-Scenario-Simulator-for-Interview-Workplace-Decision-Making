"""Evaluation view component for structured score cards, feedback, and dimensions."""

import streamlit as st
from typing import Optional
from models.evaluation_model import EvaluationResult
from config.settings import SCORING_DIMENSION_LABELS


def render_evaluation_view(evaluation: Optional[EvaluationResult] = None):
    """
    Render detailed, multi-dimensional evaluation results and feedback.
    """
    if not evaluation:
        st.info(
            "📊 No evaluation available yet. Generate a scenario and submit your response to receive structured AI evaluation."
        )
        return

    # Overall Score Header
    st.markdown("## 📊 Evaluation Results")
    
    score = evaluation.overall_score
    if score >= 80:
        score_color = "🟢"
        score_label = "Excellent Performance"
    elif score >= 60:
        score_color = "🟡"
        score_label = "Good Effort - Room for Improvement"
    else:
        score_color = "🔴"
        score_label = "Needs Work"

    col_score, col_meta = st.columns([1, 2])
    with col_score:
        st.metric(label="Overall Score", value=f"{score}/100", delta=score_label)
    with col_meta:
        st.progress(score / 100)
        st.caption(f"{score_color} Evaluated at: `{evaluation.evaluated_at or 'Just now'}`")

    st.markdown("---")

    # 6 Core Dimensions
    st.markdown("### 📈 Dimensional Breakdown")
    dim_cols = st.columns(3)
    dimensions = [
        ("communication", evaluation.communication),
        ("decision_making", evaluation.decision_making),
        ("problem_solving", evaluation.problem_solving),
        ("professionalism", evaluation.professionalism),
        ("relevance", evaluation.relevance),
        ("clarity", evaluation.clarity),
    ]

    for idx, (dim_key, val) in enumerate(dimensions):
        col = dim_cols[idx % 3]
        with col:
            label = SCORING_DIMENSION_LABELS.get(dim_key, dim_key.replace("_", " ").title())
            st.metric(label, f"{val}/100")
            st.progress(val / 100)

    st.markdown("---")

    # Strengths and Weaknesses side by side
    col_str, col_weak = st.columns(2)
    with col_str:
        st.success("### ✅ Key Strengths")
        if evaluation.strengths:
            for s in evaluation.strengths:
                st.markdown(f"- {s}")
        else:
            st.write("No specific strengths noted.")

    with col_weak:
        st.warning("### ⚠️ Areas for Improvement")
        if evaluation.weaknesses:
            for w in evaluation.weaknesses:
                st.markdown(f"- {w}")
        else:
            st.write("No major weaknesses noted.")

    st.markdown("---")

    # Narrative Feedback
    st.markdown("### 📝 Detailed Evaluator Feedback")
    st.info(evaluation.feedback)

    # Missing Critical Points
    if evaluation.missing_points:
        st.markdown("### 🔍 Missing Nuances & Key Considerations")
        for mp in evaluation.missing_points:
            st.markdown(f"- {mp}")

    # Actionable Improvement Suggestions
    if evaluation.improvement_suggestions:
        st.markdown("### 💡 Actionable Recommendations")
        for i, tip in enumerate(evaluation.improvement_suggestions, 1):
            st.markdown(f"**{i}.** {tip}")

    # Ideal / Model Response Expander
    if evaluation.ideal_response:
        with st.expander("🌟 View Ideal / Exemplary Response", expanded=False):
            st.markdown(evaluation.ideal_response)
