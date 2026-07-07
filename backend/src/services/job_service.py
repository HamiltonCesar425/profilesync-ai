from models.job_model import JobModel
from repositories.job_repository import JobRepository
from schemas.job_schema import JobCreate, JobUpdate


class JobNotFoundError(Exception):
    pass


class JobService:
    def __init__(self, repository: JobRepository) -> None:
        self.repository = repository

    def create_job(self, job_data: JobCreate, user_id: int) -> JobModel:
        return self.repository.create(
            job_data=job_data,
            user_id=user_id,
        )

    def list_jobs(self, user_id: int) -> list[JobModel]:
        return self.repository.list_by_user_id(user_id=user_id)

    def get_job(self, job_id: int, user_id: int) -> JobModel:
        job = self.repository.get_by_id_and_user_id(
            job_id=job_id,
            user_id=user_id,
        )

        if job is None:
            raise JobNotFoundError("Job not found")

        return job

    def update_job(
        self,
        job_id: int,
        job_data: JobUpdate,
        user_id: int,
    ) -> JobModel:
        job = self.get_job(job_id=job_id, user_id=user_id)

        return self.repository.update(
            job=job,
            job_data=job_data,
        )

    def delete_job(self, job_id: int, user_id: int) -> None:
        job = self.get_job(job_id=job_id, user_id=user_id)

        self.repository.delete(job)
