from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from core.auth import get_current_user
from models.user_model import User
from repositories.profile_repository import ProfileRepository
from repositories.project_repository import ProjectRepository
from schemas.project_schema import ProjectCreate, ProjectResponse, ProjectUpdate
from services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(
        project_repository=ProjectRepository(db),
        profile_repository=ProfileRepository(db),
    )


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    try:
        return service.create_project(
            project_data=project_data,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/profile/{profile_id}",
    response_model=list[ProjectResponse],
)
def list_projects_by_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectResponse]:
    try:
        return service.list_projects_by_profile(
            profile_id=profile_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{project_id}/profile/{profile_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: int,
    profile_id: int,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    try:
        return service.get_project(
            project_id=project_id,
            profile_id=profile_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{project_id}/profile/{profile_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    profile_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    try:
        return service.update_project(
            project_id=project_id,
            profile_id=profile_id,
            project_data=project_data,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{project_id}/profile/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: int,
    profile_id: int,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(get_project_service),
) -> None:
    try:
        service.delete_project(
            project_id=project_id,
            profile_id=profile_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
