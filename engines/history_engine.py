"""History engine managing session memory, chronological timeline, and metric aggregations."""

import datetime
from typing import List, Dict, Any, Tuple, Optional
from models.scenario_model import Scenario
from models.evaluation_model import EvaluationResult
from config.settings import SCORING_DIMENSIONS, SCORING_DIMENSION_LABELS


def add_to_history(
    history: List[Dict[str, Any]],
    scenario: Scenario,
    user_response: str,
    evaluation: EvaluationResult,
) -> List[Dict[str, Any]]:
    """
    Append a completed scenario run to session history.

    Returns:
        The updated history list.
    """
    entry = {
        "scenario": scenario,
        "user_response": user_response,
        "evaluation": evaluation,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    history.append(entry)
    return history


def compute_average_scores(history: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Compute average scores across all 7 evaluation dimensions.

    Returns:
        dict mapping dimension_name -> float average score.
    """
    if not history:
        return {dim: 0.0 for dim in SCORING_DIMENSIONS}

    totals = {dim: 0.0 for dim in SCORING_DIMENSIONS}
    count = 0

    for item in history:
        ev = item.get("evaluation")
        if not ev:
            continue
        count += 1
        for dim in SCORING_DIMENSIONS:
            val = getattr(ev, dim, None) or (ev.get(dim) if isinstance(ev, dict) else 0)
            totals[dim] += float(val or 0)

    if count == 0:
        return {dim: 0.0 for dim in SCORING_DIMENSIONS}

    return {dim: round(totals[dim] / count, 1) for dim in SCORING_DIMENSIONS}


def get_dimension_extremes(
    history: List[Dict[str, Any]],
) -> Tuple[Optional[Tuple[str, float]], Optional[Tuple[str, float]]]:
    """
    Identify strongest and weakest skill dimensions (excluding overall_score).

    Returns:
        tuple: ((strongest_dim, score), (weakest_dim, score))
    """
    averages = compute_average_scores(history)
    sub_dims = {k: v for k, v in averages.items() if k != "overall_score"}

    if not sub_dims or all(v == 0.0 for v in sub_dims.values()):
        return None, None

    sorted_dims = sorted(sub_dims.items(), key=lambda x: x[1])
    weakest = sorted_dims[0]
    strongest = sorted_dims[-1]

    return strongest, weakest


def get_all_strengths(history: List[Dict[str, Any]]) -> List[str]:
    """Extract deduplicated list of strengths noted across sessions."""
    strengths = []
    for item in history:
        ev = item.get("evaluation")
        if ev:
            st_list = getattr(ev, "strengths", None) or (ev.get("strengths") if isinstance(ev, dict) else [])
            if st_list:
                strengths.extend(st_list)
    return list(dict.fromkeys(strengths))


def get_all_weaknesses(history: List[Dict[str, Any]]) -> List[str]:
    """Extract deduplicated list of weaknesses noted across sessions."""
    weaknesses = []
    for item in history:
        ev = item.get("evaluation")
        if ev:
            w_list = getattr(ev, "weaknesses", None) or (ev.get("weaknesses") if isinstance(ev, dict) else [])
            if w_list:
                weaknesses.extend(w_list)
    return list(dict.fromkeys(weaknesses))


def find_recurring_mistakes(history: List[Dict[str, Any]]) -> List[str]:
    """
    Identify recurring themes or patterns of shortcomings across history.
    """
    all_w = get_all_weaknesses(history)
    if not all_w:
        return ["Incomplete consideration of secondary stakeholder impacts."]

    # Heuristic: return the top 3 weaknesses or combined patterns
    if len(history) >= 2:
        return all_w[:3]
    return all_w[:2]
