import pytest

from domain.exceptions import DomainError
from models.profile_model import ProfileModel
from models.technology_model import TechnologyModel
from models.user_model import User
from repositories.profile_repository import ProfileRepository
from repositories.technology_repository import TechnologyRepository
from schemas.technology_schema import TechnologyCreate, TechnologyUpdate
from services.technology_service import TechnologyService


def create_test_user(db, email: str = "service-tech-user@example.com"):
    user = User(
        email=email,
        hashed_password="hashed-password",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_profile(db, user_id: int):
    profile = ProfileModel(
        user_id=user_id,
        full_name="Technology Service User",
        professional_title="Backend Developer",
        summary="Developer profile for technology service tests.",
        location="Campinas, SP",
        linkedin_url="https://linkedin.com/in/service-tech-user",
        github_url="https://github.com/service-tech-user",
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def create_service(db) -> TechnologyService:
    return TechnologyService(
        technology_repository=TechnologyRepository(db),
        profile_repository=ProfileRepository(db),
    )


def test_create_technology(reset_database):
    db = reset_database
    user = create_test_user(db)
    profile = create_test_profile(db, user.id)
    service = create_service(db)

    technology_data = TechnologyCreate(
        name="Python",
        category="Language",
        proficiency_level="Advanced",
        years_experience=3,
    )

    technology = service.create_technology(
        profile_id=profile.id,
        user_id=user.id,
        technology_data=technology_data,
    )

    assert technology.id is not None
    assert technology.profile_id == profile.id
    assert technology.name == "Python"


def test_create_technology_for_missing_profile_raises_error(reset_database):
    db = reset_database
    user = create_test_user(db)
    service = create_service(db)

    technology_data = TechnologyCreate(
        name="FastAPI",
        category="Framework",
        proficiency_level="Intermediate",
        years_experience=2,
    )

    with pytest.raises(DomainError, match="Profile not found"):
        service.create_technology(
            profile_id=999,
            user_id=user.id,
            technology_data=technology_data,
        )


def test_list_profile_technologies(reset_database):
    db = reset_database
    user = create_test_user(db)
    profile = create_test_profile(db, user.id)
    service = create_service(db)

    first_technology = TechnologyModel(
        profile_id=profile.id,
        name="Python",
        category="Language",
        proficiency_level="Advanced",
        years_experience=3,
    )
    second_technology = TechnologyModel(
        profile_id=profile.id,
        name="Docker",
        category="DevOps",
        proficiency_level="Intermediate",
        years_experience=2,
    )

    db.add_all([first_technology, second_technology])
    db.commit()

    technologies = service.list_profile_technologies(
        profile_id=profile.id,
        user_id=user.id,
    )

    assert len(technologies) == 2
    assert technologies[0].profile_id == profile.id
    assert technologies[1].profile_id == profile.id


def test_list_profile_technologies_for_missing_profile_raises_error(
    reset_database,
):
    db = reset_database
    user = create_test_user(db)
    service = create_service(db)

    with pytest.raises(DomainError, match="Profile not found"):
        service.list_profile_technologies(
            profile_id=999,
            user_id=user.id,
        )


def test_get_technology(reset_database):
    db = reset_database
    user = create_test_user(db)
    profile = create_test_profile(db, user.id)
    service = create_service(db)

    technology = TechnologyModel(
        profile_id=profile.id,
        name="PostgreSQL",
        category="Database",
        proficiency_level="Advanced",
        years_experience=4,
    )
    db.add(technology)
    db.commit()
    db.refresh(technology)

    found_technology = service.get_technology(
        technology_id=technology.id,
        user_id=user.id,
    )

    assert found_technology.id == technology.id
    assert found_technology.name == "PostgreSQL"


def test_get_missing_technology_raises_error(reset_database):
    db = reset_database
    user = create_test_user(db)
    service = create_service(db)

    with pytest.raises(DomainError, match="Technology not found"):
        service.get_technology(
            technology_id=999,
            user_id=user.id,
        )


def test_user_cannot_access_technology_from_another_user(reset_database):
    db = reset_database

    owner = create_test_user(db, email="owner@example.com")
    intruder = create_test_user(db, email="intruder@example.com")
    owner_profile = create_test_profile(db, owner.id)
    service = create_service(db)

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

    with pytest.raises(DomainError, match="Technology not found"):
        service.get_technology(
            technology_id=technology.id,
            user_id=intruder.id,
        )


def test_update_technology(reset_database):
    db = reset_database
    user = create_test_user(db)
    profile = create_test_profile(db, user.id)
    service = create_service(db)

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

    update_data = TechnologyUpdate(
        name="PostgreSQL",
        proficiency_level="Advanced",
        years_experience=4,
    )

    updated_technology = service.update_technology(
        technology_id=technology.id,
        user_id=user.id,
        technology_data=update_data,
    )

    assert updated_technology.id == technology.id
    assert updated_technology.name == "PostgreSQL"
    assert updated_technology.category == "Database"
    assert updated_technology.proficiency_level == "Advanced"
    assert updated_technology.years_experience == 4


def test_delete_technology(reset_database):
    db = reset_database
    user = create_test_user(db)
    profile = create_test_profile(db, user.id)
    service = create_service(db)

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

    service.delete_technology(
        technology_id=technology.id,
        user_id=user.id,
    )

    deleted_technology = (
        db.query(TechnologyModel).filter(TechnologyModel.id == technology.id).first()
    )

    assert deleted_technology is None
