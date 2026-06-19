from fastapi.testclient import TestClient
from jose import jwt

from core.security import ALGORITHM, SECRET_KEY
from main import app

client = TestClient(app)


def get_auth_headers() -> dict[str, str]:
    payload = {
        "email": "authorization-test@example.com",
        "password": "strong-password",
    }

    client.post("/auth/register", json=payload)

    response = client.post("/auth/login", json=payload)
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_profiles_requires_authentication() -> None:
    response = client.get("/profiles")

    assert response.status_code == 401


def test_profiles_rejects_invalid_token() -> None:
    response = client.get(
        "/profiles",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401


def test_profiles_accepts_valid_token() -> None:
    response = client.get(
        "/profiles",
        headers=get_auth_headers(),
    )

    assert response.status_code == 200


def test_profiles_rejects_token_without_subject() -> None:
    token = jwt.encode(
        {"invalid": "payload"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    response = client.get(
        "/profiles",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_profiles_rejects_token_for_missing_user() -> None:
    token = jwt.encode(
        {"sub": "missing-user@example.com"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    response = client.get(
        "/profiles",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
