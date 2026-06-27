from abc import ABC, abstractmethod
from dataclasses import dataclass

from schemas.resume_schema import ResumeResponse


@dataclass(slots=True)
class ATSRuleResult:
    """Resultado produzido por uma regra ATS."""

    rule: str
    passed: bool
    severity: str | None = None
    message: str | None = None
    suggestion: str | None = None
    score_penalty: int = 0


class ATSRule(ABC):
    """Classe base para todas as regras de validação ATS."""

    name: str

    @abstractmethod
    def validate(self, resume: ResumeResponse) -> ATSRuleResult:
        """Executa a validação da regra."""
        raise NotImplementedError
