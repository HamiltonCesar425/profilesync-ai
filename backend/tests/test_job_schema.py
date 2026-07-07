from pydantic import ValidationError

from schemas.job_schema import JobCreate, JobUpdate


def test_job_create_validates_required_lengths() -> None:
    job = JobCreate(
        title="Backend Developer",
        company="ProfileSync",
        description="Build and maintain API services.",
    )

    assert job.title == "Backend Developer"
    assert job.company == "ProfileSync"

    try:
        JobCreate(title="x", description="y")
    except ValidationError as exc:
        fields = {tuple(error["loc"])[0] for error in exc.errors()}
        assert fields == {"title", "description"}
    else:
        raise AssertionError("JobCreate accepted invalid short values")


def test_job_update_allows_partial_payloads() -> None:
    assert JobUpdate(company="ProfileSync").model_dump(exclude_unset=True) == {
        "company": "ProfileSync",
    }
