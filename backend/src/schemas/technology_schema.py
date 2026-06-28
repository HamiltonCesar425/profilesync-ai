from pydantic import BaseModel, ConfigDict, Field


class TechnologyBase(BaseModel):
    """Campos base para tecnologias e competências."""

    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    proficiency_level: str = Field(..., min_length=1, max_length=30)
    years_experience: int | None = Field(default=None, ge=0)


class TechnologyCreate(TechnologyBase):
    """Schema para criação de tecnologia."""


class TechnologyUpdate(BaseModel):
    """Schema para atualização parcial de tecnologia."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    proficiency_level: str | None = Field(default=None, min_length=1, max_length=30)
    years_experience: int | None = Field(default=None, ge=0)


class TechnologyResponse(TechnologyBase):
    """Schema de resposta para tecnologia."""

    id: int
    profile_id: int

    model_config = ConfigDict(from_attributes=True)
