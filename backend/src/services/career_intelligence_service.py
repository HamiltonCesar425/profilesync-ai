from schemas.career_goal_schema import (
    CareerAnalysisResponse,
    CareerGoalRequest,
)

from services.impact_recommendation_service import (
    ImpactRecommendationService,
)


class CareerIntelligenceService:
    def __init__(self):
        self.recommendation_service = ImpactRecommendationService()

    def analyze(
        self,
        goal: CareerGoalRequest,
        skills: list[str],
    ) -> CareerAnalysisResponse:
        required_skills = {
            "backend python": [
                "python",
                "fastapi",
                "sql",
                "docker",
                "tests",
            ],
        }

        target = goal.target_role.lower().strip()
        normalized_skills = {skill.lower().strip() for skill in skills}

        expected = required_skills.get(target, [])

        matches = [skill for skill in expected if skill in normalized_skills]

        gaps = [skill for skill in expected if skill not in normalized_skills]

        score = int(len(matches) / len(expected) * 100) if expected else 0

        impact_recommendations = self.recommendation_service.generate(gaps)

        return CareerAnalysisResponse(
            target_role=goal.target_role.strip(),
            compatibility_score=score,
            strengths=matches,
            gaps=gaps,
            recommendations=impact_recommendations.recommendations,
        )

