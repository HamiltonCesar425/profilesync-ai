from uuid import uuid4

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def create_auth_headers() -> dict[str, str]:
    email = f"resume-{uuid4()}@example.com"
    password = "strong-password"

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Resume Test User",
        },
    )

    assert register_response.status_code in (200, 201), register_response.json()

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200, login_response.json()

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def create_profile(headers: dict[str, str]) -> int:
    response = client.post(
        "/profiles",
        headers=headers,
        json={
            "full_name": "Hamilton Cesar",
            "professional_title": "Desenvolvedor Full Stack",
            "summary": "Perfil técnico para testes automatizados.",
            "location": "Campinas, SP",
            "linkedin_url": "https://linkedin.com/in/test",
            "github_url": "https://github.com/test",
            "portfolio_url": "https://portfolio.test",
            "skills": "Python, FastAPI, SQLAlchemy",
        },
    )

    assert response.status_code in (200, 201)
    return response.json()["id"]


def create_resume(headers: dict[str, str], profile_id: int) -> dict:
    response = client.post(
        "/resumes",
        headers=headers,
        json={
            "profile_id": profile_id,
            "title": "Currículo Backend Python",
            "target_role": "Desenvolvedor Backend Python",
            "summary": "Currículo focado em APIs, testes e banco de dados.",
            "content": "Experiência com FastAPI, SQLAlchemy e pytest.",
        },
    )

    assert response.status_code == 201
    return response.json()


def test_create_resume_success() -> None:
    headers = create_auth_headers()
    profile_id = create_profile(headers)

    response = client.post(
        "/resumes",
        headers=headers,
        json={
            "profile_id": profile_id,
            "title": "Currículo Full Stack",
            "target_role": "Desenvolvedor Full Stack",
            "summary": "Resumo profissional para currículo.",
            "content": "Conteúdo do currículo.",
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["id"] is not None
    assert data["profile_id"] == profile_id
    assert data["title"] == "Currículo Full Stack"


def test_list_resumes_by_profile_success() -> None:
    headers = create_auth_headers()
    profile_id = create_profile(headers)
    create_resume(headers, profile_id)

    response = client.get(
        f"/resumes/profile/{profile_id}",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data) >= 1
    assert data[0]["profile_id"] == profile_id


def test_get_resume_success() -> None:
    headers = create_auth_headers()
    profile_id = create_profile(headers)
    resume = create_resume(headers, profile_id)

    response = client.get(
        f"/resumes/{resume['id']}/profile/{profile_id}",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == resume["id"]
    assert data["profile_id"] == profile_id


def test_update_resume_success() -> None:
    headers = create_auth_headers()
    profile_id = create_profile(headers)
    resume = create_resume(headers, profile_id)

    response = client.put(
        f"/resumes/{resume['id']}/profile/{profile_id}",
        headers=headers,
        json={
            "title": "Currículo Backend Atualizado",
            "target_role": "Backend Engineer",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == resume["id"]
    assert data["title"] == "Currículo Backend Atualizado"
    assert data["target_role"] == "Backend Engineer"


def test_delete_resume_success() -> None:
    headers = create_auth_headers()
    profile_id = create_profile(headers)
    resume = create_resume(headers, profile_id)

    response = client.delete(
        f"/resumes/{resume['id']}/profile/{profile_id}",
        headers=headers,
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/resumes/{resume['id']}/profile/{profile_id}",
        headers=headers,
    )

    assert get_response.status_code == 404


def test_create_resume_without_authentication_returns_401() -> None:
    response = client.post(
        "/resumes",
        json={
            "profile_id": 1,
            "title": "Currículo sem autenticação",
            "target_role": "Backend",
            "summary": "Resumo",
            "content": "Conteúdo válido.",
        },
    )

    assert response.status_code == 401


def test_create_resume_for_nonexistent_profile_returns_404() -> None:
    headers = create_auth_headers()

    response = client.post(
        "/resumes",
        headers=headers,
        json={
            "profile_id": 999999,
            "title": "Currículo inválido",
            "target_role": "Backend",
            "summary": "Resumo",
            "content": "Conteúdo válido.",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"


def test_user_cannot_access_resume_from_another_user_profile() -> None:
    owner_headers = create_auth_headers()
    intruder_headers = create_auth_headers()

    owner_profile_id = create_profile(owner_headers)
    owner_resume = create_resume(owner_headers, owner_profile_id)

    response = client.get(
        f"/resumes/{owner_resume['id']}/profile/{owner_profile_id}",
        headers=intruder_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Profile not found"
