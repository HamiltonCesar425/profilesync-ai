from pydantic import BaseModel, Field


class ProfessionalDiagnosis(BaseModel):
    score: int = Field(ge=0, le=100)
    strengths: list[str]
    improvements: list[str]
    recommendations: list[str]
