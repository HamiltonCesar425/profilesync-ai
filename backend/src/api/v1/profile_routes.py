from fastapi import APIRouter, Depends

from app.dependencies import get_profile_service
from schemas.profile_schema import ProfileCreate, ProfileResponse
from services.profile_service import ProfileService

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("", response_model=ProfileResponse)
def create_profile(
    request: ProfileCreate,
    service: ProfileService = Depends(get_profile_service),
):
    return service.create_profile(
        full_name=request.full_name,
        professional_title=request.professional_title,
        summary=request.summary,
        location=request.location,
        linkedin_url=request.linkedin_url,
        github_url=request.github_url,
    )


@router.get("", response_model=list[ProfileResponse])
def list_profiles(
    service: ProfileService = Depends(get_profile_service),
):
    return service.list_profiles()


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile_by_id(
    profile_id: int,
    service: ProfileService = Depends(get_profile_service),
):
    return service.get_profile(profile_id)
