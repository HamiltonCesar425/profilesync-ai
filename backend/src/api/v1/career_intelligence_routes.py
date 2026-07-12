from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.auth import get_current_user
from database.session import get_db
from models.user_model import User
from repositories.job_repository import JobRepository
from schemas.career_goal_schema import (
    CareerAnalysisResponse,
    CareerGoalRequest,
)
from services.career_intelligence_service import CareerIntelligenceService
from services.job_service import JobNotFoundError, JobService

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


@router.post(
    "/jobs/{job_id}/analyze",
    response_model=CareerAnalysisResponse,
)
def analyze_registered_job(
    job_id: int,
    request: CareerGoalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CareerAnalysisResponse:
    job_service = JobService(JobRepository(db))

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

    career_service = CareerIntelligenceService()
    goal = CareerGoalRequest(
        target_role=job.title,
        description=job.description,
        skills=request.skills,
    )

    return career_service.analyze(
        goal=goal,
        skills=request.skills,
    )
