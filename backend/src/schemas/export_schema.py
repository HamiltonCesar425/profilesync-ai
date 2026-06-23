from enum import Enum

from pydantic import BaseModel, Field


class ExportFormat(str, Enum):
    MARKDOWN = "markdown"
    PDF = "pdf"
    DOCX = "docx"


class ExportResponse(BaseModel):
    resume_id: int = Field(..., gt=0)
    format: ExportFormat
    filename: str
    content_type: str
