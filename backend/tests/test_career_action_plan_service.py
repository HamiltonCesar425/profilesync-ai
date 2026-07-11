from services.career_action_plan_service import CareerActionPlanService


def test_build_plan_orders_actions_by_impact() -> None:
    service = CareerActionPlanService()

    plan = service.build_plan(
        current_score=60,
        missing_skills=["git", "docker", "python"],
    )

    assert plan.current_score == 60
    assert plan.estimated_score_after_actions == 84
    assert [action.priority for action in plan.actions] == [1, 2, 3]
    assert [action.impact_score for action in plan.actions] == [10, 9, 5]
    assert [action.title for action in plan.actions] == [
        "Fortalecer conhecimentos em Python",
        "Containerizar um projeto com Docker",
        "Demonstrar domínio de Git",
    ]


def test_build_plan_uses_alphabetical_order_for_equal_impacts() -> None:
    service = CareerActionPlanService()

    plan = service.build_plan(
        current_score=50,
        missing_skills=["fastapi", "python"],
    )

    assert [action.title for action in plan.actions] == [
        "Criar uma API com FastAPI",
        "Fortalecer conhecimentos em Python",
    ]


def test_build_plan_normalizes_and_deduplicates_skills() -> None:
    service = CareerActionPlanService()

    plan = service.build_plan(
        current_score=70,
        missing_skills=[
            " Docker ",
            "docker",
            "DOCKER",
            "",
            "   ",
        ],
    )

    assert len(plan.actions) == 1
    assert plan.actions[0].title == "Containerizar um projeto com Docker"
    assert plan.estimated_score_after_actions == 79


def test_build_plan_uses_default_rule_for_unknown_skill() -> None:
    service = CareerActionPlanService()

    plan = service.build_plan(
        current_score=55,
        missing_skills=["Kafka"],
    )

    assert len(plan.actions) == 1
    assert plan.actions[0].priority == 1
    assert plan.actions[0].title == "Desenvolver conhecimento em kafka"
    assert plan.actions[0].impact_score == 5
    assert plan.actions[0].estimated_effort == "2 semanas"
    assert plan.actions[0].category == "technical_skill"
    assert plan.estimated_score_after_actions == 60


def test_build_plan_returns_empty_actions_when_no_skills_are_missing() -> None:
    service = CareerActionPlanService()

    plan = service.build_plan(
        current_score=85,
        missing_skills=[],
    )

    assert plan.current_score == 85
    assert plan.estimated_score_after_actions == 85
    assert plan.actions == []


def test_build_plan_limits_estimated_score_to_one_hundred() -> None:
    service = CareerActionPlanService()

    plan = service.build_plan(
        current_score=95,
        missing_skills=["python", "docker", "tests"],
    )

    assert plan.estimated_score_after_actions == 100


def test_build_plan_preserves_current_score() -> None:
    service = CareerActionPlanService()

    plan = service.build_plan(
        current_score=42,
        missing_skills=["sql"],
    )

    assert plan.current_score == 42


def test_build_plan_assigns_sequential_priorities_after_sorting() -> None:
    service = CareerActionPlanService()

    plan = service.build_plan(
        current_score=50,
        missing_skills=["git", "tests", "docker", "python"],
    )

    assert [action.priority for action in plan.actions] == [1, 2, 3, 4]
