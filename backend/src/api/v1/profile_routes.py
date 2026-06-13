from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.session import get_db
from repositories.profile_repository import ProfileRepository
from schemas.profile_schema import ProfileCreate, ProfileResponse
from services.profile_service import ProfileService

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", response_model=ProfileResponse)
def create_profile(
    payload: ProfileCreate,
    db: Session = Depends(get_db),
):
    repository = ProfileRepository(db)
    service = ProfileService(repository)

    profile = service.create_profile(
        full_name=payload.full_name,
        professional_title=payload.professional_title,
        summary=payload.summary,
        location=payload.location,
        linkedin_url=payload.linkedin_url,
        github_url=payload.github_url,
    )

    return profile


@router.get("/", response_model=list[ProfileResponse])
def list_profiles(db: Session = Depends(get_db)):
    repository = ProfileRepository(db)
    service = ProfileService(repository)

    return service.list_profiles()


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
):
    repository = ProfileRepository(db)
    service = ProfileService(repository)

    profile = service.get_profile(profile_id)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return profile
