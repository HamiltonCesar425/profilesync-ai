from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.auth import get_current_user
from database import get_db
from models.user_model import User
from schemas.job_schema import JobCreate, JobResponse
from services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobResponse:
    service = JobService(db)
    return service.create_job(payload, current_user.id)


@router.get(
    "",
    response_model=list[JobResponse],
)
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[JobResponse]:
    service = JobService(db)
    return service.list_jobs(current_user.id)
