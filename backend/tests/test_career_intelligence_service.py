from schemas.career_goal_schema import CareerGoalRequest
from services.career_intelligence_service import CareerIntelligenceService


def test_analyze_backend_python_with_partial_match():
    service = CareerIntelligenceService()

    goal = CareerGoalRequest(target_role="backend python")

    result = service.analyze(
        goal=goal,
        skills=["Python", "FastAPI", "SQL"],
    )

    assert result.target_role == "backend python"
    assert result.compatibility_score == 60
    assert result.strengths == ["python", "fastapi", "sql"]
    assert result.gaps == ["docker", "tests"]
    assert len(result.recommendations) == 2


def test_analyze_backend_python_with_match():
    service = CareerIntelligenceService()

    goal = CareerGoalRequest(target_role="backend python")

    result = service.analyze(
        goal=goal,
        skills=["Python", "FastAPI", "SQL", "Docker", "Tests"],
    )

    assert result.compatibility_score == 100
    assert result.gaps == []
    assert result.recommendations == []


def test_analyze_unknown_target_role_returns_safe_empty_analysis():
    service = CareerIntelligenceService()

    goal = CareerGoalRequest(target_role="unknow role")

    result = service.analyze(
        goal=goal,
        skills=["Python", "FastAPI"],
    )

    assert result.compatibility_score == 0
    assert result.strengths == []
    assert result.gaps == []
    assert result.recommendations == []


def test_analyze_normalizes_target_role_and_skills():
    service = CareerIntelligenceService()

    goal = CareerGoalRequest(target_role=" Backend Python ")

    result = service.analyze(
        goal=goal,
        skills=[" python ", " FASTAPI ", " sql "],
    )

    assert result.compatibility_score == 60
    assert result.strengths == ["python", "fastapi", "sql"]
    assert result.gaps == ["docker", "tests"]
