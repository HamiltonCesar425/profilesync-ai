from schemas.impact_recommendation_schema import (
    ImpactRecommendation,
    ImpactRecommendationResponse,
)


class ImpactRecommendationService:
    def generate(
        self,
        gaps: list[str],
    ) -> ImpactRecommendationResponse:
        impact_map = {
            "docker": {
                "priority": "high",
                "impact_score": 90,
                "reason": (
                    "Docker aumenta aderência profissional por demonstrar "
                    "capacidade de empacotar, executar e entregar aplicações."
                ),
            },
            "tests": {
                "priority": "high",
                "impact_score": 85,
                "reason": (
                    "Testes automatizados aumentam confiabilidade técnica "
                    "e reduzem risco em aplicações profissionais."
                ),
            },
            "sql": {
                "priority": "medium",
                "impact_score": 75,
                "reason": (
                    "SQL fortalece a capacidade de trabalhar com dados "
                    "persistentes e consultas estruturadas."
                ),
            },
        }

        recommendations = []

        for gap in gaps:
            normalized_gap = gap.lower().strip()
            impact_data = impact_map.get(
                normalized_gap,
                {
                    "priority": "low",
                    "impact_score": 50,
                    "reason": (
                        "Esta competência pode contribuir para a evolução "
                        "profissional, mas exige análise contextual adicional."
                    ),
                },
            )

            recommendations.append(
                ImpactRecommendation(
                    skill=normalized_gap,
                    priority=impact_data["priority"],
                    impact_score=impact_data["impact_score"],
                    reason=impact_data["reason"],
                )
            )

        recommendations.sort(
            key=lambda recommendation: recommendation.impact_score,
            reverse=True,
        )

        return ImpactRecommendationResponse(
            recommendations=recommendations,
        )
