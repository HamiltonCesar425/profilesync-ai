from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from core.auth import get_current_user
from domain.targeted_resume import TargetedResumeCompositionError
from models.user_model import User
from repositories.job_repository import JobRepository
from repositories.professional_experience_repository import (
    ProfessionalExperienceRepository,
)
from repositories.profile_repository import ProfileRepository
from repositories.project_repository import ProjectRepository
from repositories.technology_repository import TechnologyRepository
from schemas.targeted_resume_schema import (
    TargetedResumePreviewRequest,
    TargetedResumePreviewResponse,
)
from services.targeted_resume_composer import TargetedResumeComposer
from services.targeted_resume_preview_service import (
    TargetedResumePreviewService,
    TargetedResumePreviewStructuralError,
)
from services.targeted_resume_source_loader import (
    AuthorizedCompositionSourcesUnavailableError,
    TargetedResumeSourceLoader,
)


router = APIRouter(prefix="/targeted-resumes", tags=["Targeted Resumes"])


def get_targeted_resume_preview_service(
    db: Session = Depends(get_db),
) -> TargetedResumePreviewService:
    source_loader = TargetedResumeSourceLoader(
        profile_repository=ProfileRepository(db),
        job_repository=JobRepository(db),
        experience_repository=ProfessionalExperienceRepository(db),
        project_repository=ProjectRepository(db),
        technology_repository=TechnologyRepository(db),
    )
    return TargetedResumePreviewService(
        source_loader=source_loader,
        composer=TargetedResumeComposer(),
    )


@router.post(
    "/preview",
    response_model=TargetedResumePreviewResponse,
    status_code=status.HTTP_200_OK,
)
def generate_targeted_resume_preview(
    request: TargetedResumePreviewRequest,
    current_user: User = Depends(get_current_user),
    preview_service: TargetedResumePreviewService = Depends(
        get_targeted_resume_preview_service
    ),
) -> TargetedResumePreviewResponse:
    try:
        return preview_service.generate_preview(
            profile_id=request.profile_id,
            job_id=request.job_id,
            authenticated_user_id=current_user.id,
        )
    except AuthorizedCompositionSourcesUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authorized preview sources are unavailable.",
        ) from exc
    except (
        TargetedResumePreviewStructuralError,
        TargetedResumeCompositionError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate targeted resume preview.",
        ) from exc
