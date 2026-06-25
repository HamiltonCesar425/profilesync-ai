from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.dependencies import get_db
from core.auth import get_current_user
from main import app
from services.export_service import ExportService

client = TestClient(app)


def override_get_db():
    yield SimpleNamespace()


def override_get_current_user():
    return SimpleNamespace(id=10)


def test_export_resume_markdown_route(monkeypatch):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    try:

        def fake_export_resume_to_markdown(self, resume_id: int, user_id: int):
            assert resume_id == 1
            assert user_id == 10
            return "# Currículo Desenvolvedor Full Stack"

        monkeypatch.setattr(
            ExportService,
            "export_resume_to_markdown",
            fake_export_resume_to_markdown,
        )

        response = client.get("/exports/resumes/1/markdown")

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/markdown")
        assert response.headers["content-disposition"] == (
            'attachment; filename="resume-1.md"'
        )
        assert "# Currículo Desenvolvedor Full Stack" in response.text
    finally:
        app.dependency_overrides.clear()


def test_export_resume_pdf_route(monkeypatch):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    try:

        def fake_export_resume_to_pdf(self, resume_id: int, user_id: int):
            assert resume_id == 1
            assert user_id == 10
            return b"%PDF-1.4\nfake pdf content\n%%EOF"

        monkeypatch.setattr(
            ExportService,
            "export_resume_to_pdf",
            fake_export_resume_to_pdf,
        )

        response = client.get("/exports/resumes/1/pdf")

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("application/pdf")
        assert response.headers["content-disposition"] == (
            'attachment; filename="resume-1.pdf"'
        )
        assert response.content.startswith(b"%PDF")
        assert b"%%EOF" in response.content
    finally:
        app.dependency_overrides.clear()


def test_export_resume_docx_route(monkeypatch):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    try:

        def fake_export_resume_to_docx(self, resume_id: int, user_id: int):
            assert resume_id == 1
            assert user_id == 10
            return b"PK\x03\x04fake docx content"

        monkeypatch.setattr(
            ExportService,
            "export_resume_to_docx",
            fake_export_resume_to_docx,
        )

        response = client.get("/exports/resumes/1/docx")

        expected_content_type = (
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )

        assert response.status_code == 200
        assert response.headers["content-type"].startswith(expected_content_type)
        assert response.headers["content-disposition"] == (
            'attachment; filename="resume-1.docx"'
        )
        assert response.content.startswith(b"PK")
    finally:
        app.dependency_overrides.clear()
