from fastapi.testclient import TestClient

from app.dependencies import get_db
from core.auth import get_current_user
from main import app


class FakeATSValidationService:
    def __init__(self, repository):
        pass

    def validate_resume(self, resume_id: int, user_id: int):
        return {
            "resume_id": resume_id,
            "score": 100,
            "status": "excellent",
            "passed": True,
            "issues": [],
            "suggestions": [],
        }


class FakeUser:
    id = 1


def override_get_db():
    yield None


def override_get_current_user():
    return FakeUser()


def test_validate_resume_ats_success(monkeypatch):
    from api.v1 import ats_routes

    monkeypatch.setattr(
        ats_routes,
        "ATSValidationService",
        FakeATSValidationService,
    )

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        client = TestClient(app)
        response = client.get("/ats/resumes/1/validate")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["resume_id"] == 1
    assert data["score"] == 100
    assert data["status"] == "excellent"
    assert data["passed"] is True
    assert data["issues"] == []
    assert data["suggestions"] == []


def test_validate_resume_requires_authentication():
    client = TestClient(app)

    response = client.get("/ats/resumes/1/validate")

    assert response.status_code == 401
