from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from core.auth import get_current_user
from models.user_model import User
from repositories.professional_experience_repository import (
    ProfessionalExperienceRepository,
)
from repositories.profile_repository import ProfileRepository
from schemas.professional_experience_schema import (
    ProfessionalExperienceCreate,
    ProfessionalExperienceResponse,
    ProfessionalExperienceUpdate,
)
from services.professional_experience_service import (
    ProfessionalExperienceService,
)

router = APIRouter(
    prefix="/profiles/{profile_id}/experiences",
    tags=["Professional Experiences"],
)


def get_professional_experience_service(
    db: Session = Depends(get_db),
) -> ProfessionalExperienceService:
    return ProfessionalExperienceService(
        repository=ProfessionalExperienceRepository(db),
        profile_repository=ProfileRepository(db),
    )


@router.post(
    "",
    response_model=ProfessionalExperienceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_professional_experience(
    profile_id: int,
    experience_data: ProfessionalExperienceCreate,
    current_user: User = Depends(get_current_user),
    service: ProfessionalExperienceService = Depends(
        get_professional_experience_service,
    ),
):
    try:
        return service.create_experience(
            profile_id=profile_id,
            user_id=current_user.id,
            experience_data=experience_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[ProfessionalExperienceResponse],
)
def list_professional_experiences(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    service: ProfessionalExperienceService = Depends(
        get_professional_experience_service,
    ),
):
    try:
        return service.list_experiences(
            profile_id=profile_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{experience_id}",
    response_model=ProfessionalExperienceResponse,
)
def get_professional_experience(
    profile_id: int,
    experience_id: int,
    current_user: User = Depends(get_current_user),
    service: ProfessionalExperienceService = Depends(
        get_professional_experience_service,
    ),
):
    try:
        return service.get_experience(
            experience_id=experience_id,
            profile_id=profile_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{experience_id}",
    response_model=ProfessionalExperienceResponse,
)
def update_professional_experience(
    profile_id: int,
    experience_id: int,
    experience_data: ProfessionalExperienceUpdate,
    current_user: User = Depends(get_current_user),
    service: ProfessionalExperienceService = Depends(
        get_professional_experience_service,
    ),
):
    try:
        return service.update_experience(
            experience_id=experience_id,
            profile_id=profile_id,
            user_id=current_user.id,
            experience_data=experience_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_professional_experience(
    profile_id: int,
    experience_id: int,
    current_user: User = Depends(get_current_user),
    service: ProfessionalExperienceService = Depends(
        get_professional_experience_service,
    ),
) -> None:
    try:
        service.delete_experience(
            experience_id=experience_id,
            profile_id=profile_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
