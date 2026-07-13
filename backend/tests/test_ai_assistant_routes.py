from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.v1.ai_assistant_routes import get_ai_assistant_service, router
from core.auth import get_current_user

app = FastAPI()
app.include_router(router)

client = TestClient(app)

ENDPOINT = "/ai-assistant/improve-professional-description"


def override_get_current_user():
    return object()


class FakeAIAssistantService:
    def improve_professional_description(self, text: str):
        return SimpleNamespace(
            original_text=text,
            improved_text=("Desenvolvedor Python com experiência em APIs REST."),
        )


def override_get_ai_assistant_service():
    return FakeAIAssistantService()


def test_improve_professional_description_authenticated():

    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_ai_assistant_service] = (
        override_get_ai_assistant_service
    )

    response = client.post(
        ENDPOINT,
        json={
            "text": "desenvolvedor python com experiencia em api",
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "original_text": ("desenvolvedor python com experiencia em api"),
        "improved_text": ("Desenvolvedor Python com experiência em APIs REST."),
    }


def test_improve_professional_description_requires_authentication():
    app.dependency_overrides.clear()

    response = client.post(
        ENDPOINT,
        json={
            "text": "Desenvolvedor Python.",
        },
    )

    assert response.status_code == 401


def test_improve_professional_description_rejects_empty_text():
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_ai_assistant_service] = (
        override_get_ai_assistant_service
    )

    response = client.post(
        ENDPOINT,
        json={
            "text": "",
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 422
