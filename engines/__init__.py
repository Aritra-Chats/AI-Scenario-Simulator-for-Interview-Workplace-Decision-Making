"""Engines package for scenario, evaluation, difficulty, history, and reporting logic."""

from engines.scenario_engine import (
    generate_scenario,
    generate_followup_scenario,
)
from engines.difficulty_engine import (
    determine_next_difficulty,
    extract_history_performance_summary,
)
from engines.evaluation_engine import evaluate_response
from engines.history_engine import (
    add_to_history,
    compute_average_scores,
    get_dimension_extremes,
    get_all_strengths,
    get_all_weaknesses,
    find_recurring_mistakes,
)
from engines.report_engine import generate_performance_report

__all__ = [
    "generate_scenario",
    "generate_followup_scenario",
    "determine_next_difficulty",
    "extract_history_performance_summary",
    "evaluate_response",
    "add_to_history",
    "compute_average_scores",
    "get_dimension_extremes",
    "get_all_strengths",
    "get_all_weaknesses",
    "find_recurring_mistakes",
    "generate_performance_report",
]
