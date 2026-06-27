from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from core.auth import get_current_user
from models.user_model import User
from repositories.resume_repository import ResumeRepository
from schemas.ats_schema import ATSValidationResponse
from services.ats_validation_service import ATSValidationService

router = APIRouter(prefix="/ats", tags=["ATS Validation"])


@router.get(
    "/resumes/{resume_id}/validate",
    response_model=ATSValidationResponse,
    summary="Validate resume ATS compatibility",
)
def validate_resume_ats(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ATSValidationResponse:
    """Validate an authenticated user's resume against ATS rules."""

    resume_repository = ResumeRepository(db)
    ats_service = ATSValidationService(resume_repository)

    return ats_service.validate_resume(
        resume_id=resume_id,
        user_id=current_user.id,
    )
