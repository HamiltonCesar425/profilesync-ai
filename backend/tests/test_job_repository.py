from models.job_model import JobModel
from models.user_model import User
from repositories.job_repository import JobRepository
from schemas.job_schema import JobCreate, JobUpdate


def create_user(db_session, email: str = "user@example.com") -> User:
    user = User(
        email=email,
        hashed_password="hashed-password",
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def test_create_job(db_session):
    user = create_user(db_session)
    repository = JobRepository(db_session)

    job_data = JobCreate(
        title="Python Backend Developer",
        company="Tech Company",
        description="FastAPI, SQLAlchemy, Docker and PostgreSQL.",
    )

    job = repository.create(job_data=job_data, user_id=user.id)

    assert job.id is not None
    assert job.user_id == user.id
    assert job.title == "Python Backend Developer"
    assert job.company == "Tech Company"
    assert job.description == "FastAPI, SQLAlchemy, Docker and PostgreSQL."


def test_list_jobs_by_user_id(db_session):
    user = create_user(db_session)
    other_user = create_user(db_session, email="other@example.com")
    repository = JobRepository(db_session)

    repository.create(
        JobCreate(
            title="Backend Developer",
            company="Company A",
            description="Python and FastAPI.",
        ),
        user_id=user.id,
    )
    repository.create(
        JobCreate(
            title="Data Engineer",
            company="Company B",
            description="Airflow and Spark.",
        ),
        user_id=other_user.id,
    )

    jobs = repository.list_by_user_id(user.id)

    assert len(jobs) == 1
    assert jobs[0].user_id == user.id
    assert jobs[0].title == "Backend Developer"


def test_get_job_by_id_and_user_id(db_session):
    user = create_user(db_session)
    repository = JobRepository(db_session)

    created_job = repository.create(
        JobCreate(
            title="ML Engineer",
            company="AI Company",
            description="Python, MLflow and model monitoring.",
        ),
        user_id=user.id,
    )

    job = repository.get_by_id_and_user_id(
        job_id=created_job.id,
        user_id=user.id,
    )

    assert job is not None
    assert job.id == created_job.id
    assert job.user_id == user.id


def test_user_cannot_access_job_from_another_user(db_session):
    user = create_user(db_session)
    other_user = create_user(db_session, email="other@example.com")
    repository = JobRepository(db_session)

    other_job = repository.create(
        JobCreate(
            title="Cloud Engineer",
            company="Cloud Company",
            description="AWS, Docker and CI/CD.",
        ),
        user_id=other_user.id,
    )

    job = repository.get_by_id_and_user_id(
        job_id=other_job.id,
        user_id=user.id,
    )

    assert job is None


def test_update_job(db_session):
    user = create_user(db_session)
    repository = JobRepository(db_session)

    job = repository.create(
        JobCreate(
            title="Old Title",
            company="Old Company",
            description="Old description.",
        ),
        user_id=user.id,
    )

    updated_job = repository.update(
        job=job,
        job_data=JobUpdate(
            title="Senior Backend Developer",
            description="Python, FastAPI, PostgreSQL and Docker.",
        ),
    )

    assert updated_job.id == job.id
    assert updated_job.title == "Senior Backend Developer"
    assert updated_job.company == "Old Company"
    assert updated_job.description == "Python, FastAPI, PostgreSQL and Docker."


def test_delete_job(db_session):
    user = create_user(db_session)
    repository = JobRepository(db_session)

    job = repository.create(
        JobCreate(
            title="Temporary Job",
            company="Temporary Company",
            description="Temporary description.",
        ),
        user_id=user.id,
    )

    repository.delete(job)

    deleted_job = db_session.get(JobModel, job.id)

    assert deleted_job is None
