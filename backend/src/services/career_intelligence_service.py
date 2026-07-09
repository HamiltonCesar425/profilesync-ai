from services.job_requirement_extractor import JobRequirementExtractor
from schemas.career_goal_schema import (
    CareerAnalysisResponse,
    CareerGoalRequest,
)

from services.impact_recommendation_service import ImpactRecommendationService


class CareerIntelligenceService:
    REQUIRED_SKILLS_BY_ROLE = {
        "backend python": [
            "python",
            "fastapi",
            "sql",
            "docker",
            "tests",
        ],
    }

    def __init__(
        self,
        requirement_extractor: JobRequirementExtractor | None = None,
        recommendation_service: ImpactRecommendationService | None = None,
    ) -> None:
        self.requirement_extractor = requirement_extractor or JobRequirementExtractor()
        self.recommendation_service = (
            recommendation_service or ImpactRecommendationService()
        )

    def analyze(
        self,
        goal: CareerGoalRequest,
        skills: list[str],
    ) -> CareerAnalysisResponse:
        required_skills = self._get_required_skills(goal)

        normalized_skills = {skill.lower().strip() for skill in skills}
        expected = required_skills

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

    def _get_required_skills(self, goal: CareerGoalRequest) -> list[str]:
        target = goal.target_role.lower().strip()

        for role, required_skills in self.REQUIRED_SKILLS_BY_ROLE.items():
            if role == target or role in target:
                return required_skills

        source = goal.description or target
        return self.requirement_extractor.extract(source)
