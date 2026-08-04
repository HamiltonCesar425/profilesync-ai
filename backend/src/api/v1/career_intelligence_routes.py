from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.auth import get_current_user
from database.session import get_db
from domain.exceptions import DomainError
from models.user_model import User
from repositories.job_repository import JobRepository
from repositories.professional_experience_repository import (
    ProfessionalExperienceRepository,
)
from repositories.profile_repository import ProfileRepository
from repositories.project_repository import ProjectRepository
from repositories.technology_repository import TechnologyRepository
from schemas.career_goal_schema import (
    CareerAnalysisResponse,
    CareerGoalRequest,
    DetectedCompetenciesResponse,
    RegisteredJobAnalysisRequest,
)
from services.career_intelligence_service import CareerIntelligenceService
from services.job_service import JobNotFoundError, JobService
from services.profile_competency_service import ProfileCompetencyService

router = APIRouter(
    prefix="/career-intelligence",
    tags=["Career Intelligence"],
)


@router.post(
    "/analyze",
    response_model=CareerAnalysisResponse,
)
def analyze_career_goal(
    request: CareerGoalRequest,
    current_user: User = Depends(get_current_user),
) -> CareerAnalysisResponse:
    service = CareerIntelligenceService()

    return service.analyze(
        goal=request,
        skills=request.skills,
    )


def _build_competency_service(db: Session) -> ProfileCompetencyService:
    return ProfileCompetencyService(
        profile_repository=ProfileRepository(db),
        technology_repository=TechnologyRepository(db),
        experience_repository=ProfessionalExperienceRepository(db),
        project_repository=ProjectRepository(db),
    )


@router.get(
    "/profiles/{profile_id}/competencies",
    response_model=DetectedCompetenciesResponse,
)
def get_detected_competencies(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DetectedCompetenciesResponse:
    service = _build_competency_service(db)

    try:
        competencies = service.get_profile_competencies(
            profile_id=profile_id,
            user_id=current_user.id,
        )
    except DomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        ) from exc

    return DetectedCompetenciesResponse(
        profile_id=profile_id,
        competencies=competencies,
    )


@router.post(
    "/jobs/{job_id}/analyze",
    response_model=CareerAnalysisResponse,
)
def analyze_registered_job(
    job_id: int,
    request: RegisteredJobAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CareerAnalysisResponse:
    job_service = JobService(
        repository=JobRepository(db),
    )

    try:
        job = job_service.get_job(
            job_id=job_id,
            user_id=current_user.id,
        )
    except JobNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        ) from exc

    try:
        competencies = _build_competency_service(db).get_profile_competencies(
            profile_id=request.profile_id,
            user_id=current_user.id,
        )
    except DomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        ) from exc

    if not competencies:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Nenhuma competência foi detectada no perfil. Cadastre tecnologias "
                "ou descreva competências nas experiências e projetos."
            ),
        )

    goal = CareerGoalRequest(
        target_role=job.title,
        description=job.description,
        skills=competencies,
    )

    career_service = CareerIntelligenceService()

    return career_service.analyze(
        goal=goal,
        skills=competencies,
    )
