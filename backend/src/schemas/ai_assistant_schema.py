from pydantic import BaseModel, Field


class ImproveProfessionalDescriptionRequest(BaseModel):
    text: str = Field(
        min_length=1,
        description="Original professional description to improve.",
    )


class ImproveProfessionalDescriptionResponse(BaseModel):
    original_text: str
    improved_text: str
