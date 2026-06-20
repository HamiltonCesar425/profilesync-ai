import pytest

from database import Base, engine, SessionLocal
from repositories.profile_repository import ProfileRepository


TEST_USER_ID = 1


def setup_function() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def profile_repository():
    db = SessionLocal()
    try:
        yield ProfileRepository(db)
    finally:
        db.close()


def test_create_profile() -> None:
    db = SessionLocal()
    repository = ProfileRepository(db)

    profile = repository.create(
        user_id=TEST_USER_ID,
        full_name="Test User",
        professional_title="Software Developer",
        summary="Sample professional profile.",
        location="Test City",
        linkedin_url="https://linkedin.com/in/test-user",
        github_url="https://github.com/test-user",
    )

    assert profile.id is not None
    assert profile.full_name == "Test User"
    assert profile.professional_title == "Software Developer"
    assert profile.summary == "Sample professional profile."
    assert profile.location == "Test City"
    assert profile.linkedin_url == "https://linkedin.com/in/test-user"
    assert profile.github_url == "https://github.com/test-user"

    db.close()


def test_list_all_profiles() -> None:
    db = SessionLocal()
    repository = ProfileRepository(db)

    repository.create(
        user_id=TEST_USER_ID,
        full_name="Test User",
        professional_title="Software Developer",
        summary="Sample professional profile.",
    )

    repository.create(
        user_id=TEST_USER_ID,
        full_name="Sample User",
        professional_title="Data Analyst",
        summary="Another sample professional profile.",
    )

    profiles = repository.list_by_user_id(TEST_USER_ID)

    assert len(profiles) == 2
    assert profiles[0].full_name == "Test User"
    assert profiles[1].full_name == "Sample User"

    db.close()


def test_get_by_id_existing_profile() -> None:
    db = SessionLocal()
    repository = ProfileRepository(db)

    created_profile = repository.create(
        user_id=TEST_USER_ID,
        full_name="Test User",
        professional_title="Software Developer",
        summary="Existing sample professional profile.",
    )

    found_profile = repository.get_by_id_and_user_id(created_profile.id, TEST_USER_ID)

    assert found_profile is not None
    assert found_profile.id == created_profile.id
    assert found_profile.full_name == "Test User"

    db.close()


def test_get_by_id_non_existing_profile() -> None:
    db = SessionLocal()
    repository = ProfileRepository(db)

    profile = repository.get_by_id_and_user_id(999, TEST_USER_ID)

    assert profile is None

    db.close()


def test_update_existing_profile(profile_repository):
    profile = profile_repository.create(
        user_id=TEST_USER_ID,
        full_name="Test User",
        professional_title="Software Developer",
        summary="Initial sample professional profile.",
        location="Test City",
        linkedin_url="https://linkedin.com/in/old-test-user",
        github_url="https://github.com/old-test-user",
    )

    updated_profile = profile_repository.update(
        profile_id=profile.id,
        user_id=TEST_USER_ID,
        full_name="Updated Test User",
        professional_title="Senior Software Developer",
        summary="Updated sample professional profile.",
        location="Updated Test City",
        linkedin_url="https://linkedin.com/in/updated-test-user",
        github_url="https://github.com/updated-test-user",
    )

    assert updated_profile is not None
    assert updated_profile.id == profile.id
    assert updated_profile.full_name == "Updated Test User"
    assert updated_profile.professional_title == "Senior Software Developer"
    assert updated_profile.summary == "Updated sample professional profile."
    assert updated_profile.location == "Updated Test City"
    assert updated_profile.linkedin_url == "https://linkedin.com/in/updated-test-user"
    assert updated_profile.github_url == "https://github.com/updated-test-user"


def test_update_non_existing_profile(profile_repository):
    updated_profile = profile_repository.update(
        profile_id=999,
        user_id=TEST_USER_ID,
        full_name="Unknown Test User",
        professional_title="Unknown Role",
        summary="Unknown sample professional profile.",
    )

    assert updated_profile is None


def test_delete_existing_profile(profile_repository):
    profile = profile_repository.create(
        user_id=TEST_USER_ID,
        full_name="Test User",
        professional_title="Software Developer",
        summary="Sample profile marked for deletion.",
    )

    result = profile_repository.delete(profile.id, TEST_USER_ID)
    deleted_profile = profile_repository.get_by_id_and_user_id(profile.id, TEST_USER_ID)

    assert result is True
    assert deleted_profile is None


def test_delete_non_existing_profile(profile_repository):
    result = profile_repository.delete(profile_id=999, user_id=TEST_USER_ID)

    assert result is False
