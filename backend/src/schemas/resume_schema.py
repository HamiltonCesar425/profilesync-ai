from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResumeBase(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    target_role: str = Field(min_length=2, max_length=120)
    content: str = Field(min_length=10)
    version: int = Field(default=1, ge=1)


class ResumeCreate(ResumeBase):
    profile_id: int


class ResumeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=120)
    target_role: str | None = Field(default=None, min_length=2, max_length=120)
    content: str | None = Field(default=None, min_length=10)
    version: int | None = Field(default=None, ge=1)


class ResumeResponse(ResumeBase):
    id: int
    user_id: int
    profile_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
