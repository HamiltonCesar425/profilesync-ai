from fastapi.testclient import TestClient
import pytest

from app.dependencies import get_db
from core.security import create_access_token
from main import app
from models.profile_model import ProfileModel
from models.user_model import User

client = TestClient(app)


@pytest.fixture
def db_session(reset_database):
    return reset_database


def override_get_db(db_session):
    def _override_get_db():
        yield db_session

    return {get_db: _override_get_db}


def create_user(db_session, email="user@example.com"):
    user = User(
        email=email,
        hashed_password="hashed-password",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def create_profile(db_session, user_id: int):
    profile = ProfileModel(
        user_id=user_id,
        full_name="Maria Aparecida",
        professional_title="Desenvolvedor Backend",
        summary="Perfil profissional de teste.",
        location="CityTest, SP",
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)
    return profile


def auth_headers(email="user@example.com"):
    token = create_access_token({"sub": email})
    return {"Authorization": f"Bearer {token}"}


def test_create_project_success(db_session):
    app.dependency_overrides.update(override_get_db(db_session))

    try:
        user = create_user(db_session)
        profile = create_profile(db_session, user.id)
        headers = auth_headers(user.email)

        payload = {
            "profile_id": profile.id,
            "name": "ProfileSync AI",
            "description": "Sistema de gestão de perfil profissional.",
            "repository_url": "https://github.com/example/profilesync-ai",
            "demo_url": "https://profilesync.example.com",
            "start_date": "2026-06-01",
            "end_date": None,
        }

        response = client.post(
            "/projects",
            json=payload,
            headers=headers,
        )

        assert response.status_code == 201

        data = response.json()

        assert data["id"] is not None
        assert data["profile_id"] == profile.id
        assert data["name"] == payload["name"]
        assert data["demo_url"] == "https://profilesync.example.com/"
    finally:
        app.dependency_overrides.clear()


def test_create_project_requires_authentication(db_session):
    app.dependency_overrides.update(override_get_db(db_session))

    try:
        payload = {
            "profile_id": 1,
            "name": "Projeto sem autenticação",
            "description": "Deve falhar.",
            "repository_url": None,
            "demo_url": None,
            "start_date": None,
            "end_date": None,
        }

        response = client.post("/projects", json=payload)

        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()


def test_create_project_rejects_profile_from_another_user(db_session):
    app.dependency_overrides.update(override_get_db(db_session))

    try:
        owner = create_user(db_session, "owner@example.com")
        intruder = create_user(db_session, "intruder@example.com")
        profile = create_profile(db_session, owner.id)
        headers = auth_headers(intruder.email)

        payload = {
            "profile_id": profile.id,
            "name": "Projeto indevido",
            "description": "Tentativa de usar perfil de outro usuário.",
            "repository_url": None,
            "demo_url": None,
            "start_date": None,
            "end_date": None,
        }

        response = client.post(
            "/projects",
            json=payload,
            headers=headers,
        )

        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()


def test_list_projects_by_profile_success(db_session):
    app.dependency_overrides.update(override_get_db(db_session))

    try:
        user = create_user(db_session)
        profile = create_profile(db_session, user.id)
        headers = auth_headers(user.email)

        payload = {
            "profile_id": profile.id,
            "name": "ProfileSync AI",
            "description": "Sistema de gestão de perfil profissional.",
            "repository_url": None,
            "demo_url": None,
            "start_date": None,
            "end_date": None,
        }

        client.post("/projects", json=payload, headers=headers)

        response = client.get(
            f"/projects/profile/{profile.id}",
            headers=headers,
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["profile_id"] == profile.id
        assert data[0]["name"] == payload["name"]
    finally:
        app.dependency_overrides.clear()


def test_get_project_success(db_session):
    app.dependency_overrides.update(override_get_db(db_session))

    try:
        user = create_user(db_session)
        profile = create_profile(db_session, user.id)
        headers = auth_headers(user.email)

        create_response = client.post(
            "/projects",
            json={
                "profile_id": profile.id,
                "name": "ProfileSync AI",
                "description": "Sistema de gestão de perfil profissional.",
                "repository_url": None,
                "demo_url": None,
                "start_date": None,
                "end_date": None,
            },
            headers=headers,
        )

        project_id = create_response.json()["id"]

        response = client.get(
            f"/projects/{project_id}/profile/{profile.id}",
            headers=headers,
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == project_id
        assert data["profile_id"] == profile.id
    finally:
        app.dependency_overrides.clear()


def test_get_project_rejects_other_user(db_session):
    app.dependency_overrides.update(override_get_db(db_session))

    try:
        owner = create_user(db_session, "owner@example.com")
        intruder = create_user(db_session, "intruder@example.com")
        profile = create_profile(db_session, owner.id)

        owner_headers = auth_headers(owner.email)
        intruder_headers = auth_headers(intruder.email)

        create_response = client.post(
            "/projects",
            json={
                "profile_id": profile.id,
                "name": "Projeto protegido",
                "description": "Projeto de outro usuário.",
                "repository_url": None,
                "demo_url": None,
                "start_date": None,
                "end_date": None,
            },
            headers=owner_headers,
        )

        project_id = create_response.json()["id"]

        response = client.get(
            f"/projects/{project_id}/profile/{profile.id}",
            headers=intruder_headers,
        )

        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()


def test_update_project_success(db_session):
    app.dependency_overrides.update(override_get_db(db_session))

    try:
        user = create_user(db_session)
        profile = create_profile(db_session, user.id)
        headers = auth_headers(user.email)

        create_response = client.post(
            "/projects",
            json={
                "profile_id": profile.id,
                "name": "ProfileSync AI",
                "description": "Descrição inicial.",
                "repository_url": None,
                "demo_url": None,
                "start_date": None,
                "end_date": None,
            },
            headers=headers,
        )

        project_id = create_response.json()["id"]

        response = client.put(
            f"/projects/{project_id}/profile/{profile.id}",
            json={
                "name": "ProfileSync AI Atualizado",
                "description": "Descrição atualizada.",
                "repository_url": "https://github.com/example/updated",
                "demo_url": None,
                "start_date": "2026-06-10",
                "end_date": None,
            },
            headers=headers,
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == project_id
        assert data["name"] == "ProfileSync AI Atualizado"
        assert data["repository_url"] == "https://github.com/example/updated"
    finally:
        app.dependency_overrides.clear()


def test_delete_project_success(db_session):
    app.dependency_overrides.update(override_get_db(db_session))

    try:
        user = create_user(db_session)
        profile = create_profile(db_session, user.id)
        headers = auth_headers(user.email)

        create_response = client.post(
            "/projects",
            json={
                "profile_id": profile.id,
                "name": "Projeto removível",
                "description": "Será removido.",
                "repository_url": None,
                "demo_url": None,
                "start_date": None,
                "end_date": None,
            },
            headers=headers,
        )

        project_id = create_response.json()["id"]

        response = client.delete(
            f"/projects/{project_id}/profile/{profile.id}",
            headers=headers,
        )

        assert response.status_code == 204

        get_response = client.get(
            f"/projects/{project_id}/profile/{profile.id}",
            headers=headers,
        )

        assert get_response.status_code == 404
    finally:
        app.dependency_overrides.clear()
