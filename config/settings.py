"""Application constants, configuration settings, and taxonomy definitions."""

from typing import Dict, List

# Application Metadata
APP_TITLE = "AI Scenario Simulator for Interview & Workplace Decision Making"
APP_SUBTITLE = "Realistic AI-driven interview and workplace decision simulations with structured feedback"
APP_ICON = "🎯"
APP_VERSION = "1.0.0"

# Scenario Categories
INTERVIEW_CATEGORIES: List[str] = [
    "Technical interview",
    "HR interview",
    "Behavioral interview",
    "Leadership interview",
    "Situational interview",
]

WORKPLACE_CATEGORIES: List[str] = [
    "Team conflict",
    "Missed deadline",
    "Difficult teammate",
    "Client communication",
    "Leadership decision",
    "Ethical dilemma",
    "Time management",
    "Project failure",
    "Workplace communication",
]

SCENARIO_CATEGORIES_GROUPED: Dict[str, List[str]] = {
    "Interview Scenarios": INTERVIEW_CATEGORIES,
    "Workplace Scenarios": WORKPLACE_CATEGORIES,
}

ALL_CATEGORIES: List[str] = INTERVIEW_CATEGORIES + WORKPLACE_CATEGORIES

# Difficulty Levels
DIFFICULTY_BEGINNER = "Beginner"
DIFFICULTY_INTERMEDIATE = "Intermediate"
DIFFICULTY_ADVANCED = "Advanced"

DIFFICULTY_LEVELS: List[str] = [
    DIFFICULTY_BEGINNER,
    DIFFICULTY_INTERMEDIATE,
    DIFFICULTY_ADVANCED,
]
DEFAULT_DIFFICULTY = DIFFICULTY_INTERMEDIATE

# Experience Levels
EXPERIENCE_FRESHER = "Fresher"
EXPERIENCE_JUNIOR = "Junior"
EXPERIENCE_MID = "Mid-level"
EXPERIENCE_SENIOR = "Senior"

EXPERIENCE_LEVELS: List[str] = [
    EXPERIENCE_FRESHER,
    EXPERIENCE_JUNIOR,
    EXPERIENCE_MID,
    EXPERIENCE_SENIOR,
]
DEFAULT_EXPERIENCE = EXPERIENCE_FRESHER

# Roles Taxonomy
DEFAULT_ROLES: List[str] = [
    "Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Data Scientist / AI Engineer",
    "Product Manager",
    "Project Manager",
    "Business Analyst",
    "DevOps / Cloud Engineer",
    "Quality Assurance Engineer",
    "HR Specialist / People Ops",
    "Marketing Specialist",
    "Financial Analyst",
    "Customer Success Manager",
    "Other (Custom Role)",
]
DEFAULT_ROLE = "Software Engineer"

# Scoring Dimensions
SCORING_DIMENSIONS: List[str] = [
    "overall_score",
    "communication",
    "decision_making",
    "problem_solving",
    "professionalism",
    "relevance",
    "clarity",
]

SCORING_DIMENSION_LABELS: Dict[str, str] = {
    "overall_score": "Overall Performance",
    "communication": "Communication Skills",
    "decision_making": "Decision Making",
    "problem_solving": "Problem Solving",
    "professionalism": "Professionalism & Demeanor",
    "relevance": "Relevance & Directness",
    "clarity": "Clarity & Articulation",
}

SCORING_DIMENSION_DESCRIPTIONS: Dict[str, str] = {
    "overall_score": "Comprehensive rating reflecting effectiveness across all dimensions.",
    "communication": "Ability to convey ideas persuasively, clearly, and constructively.",
    "decision_making": "Sound judgment, risk assessment, and balance of trade-offs.",
    "problem_solving": "Analytical thinking, practical solutions, and root cause focus.",
    "professionalism": "Composure, emotional intelligence, diplomacy, and ethical alignment.",
    "relevance": "Directly addressing core scenario constraints and questions.",
    "clarity": "Conciseness, structured thinking, and absence of ambiguity.",
}

# Adaptive Difficulty Thresholds
DIFFICULTY_UPGRADE_THRESHOLD: int = 75    # Average score >= 75 upgrades difficulty
DIFFICULTY_DOWNGRADE_THRESHOLD: int = 50  # Average score < 50 downgrades difficulty
MIN_SESSIONS_FOR_ADAPTATION: int = 2      # Need at least 2 sessions to adapt difficulty

# LLM Providers
PROVIDER_GEMINI = "Google Gemini"
PROVIDER_GROQ = "Groq"
SUPPORTED_PROVIDERS: List[str] = [PROVIDER_GEMINI, PROVIDER_GROQ]
