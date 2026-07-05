from pydantic import BaseModel


class ImpactRecommendation(BaseModel):
    skill: str
    priority: str
    impact_score: int
    reason: str


class ImpactRecommendationResponse(BaseModel):
    recommendations: list[ImpactRecommendation]
