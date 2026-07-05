from pydantic import BaseModel


class CareerGoalRequest(BaseModel):
    target_role: str
    seniority: str | None = None


class CareerAnalysisResponse(BaseModel):
    target_role: str
    compatibility_score: int
    strengths: list[str]
    gaps: list[str]
    recommendations: list[str]
