from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.dependencies import get_db
from core.auth import get_current_user
from models.user_model import User
from repositories.resume_repository import ResumeRepository
from schemas.export_schema import ExportFormat
from services.export_service import ExportService

router = APIRouter(prefix="/exports", tags=["Exports"])


@router.get(
    "/resumes/{resume_id}/markdown",
    response_class=Response,
    summary="Exportar currículo em Markdown",
    description="Exporta um currículo do usuário autenticado em formato Markdown ATS-friendly.",
)
def export_resume_markdown(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    resume_repository = ResumeRepository(db)
    export_service = ExportService(resume_repository)

    content = export_service.export_resume(
        resume_id=resume_id,
        user_id=current_user.id,
        export_format=ExportFormat.MARKDOWN,
    )

    return Response(
        content=content,
        media_type="text/markdown",
    )
