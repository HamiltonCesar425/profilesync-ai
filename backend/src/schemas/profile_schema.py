from pydantic import BaseModel, Field

class ProfileCreate(BaseModel):
    full_name: str = Field(..., min_lenght=3, max_lenght=120)
    professional_title: str = Field(..., min_lenght=3, max_lenght=120)
    summary: str = Field(..., min_lenght=20, max_lenght=1000)
    location: str = Field(..., default=None,max_lenght=120)
    linkedin_url: str | None = Field(default=None, max_lenght=255)
    github_url: str | None = Field(default=None, max_lenght=255)


class ProfileResponse(ProfileCreate):
    id: int