from datetime import date

from models.professional_experience_model import ProfessionalExperienceModel
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

    @staticmethod
    def _validate_dates(
        *,
        start_date: date,
        end_date: date | None,
        is_current: bool,
    ) -> None:
        """Valida a consistência cronológica de uma experiência."""
        today = date.today()

        if start_date > today:
            raise ValueError("A data de início não pode ser posterior à data atual.")

        if end_date is not None and end_date > today:
            raise ValueError("A data de término não pode ser posterior à data atual.")

        if end_date is not None and end_date < start_date:
            raise ValueError(
                "A data de término não pode ser anterior à data de início."
            )

        if is_current and end_date is not None:
            raise ValueError("Uma experiência atual não pode possuir data de término.")

        if not is_current and end_date is None:
            raise ValueError("Uma experiência encerrada deve possuir data de término.")

    def create_experience(
        self,
        profile_id: int,
        user_id: int,
        experience_data: ProfessionalExperienceCreate,
    ) -> ProfessionalExperienceModel:
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise ValueError("Perfil não encontrado.")

        self._validate_dates(
            start_date=experience_data.start_date,
            end_date=experience_data.end_date,
            is_current=experience_data.is_current,
        )

        return self.repository.create(
            profile_id=profile_id,
            experience_data=experience_data,
        )

    def list_experiences(
        self,
        profile_id: int,
        user_id: int,
    ) -> list[ProfessionalExperienceModel]:
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
    ) -> ProfessionalExperienceModel:
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
    ) -> ProfessionalExperienceModel:
        experience = self.get_experience(
            experience_id=experience_id,
            profile_id=profile_id,
            user_id=user_id,
        )

        update_data = experience_data.model_dump(exclude_unset=True)

        start_date = update_data.get(
            "start_date",
            experience.start_date,
        )
        end_date = update_data.get(
            "end_date",
            experience.end_date,
        )
        is_current = update_data.get(
            "is_current",
            experience.is_current,
        )

        self._validate_dates(
            start_date=start_date,
            end_date=end_date,
            is_current=is_current,
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
