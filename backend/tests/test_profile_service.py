import pytest

from domain.exceptions import ProfileNotFoundError
from domain.profile import Profile
from services.profile_service import ProfileService


TEST_USER_ID = 1


class FakeProfileRepository:
    def __init__(self) -> None:
        self.profiles: list[Profile] = []

    def create(
        self,
        user_id: int,
        full_name: str,
        professional_title: str,
        summary: str,
        location: str | None = None,
        linkedin_url: str | None = None,
        github_url: str | None = None,
    ) -> Profile:
        profile = Profile(
            id=len(self.profiles) + 1,
            user_id=user_id,
            full_name=full_name,
            professional_title=professional_title,
            summary=summary,
            location=location,
            linkedin_url=linkedin_url,
            github_url=github_url,
        )

        self.profiles.append(profile)
        return profile

    def list_by_user_id(self, user_id: int) -> list[Profile]:
        return [profile for profile in self.profiles if profile.user_id == user_id]

    def get_by_id_and_user_id(self, profile_id: int, user_id: int) -> Profile | None:
        for profile in self.profiles:
            if profile.id == profile_id and profile.user_id == user_id:
                return profile

        return None

    def update(
        self,
        profile_id: int,
        user_id: int,
        full_name: str,
        professional_title: str,
        summary: str,
        location: str | None = None,
        linkedin_url: str | None = None,
        github_url: str | None = None,
    ) -> Profile | None:
        for index, profile in enumerate(self.profiles):
            if profile.id == profile_id and profile.user_id == user_id:
                updated_profile = Profile(
                    id=profile.id,
                    user_id=user_id,
                    full_name=full_name,
                    professional_title=professional_title,
                    summary=summary,
                    location=location,
                    linkedin_url=linkedin_url,
                    github_url=github_url,
                )
                self.profiles[index] = updated_profile
                return updated_profile

        return None

    def delete(self, profile_id: int, user_id: int) -> bool:
        for profile in self.profiles:
            if profile.id == profile_id and profile.user_id == user_id:
                self.profiles.remove(profile)
                return True

        return False


class FakeUserRepository:
    def get_by_id(self, user_id: int) -> object | None:
        return object() if user_id == TEST_USER_ID else None


@pytest.fixture
def profile_service() -> ProfileService:
    repository = FakeProfileRepository()
    return ProfileService(repository, FakeUserRepository())


def test_create_profile(profile_service: ProfileService) -> None:
    profile = profile_service.create_profile(
        user_id=TEST_USER_ID,
        full_name="Test User",
        professional_title="Software Developer",
        summary="Sample professional profile",
    )

    assert profile.id == 1
    assert profile.full_name == "Test User"


def test_list_profiles(profile_service: ProfileService) -> None:
    profile_service.create_profile(
        user_id=TEST_USER_ID,
        full_name="Test User",
        professional_title="Software Developer",
        summary="Sample profile one",
    )

    profile_service.create_profile(
        user_id=TEST_USER_ID,
        full_name="Sample User",
        professional_title="Data Scientist",
        summary="Sample profile two",
    )

    profiles = profile_service.list_profiles(TEST_USER_ID)

    assert len(profiles) == 2


def test_get_existing_profile(profile_service: ProfileService) -> None:
    created = profile_service.create_profile(
        user_id=TEST_USER_ID,
        full_name="Test User",
        professional_title="Software Developer",
        summary="Sample profile",
    )

    profile = profile_service.get_profile(created.id, TEST_USER_ID)

    assert profile.id == created.id


def test_get_non_existing_profile(profile_service: ProfileService) -> None:
    with pytest.raises(ProfileNotFoundError):
        profile_service.get_profile(999, TEST_USER_ID)


def test_update_existing_profile(profile_service: ProfileService) -> None:
    profile = profile_service.create_profile(
        user_id=TEST_USER_ID,
        full_name="Test User",
        professional_title="Software Developer",
        summary="Initial sample profile summary",
    )

    updated_profile = profile_service.update_profile(
        profile_id=profile.id,
        user_id=TEST_USER_ID,
        full_name="Test User",
        professional_title="Senior Software Developer",
        summary="Updated sample profile summary",
        location="Test City",
        linkedin_url="https://linkedin.com/in/test-profile",
        github_url="https://github.com/test-profile",
    )

    assert updated_profile is not None
    assert updated_profile.id == profile.id
    assert updated_profile.full_name == "Test User"
    assert updated_profile.professional_title == "Senior Software Developer"
    assert updated_profile.summary == "Updated sample profile summary"
    assert updated_profile.location == "Test City"
    assert updated_profile.linkedin_url == "https://linkedin.com/in/test-profile"
    assert updated_profile.github_url == "https://github.com/test-profile"


def test_update_non_existing_profile(profile_service: ProfileService) -> None:
    updated_profile = profile_service.update_profile(
        profile_id=999,
        user_id=TEST_USER_ID,
        full_name="Unknown",
        professional_title="Unknown",
        summary="Unknown",
    )

    assert updated_profile is None


def test_delete_existing_profile(profile_service: ProfileService) -> None:
    profile = profile_service.create_profile(
        user_id=TEST_USER_ID,
        full_name="Test User",
        professional_title="Software Developer",
        summary="Sample profile marked for deletion",
    )

    result = profile_service.delete_profile(profile.id, TEST_USER_ID)

    assert result is True

    with pytest.raises(ProfileNotFoundError):
        profile_service.get_profile(profile.id, TEST_USER_ID)


def test_delete_non_existing_profile(profile_service: ProfileService) -> None:
    result = profile_service.delete_profile(profile_id=999, user_id=TEST_USER_ID)

    assert result is False

