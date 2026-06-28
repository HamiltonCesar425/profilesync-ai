from domain.exceptions import DomainError
from models.technology_model import TechnologyModel
from repositories.profile_repository import ProfileRepository
from repositories.technology_repository import TechnologyRepository
from schemas.technology_schema import TechnologyCreate, TechnologyUpdate


class TechnologyService:
    """Serviço para regras de negócio de tecnologias e competências."""

    def __init__(
        self,
        technology_repository: TechnologyRepository,
        profile_repository: ProfileRepository,
    ) -> None:
        self.technology_repository = technology_repository
        self.profile_repository = profile_repository

    def create_technology(
        self,
        profile_id: int,
        user_id: int,
        technology_data: TechnologyCreate,
    ) -> TechnologyModel:
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise DomainError("Profile not found")

        return self.technology_repository.create(
            profile_id=profile_id,
            technology_data=technology_data,
        )

    def list_profile_technologies(
        self,
        profile_id: int,
        user_id: int,
    ) -> list[TechnologyModel]:
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise DomainError("Profile not found")

        return self.technology_repository.list_by_profile_id(
            profile_id=profile_id,
        )

    def get_technology(
        self,
        technology_id: int,
        user_id: int,
    ) -> TechnologyModel:
        technology = self.technology_repository.get_by_id(
            technology_id=technology_id,
        )

        if technology is None:
            raise DomainError("Technology not found")

        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=technology.profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise DomainError("Technology not found")

        return technology

    def update_technology(
        self,
        technology_id: int,
        user_id: int,
        technology_data: TechnologyUpdate,
    ) -> TechnologyModel:
        technology = self.get_technology(
            technology_id=technology_id,
            user_id=user_id,
        )

        return self.technology_repository.update(
            technology=technology,
            technology_data=technology_data,
        )

    def delete_technology(
        self,
        technology_id: int,
        user_id: int,
    ) -> None:
        technology = self.get_technology(
            technology_id=technology_id,
            user_id=user_id,
        )

        self.technology_repository.delete(technology)
