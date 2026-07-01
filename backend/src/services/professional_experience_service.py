from repositories.professional_experience_repository import (
    ProfessionalExperienceRepository,
)
from repositories.profile_repository import ProfileRepository
from schemas.professional_experience_schema import (
    ProfessionalExperienceCreate,
    ProfessionalExperienceUpdate,
)


class ProfessionalExperienceService:
    """Regras de negócio para experiências profissionais."""

    def __init__(
        self,
        repository: ProfessionalExperienceRepository,
        profile_repository: ProfileRepository,
    ) -> None:
        self.repository = repository
        self.profile_repository = profile_repository

    def create_experience(
        self,
        profile_id: int,
        user_id: int,
        experience_data: ProfessionalExperienceCreate,
    ):
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise ValueError("Perfil não encontrado.")

        return self.repository.create(
            profile_id=profile_id,
            experience_data=experience_data,
        )

    def list_experiences(
        self,
        profile_id: int,
        user_id: int,
    ):
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise ValueError("Perfil não encontrado.")

        return self.repository.list_by_profile_id(profile_id)

    def get_experience(
        self,
        experience_id: int,
        profile_id: int,
        user_id: int,
    ):
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise ValueError("Perfil não encontrado.")

        experience = self.repository.get_by_id_and_profile_id(
            experience_id=experience_id,
            profile_id=profile_id,
        )

        if experience is None:
            raise ValueError("Experiência profissional não encontrada.")

        return experience

    def update_experience(
        self,
        experience_id: int,
        profile_id: int,
        user_id: int,
        experience_data: ProfessionalExperienceUpdate,
    ):
        experience = self.get_experience(
            experience_id=experience_id,
            profile_id=profile_id,
            user_id=user_id,
        )

        return self.repository.update(
            experience=experience,
            experience_data=experience_data,
        )

    def delete_experience(
        self,
        experience_id: int,
        profile_id: int,
        user_id: int,
    ) -> None:
        experience = self.get_experience(
            experience_id=experience_id,
            profile_id=profile_id,
            user_id=user_id,
        )

        self.repository.delete(experience)
