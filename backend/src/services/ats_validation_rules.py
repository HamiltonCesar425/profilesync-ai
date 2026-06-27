from schemas.resume_schema import ResumeResponse
from services.ats_rules import ATSRule, ATSRuleResult


class ResumeTitleRule(ATSRule):
    """Valida o título interno do currículo."""

    name = "ResumeTitleRule"

    def validate(self, resume: ResumeResponse) -> ATSRuleResult:
        if not resume.title.strip():
            return ATSRuleResult(
                rule=self.name,
                passed=False,
                severity="critical",
                message="O currículo não possui título.",
                suggestion="Informe um título claro para identificar o currículo.",
                score_penalty=10,
            )

        return ATSRuleResult(rule=self.name, passed=True)


class TargetRoleRule(ATSRule):
    """Valida o cargo-alvo do currículo."""

    name = "TargetRoleRule"

    def validate(self, resume: ResumeResponse) -> ATSRuleResult:
        if not resume.target_role.strip():
            return ATSRuleResult(
                rule=self.name,
                passed=False,
                severity="critical",
                message="O currículo não possui cargo-alvo.",
                suggestion="Informe o cargo-alvo do currículo.",
                score_penalty=15,
            )

        return ATSRuleResult(rule=self.name, passed=True)


class ContentLengthRule(ATSRule):
    """Valida se o conteúdo possui tamanho mínimo para análise ATS."""

    name = "ContentLengthRule"
    minimum_length = 300

    def validate(self, resume: ResumeResponse) -> ATSRuleResult:
        content = resume.content.strip()

        if len(content) < self.minimum_length:
            return ATSRuleResult(
                rule=self.name,
                passed=False,
                severity="warning",
                message="O conteúdo do currículo está curto para análise ATS.",
                suggestion="Inclua resumo, experiências, competências e formação.",
                score_penalty=15,
            )

        return ATSRuleResult(rule=self.name, passed=True)


class RequiredSectionsRule(ATSRule):
    """Valida se o conteúdo contém seções essenciais de currículo."""

    name = "RequiredSectionsRule"

    required_sections = {
        "resumo": "Inclua uma seção de resumo profissional.",
        "experiência": "Inclua uma seção de experiência profissional.",
        "competências": "Inclua uma seção de competências técnicas.",
        "formação": "Inclua uma seção de formação acadêmica.",
    }

    def validate(self, resume: ResumeResponse) -> ATSRuleResult:
        content = resume.content.lower()
        missing_sections = [
            section for section in self.required_sections if section not in content
        ]

        if missing_sections:
            return ATSRuleResult(
                rule=self.name,
                passed=False,
                severity="critical",
                message=(
                    "O currículo não contém todas as seções essenciais: "
                    f"{', '.join(missing_sections)}."
                ),
                suggestion="Estruture o currículo com resumo, experiência, competências e formação.",
                score_penalty=20,
            )

        return ATSRuleResult(rule=self.name, passed=True)
