from sqlalchemy.orm import Session

from models.job_model import JobModel
from schemas.job_schema import JobCreate, JobUpdate


class JobRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, job_data: JobCreate, user_id: int) -> JobModel:
        job = JobModel(
            **job_data.model_dump(),
            user_id=user_id,
        )

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job

    def list_by_user_id(self, user_id: int) -> list[JobModel]:
        return self.db.query(JobModel).filter(JobModel.user_id == user_id).all()

    def get_by_id_and_user_id(
        self,
        job_id: int,
        user_id: int,
    ) -> JobModel | None:
        return (
            self.db.query(JobModel)
            .filter(
                JobModel.id == job_id,
                JobModel.user_id == user_id,
            )
            .first()
        )

    def update(
        self,
        job: JobModel,
        job_data: JobUpdate,
    ) -> JobModel:
        update_data = job_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(job, field, value)

        self.db.commit()
        self.db.refresh(job)

        return job

    def delete(self, job: JobModel) -> None:
        self.db.delete(job)
        self.db.commit()
