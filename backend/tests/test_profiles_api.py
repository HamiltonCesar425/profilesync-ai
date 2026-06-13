from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "ProfileSync AI API is running"}


def test_create_profile() -> None:
    payload = {
        "full_name": "Hamilton Cesar",
        "professional_title": "Python Developer",
        "summary": "Professional profile",
        "location": "Campinas",
        "linkedin_url": "https://linkedin.com/in/hamilton",
        "github_url": "https://github.com/HamiltonCesar425",
    }

    response = client.post(
        "/profiles",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["full_name"] == payload["full_name"]
    assert data["professional_title"] == payload["professional_title"]


def test_list_profiles() -> None:
    response = client.get("/profiles")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_profile_by_id() -> None:
    payload = {
        "full_name": "Profile Test",
        "professional_title": "Backend Developer",
        "summary": "Testing profile summary",
    }

    create_response = client.post(
        "/profiles",
        json=payload,
    )

    profile_id = create_response.json()["id"]

    response = client.get(f"/profiles/{profile_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == profile_id
    assert data["full_name"] == "Profile Test"


def test_get_profile_by_id_not_found() -> None:
    response = client.get("/profiles/999999")

    assert response.status_code == 404
    assert response.json() == {
        "error": "profile_not_found",
        "message": "Profile with id 999999 not found",
    }
