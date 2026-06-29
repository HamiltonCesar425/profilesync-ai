from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = None
    role: str | None = Field(default=None, max_length=120)
    repository_url: HttpUrl | None = None
    demo_url: HttpUrl | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False


class ProjectCreate(ProjectBase):
    profile_id: int = Field(..., gt=0)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    role: str | None = Field(default=None, max_length=120)
    repository_url: HttpUrl | None = None
    demo_url: HttpUrl | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None


class ProjectResponse(ProjectBase):
    id: int
    profile_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
