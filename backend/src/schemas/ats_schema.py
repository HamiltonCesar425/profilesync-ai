from enum import Enum

from pydantic import BaseModel, Field


class ATSIssueSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class ATSValidationStatus(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    NEEDS_IMPROVEMENT = "needs_improvement"
    POOR = "poor"


class ATSValidationIssue(BaseModel):
    rule: str = Field(..., description="nome da regra ATS executada.")
    severity: ATSIssueSeverity = Field(
        ..., description="Nível de severidade do problema encontrado."
    )
    message: str = Field(..., description="Descrição objetiva do problema encontrado.")


class ATSValidationResponse(BaseModel):
    resume_id: int = Field(..., description="ID do currículo validado.")
    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Pontuação ATS calculadora entre 0 e 100.",
    )
    status: ATSValidationStatus = Field(
        ..., description="Classificação geral da compatibilidade ATS."
    )
    passed: bool = Field(
        ..., description="Indica se o currículo atingiu o mínimo aceitável."
    )
    issues: list[ATSValidationIssue] = Field(
        default_factory=list,
        description="Lista de problemas encontrados durante a validação.",
    )
    suggestions: list[str] = Field(
        default_factory=list,
        description="Sugestões objetivas para melhorar o currículo.",
    )
