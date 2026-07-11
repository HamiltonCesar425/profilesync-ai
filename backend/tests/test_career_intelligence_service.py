from schemas.career_goal_schema import CareerGoalRequest
from services.career_intelligence_service import CareerIntelligenceService


def test_analyze_backend_python_with_partial_match() -> None:
    service = CareerIntelligenceService()

    goal = CareerGoalRequest(
        target_role="backend python",
    )

    result = service.analyze(
        goal=goal,
        skills=[
            "Python",
            "FastAPI",
            "SQL",
        ],
    )

    assert result.compatibility_score == 60
    assert result.strengths == [
        "python",
        "fastapi",
        "sql",
    ]
    assert result.gaps == [
        "docker",
        "tests",
    ]

    assert len(result.recommendations) == 2
    assert result.recommendations[0].skill == "docker"
    assert (
        result.recommendations[0].impact_score >= result.recommendations[1].impact_score
    )

    assert result.action_plan.current_score == result.compatibility_score
    assert result.action_plan.estimated_score_after_actions == 77
    assert len(result.action_plan.actions) == 2

    assert result.action_plan.actions[0].priority == 1
    assert result.action_plan.actions[0].title == (
        "Containerizar um projeto com Docker"
    )
    assert result.action_plan.actions[0].impact_score == 9

    assert result.action_plan.actions[1].priority == 2
    assert result.action_plan.actions[1].title == ("Adicionar testes automatizados")
    assert result.action_plan.actions[1].impact_score == 8


def test_analyze_backend_python_with_match() -> None:
    service = CareerIntelligenceService()

    goal = CareerGoalRequest(
        target_role="backend python",
    )

    result = service.analyze(
        goal=goal,
        skills=[
            "Python",
            "FastAPI",
            "SQL",
            "Docker",
            "Tests",
        ],
    )

    assert result.compatibility_score == 100
    assert result.strengths == [
        "python",
        "fastapi",
        "sql",
        "docker",
        "tests",
    ]
    assert result.gaps == []
    assert result.recommendations == []

    assert result.action_plan.current_score == 100
    assert result.action_plan.estimated_score_after_actions == 100
    assert result.action_plan.actions == []


def test_analyze_unknown_target_role_returns_safe_empty_analysis() -> None:
    service = CareerIntelligenceService()

    goal = CareerGoalRequest(
        target_role="unknown role",
    )

    result = service.analyze(
        goal=goal,
        skills=[
            "Python",
            "FastAPI",
        ],
    )

    assert result.target_role == "unknown role"
    assert result.compatibility_score == 0
    assert result.strengths == []
    assert result.gaps == []
    assert result.recommendations == []

    assert result.action_plan.current_score == 0
    assert result.action_plan.estimated_score_after_actions == 0
    assert result.action_plan.actions == []


def test_analyze_normalizes_target_role_and_skills() -> None:
    service = CareerIntelligenceService()

    goal = CareerGoalRequest(
        target_role=" Backend Python ",
    )

    result = service.analyze(
        goal=goal,
        skills=[
            " python ",
            " FASTAPI ",
            " sql ",
        ],
    )

    assert result.target_role == "Backend Python"
    assert result.compatibility_score == 60
    assert result.strengths == [
        "python",
        "fastapi",
        "sql",
    ]
    assert result.gaps == [
        "docker",
        "tests",
    ]

    assert result.action_plan.current_score == 60
    assert result.action_plan.estimated_score_after_actions == 77
    assert [action.priority for action in result.action_plan.actions] == [
        1,
        2,
    ]
    assert [action.impact_score for action in result.action_plan.actions] == [
        9,
        8,
    ]
