from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    company: str | None = Field(default=None, max_length=150)
    description: str = Field(..., min_length=2)


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    company: str | None = Field(default=None, max_length=150)
    description: str | None = Field(default=None, min_length=2)


class JobResponse(JobBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
