from sqlalchemy.orm import Session

from models.technology_model import TechnologyModel
from schemas.technology_schema import TechnologyCreate, TechnologyUpdate


class TechnologyRepository:
    """Repositório para operações de persistência de tecnologias."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        profile_id: int,
        technology_data: TechnologyCreate,
    ) -> TechnologyModel:
        technology = TechnologyModel(
            profile_id=profile_id,
            **technology_data.model_dump(),
        )

        self.db.add(technology)
        self.db.commit()
        self.db.refresh(technology)

        return technology

    def list_by_profile_id(self, profile_id: int) -> list[TechnologyModel]:
        return (
            self.db.query(TechnologyModel)
            .filter(TechnologyModel.profile_id == profile_id)
            .all()
        )

    def get_by_id(self, technology_id: int) -> TechnologyModel | None:
        return (
            self.db.query(TechnologyModel)
            .filter(TechnologyModel.id == technology_id)
            .first()
        )

    def update(
        self,
        technology: TechnologyModel,
        technology_data: TechnologyUpdate,
    ) -> TechnologyModel:
        update_data = technology_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(technology, field, value)

        self.db.commit()
        self.db.refresh(technology)

        return technology

    def delete(self, technology: TechnologyModel) -> None:
        self.db.delete(technology)
        self.db.commit()
