from fastapi import HTTPException, status
from exporters.markdown_exporter import MarkdownExporter
from repositories.resume_repository import ResumeRepository
from schemas.export_schema import ExportFormat


class ExportService:
    def __init__(self, resume_repository: ResumeRepository):
        self.resume_repository = resume_repository

    def export_resume(
        self,
        resume_id: int,
        user_id: int,
        export_format: ExportFormat,
    ) -> str:
        resume = self.resume_repository.get_by_id_and_user_id(
            resume_id=resume_id,
            user_id=user_id,
        )

        if resume is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Currículo não encontrado.",
            )
        if export_format == ExportFormat.MARKDOWN:
            return MarkdownExporter.export(resume)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de exportação não suportado.",
        )
