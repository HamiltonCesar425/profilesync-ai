from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_register_user() -> None:
    response = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "password": "strong-password",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "user@example.com"
    assert "id" in data


def test_register_existing_user() -> None:
    payload = {
        "email": "duplicate@example.com",
        "password": "strong-password",
    }

    client.post("/auth/register", json=payload)

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400


def test_login_user() -> None:
    payload = {
        "email": "login@example.com",
        "password": "strong-password",
    }

    client.post("/auth/register", json=payload)

    response = client.post(
        "/auth/login",
        data={"username": payload["email"], "password": payload["password"]},
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_invalid_password() -> None:
    payload = {
        "email": "invalid@example.com",
        "password": "strong-password",
    }

    client.post("/auth/register", json=payload)

    response = client.post(
        "/auth/login",
        data={
            "username": "invalid@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_login_with_invalid_email() -> None:
    response = client.post(
        "/auth/login",
        data={
            "username": "missing@example.com",
            "password": "strong-password",
        },
    )

    assert response.status_code == 401
