import pytest

from domain.exceptions import ProfileNotFoundError
from domain.profile import Profile
from services.profile_service import ProfileService


class FakeProfileRepository:
    def __init__(self) -> None:
        self.profiles: list[Profile] = []

    def create(
        self,
        full_name: str,
        professional_title: str,
        summary: str,
        location: str | None = None,
        linkedin_url: str | None = None,
        github_url: str | None = None,
    ) -> Profile:
        profile = Profile(
            id=len(self.profiles) + 1,
            full_name=full_name,
            professional_title=professional_title,
            summary=summary,
            location=location,
            linkedin_url=linkedin_url,
            github_url=github_url,
        )

        self.profiles.append(profile)
        return profile

    def list_all(self) -> list[Profile]:
        return self.profiles.copy()

    def get_by_id(self, profile_id: int) -> Profile | None:
        for profile in self.profiles:
            if profile.id == profile_id:
                return profile

        return None

    def update(
        self,
        profile_id: int,
        full_name: str,
        professional_title: str,
        summary: str,
        location: str | None = None,
        linkedin_url: str | None = None,
        github_url: str | None = None,
    ) -> Profile | None:
        for index, profile in enumerate(self.profiles):
            if profile.id == profile_id:
                updated_profile = Profile(
                    id=profile.id,
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

    def delete(self, profile_id: int) -> bool:
        for profile in self.profiles:
            if profile.id == profile_id:
                self.profiles.remove(profile)
                return True

        return False


@pytest.fixture
def profile_service() -> ProfileService:
    repository = FakeProfileRepository()
    return ProfileService(repository)


def test_create_profile(profile_service: ProfileService) -> None:
    profile = profile_service.create_profile(
        full_name="Test User",
        professional_title="Software Developer",
        summary="Sample professional profile",
    )

    assert profile.id == 1
    assert profile.full_name == "Test User"


def test_list_profiles(profile_service: ProfileService) -> None:
    profile_service.create_profile(
        full_name="Test User",
        professional_title="Software Developer",
        summary="Sample profile one",
    )

    profile_service.create_profile(
        full_name="Sample User",
        professional_title="Data Scientist",
        summary="Sample profile two",
    )

    profiles = profile_service.list_profiles()

    assert len(profiles) == 2


def test_get_existing_profile(profile_service: ProfileService) -> None:
    created = profile_service.create_profile(
        full_name="Test User",
        professional_title="Software Developer",
        summary="Sample profile",
    )

    profile = profile_service.get_profile(created.id)

    assert profile.id == created.id


def test_get_non_existing_profile(profile_service: ProfileService) -> None:
    with pytest.raises(ProfileNotFoundError):
        profile_service.get_profile(999)


def test_update_existing_profile(profile_service: ProfileService) -> None:
    profile = profile_service.create_profile(
        full_name="Test User",
        professional_title="Software Developer",
        summary="Initial sample profile summary",
    )

    updated_profile = profile_service.update_profile(
        profile_id=profile.id,
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
        full_name="Unknown",
        professional_title="Unknown",
        summary="Unknown",
    )

    assert updated_profile is None


def test_delete_existing_profile(profile_service: ProfileService) -> None:
    profile = profile_service.create_profile(
        full_name="Test User",
        professional_title="Software Developer",
        summary="Sample profile marked for deletion",
    )

    result = profile_service.delete_profile(profile.id)

    assert result is True

    with pytest.raises(ProfileNotFoundError):
        profile_service.get_profile(profile.id)


def test_delete_non_existing_profile(profile_service: ProfileService) -> None:
    result = profile_service.delete_profile(profile_id=999)

    assert result is False

