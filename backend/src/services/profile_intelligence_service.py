from schemas.profile_intelligence_schema import ProfessionalDiagnosis


class ProfileIntelligenceService:
    """Gera diagnóstico profissional a partir dos dados estruturados do perfil."""

    def generate_diagnosis(
        self,
        target_role: str,
        technologies: list[str],
        projects_count: int,
        experiences_count: int,
    ) -> ProfessionalDiagnosis:
        score = self._calculate_score(
            target_role=target_role,
            technologies=technologies,
            projects_count=projects_count,
            experiences_count=experiences_count,
        )

        return ProfessionalDiagnosis(
            score=score,
            strengths=self._identify_strengths(
                technologies=technologies,
                projects_count=projects_count,
                experiences_count=experiences_count,
            ),
            improvements=self._identify_improvements(
                target_role=target_role,
                technologies=technologies,
                projects_count=projects_count,
                experiences_count=experiences_count,
            ),
            recommendations=self._generate_recommendations(
                target_role=target_role,
                technologies=technologies,
                projects_count=projects_count,
                experiences_count=experiences_count,
            ),
        )

    def _calculate_score(
        self,
        target_role: str,
        technologies: list[str],
        projects_count: int,
        experiences_count: int,
    ) -> int:
        score = 0

        if target_role.strip():
            score += 20

        if technologies:
            score += min(len(technologies) * 5, 30)

        if projects_count > 0:
            score += min(projects_count * 10, 25)

        if experiences_count > 0:
            score += min(experiences_count * 10, 25)

        return min(score, 100)

    def _identify_strengths(
        self,
        technologies: list[str],
        projects_count: int,
        experiences_count: int,
    ) -> list[str]:
        strengths = []

        if technologies:
            strengths.append("Perfil possui tecnologias cadastradas.")

        if projects_count > 0:
            strengths.append("Perfil possui projetos profissionais registrados.")

        if experiences_count > 0:
            strengths.append("Perfil possui experiências profissionais estruturadas.")

        return strengths

    def _identify_improvements(
        self,
        target_role: str,
        technologies: list[str],
        projects_count: int,
        experiences_count: int,
    ) -> list[str]:
        improvements = []

        if not target_role.strip():
            improvements.append("Definir um cargo alvo para orientar o diagnóstico.")

        if not technologies:
            improvements.append("Adicionar tecnologias relevantes ao perfil.")

        if projects_count == 0:
            improvements.append(
                "Adicionar projetos para demonstrar experiência prática."
            )

        if experiences_count == 0:
            improvements.append("Adicionar experiências profissionais estruturadas.")

        return improvements

    def _generate_recommendations(
        self,
        target_role: str,
        technologies: list[str],
        projects_count: int,
        experiences_count: int,
    ) -> list[str]:
        recommendations = []

        if target_role.strip():
            recommendations.append(
                f"Alinhar currículo, projetos e tecnologias ao cargo alvo: {target_role}."
            )

        if technologies:
            recommendations.append(
                "Destacar as tecnologias mais relevantes nas descrições de projetos e experiências."
            )

        if projects_count > 0:
            recommendations.append(
                "Transformar projetos cadastrados em evidências claras de competência técnica."
            )

        if experiences_count > 0:
            recommendations.append(
                "Reescrever experiências com foco em impacto, responsabilidade e resultado."
            )

        return recommendations
