from fastapi.testclient import TestClient

from core.security import create_access_token

from main import app

client = TestClient(app)


def test_analyze_career_goal_authenticated(auth_headers):
    payload = {
        "target_role": "Backend Python",
        "skills": ["Python", "FastAPI", "SQL"],
    }

    response = client.post(
        "/career-intelligence/analyze",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["target_role"] == "Backend Python"
    assert data["compatibility_score"] == 60
    assert "python" in data["strengths"]
    assert "fastapi" in data["strengths"]
    assert "sql" in data["strengths"]
    assert "docker" in data["gaps"]
    assert "tests" in data["gaps"]
    assert "recommendations" in data


def test_analyze_career_goal_requires_authentication():
    payload = {
        "target_role": "Backend Python",
        "skills": ["Python", "FastAPI", "SQL"],
    }

    response = client.post(
        "/career-intelligence/analyze",
        json=payload,
    )

    assert response.status_code == 401


def test_analyze_registered_job_authenticated(auth_headers):
    job_payload = {
        "title": "Backend Python Developer",
        "description": (
            "Vaga para pessoa desenvolvedora backend com Python, "
            "FastAPI, SQL, Docker e testes automatizados."
        ),
        "company": "ProfileSync Test Company",
        "location": "Remote",
        "url": "https://example.com/jobs/backend-python",
    }

    create_job_response = client.post(
        "/jobs",
        json=job_payload,
        headers=auth_headers,
    )

    assert create_job_response.status_code == 201

    job_id = create_job_response.json()["id"]

    analysis_payload = {
        "target_role": "Backend Python Developer",
        "description": job_payload["description"],
        "skills": ["Python", "FastAPI", "SQL"],
    }

    response = client.post(
        f"/career-intelligence/jobs/{job_id}/analyze",
        json=analysis_payload,
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["compatibility_score"] > 0
    assert "python" in data["strengths"]
    assert "fastapi" in data["strengths"]
    assert "sql" in data["strengths"]
    assert "docker" in data["gaps"]
    assert "tests" in data["gaps"]
    assert "recommendations" in data


def test_analyze_registered_job_requires_authentication():
    response = client.post(
        "/career-intelligence/jobs/1/analyze",
        json={
            "target_role": "Backend Python Developer",
            "description": (
                "Vaga para pessoa desenvolvedora backend com Python, "
                "FastAPI, SQL, Docker e testes automatizados."
            ),
            "skills": ["Python", "FastAPI", "SQL"],
        },
    )

    assert response.status_code == 401


def test_user_cannot_analyze_job_from_another_user(auth_headers, other_user):
    other_user_headers = {
        "Authorization": f"Bearer {create_access_token(data={'sub': other_user.email})}"
    }

    job_payload = {
        "title": "Backend Python Developer",
        "description": "Python FastAPI SQL Docker tests",
        "company": "Other Company",
    }

    create_response = client.post(
        "/jobs",
        json=job_payload,
        headers=other_user_headers,
    )

    assert create_response.status_code == 201

    job_id = create_response.json()["id"]

    response = client.post(
        f"/career-intelligence/jobs/{job_id}/analyze",
        json={
            "target_role": "Backend Python Developer",
            "skills": ["Python", "FastAPI"],
        },
        headers=auth_headers,
    )

    assert response.status_code == 404
