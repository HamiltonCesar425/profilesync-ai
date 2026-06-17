from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=120)
    professional_title: str = Field(..., min_length=3, max_length=120)
    summary: str = Field(..., min_length=20, max_length=1000)
    location: str | None = Field(default=None, max_length=120)
    linkedin_url: str | None = Field(default=None, max_length=255)
    github_url: str | None = Field(default=None, max_length=255)


class ProfileUpdate(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=120)
    professional_title: str = Field(..., min_length=3, max_length=120)
    summary: str = Field(..., min_length=20, max_length=1000)
    location: str | None = Field(default=None, max_length=120)
    linkedin_url: str | None = Field(default=None, max_length=255)
    github_url: str | None = Field(default=None, max_length=255)


class ProfileResponse(ProfileCreate):
    id: int
