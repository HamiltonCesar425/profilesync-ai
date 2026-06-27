from repositories.resume_repository import ResumeRepository
from schemas.ats_schema import (
    ATSValidationIssue,
    ATSValidationResponse,
    ATSValidationStatus,
)
from services.ats_validation_rules import (
    ContentLengthRule,
    RequiredSectionsRule,
    ResumeTitleRule,
    TargetRoleRule,
)
from services.ats_rules import ATSRuleResult


class ATSValidationService:
    """Serviço responsável por validar currículos contra regras ATS."""

    def __init__(self, resume_repository: ResumeRepository) -> None:
        self.resume_repository = resume_repository
        self.rules = [
            ResumeTitleRule(),
            TargetRoleRule(),
            ContentLengthRule(),
            RequiredSectionsRule(),
        ]

    def validate_resume(
        self,
        resume_id: int,
        user_id: int,
    ) -> ATSValidationResponse:
        """Valida um currículo pertencente ao usuário autenticado."""

        resume = self.resume_repository.get_by_id_and_user_id(
            resume_id=resume_id,
            user_id=user_id,
        )

        results = [rule.validate(resume) for rule in self.rules]

        score = self._calculate_score(results)
        failed_results = [result for result in results if not result.passed]

        return ATSValidationResponse(
            resume_id=resume.id,
            score=score,
            status=self._get_status(score),
            passed=score >= 75,
            issues=[
                ATSValidationIssue(
                    rule=result.rule,
                    severity=result.severity or "warning",
                    message=result.message or "Regra ATS não atendida.",
                )
                for result in failed_results
            ],
            suggestions=[
                result.suggestion
                for result in failed_results
                if result.suggestion is not None
            ],
        )

    @staticmethod
    def _calculate_score(results: list[ATSRuleResult]) -> int:
        """Calcula o score ATS com base nas regras aprovadas."""

        if not results:
            return 0

        passed_rules = sum(1 for result in results if result.passed)
        total_rules = len(results)

        return round((passed_rules / total_rules) * 100)

    @staticmethod
    def _get_status(score: int) -> ATSValidationStatus:
        """Classifica a compatibilidade ATS a partir do score calculado."""

        if score >= 90:
            return ATSValidationStatus.EXCELLENT
        if score >= 75:
            return ATSValidationStatus.GOOD
        if score >= 50:
            return ATSValidationStatus.NEEDS_IMPROVEMENT
        return ATSValidationStatus.POOR
