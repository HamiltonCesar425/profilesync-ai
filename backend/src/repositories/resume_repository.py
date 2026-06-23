from sqlalchemy import select
from sqlalchemy.orm import Session

from models.resume_model import Resume


class ResumeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, resume: Resume) -> Resume:
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def list_by_profile_id(self, profile_id: int) -> list[Resume]:
        statement = select(Resume).where(Resume.profile_id == profile_id)
        return list(self.db.scalars(statement).all())

    def get_by_id(self, resume_id: int) -> Resume | None:
        statement = select(Resume).where(Resume.id == resume_id)
        return self.db.scalar(statement)

    def get_by_id_and_profile_id(
        self,
        resume_id: int,
        profile_id: int,
    ) -> Resume | None:
        statement = select(Resume).where(
            Resume.id == resume_id,
            Resume.profile_id == profile_id,
        )
        return self.db.scalar(statement)

    def update(self, resume: Resume, data: dict) -> Resume:
        for field, value in data.items():
            setattr(resume, field, value)

        self.db.commit()
        self.db.refresh(resume)
        return resume

    def delete(self, resume: Resume) -> None:
        self.db.delete(resume)
        self.db.commit()