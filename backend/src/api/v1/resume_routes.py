from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from core.auth import get_current_user
from models.user_model import User
from repositories.profile_repository import ProfileRepository
from repositories.resume_repository import ResumeRepository
from schemas.resume_schema import ResumeCreate, ResumeResponse, ResumeUpdate
from services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["Resumes"])


def get_resume_service(db: Session = Depends(get_db)) -> ResumeService:
    resume_repository = ResumeRepository(db)
    profile_repository = ProfileRepository(db)

    return ResumeService(
        resume_repository=resume_repository,
        profile_repository=profile_repository,
    )


@router.post(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_resume(
    resume_data: ResumeCreate,
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
) -> ResumeResponse:
    try:
        return resume_service.create_resume(
            resume_data=resume_data,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/profile/{profile_id}",
    response_model=list[ResumeResponse],
)
def list_resumes_by_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
) -> list[ResumeResponse]:
    try:
        return resume_service.list_resumes_by_profile(
            profile_id=profile_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{resume_id}/profile/{profile_id}",
    response_model=ResumeResponse,
)
def get_resume(
    resume_id: int,
    profile_id: int,
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
) -> ResumeResponse:
    try:
        return resume_service.get_resume(
            resume_id=resume_id,
            profile_id=profile_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{resume_id}/profile/{profile_id}",
    response_model=ResumeResponse,
)
def update_resume(
    resume_id: int,
    profile_id: int,
    resume_data: ResumeUpdate,
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
) -> ResumeResponse:
    try:
        return resume_service.update_resume(
            resume_id=resume_id,
            profile_id=profile_id,
            resume_data=resume_data,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{resume_id}/profile/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_resume(
    resume_id: int,
    profile_id: int,
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
) -> None:
    try:
        resume_service.delete_resume(
            resume_id=resume_id,
            profile_id=profile_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
