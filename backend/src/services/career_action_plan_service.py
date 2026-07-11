from dataclasses import dataclass

from schemas.career_action_plan_schema import (
    CareerActionItem,
    CareerActionPlanResponse,
)


@dataclass(frozen=True)
class ActionRule:
    """Define uma regra determinística para um gap profissional."""

    title: str
    description: str
    impact_score: int
    estimated_effort: str
    category: str


class CareerActionPlanService:
    """Gera um plano priorizado a partir dos gaps identificados."""

    _DEFAULT_RULE = ActionRule(
        title="Desenvolver competência ausente",
        description=(
            "Estude a competência identificada e produza uma evidência prática "
            "que possa ser demonstrada no currículo ou portfólio."
        ),
        impact_score=5,
        estimated_effort="2 semanas",
        category="technical_skill",
    )

    _ACTION_RULES: dict[str, ActionRule] = {
        "python": ActionRule(
            title="Fortalecer conhecimentos em Python",
            description=(
                "Desenvolva uma aplicação Python aplicando organização em "
                "camadas, tratamento de erros e testes automatizados."
            ),
            impact_score=10,
            estimated_effort="2 semanas",
            category="technical_skill",
        ),
        "fastapi": ActionRule(
            title="Criar uma API com FastAPI",
            description=(
                "Implemente e publique uma API REST com validação de dados, "
                "autenticação, documentação OpenAPI e testes automatizados."
            ),
            impact_score=10,
            estimated_effort="2 semanas",
            category="technical_skill",
        ),
        "sql": ActionRule(
            title="Aprimorar conhecimentos em SQL",
            description=(
                "Pratique consultas, relacionamentos, agregações e modelagem "
                "relacional em um projeto com persistência de dados."
            ),
            impact_score=8,
            estimated_effort="1 semana",
            category="data",
        ),
        "docker": ActionRule(
            title="Containerizar um projeto com Docker",
            description=(
                "Crie um Dockerfile e uma configuração reproduzível para "
                "executar uma aplicação existente em contêiner."
            ),
            impact_score=9,
            estimated_effort="1 semana",
            category="devops",
        ),
        "tests": ActionRule(
            title="Adicionar testes automatizados",
            description=(
                "Implemente testes unitários e de integração para os fluxos "
                "principais de um projeto e documente a cobertura alcançada."
            ),
            impact_score=8,
            estimated_effort="1 semana",
            category="software_quality",
        ),
        "testing": ActionRule(
            title="Adicionar testes automatizados",
            description=(
                "Implemente testes unitários e de integração para os fluxos "
                "principais de um projeto e documente a cobertura alcançada."
            ),
            impact_score=8,
            estimated_effort="1 semana",
            category="software_quality",
        ),
        "git": ActionRule(
            title="Demonstrar domínio de Git",
            description=(
                "Organize um repositório com commits claros, branches de "
                "trabalho e documentação objetiva do fluxo de desenvolvimento."
            ),
            impact_score=5,
            estimated_effort="3 dias",
            category="development_practice",
        ),
        "ci/cd": ActionRule(
            title="Implementar um pipeline de CI/CD",
            description=(
                "Configure um pipeline para executar análise estática, testes "
                "e verificações de segurança automaticamente."
            ),
            impact_score=8,
            estimated_effort="1 semana",
            category="devops",
        ),
    }

    def build_plan(
        self,
        current_score: int,
        missing_skills: list[str],
    ) -> CareerActionPlanResponse:
        """
        Constrói um plano priorizado para os gaps profissionais informados.

        Args:
            current_score: Score atual de compatibilidade com a vaga.
            missing_skills: Competências exigidas pela vaga e ausentes no perfil.

        Returns:
            Plano de ações ordenado pelo maior impacto estimado.
        """
        normalized_skills = self._normalize_and_deduplicate(missing_skills)

        action_candidates = [
            self._build_action_candidate(skill) for skill in normalized_skills
        ]

        sorted_candidates = sorted(
            action_candidates,
            key=lambda item: (-item.impact_score, item.title.casefold()),
        )

        actions = [
            CareerActionItem(
                priority=index,
                title=action.title,
                description=action.description,
                impact_score=action.impact_score,
                estimated_effort=action.estimated_effort,
                category=action.category,
            )
            for index, action in enumerate(sorted_candidates, start=1)
        ]

        estimated_score = min(
            current_score + sum(action.impact_score for action in actions),
            100,
        )

        return CareerActionPlanResponse(
            current_score=current_score,
            estimated_score_after_actions=estimated_score,
            actions=actions,
        )

    def _build_action_candidate(
        self,
        normalized_skill: str,
    ) -> CareerActionItem:
        rule = self._ACTION_RULES.get(normalized_skill)

        if rule is None:
            return CareerActionItem(
                priority=1,
                title=f"Desenvolver conhecimento em {normalized_skill}",
                description=self._DEFAULT_RULE.description,
                impact_score=self._DEFAULT_RULE.impact_score,
                estimated_effort=self._DEFAULT_RULE.estimated_effort,
                category=self._DEFAULT_RULE.category,
            )

        return CareerActionItem(
            priority=1,
            title=rule.title,
            description=rule.description,
            impact_score=rule.impact_score,
            estimated_effort=rule.estimated_effort,
            category=rule.category,
        )

    @staticmethod
    def _normalize_and_deduplicate(
        missing_skills: list[str],
    ) -> list[str]:
        normalized_skills: list[str] = []
        seen: set[str] = set()

        for skill in missing_skills:
            normalized_skill = skill.strip().casefold()

            if not normalized_skill or normalized_skill in seen:
                continue

            seen.add(normalized_skill)
            normalized_skills.append(normalized_skill)

        return normalized_skills
