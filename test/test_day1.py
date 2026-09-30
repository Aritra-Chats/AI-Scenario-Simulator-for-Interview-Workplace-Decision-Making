import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""Quick validation script to verify Day 1 configuration and data models."""

from config.settings import (
    APP_TITLE,
    ALL_CATEGORIES,
    DIFFICULTY_LEVELS,
    EXPERIENCE_LEVELS,
    SCORING_DIMENSIONS,
    SUPPORTED_PROVIDERS,
)
from models import UserProfile, Scenario, EvaluationResult


def main():
    print(f"Checking {APP_TITLE} configuration...")
    print(f"Categories count: {len(ALL_CATEGORIES)}")
    print(f"Difficulty levels: {DIFFICULTY_LEVELS}")
    print(f"Experience levels: {EXPERIENCE_LEVELS}")
    print(f"Scoring dimensions count: {len(SCORING_DIMENSIONS)}")
    print(f"Supported providers: {SUPPORTED_PROVIDERS}")

    # Test UserProfile schema
    profile = UserProfile(
        role="Software Engineer",
        experience="Fresher",
        category="Technical interview",
        difficulty="Intermediate",
        skills="Python, Algorithms",
    )
    print("UserProfile instantiation: OK", profile.role)

    # Test Scenario schema
    scenario = Scenario(
        scenario_title="Design a URL Shortener Under High Load",
        scenario_type="Interview",
        category="Technical interview",
        context="You are in a system design round at a high-growth tech startup.",
        scenario_description="The interviewer asks you to architect a URL shortening service.",
        specific_challenge="Explain how you would handle 100,000 requests per second with low latency.",
        key_considerations=["Data partitioning", "Caching strategy", "Fault tolerance"],
        difficulty="Advanced",
        expected_skills=["System Design", "Scalability", "Database Optimization"],
        target_role="Software Engineer",
    )
    print("Scenario instantiation: OK", scenario.scenario_title)

    # Test EvaluationResult schema
    eval_result = EvaluationResult(
        overall_score=85,
        communication=80,
        decision_making=85,
        problem_solving=90,
        professionalism=90,
        relevance=85,
        clarity=80,
        strengths=["Clear articulation of caching layers", "Good awareness of bottlenecks"],
        weaknesses=["Did not mention rate limiting initially"],
        feedback="Strong system design answer with practical scaling considerations.",
        ideal_response="A comprehensive design includes API Gateway, Redis cache, consistent hashing, and database sharding.",
        missing_points=["Rate limiting and DDoS protection", "Analytics logging"],
        improvement_suggestions=["Structure your answer using the RADIO framework."],
        scenario_id=scenario.id,
    )
    print("EvaluationResult instantiation: OK, score =", eval_result.overall_score)
    print("ALL DAY 1 CHECKS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
