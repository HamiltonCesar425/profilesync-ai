import logging

from domain.exceptions import ProfileNotFoundError, UserNotFoundError
from domain.profile import Profile
from repositories.profile_repository import ProfileRepository
from repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class ProfileService:
    def __init__(
        self,
        repository: ProfileRepository,
        user_repository: UserRepository,
    ) -> None:
        self._repository = repository
        self._user_repository = user_repository

    def create_profile(
        self,
        user_id: int,
        full_name: str,
        professional_title: str,
        summary: str,
        location: str | None = None,
        linkedin_url: str | None = None,
        github_url: str | None = None,
    ) -> Profile:

        user = self._user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(f"User with id {user_id} not found")

        profile = self._repository.create(
            user_id=user_id,
            full_name=full_name,
            professional_title=professional_title,
            summary=summary,
            location=location,
            linkedin_url=linkedin_url,
            github_url=github_url,
        )

        logger.info("Profile created")

        return profile

    def list_profiles(self, user_id: int) -> list[Profile]:
        return self._repository.list_by_user_id(user_id)

    def get_profile(self, profile_id: int, user_id: int) -> Profile:
        logger.info(f"Searching profile id={profile_id} for user id={user_id}")

        profile = self._repository.get_by_id_and_user_id(
            profile_id=profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise ProfileNotFoundError(f"Profile with id {profile_id} not found")

        logger.info(f"Profile found id={profile_id} for user id={user_id}")

        return profile

    def update_profile(
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
        return self._repository.update(
            profile_id=profile_id,
            user_id=user_id,
            full_name=full_name,
            professional_title=professional_title,
            summary=summary,
            location=location,
            linkedin_url=linkedin_url,
            github_url=github_url,
        )

    def delete_profile(self, profile_id: int, user_id: int) -> bool:
        return self._repository.delete(
            profile_id=profile_id,
            user_id=user_id,
        )
