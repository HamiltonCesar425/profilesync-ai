from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_profile_intelligence_requires_authentication():
    response = client.post(
        "/profile-intelligence/analyze",
        params={
            "profile_id": 1,
            "target_role": "Python Developer",
        },
    )

    assert response.status_code == 401


def test_profile_intelligence_returns_diagnosis(reset_database):
    register_response = client.post(
        "/auth/register",
        json={
            "email": "profile.intelligence@example.com",
            "password": "strong-password",
            "full_name": "Profile Intelligence User",
        },
    )

    assert register_response.status_code == 201, register_response.json()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "profile.intelligence@example.com",
            "password": "strong-password",
        },
    )

    assert login_response.status_code == 200, login_response.json()

    token = login_response.json()["access_token"]

    profile_response = client.post(
        "/profiles",
        json={
            "full_name": "Profile Intelligence User",
            "professional_title": "Python Developer",
            "summary": "Backend developer focused on APIs.",
            "location": "Campinas, SP",
            "linkedin_url": None,
            "github_url": None,
            "portfolio_url": None,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert profile_response.status_code == 200, profile_response.json()

    profile_id = profile_response.json()["id"]

    response = client.post(
        "/profile-intelligence/analyze",
        params={
            "profile_id": profile_id,
            "target_role": "Python Developer",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["score"] == 20
    assert data["strengths"] == []
    assert data["improvements"]
    assert data["recommendations"]
