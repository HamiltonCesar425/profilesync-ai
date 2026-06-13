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
        return self.profiles

    def get_by_id(self, profile_id: int) -> Profile | None:
        for profile in self.profiles:
            if profile.id == profile_id:
                return profile

        return None


def test_create_profile() -> None:
    repository = FakeProfileRepository()
    service = ProfileService(repository)

    profile = service.create_profile(
        full_name="Hamilton Cesar",
        professional_title="Python Developer",
        summary="Professional profile",
    )

    assert profile.id == 1
    assert profile.full_name == "Hamilton Cesar"


def test_list_profiles() -> None:
    repository = FakeProfileRepository()
    service = ProfileService(repository)

    service.create_profile(
        full_name="Hamilton Cesar",
        professional_title="Python Developer",
        summary="Profile 1",
    )

    service.create_profile(
        full_name="Ana Silva",
        professional_title="Data Scientist",
        summary="Profile 2",
    )

    profiles = service.list_profiles()

    assert len(profiles) == 2


def test_get_existing_profile() -> None:
    repository = FakeProfileRepository()
    service = ProfileService(repository)

    created = service.create_profile(
        full_name="Hamilton Cesar",
        professional_title="Python Developer",
        summary="Profile",
    )

    profile = service.get_profile(created.id)

    assert profile.id == created.id


def test_get_non_existing_profile() -> None:
    repository = FakeProfileRepository()
    service = ProfileService(repository)

    with pytest.raises(ProfileNotFoundError):
        service.get_profile(999)
