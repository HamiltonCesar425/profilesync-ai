from pydantic import BaseModel, Field

from schemas.career_action_plan_schema import CareerActionPlanResponse
from schemas.impact_recommendation_schema import ImpactRecommendation


class CareerGoalRequest(BaseModel):
    target_role: str
    description: str | None = None
    skills: list[str] = Field(default_factory=list)
    seniority: str | None = None


class CareerAnalysisResponse(BaseModel):
    target_role: str
    compatibility_score: int
    strengths: list[str]
    gaps: list[str]
    recommendations: list[ImpactRecommendation]
    action_plan: CareerActionPlanResponse
