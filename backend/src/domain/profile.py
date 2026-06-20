from dataclasses import dataclass

@dataclass(frozen=True)
class Profile:
    id: int
    user_id: int
    full_name: str
    professional_title: str
    summary: str
    location: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None

    