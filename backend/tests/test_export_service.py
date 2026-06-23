from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from schemas.export_schema import ExportFormat
from services.export_service import ExportService


class FakeResumeRepository:
    def get_by_id_and_user_id(self, resume_id: int, user_id: int):
        assert resume_id == 1
        assert user_id == 10

        return SimpleNamespace(
            title="Currículo Desenvolvedor Full Stack",
            target_role="Desenvolvedor Full Stack",
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

    content = service.export_resume(
        resume_id=1,
        user_id=10,
        export_format=ExportFormat.MARKDOWN,
    )

    assert "# Currículo Desenvolvedor Full Stack" in content
    assert "## Cargo Alvo" in content
    assert "Desenvolvedor Full Stack" in content
    assert "## Conteúdo do Currículo" in content
    assert "FastAPI" in content
    assert "## Versão" in content
    assert "1" in content


def test_export_service_rejects_unsupported_format():
    service = ExportService(resume_repository=FakeResumeRepository())

    with pytest.raises(HTTPException) as error:
        service.export_resume(
            resume_id=1,
            user_id=10,
            export_format=ExportFormat.PDF,
        )

    assert error.value.status_code == 400
    assert error.value.detail == "Formato de exportação não suportado."


def test_export_service_raises_404_when_resume_not_found():
    service = ExportService(resume_repository=FakeEmptyResumeRepository())

    with pytest.raises(HTTPException) as error:
        service.export_resume(
            resume_id=999,
            user_id=10,
            export_format=ExportFormat.MARKDOWN,
        )

    assert error.value.status_code == 404
    assert error.value.detail == "Currículo não encontrado."
