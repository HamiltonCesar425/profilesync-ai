from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_profile_service
from services.profile_service import ProfileService
from schemas.profile_schema import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)

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


@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(
    profile_id: int,
    profile_data: ProfileUpdate,
    service: ProfileService = Depends(get_profile_service),
) -> ProfileResponse:
    update_profile = service.update_profile(
        profile_id=profile_id,
        full_name=profile_data.full_name,
        professional_title=profile_data.professional_title,
        summary=profile_data.summary,
        location=profile_data.location,
        linkedin_url=profile_data.linkedin_url,
        github_url=profile_data.github_url,
    )

    if update_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return update_profile


@router.delete("/{profile_id}", status_code=204)
def delete_profile(
    profile_id: int,
    service: ProfileService = Depends(get_profile_service),
) -> None:
    deleted = service.delete_profile(profile_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Profile not found")
