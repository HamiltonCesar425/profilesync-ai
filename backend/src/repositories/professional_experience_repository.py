from sqlalchemy.orm import Session

from models.professional_experience_model import ProfessionalExperienceModel
from schemas.professional_experience_schema import (
    ProfessionalExperienceCreate,
    ProfessionalExperienceUpdate,
)


class ProfessionalExperienceRepository:
    """Camada de persistência para experiências profissionais."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        profile_id: int,
        experience_data: ProfessionalExperienceCreate,
    ) -> ProfessionalExperienceModel:
        experience = ProfessionalExperienceModel(
            profile_id=profile_id,
            **experience_data.model_dump(),
        )

        self.db.add(experience)
        self.db.commit()
        self.db.refresh(experience)

        return experience

    def list_by_profile_id(
        self,
        profile_id: int,
    ) -> list[ProfessionalExperienceModel]:
        return (
            self.db.query(ProfessionalExperienceModel)
            .filter(ProfessionalExperienceModel.profile_id == profile_id)
            .order_by(
                ProfessionalExperienceModel.start_date.desc(),
                ProfessionalExperienceModel.id.desc(),
            )
            .all()
        )

    def get_by_id(
        self,
        experience_id: int,
    ) -> ProfessionalExperienceModel | None:
        return (
            self.db.query(ProfessionalExperienceModel)
            .filter(ProfessionalExperienceModel.id == experience_id)
            .first()
        )

    def get_by_id_and_profile_id(
        self,
        experience_id: int,
        profile_id: int,
    ) -> ProfessionalExperienceModel | None:
        return (
            self.db.query(ProfessionalExperienceModel)
            .filter(
                ProfessionalExperienceModel.id == experience_id,
                ProfessionalExperienceModel.profile_id == profile_id,
            )
            .first()
        )

    def update(
        self,
        experience: ProfessionalExperienceModel,
        experience_data: ProfessionalExperienceUpdate,
    ) -> ProfessionalExperienceModel:
        update_data = experience_data.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(experience, field, value)

        self.db.commit()
        self.db.refresh(experience)

        return experience

    def delete(
        self,
        experience: ProfessionalExperienceModel,
    ) -> None:
        self.db.delete(experience)
        self.db.commit()
