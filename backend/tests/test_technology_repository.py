from models.profile_model import ProfileModel
from models.technology_model import TechnologyModel
from models.user_model import User
from repositories.technology_repository import TechnologyRepository
from schemas.technology_schema import TechnologyCreate, TechnologyUpdate


def create_test_user(db):
    user = User(
        email="tech-user@example.com",
        hashed_password="hashed-password",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_profile(db, user_id: int):
    profile = ProfileModel(
        user_id=user_id,
        full_name="Technology User",
        professional_title="Backend Developer",
        summary="Developer profile for technology repository tests.",
        location="Campinas, SP",
        linkedin_url="https://linkedin.com/in/tech-user",
        github_url="https://github.com/tech-user",
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def test_create_technology(reset_database):
    db = reset_database
    user = create_test_user(db)
    profile = create_test_profile(db, user.id)
    repository = TechnologyRepository(db)

    technology_data = TechnologyCreate(
        name="Python",
        category="Language",
        proficiency_level="Advanced",
        years_experience=3,
    )

    technology = repository.create(
        profile_id=profile.id,
        technology_data=technology_data,
    )

    assert technology.id is not None
    assert technology.profile_id == profile.id
    assert technology.name == "Python"
    assert technology.category == "Language"
    assert technology.proficiency_level == "Advanced"
    assert technology.years_experience == 3


def test_list_by_profile_id(reset_database):
    db = reset_database
    user = create_test_user(db)
    profile = create_test_profile(db, user.id)
    repository = TechnologyRepository(db)

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

    reset_database.add_all([first_technology, second_technology])
    reset_database.commit()

    technologies = repository.list_by_profile_id(profile.id)

    assert len(technologies) == 2
    assert technologies[0].profile_id == profile.id
    assert technologies[1].profile_id == profile.id


def test_get_by_id_existing_technology(reset_database):
    db = reset_database
    user = create_test_user(reset_database)
    profile = create_test_profile(db, user.id)
    repository = TechnologyRepository(db)

    technology = TechnologyModel(
        profile_id=profile.id,
        name="Docker",
        category="DevOps",
        proficiency_level="Intermediate",
        years_experience=2,
    )
    reset_database.add(technology)
    reset_database.commit()
    reset_database.refresh(technology)

    found_technology = repository.get_by_id(technology.id)

    assert found_technology is not None
    assert found_technology.id == technology.id
    assert found_technology.name == "Docker"


def test_get_by_id_non_existing_technology(reset_database):
    repository = TechnologyRepository(reset_database)

    technology = repository.get_by_id(999)

    assert technology is None


def test_update_existing_technology(reset_database):
    db = reset_database
    user = create_test_user(db)
    profile = create_test_profile(db, user.id)
    repository = TechnologyRepository(db)

    technology = TechnologyModel(
        profile_id=profile.id,
        name="SQL",
        category="Database",
        proficiency_level="Intermediate",
        years_experience=2,
    )
    reset_database.add(technology)
    reset_database.commit()
    reset_database.refresh(technology)

    update_data = TechnologyUpdate(
        name="PostgreSQL",
        proficiency_level="Advanced",
        years_experience=4,
    )

    updated_technology = repository.update(
        technology=technology,
        technology_data=update_data,
    )

    assert updated_technology.id == technology.id
    assert updated_technology.name == "PostgreSQL"
    assert updated_technology.category == "Database"
    assert updated_technology.proficiency_level == "Advanced"
    assert updated_technology.years_experience == 4


def test_delete_existing_technology(reset_database):
    db = reset_database
    user = create_test_user(db)
    profile = create_test_profile(db, user.id)
    repository = TechnologyRepository(db)

    technology = TechnologyModel(
        profile_id=profile.id,
        name="Git",
        category="Version Control",
        proficiency_level="Advanced",
        years_experience=5,
    )
    reset_database.add(technology)
    reset_database.commit()
    reset_database.refresh(technology)

    repository.delete(technology)

    deleted_technology = repository.get_by_id(technology.id)

    assert deleted_technology is None
