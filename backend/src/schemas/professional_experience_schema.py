from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ProfessionalExperienceBase(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=200)
    position: str = Field(..., min_length=2, max_length=150)
    employment_type: str | None = Field(default=None, max_length=50)
    work_model: str | None = Field(default=None, max_length=30)
    location: str | None = Field(default=None, max_length=120)
    description: str | None = None
    start_date: date
    end_date: date | None = None
    is_current: bool = False


class ProfessionalExperienceCreate(ProfessionalExperienceBase):
    pass


class ProfessionalExperienceUpdate(BaseModel):
    company_name: str | None = Field(default=None, min_length=2, max_length=200)
    position: str | None = Field(default=None, min_length=2, max_length=150)
    employment_type: str | None = Field(default=None, max_length=50)
    work_model: str | None = Field(default=None, max_length=30)
    location: str | None = Field(default=None, max_length=120)
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None


class ProfessionalExperienceResponse(ProfessionalExperienceBase):
    id: int
    profile_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
