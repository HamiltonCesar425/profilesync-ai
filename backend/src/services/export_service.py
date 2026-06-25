from fastapi import HTTPException, status

from exporters.markdown_exporter import MarkdownExporter
from exporters.pdf_exporter import PDFExporter
from exporters.docx_exporter import DOCXExporter
from repositories.resume_repository import ResumeRepository


class ExportService:
    def __init__(self, resume_repository: ResumeRepository) -> None:
        self.resume_repository = resume_repository

    def export_resume_to_markdown(self, resume_id: int, user_id: int) -> str:
        resume = self.resume_repository.get_by_id_and_user_id(
            resume_id=resume_id,
            user_id=user_id,
        )

        if resume is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Currículo não encontrado.",
            )

        return MarkdownExporter.export(resume)

    def export_resume_to_pdf(self, resume_id: int, user_id: int) -> bytes:
        resume = self.resume_repository.get_by_id_and_user_id(
            resume_id=resume_id,
            user_id=user_id,
        )

        if resume is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Currículo não encontrado.",
            )
        return PDFExporter().export(resume)
        
    def export_resume_to_docx(self, resume_id: int, user_id: int) -> bytes:
        resume = self.resume_repository.get_by_id_and_user_id(
            resume_id=resume_id,
            user_id=user_id,
        )

        if resume is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Currículo não encontrado.",
            )
        
        return DOCXExporter().export(resume)  

