import pytest
from pydantic import ValidationError

from schemas.career_action_plan_schema import (
    CareerActionItem,
    CareerActionPlanResponse,
)


def test_create_valid_career_action_item() -> None:
    action = CareerActionItem(
        priority=1,
        title="Aprender Docker",
        description="Containerizar um projeto FastAPI existente.",
        impact_score=12,
        estimated_effort="2 semanas",
        category="technical_skill",
    )

    assert action.priority == 1
    assert action.title == "Aprender Docker"
    assert action.impact_score == 12
    assert action.estimated_effort == "2 semanas"
    assert action.category == "technical_skill"


def test_create_valid_career_action_plan_response() -> None:
    action = CareerActionItem(
        priority=1,
        title="Adicionar testes automatizados",
        description="Criar testes unitários para os serviços principais.",
        impact_score=8,
        estimated_effort="1 semana",
        category="software_quality",
    )

    plan = CareerActionPlanResponse(
        current_score=70,
        estimated_score_after_actions=78,
        actions=[action],
    )

    assert plan.current_score == 70
    assert plan.estimated_score_after_actions == 78
    assert len(plan.actions) == 1
    assert plan.actions[0].title == "Adicionar testes automatizados"


def test_career_action_plan_actions_default_to_empty_list() -> None:
    plan = CareerActionPlanResponse(
        current_score=60,
        estimated_score_after_actions=60,
    )

    assert plan.actions == []


def test_career_action_item_rejects_priority_below_one() -> None:
    with pytest.raises(ValidationError):
        CareerActionItem(
            priority=0,
            title="Aprender Docker",
            description="Containerizar um projeto.",
            impact_score=10,
            estimated_effort="2 semanas",
            category="technical_skill",
        )


def test_career_action_item_rejects_negative_impact_score() -> None:
    with pytest.raises(ValidationError):
        CareerActionItem(
            priority=1,
            title="Aprender Docker",
            description="Containerizar um projeto.",
            impact_score=-1,
            estimated_effort="2 semanas",
            category="technical_skill",
        )


def test_career_action_item_rejects_impact_score_above_one_hundred() -> None:
    with pytest.raises(ValidationError):
        CareerActionItem(
            priority=1,
            title="Aprender Docker",
            description="Containerizar um projeto.",
            impact_score=101,
            estimated_effort="2 semanas",
            category="technical_skill",
        )


def test_career_action_item_rejects_missing_required_fields() -> None:
    with pytest.raises(ValidationError):
        CareerActionItem(
            priority=1,
            title="Aprender Docker",
            impact_score=10,
            estimated_effort="2 semanas",
            category="technical_skill",
        )


def test_career_action_plan_rejects_invalid_scores() -> None:
    with pytest.raises(ValidationError):
        CareerActionPlanResponse(
            current_score=101,
            estimated_score_after_actions=90,
        )

    with pytest.raises(ValidationError):
        CareerActionPlanResponse(
            current_score=70,
            estimated_score_after_actions=-1,
        )
