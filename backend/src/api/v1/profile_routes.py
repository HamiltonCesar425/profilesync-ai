from fastapi import APIRouter, HTTPException

from repositories.profile_repository import ProfileRepository
from schemas.profile_schema import (
    ProfileCreate,
    ProfileResponse,
)

router = APIRouter(prefix="/profiles", tags=["Profiles"])
repository = ProfileRepository()


@router.post("/", response_model=ProfileResponse)
def create_profile(payload: ProfileCreate):

    profile = repository.create(
        full_name=payload.full_name,
        professional_title=payload.professional_title,
        summary=payload.summary,
        location=payload.location,
        linkedin_url=payload.linkedin_url,
        github_url=payload.github_url,
    )
    return ProfileResponse(**profile.__dict__)


@router.get("/", response_model=list[ProfileResponse])
def list_profiles():

    profiles = repository.list_all()

    return [ProfileResponse(**profile.__dict__) for profile in profiles]


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int):

    profile = repository.get_by_id(profile_id)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detatil="Profile not found",
        )

    return ProfileResponse(**profile.__dict__)
