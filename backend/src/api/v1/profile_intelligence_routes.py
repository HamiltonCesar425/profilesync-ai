from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from core.auth import get_current_user
from models.user_model import User
from repositories.professional_experience_repository import (
    ProfessionalExperienceRepository,
)
from repositories.profile_repository import ProfileRepository
from repositories.project_repository import ProjectRepository
from repositories.technology_repository import TechnologyRepository
from schemas.profile_intelligence_schema import ProfessionalDiagnosis
from services.profile_intelligence_service import ProfileIntelligenceService

router = APIRouter(
    prefix="/profile-intelligence",
    tags=["Profile Intelligence"],
)


@router.post(
    "/analyze",
    response_model=ProfessionalDiagnosis,
    status_code=status.HTTP_200_OK,
)
def analyze_profile(
    profile_id: int,
    target_role: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfessionalDiagnosis:
    """Gera diagnóstico profissional com base nos dados reais do perfil."""

    profile_repository = ProfileRepository(db)
    technology_repository = TechnologyRepository(db)
    project_repository = ProjectRepository(db)
    experience_repository = ProfessionalExperienceRepository(db)

    profile = profile_repository.get_by_id_and_user_id(
        profile_id=profile_id,
        user_id=current_user.id,
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )

    technologies = technology_repository.list_by_profile_id(profile_id)
    projects = project_repository.list_by_profile_id(profile_id)
    experiences = experience_repository.list_by_profile_id(profile_id)

    service = ProfileIntelligenceService()

    return service.generate_diagnosis(
        target_role=target_role,
        technologies=[technology.name for technology in technologies],
        projects_count=len(projects),
        experiences_count=len(experiences),
    )
