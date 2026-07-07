import pytest

from repositories.job_repository import JobRepository
from schemas.job_schema import JobCreate, JobUpdate
from services.job_service import JobNotFoundError, JobService


def test_create_job(db_session, test_user):
    service = JobService(JobRepository(db_session))

    job = service.create_job(
        job_data=JobCreate(
            title="Backend Developer",
            company="Tech Company",
            description="Python, FastAPI and SQLAlchemy.",
        ),
        user_id=test_user.id,
    )

    assert job.id is not None
    assert job.user_id == test_user.id
    assert job.title == "Backend Developer"


def test_list_jobs(db_session, test_user):
    service = JobService(JobRepository(db_session))

    service.create_job(
        job_data=JobCreate(
            title="Backend Developer",
            company="Company A",
            description="Python and FastAPI.",
        ),
        user_id=test_user.id,
    )

    jobs = service.list_jobs(user_id=test_user.id)

    assert len(jobs) == 1
    assert jobs[0].title == "Backend Developer"


def test_get_job(db_session, test_user):
    service = JobService(JobRepository(db_session))

    created_job = service.create_job(
        job_data=JobCreate(
            title="Data Engineer",
            company="Data Company",
            description="Airflow, SQL and Python.",
        ),
        user_id=test_user.id,
    )

    job = service.get_job(
        job_id=created_job.id,
        user_id=test_user.id,
    )

    assert job.id == created_job.id
    assert job.user_id == test_user.id


def test_get_job_not_found(db_session, test_user):
    service = JobService(JobRepository(db_session))

    with pytest.raises(JobNotFoundError, match="Job not found"):
        service.get_job(job_id=999, user_id=test_user.id)


def test_update_job(db_session, test_user):
    service = JobService(JobRepository(db_session))

    job = service.create_job(
        job_data=JobCreate(
            title="Old Title",
            company="Old Company",
            description="Old description.",
        ),
        user_id=test_user.id,
    )

    updated_job = service.update_job(
        job_id=job.id,
        job_data=JobUpdate(
            title="Updated Title",
            description="Updated description.",
        ),
        user_id=test_user.id,
    )

    assert updated_job.title == "Updated Title"
    assert updated_job.company == "Old Company"
    assert updated_job.description == "Updated description."


def test_update_job_not_found(db_session, test_user):
    service = JobService(JobRepository(db_session))

    with pytest.raises(JobNotFoundError, match="Job not found"):
        service.update_job(
            job_id=999,
            job_data=JobUpdate(title="Updated Title"),
            user_id=test_user.id,
        )


def test_delete_job(db_session, test_user):
    service = JobService(JobRepository(db_session))

    job = service.create_job(
        job_data=JobCreate(
            title="Temporary Job",
            company="Temporary Company",
            description="Temporary description.",
        ),
        user_id=test_user.id,
    )

    service.delete_job(job_id=job.id, user_id=test_user.id)

    with pytest.raises(JobNotFoundError, match="Job not found"):
        service.get_job(job_id=job.id, user_id=test_user.id)


def test_delete_job_not_found(db_session, test_user):
    service = JobService(JobRepository(db_session))

    with pytest.raises(JobNotFoundError, match="Job not found"):
        service.delete_job(job_id=999, user_id=test_user.id)


def test_user_cannot_access_job_from_another_user(
    db_session,
    test_user,
    other_user,
):
    service = JobService(JobRepository(db_session))

    other_job = service.create_job(
        job_data=JobCreate(
            title="Private Job",
            company="Private Company",
            description="Private description.",
        ),
        user_id=other_user.id,
    )

    with pytest.raises(JobNotFoundError, match="Job not found"):
        service.get_job(
            job_id=other_job.id,
            user_id=test_user.id,
        )
