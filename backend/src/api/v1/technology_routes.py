from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from core.auth import get_current_user
from domain.exceptions import DomainError
from models.user_model import User
from repositories.profile_repository import ProfileRepository
from repositories.technology_repository import TechnologyRepository
from schemas.technology_schema import (
    TechnologyCreate,
    TechnologyResponse,
    TechnologyUpdate,
)
from services.technology_service import TechnologyService

router = APIRouter(prefix="/technologies", tags=["Technologies"])


def get_technology_service(
    db: Session = Depends(get_db),
) -> TechnologyService:
    """Cria a instância do serviço de tecnologias."""
    return TechnologyService(
        technology_repository=TechnologyRepository(db),
        profile_repository=ProfileRepository(db),
    )


@router.post(
    "/profiles/{profile_id}",
    response_model=TechnologyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_technology(
    profile_id: int,
    technology_data: TechnologyCreate,
    current_user: User = Depends(get_current_user),
    technology_service: TechnologyService = Depends(get_technology_service),
) -> TechnologyResponse:
    """Cria uma tecnologia ou competência vinculada a um perfil."""
    try:
        return technology_service.create_technology(
            profile_id=profile_id,
            user_id=current_user.id,
            technology_data=technology_data,
        )
    except DomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/profiles/{profile_id}",
    response_model=list[TechnologyResponse],
)
def list_profile_technologies(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    technology_service: TechnologyService = Depends(get_technology_service),
) -> list[TechnologyResponse]:
    """Lista tecnologias e competências vinculadas a um perfil."""
    try:
        return technology_service.list_profile_technologies(
            profile_id=profile_id,
            user_id=current_user.id,
        )
    except DomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{technology_id}",
    response_model=TechnologyResponse,
)
def get_technology(
    technology_id: int,
    current_user: User = Depends(get_current_user),
    technology_service: TechnologyService = Depends(get_technology_service),
) -> TechnologyResponse:
    """Busca uma tecnologia ou competência pelo identificador."""
    try:
        return technology_service.get_technology(
            technology_id=technology_id,
            user_id=current_user.id,
        )
    except DomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{technology_id}",
    response_model=TechnologyResponse,
)
def update_technology(
    technology_id: int,
    technology_data: TechnologyUpdate,
    current_user: User = Depends(get_current_user),
    technology_service: TechnologyService = Depends(get_technology_service),
) -> TechnologyResponse:
    """Atualiza parcialmente uma tecnologia ou competência."""
    try:
        return technology_service.update_technology(
            technology_id=technology_id,
            user_id=current_user.id,
            technology_data=technology_data,
        )
    except DomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{technology_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_technology(
    technology_id: int,
    current_user: User = Depends(get_current_user),
    technology_service: TechnologyService = Depends(get_technology_service),
) -> None:
    """Remove uma tecnologia ou competência."""
    try:
        technology_service.delete_technology(
            technology_id=technology_id,
            user_id=current_user.id,
        )
    except DomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    
