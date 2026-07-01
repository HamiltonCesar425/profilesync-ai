from datetime import date

from fastapi.testclient import TestClient

from main import app
from models.profile_model import ProfileModel
from models.user_model import User
from core.security import create_access_token, get_password_hash

client = TestClient(app)


def create_user(db_session, email: str = "user@example.com") -> User:
    user = User(
        email=email,
        hashed_password=get_password_hash("strong-password"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def create_profile(db_session, user_id: int) -> ProfileModel:
    profile = ProfileModel(
        full_name="TestUser",
        professional_title="Desenvolvedor Full Stack",
        summary="Resumo profissional.",
        location="CityTest , SP",
        linkedin_url=None,
        github_url=None,
        user_id=user_id,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)
    return profile


def auth_headers(user: User) -> dict[str, str]:
    token = create_access_token(data={"sub": user.email})
    return {"Authorization": f"Bearer {token}"}


def make_payload() -> dict:
    return {
        "company_name": "Empresa Teste",
        "position": "Desenvolvedor Python",
        "employment_type": "PJ",
        "work_model": "Remoto",
        "location": "Campinas, SP",
        "description": "Desenvolvimento de APIs e pipelines de dados.",
        "start_date": str(date(2024, 1, 1)),
        "end_date": None,
        "is_current": True,
    }


def test_create_professional_experience_success(reset_database):
    db_session = reset_database
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)

    response = client.post(
        f"/profiles/{profile.id}/experiences",
        json=make_payload(),
        headers=auth_headers(user),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["profile_id"] == profile.id
    assert data["company_name"] == "Empresa Teste"
    assert data["position"] == "Desenvolvedor Python"


def test_create_professional_experience_requires_authentication(reset_database):
    db_session = reset_database
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)

    response = client.post(
        f"/profiles/{profile.id}/experiences",
        json=make_payload(),
    )

    assert response.status_code == 401


def test_create_professional_experience_rejects_other_user_profile(
    reset_database,
):
    db_session = reset_database
    owner = create_user(db_session, email="owner@example.com")
    other_user = create_user(db_session, email="other@example.com")
    profile = create_profile(db_session, owner.id)

    response = client.post(
        f"/profiles/{profile.id}/experiences",
        json=make_payload(),
        headers=auth_headers(other_user),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Perfil não encontrado."


def test_list_professional_experiences_success(reset_database):
    db_session = reset_database
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)

    client.post(
        f"/profiles/{profile.id}/experiences",
        json=make_payload(),
        headers=auth_headers(user),
    )

    response = client.get(
        f"/profiles/{profile.id}/experiences",
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["company_name"] == "Empresa Teste"


def test_get_professional_experience_success(reset_database):
    db_session = reset_database
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)

    create_response = client.post(
        f"/profiles/{profile.id}/experiences",
        json=make_payload(),
        headers=auth_headers(user),
    )
    experience_id = create_response.json()["id"]

    response = client.get(
        f"/profiles/{profile.id}/experiences/{experience_id}",
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    assert response.json()["id"] == experience_id


def test_update_professional_experience_success(reset_database):
    db_session = reset_database
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)

    create_response = client.post(
        f"/profiles/{profile.id}/experiences",
        json=make_payload(),
        headers=auth_headers(user),
    )
    experience_id = create_response.json()["id"]

    update_payload = {
        "company_name": "Empresa Atualizada",
        "position": "Engenheiro de Software",
        "employment_type": "CLT",
        "work_model": "Híbrido",
        "location": "São Paulo, SP",
        "description": "Atuação em backend e dados.",
        "start_date": "2024-02-01",
        "end_date": "2025-02-01",
        "is_current": False,
    }

    response = client.put(
        f"/profiles/{profile.id}/experiences/{experience_id}",
        json=update_payload,
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "Empresa Atualizada"
    assert data["position"] == "Engenheiro de Software"
    assert data["is_current"] is False


def test_delete_professional_experience_success(reset_database):
    db_session = reset_database
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)

    create_response = client.post(
        f"/profiles/{profile.id}/experiences",
        json=make_payload(),
        headers=auth_headers(user),
    )
    experience_id = create_response.json()["id"]

    response = client.delete(
        f"/profiles/{profile.id}/experiences/{experience_id}",
        headers=auth_headers(user),
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/profiles/{profile.id}/experiences/{experience_id}",
        headers=auth_headers(user),
    )

    assert get_response.status_code == 404
