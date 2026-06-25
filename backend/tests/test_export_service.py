from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from services.export_service import ExportService


class FakeResumeRepository:
    def get_by_id_and_user_id(self, resume_id: int, user_id: int):
        assert resume_id == 1
        assert user_id == 10

        return SimpleNamespace(
            title="Currículo Desenvolvedor Full Stack",
            target_role="Desenvolvedor Full Stack",
            summary=(
                "Desenvolvedor Full Stack com experiência em Python, "
                "FastAPI, SQLAlchemy, React e construção de produtos digitais."
            ),           
            content=(
                "Desenvolvedor Full Stack com experiência em Python, "
                "FastAPI, SQLAlchemy, React e construção de produtos digitais."
            ),
            version=1,
        )


class FakeEmptyResumeRepository:
    def get_by_id_and_user_id(self, resume_id: int, user_id: int):
        return None


def test_export_service_exports_resume_as_markdown():
    service = ExportService(resume_repository=FakeResumeRepository())

    content = service.export_resume_to_markdown(
        resume_id=1,
        user_id=10,
    )

    assert "# Currículo Desenvolvedor Full Stack" in content
    assert "## Cargo Alvo" in content
    assert "Desenvolvedor Full Stack" in content
    assert "## Conteúdo do Currículo" in content
    assert "FastAPI" in content
    assert "## Versão" in content
    assert "1" in content


def test_export_service_exports_resume_as_pdf():
    service = ExportService(resume_repository=FakeResumeRepository())

    content = service.export_resume_to_pdf(
        resume_id=1,
        user_id=10,
    )

    assert isinstance(content, bytes)
    assert content.startswith(b"%PDF")
    assert b"%%EOF" in content

def test_export_service_exports_resume_as_docx():
    service = ExportService(resume_repository=FakeResumeRepository())

    content = service.export_resume_to_docx(
        resume_id=1,
        user_id=10,
    )

    assert isinstance(content, bytes)
    assert content.startswith(b"PK")


def test_export_service_raises_404_when_resume_not_found():
    service = ExportService(resume_repository=FakeEmptyResumeRepository())

    with pytest.raises(HTTPException) as error:
        service.export_resume_to_markdown(
            resume_id=999,
            user_id=10,
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Currículo não encontrado."


