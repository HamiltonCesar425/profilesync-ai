from datetime import date

from fastapi.testclient import TestClient

from main import app
from models.job_model import JobModel
from models.professional_experience_model import ProfessionalExperienceModel
from models.profile_model import ProfileModel
from models.project_model import Project
from models.resume_model import Resume
from models.technology_model import TechnologyModel


client = TestClient(app)
UNAVAILABLE_RESPONSE = {"detail": "Authorized preview sources are unavailable."}


def create_profile(db_session, user_id: int, name: str) -> ProfileModel:
    profile = ProfileModel(
        user_id=user_id,
        full_name=name,
        professional_title="Backend Engineer",
        summary="Desenvolve APIs Python.",
        location=None,
        linkedin_url=None,
        github_url=None,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)
    return profile


def create_job(
    db_session,
    user_id: int,
    description: str = "Python, APIs e Kubernetes.",
) -> JobModel:
    job = JobModel(
        user_id=user_id,
        title="Backend Engineer",
        company=None,
        description=description,
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)
    return job


def add_profile_sources(db_session, profile_id: int, suffix: str = "") -> None:
    db_session.add_all(
        [
            ProfessionalExperienceModel(
                profile_id=profile_id,
                company_name=f"Analytical Engines{suffix}",
                position="Backend Engineer",
                employment_type=None,
                work_model="Remote",
                location=None,
                description="Desenvolveu APIs Python.",
                start_date=date(2023, 1, 1),
                end_date=None,
                is_current=True,
            ),
            Project(
                profile_id=profile_id,
                name=f"API Platform{suffix}",
                description="API factual.",
                role="Developer",
                repository_url=None,
                demo_url=None,
                start_date=None,
                end_date=None,
                is_current=False,
            ),
            TechnologyModel(
                profile_id=profile_id,
                name=f"Python{suffix}",
                category="Language",
                proficiency_level="Advanced",
                years_experience=4,
            ),
            TechnologyModel(
                profile_id=profile_id,
                name=f"SQL{suffix}",
                category="Database",
                proficiency_level="Intermediate",
                years_experience=None,
            ),
        ]
    )
    db_session.commit()


def preview_request(
    auth_headers: dict[str, str],
    profile_id: int,
    job_id: int,
    **extra,
):
    return client.post(
        "/targeted-resumes/preview",
        headers=auth_headers,
        json={"profile_id": profile_id, "job_id": job_id, **extra},
    )


def factual_values(response_data: dict) -> list[object]:
    return [
        fact["value"]
        for block in response_data["composition"]["blocks"]
        for fact in block["facts"]
    ]


def test_preview_requires_authentication() -> None:
    response = client.post(
        "/targeted-resumes/preview",
        json={"profile_id": 1, "job_id": 1},
    )

    assert response.status_code == 401


def test_preview_rejects_invalid_token() -> None:
    response = client.post(
        "/targeted-resumes/preview",
        headers={"Authorization": "Bearer invalid-token"},
        json={"profile_id": 1, "job_id": 1},
    )

    assert response.status_code == 401


def test_preview_rejects_additional_fields(auth_headers) -> None:
    response = preview_request(
        auth_headers,
        profile_id=1,
        job_id=1,
        authenticated_user_id=999,
    )

    assert response.status_code == 422


def test_preview_rejects_non_positive_identifiers(auth_headers) -> None:
    for profile_id, job_id in ((0, 1), (1, 0), (-1, 1), (1, -1)):
        response = preview_request(auth_headers, profile_id, job_id)
        assert response.status_code == 422


def test_generates_structured_preview_through_real_integration(
    db_session,
    test_user,
    auth_headers,
) -> None:
    profile = create_profile(db_session, test_user.id, "Ada Lovelace")
    job = create_job(db_session, test_user.id)
    add_profile_sources(db_session, profile.id)
    resumes_before = db_session.query(Resume).count()

    first_response = preview_request(auth_headers, profile.id, job.id)
    second_response = preview_request(auth_headers, profile.id, job.id)

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    data = first_response.json()
    assert set(data) == {"preview_id", "state", "composition"}
    assert data["state"] == "preview"
    assert data["preview_id"] == second_response.json()["preview_id"]
    assert set(data["composition"]) == {
        "profile_id",
        "job_id",
        "ruleset_version",
        "blocks",
        "source_manifest",
    }
    assert data["composition"]["profile_id"] == profile.id
    assert data["composition"]["job_id"] == job.id
    assert all(block["provenance"] for block in data["composition"]["blocks"])
    block_references = {
        (reference["source_type"], reference["source_id"])
        for block in data["composition"]["blocks"]
        for reference in block["provenance"]
    }
    manifest_references = {
        (reference["source_type"], reference["source_id"])
        for reference in data["composition"]["source_manifest"]
    }
    assert block_references == manifest_references
    assert db_session.query(Resume).count() == resumes_before
    assert "user_id" not in str(data)
    assert "email" not in str(data)
    assert "token" not in str(data)


def test_preview_uses_authenticated_identity_and_isolates_users(
    db_session,
    test_user,
    other_user,
    auth_headers,
) -> None:
    other_profile = create_profile(db_session, other_user.id, "Other User")
    other_job = create_job(db_session, other_user.id)
    add_profile_sources(db_session, other_profile.id, " Other")

    response = preview_request(auth_headers, other_profile.id, other_job.id)

    assert response.status_code == 404
    assert response.json() == UNAVAILABLE_RESPONSE


def test_missing_and_unauthorized_resources_have_uniform_responses(
    db_session,
    test_user,
    other_user,
    auth_headers,
) -> None:
    own_profile = create_profile(db_session, test_user.id, "Owner")
    own_job = create_job(db_session, test_user.id)
    other_profile = create_profile(db_session, other_user.id, "Other")
    other_job = create_job(db_session, other_user.id)

    missing_profile = preview_request(auth_headers, 999_999, own_job.id)
    unauthorized_profile = preview_request(auth_headers, other_profile.id, own_job.id)
    missing_job = preview_request(auth_headers, own_profile.id, 999_999)
    unauthorized_job = preview_request(auth_headers, own_profile.id, other_job.id)

    assert missing_profile.status_code == unauthorized_profile.status_code == 404
    assert missing_job.status_code == unauthorized_job.status_code == 404
    assert missing_profile.json() == unauthorized_profile.json() == UNAVAILABLE_RESPONSE
    assert missing_job.json() == unauthorized_job.json() == UNAVAILABLE_RESPONSE


def test_preview_isolates_profiles_and_does_not_fabricate_job_requirements(
    db_session,
    test_user,
    auth_headers,
) -> None:
    selected_profile = create_profile(db_session, test_user.id, "Selected")
    other_profile = create_profile(db_session, test_user.id, "Other")
    job = create_job(db_session, test_user.id, "Kubernetes e liderança técnica.")
    add_profile_sources(db_session, selected_profile.id, " Selected")
    add_profile_sources(db_session, other_profile.id, " Other")

    response = preview_request(auth_headers, selected_profile.id, job.id)

    assert response.status_code == 200
    values = factual_values(response.json())
    assert "Python Selected" in values
    assert "Python Other" not in values
    assert "Kubernetes" not in values
    assert "liderança técnica" not in values


def test_preview_returns_technologies_in_canonical_source_order(
    db_session,
    test_user,
    auth_headers,
) -> None:
    profile = create_profile(db_session, test_user.id, "Owner")
    job = create_job(db_session, test_user.id)
    add_profile_sources(db_session, profile.id)

    response = preview_request(auth_headers, profile.id, job.id)

    assert response.status_code == 200
    technology_source_ids = [
        block["provenance"][0]["source_id"]
        for block in response.json()["composition"]["blocks"]
        if block["section"] == "TECHNOLOGIES"
    ]
    assert technology_source_ids == sorted(technology_source_ids)
