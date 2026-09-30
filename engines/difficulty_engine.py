"""Adaptive difficulty engine adjusting scenario challenge level based on user history."""

from typing import List, Dict, Any, Tuple
from config.settings import (
    DIFFICULTY_BEGINNER,
    DIFFICULTY_INTERMEDIATE,
    DIFFICULTY_ADVANCED,
    DIFFICULTY_UPGRADE_THRESHOLD,
    DIFFICULTY_DOWNGRADE_THRESHOLD,
    MIN_SESSIONS_FOR_ADAPTATION,
)


def determine_next_difficulty(
    history: List[Dict[str, Any]],
    current_difficulty: str = DIFFICULTY_INTERMEDIATE,
) -> Tuple[str, str]:
    """
    Determine the next difficulty level using transparent rule-based adaptation.

    Rules:
    - Recent 2-session average >= 75 -> Increase difficulty level.
    - Recent 2-session average < 50  -> Decrease difficulty level.
    - Otherwise                      -> Maintain current difficulty level.

    Args:
        history: List of session records containing 'evaluation' and 'scenario'.
        current_difficulty: Current difficulty level string.

    Returns:
        tuple: (adapted_difficulty: str, reason: str)
    """
    if not history or len(history) < MIN_SESSIONS_FOR_ADAPTATION:
        return (
            current_difficulty,
            f"Difficulty maintained at '{current_difficulty}' (requires at least {MIN_SESSIONS_FOR_ADAPTATION} completed sessions to adapt).",
        )

    # Extract overall scores from last 2 sessions
    recent_sessions = history[-2:]
    recent_scores = []
    for item in recent_sessions:
        ev = item.get("evaluation")
        if ev:
            score = getattr(ev, "overall_score", None) or (
                ev.get("overall_score") if isinstance(ev, dict) else None
            )
            if score is not None:
                recent_scores.append(score)

    if not recent_scores:
        return current_difficulty, "No valid scores found in recent history."

    avg_score = sum(recent_scores) / len(recent_scores)

    # Check upgrade
    if avg_score >= DIFFICULTY_UPGRADE_THRESHOLD:
        if current_difficulty == DIFFICULTY_BEGINNER:
            return (
                DIFFICULTY_INTERMEDIATE,
                f"Promoted to '{DIFFICULTY_INTERMEDIATE}'! High recent average score ({avg_score:.0f}/100 >= {DIFFICULTY_UPGRADE_THRESHOLD}).",
            )
        elif current_difficulty == DIFFICULTY_INTERMEDIATE:
            return (
                DIFFICULTY_ADVANCED,
                f"Promoted to '{DIFFICULTY_ADVANCED}'! Exceptional recent average score ({avg_score:.0f}/100 >= {DIFFICULTY_UPGRADE_THRESHOLD}).",
            )
        else:
            return (
                DIFFICULTY_ADVANCED,
                f"Maintained at '{DIFFICULTY_ADVANCED}' (top difficulty tier mastered with {avg_score:.0f}/100).",
            )

    # Check downgrade
    elif avg_score < DIFFICULTY_DOWNGRADE_THRESHOLD:
        if current_difficulty == DIFFICULTY_ADVANCED:
            return (
                DIFFICULTY_INTERMEDIATE,
                f"Adjusted to '{DIFFICULTY_INTERMEDIATE}' to rebuild core fundamentals (recent average {avg_score:.0f}/100 < {DIFFICULTY_DOWNGRADE_THRESHOLD}).",
            )
        elif current_difficulty == DIFFICULTY_INTERMEDIATE:
            return (
                DIFFICULTY_BEGINNER,
                f"Adjusted to '{DIFFICULTY_BEGINNER}' to strengthen foundational techniques (recent average {avg_score:.0f}/100 < {DIFFICULTY_DOWNGRADE_THRESHOLD}).",
            )
        else:
            return (
                DIFFICULTY_BEGINNER,
                f"Maintained at '{DIFFICULTY_BEGINNER}' to focus on foundational practice (recent average {avg_score:.0f}/100).",
            )

    # Steady state
    return (
        current_difficulty,
        f"Maintained at '{current_difficulty}' (steady recent average of {avg_score:.0f}/100).",
    )


def extract_history_performance_summary(history: List[Dict[str, Any]]) -> str:
    """
    Summarize past evaluations into a prompt-injectable performance snippet.

    Args:
        history: Session history list.

    Returns:
        Summary text describing recent performance and recurring weaknesses.
    """
    if not history:
        return ""

    scores = []
    all_weaknesses = []

    for item in history[-3:]:
        ev = item.get("evaluation")
        if ev:
            score = getattr(ev, "overall_score", None) or (
                ev.get("overall_score") if isinstance(ev, dict) else None
            )
            if score is not None:
                scores.append(score)

            w = getattr(ev, "weaknesses", None) or (
                ev.get("weaknesses") if isinstance(ev, dict) else []
            )
            if w:
                all_weaknesses.extend(w[:2])

    if not scores:
        return ""

    avg_score = sum(scores) / len(scores)
    summary = f"Candidate completed {len(history)} scenario(s) with an average recent score of {avg_score:.0f}/100."
    if all_weaknesses:
        unique_w = list(dict.fromkeys(all_weaknesses))[:3]
        summary += f" Recent areas needing improvement: {'; '.join(unique_w)}."

    return summary
