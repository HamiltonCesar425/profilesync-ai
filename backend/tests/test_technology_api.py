from fastapi.testclient import TestClient

from main import app
from models.profile_model import ProfileModel
from models.technology_model import TechnologyModel
from models.user_model import User
from core.security import get_password_hash, create_access_token
from database.session import SessionLocal

client = TestClient(app)


def create_test_user(db, email: str):
    user = User(
        email=email,
        hashed_password=get_password_hash("strong-password"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_profile(db, user_id: int):
    profile = ProfileModel(
        user_id=user_id,
        full_name="Technology API User",
        professional_title="Backend Developer",
        summary="Profile for technology API tests.",
        location="Campinas, SP",
        linkedin_url="https://linkedin.com/in/technology-api-user",
        github_url="https://github.com/technology-api-user",
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def auth_headers(email: str) -> dict[str, str]:
    token = create_access_token({"sub": email})
    return {"Authorization": f"Bearer {token}"}


def test_create_technology_success(reset_database):
    db = SessionLocal()

    try:
        user = create_test_user(db, "create-tech@example.com")
        profile = create_test_profile(db, user.id)

        response = client.post(
            f"/technologies/profiles/{profile.id}",
            json={
                "name": "Python",
                "category": "Language",
                "proficiency_level": "Advanced",
                "years_experience": 3,
            },
            headers=auth_headers(user.email),
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["profile_id"] == profile.id
        assert data["name"] == "Python"
        assert data["category"] == "Language"
        assert data["proficiency_level"] == "Advanced"
        assert data["years_experience"] == 3
    finally:
        db.close()


def test_list_profile_technologies_success(reset_database):
    db = SessionLocal()

    try:
        user = create_test_user(db, "list-tech@example.com")
        profile = create_test_profile(db, user.id)

        first_technology = TechnologyModel(
            profile_id=profile.id,
            name="Python",
            category="Language",
            proficiency_level="Advanced",
            years_experience=3,
        )
        second_technology = TechnologyModel(
            profile_id=profile.id,
            name="FastAPI",
            category="Framework",
            proficiency_level="Intermediate",
            years_experience=2,
        )

        db.add_all([first_technology, second_technology])
        db.commit()

        response = client.get(
            f"/technologies/profiles/{profile.id}",
            headers=auth_headers(user.email),
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["profile_id"] == profile.id
        assert data[1]["profile_id"] == profile.id
    finally:
        db.close()


def test_get_technology_success(reset_database):
    db = SessionLocal()

    try:
        user = create_test_user(db, "get-tech@example.com")
        profile = create_test_profile(db, user.id)

        technology = TechnologyModel(
            profile_id=profile.id,
            name="Docker",
            category="DevOps",
            proficiency_level="Intermediate",
            years_experience=2,
        )
        db.add(technology)
        db.commit()
        db.refresh(technology)

        response = client.get(
            f"/technologies/{technology.id}",
            headers=auth_headers(user.email),
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == technology.id
        assert data["name"] == "Docker"
    finally:
        db.close()


def test_update_technology_success(reset_database):
    db = SessionLocal()

    try:
        user = create_test_user(db, "update-tech@example.com")
        profile = create_test_profile(db, user.id)

        technology = TechnologyModel(
            profile_id=profile.id,
            name="SQL",
            category="Database",
            proficiency_level="Intermediate",
            years_experience=2,
        )
        db.add(technology)
        db.commit()
        db.refresh(technology)

        response = client.put(
            f"/technologies/{technology.id}",
            json={
                "name": "PostgreSQL",
                "proficiency_level": "Advanced",
                "years_experience": 4,
            },
            headers=auth_headers(user.email),
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == technology.id
        assert data["name"] == "PostgreSQL"
        assert data["category"] == "Database"
        assert data["proficiency_level"] == "Advanced"
        assert data["years_experience"] == 4
    finally:
        db.close()


def test_delete_technology_success(reset_database):
    db = SessionLocal()

    try:
        user = create_test_user(db, "delete-tech@example.com")
        profile = create_test_profile(db, user.id)

        technology = TechnologyModel(
            profile_id=profile.id,
            name="Git",
            category="Version Control",
            proficiency_level="Advanced",
            years_experience=5,
        )
        db.add(technology)
        db.commit()
        db.refresh(technology)

        response = client.delete(
            f"/technologies/{technology.id}",
            headers=auth_headers(user.email),
        )

        deleted_technology = (
            db.query(TechnologyModel)
            .filter(TechnologyModel.id == technology.id)
            .first()
        )

        assert response.status_code == 204
        assert deleted_technology is None
    finally:
        db.close()


def test_create_technology_without_authentication_returns_401(reset_database):
    db = SessionLocal()

    try:
        user = create_test_user(db, "unauth-tech@example.com")
        profile = create_test_profile(db, user.id)

        response = client.post(
            f"/technologies/profiles/{profile.id}",
            json={
                "name": "Python",
                "category": "Language",
                "proficiency_level": "Advanced",
                "years_experience": 3,
            },
        )

        assert response.status_code == 401
    finally:
        db.close()


def test_create_technology_for_nonexistent_profile_returns_404(reset_database):
    db = SessionLocal()

    try:
        user = create_test_user(db, "missing-profile-tech@example.com")

        response = client.post(
            "/technologies/profiles/999",
            json={
                "name": "Python",
                "category": "Language",
                "proficiency_level": "Advanced",
                "years_experience": 3,
            },
            headers=auth_headers(user.email),
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Profile not found"
    finally:
        db.close()


def test_user_cannot_access_technology_from_another_user_profile(
    reset_database,
):
    db = SessionLocal()

    try:
        owner = create_test_user(db, "owner-tech@example.com")
        intruder = create_test_user(db, "intruder-tech@example.com")
        owner_profile = create_test_profile(db, owner.id)

        technology = TechnologyModel(
            profile_id=owner_profile.id,
            name="Kubernetes",
            category="DevOps",
            proficiency_level="Intermediate",
            years_experience=1,
        )
        db.add(technology)
        db.commit()
        db.refresh(technology)

        response = client.get(
            f"/technologies/{technology.id}",
            headers=auth_headers(intruder.email),
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Technology not found"
    finally:
        db.close()
