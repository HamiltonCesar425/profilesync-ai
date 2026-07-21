from pydantic import BaseModel, Field


class CareerActionItem(BaseModel):
    """Representa uma ação priorizada do plano de evolução profissional do usuário."""

    priority: int = Field(
        ge=1,
        description="Ordem de prioridade da ação no plano.",
    )
    title: str = Field(
        min_length=1,
        description="Título objetivo da ação recomendsada.",
    )
    description: str = Field(
        min_length=1, description="Orientação prática para executar a ação."
    )
    impact_score: int = Field(
        ge=0,
        le=100,
        description="Impacto estimado da ação no score de compatibilidade.",
    )
    estimated_effort: str = Field(
        min_length=1,
        description="Estimativa qualitativa de esforço para conclir a ação.",
    )
    category: str = Field(
        min_length=1, description="Categoria profissional associada à ação."
    )


class CareerActionPlanResponse(BaseModel):
    """Representa o plano priorizado de evolução profissional do usuário."""

    current_score: int = Field(
        ge=0,
        le=100,
        description="Score atual de compatibilidade com a vaga.",
    )
    estimated_score_after_actions: int = Field(
        ge=0,
        le=100,
        description="Score estimado após a execusão das ações.",
    )
    actions: list[CareerActionItem] = Field(
        default_factory=list,
        description="Açoes ordenadas por prioridade e impacto.",
    )
