"""Report view component for rendering comprehensive performance analytics."""

import streamlit as st
from typing import Dict, Any, List


def render_report_view(report: Dict[str, Any], history: List[Dict[str, Any]]):
    """
    Render cumulative performance analytics, recurring patterns, and improvement roadmap.
    """
    if not history or len(history) < 2:
        st.info(
            "📈 Complete at least 2 scenarios to unlock the comprehensive AI Performance Report "
            "and personalized growth recommendations."
        )
        return

    st.markdown("## 📈 Comprehensive Performance Report")
    
    overall_avg = report.get("overall_average_score", 0)
    st.metric(
        label="Cumulative Average Score",
        value=f"{overall_avg:.1f}/100" if isinstance(overall_avg, (int, float)) else f"{overall_avg}/100",
        delta="Across all sessions"
    )

    st.markdown("---")

    # Average Dimension Scores
    avg_scores = report.get("average_scores", {})
    if avg_scores:
        st.markdown("### 📊 Skill Dimension Averages")
        cols = st.columns(len(avg_scores) if len(avg_scores) <= 6 else 3)
        for idx, (dim_name, val) in enumerate(avg_scores.items()):
            col = cols[idx % len(cols)]
            with col:
                st.metric(dim_name.replace("_", " ").title(), f"{val:.0f}/100" if isinstance(val, (int, float)) else f"{val}/100")
                if isinstance(val, (int, float)):
                    st.progress(min(max(val / 100, 0.0), 1.0))

    st.markdown("---")

    # Strengths vs Weaknesses Summary
    col_str, col_weak = st.columns(2)
    with col_str:
        st.success("### 🏆 Consistent Strengths")
        for s in report.get("strongest_areas", ["Consistent composure", "Structured approach"]):
            st.markdown(f"- {s}")

    with col_weak:
        st.warning("### 🎯 Priority Focus Areas")
        for w in report.get("weakest_areas", ["Quantifying impact", "Addressing edge cases"]):
            st.markdown(f"- {w}")

    # Recurring Mistakes
    recurring = report.get("recurring_mistakes", [])
    if recurring:
        st.markdown("### ⚠️ Recurring Blindspots Identified")
        for rm in recurring:
            st.markdown(f"- {rm}")

    # Actionable Recommendations
    recommendations = report.get("personalized_recommendations", [])
    if recommendations:
        st.markdown("### 🚀 Personalized Development Action Plan")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}.** {rec}")

    # Suggested Practice Areas
    practice = report.get("suggested_practice_areas", [])
    if practice:
        st.markdown("### 📚 Recommended Next Practice Topics")
        badges = " ".join([f"`{p}`" for p in practice])
        st.markdown(badges)
