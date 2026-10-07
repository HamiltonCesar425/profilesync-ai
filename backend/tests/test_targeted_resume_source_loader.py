from datetime import date
from types import SimpleNamespace

import pytest

from domain.targeted_resume import (
    AuthorizedCompositionSources,
    JobContext,
    ProfessionalExperienceFacts,
    ProfileFacts,
    ProjectFacts,
    TechnologyFacts,
)
from models.job_model import JobModel
from models.professional_experience_model import ProfessionalExperienceModel
from models.profile_model import ProfileModel
from models.project_model import Project
from models.technology_model import TechnologyModel
from models.user_model import User
from repositories.job_repository import JobRepository
from repositories.professional_experience_repository import (
    ProfessionalExperienceRepository,
)
from repositories.profile_repository import ProfileRepository
from repositories.project_repository import ProjectRepository
from repositories.technology_repository import TechnologyRepository
from services.targeted_resume_source_loader import (
    AuthorizedCompositionSourcesUnavailableError,
    TargetedResumeSourceLoader,
)


UNAVAILABLE_MESSAGE = "Authorized composition sources are unavailable."


def create_user(db_session, email: str) -> User:
    user = User(email=email, hashed_password="hashed-password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def create_profile(db_session, user_id: int, name: str) -> ProfileModel:
    profile = ProfileModel(
        user_id=user_id,
        full_name=name,
        professional_title="Backend Engineer",
        summary="Desenvolve serviços Python.",
        location=None,
        linkedin_url=None,
        github_url="https://github.com/example",
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)
    return profile


def create_job(db_session, user_id: int, title: str = "Backend Engineer") -> JobModel:
    job = JobModel(
        user_id=user_id,
        title=title,
        company=None,
        description="Python, Kubernetes e liderança técnica.",
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)
    return job


def create_loader(db_session) -> TargetedResumeSourceLoader:
    return TargetedResumeSourceLoader(
        profile_repository=ProfileRepository(db_session),
        job_repository=JobRepository(db_session),
        experience_repository=ProfessionalExperienceRepository(db_session),
        project_repository=ProjectRepository(db_session),
        technology_repository=TechnologyRepository(db_session),
    )


def assert_sources_unavailable(
    loader: TargetedResumeSourceLoader,
    *,
    profile_id: int,
    job_id: int,
    authenticated_user_id: int,
) -> None:
    with pytest.raises(AuthorizedCompositionSourcesUnavailableError) as exc_info:
        loader.load(
            profile_id=profile_id,
            job_id=job_id,
            authenticated_user_id=authenticated_user_id,
        )

    assert str(exc_info.value) == UNAVAILABLE_MESSAGE


def add_factual_sources(db_session, profile_id: int, suffix: str = "") -> tuple:
    experience = ProfessionalExperienceModel(
        profile_id=profile_id,
        company_name=f"Analytical Engines{suffix}",
        position="Backend Engineer",
        employment_type=None,
        work_model="Remote",
        location=None,
        description="Desenvolveu serviços Python.",
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        is_current=False,
    )
    project = Project(
        profile_id=profile_id,
        name=f"API Platform{suffix}",
        description="",
        role=None,
        repository_url=None,
        demo_url=None,
        start_date=None,
        end_date=None,
        is_current=False,
    )
    technology = TechnologyModel(
        profile_id=profile_id,
        name=f"Python{suffix}",
        category="Language",
        proficiency_level="Advanced",
        years_experience=0,
    )
    db_session.add_all([experience, project, technology])
    db_session.commit()
    for source in (experience, project, technology):
        db_session.refresh(source)
    return experience, project, technology


def test_loads_complete_authorized_persisted_state_with_literal_mapping(
    db_session,
) -> None:
    user = create_user(db_session, "owner@example.com")
    profile = create_profile(db_session, user.id, "Ada Lovelace")
    job = create_job(db_session, user.id)
    experience, project, technology = add_factual_sources(db_session, profile.id)

    sources = create_loader(db_session).load(
        profile_id=profile.id,
        job_id=job.id,
        authenticated_user_id=user.id,
    )

    assert sources == AuthorizedCompositionSources(
        authenticated_user_id=user.id,
        profile=ProfileFacts(
            source_id=profile.id,
            user_id=user.id,
            full_name="Ada Lovelace",
            professional_title="Backend Engineer",
            summary="Desenvolve serviços Python.",
            location=None,
            linkedin_url=None,
            github_url="https://github.com/example",
        ),
        job=JobContext(
            source_id=job.id,
            user_id=user.id,
            title="Backend Engineer",
            description="Python, Kubernetes e liderança técnica.",
        ),
        professional_experiences=(
            ProfessionalExperienceFacts(
                source_id=experience.id,
                profile_id=profile.id,
                company_name="Analytical Engines",
                position="Backend Engineer",
                start_date=date(2023, 1, 1),
                employment_type=None,
                work_model="Remote",
                location=None,
                description="Desenvolveu serviços Python.",
                end_date=date(2024, 1, 1),
                is_current=False,
            ),
        ),
        projects=(
            ProjectFacts(
                source_id=project.id,
                profile_id=profile.id,
                name="API Platform",
                description="",
                role=None,
                repository_url=None,
                demo_url=None,
                start_date=None,
                end_date=None,
                is_current=False,
            ),
        ),
        technologies=(
            TechnologyFacts(
                source_id=technology.id,
                profile_id=profile.id,
                name="Python",
                category="Language",
                proficiency_level="Advanced",
                years_experience=0,
            ),
        ),
    )


def test_rejects_profile_owned_by_another_user(db_session) -> None:
    owner = create_user(db_session, "owner@example.com")
    intruder = create_user(db_session, "intruder@example.com")
    profile = create_profile(db_session, owner.id, "Owner")
    job = create_job(db_session, intruder.id)

    assert_sources_unavailable(
        create_loader(db_session),
        profile_id=profile.id,
        job_id=job.id,
        authenticated_user_id=intruder.id,
    )


def test_rejects_job_owned_by_another_user(db_session) -> None:
    owner = create_user(db_session, "owner@example.com")
    intruder = create_user(db_session, "intruder@example.com")
    profile = create_profile(db_session, owner.id, "Owner")
    job = create_job(db_session, intruder.id)

    assert_sources_unavailable(
        create_loader(db_session),
        profile_id=profile.id,
        job_id=job.id,
        authenticated_user_id=owner.id,
    )


def test_rejects_cross_user_profile_and_job_combination(db_session) -> None:
    first_user = create_user(db_session, "first@example.com")
    second_user = create_user(db_session, "second@example.com")
    profile = create_profile(db_session, first_user.id, "First")
    job = create_job(db_session, second_user.id)

    assert_sources_unavailable(
        create_loader(db_session),
        profile_id=profile.id,
        job_id=job.id,
        authenticated_user_id=first_user.id,
    )


def test_isolates_factual_sources_between_profiles_of_same_user(db_session) -> None:
    user = create_user(db_session, "owner@example.com")
    selected_profile = create_profile(db_session, user.id, "Selected")
    other_profile = create_profile(db_session, user.id, "Other")
    job = create_job(db_session, user.id)
    selected_sources = add_factual_sources(db_session, selected_profile.id, " Selected")
    add_factual_sources(db_session, other_profile.id, " Other")

    sources = create_loader(db_session).load(
        profile_id=selected_profile.id,
        job_id=job.id,
        authenticated_user_id=user.id,
    )

    assert [source.source_id for source in sources.professional_experiences] == [
        selected_sources[0].id
    ]
    assert [source.source_id for source in sources.projects] == [selected_sources[1].id]
    assert [source.source_id for source in sources.technologies] == [
        selected_sources[2].id
    ]


def test_isolates_factual_sources_between_users(db_session) -> None:
    owner = create_user(db_session, "owner@example.com")
    other_user = create_user(db_session, "other@example.com")
    owner_profile = create_profile(db_session, owner.id, "Owner")
    other_profile = create_profile(db_session, other_user.id, "Other")
    job = create_job(db_session, owner.id)
    owner_sources = add_factual_sources(db_session, owner_profile.id, " Owner")
    add_factual_sources(db_session, other_profile.id, " Other")

    sources = create_loader(db_session).load(
        profile_id=owner_profile.id,
        job_id=job.id,
        authenticated_user_id=owner.id,
    )

    assert [source.source_id for source in sources.professional_experiences] == [
        owner_sources[0].id
    ]
    assert [source.source_id for source in sources.projects] == [owner_sources[1].id]
    assert [source.source_id for source in sources.technologies] == [
        owner_sources[2].id
    ]


def test_rejects_missing_profile(db_session) -> None:
    user = create_user(db_session, "owner@example.com")
    job = create_job(db_session, user.id)

    assert_sources_unavailable(
        create_loader(db_session),
        profile_id=999_999,
        job_id=job.id,
        authenticated_user_id=user.id,
    )


def test_rejects_missing_job(db_session) -> None:
    user = create_user(db_session, "owner@example.com")
    profile = create_profile(db_session, user.id, "Owner")

    assert_sources_unavailable(
        create_loader(db_session),
        profile_id=profile.id,
        job_id=999_999,
        authenticated_user_id=user.id,
    )


def test_accepts_empty_factual_collections(db_session) -> None:
    user = create_user(db_session, "owner@example.com")
    profile = create_profile(db_session, user.id, "Owner")
    job = create_job(db_session, user.id)

    sources = create_loader(db_session).load(
        profile_id=profile.id,
        job_id=job.id,
        authenticated_user_id=user.id,
    )

    assert sources.professional_experiences == ()
    assert sources.projects == ()
    assert sources.technologies == ()


class SpyChildRepository:
    def __init__(self) -> None:
        self.calls = 0

    def list_by_profile_id(self, profile_id: int) -> list:
        self.calls += 1
        return []


class StubAuthorizedRepository:
    def __init__(self, result) -> None:
        self.result = result
        self.calls = 0

    def get_by_id_and_user_id(self, **kwargs):
        self.calls += 1
        return self.result


@pytest.mark.parametrize("failed_authorization", ["profile", "job"])
def test_does_not_query_child_sources_when_authorization_fails(
    failed_authorization,
) -> None:
    profile = SimpleNamespace(
        id=11,
        user_id=7,
        full_name="Ada Lovelace",
        professional_title="Backend Engineer",
        summary="Resumo",
        location=None,
        linkedin_url=None,
        github_url=None,
    )
    job = SimpleNamespace(
        id=21,
        user_id=7,
        title="Backend Engineer",
        description="Python",
    )
    profile_repository = StubAuthorizedRepository(
        None if failed_authorization == "profile" else profile
    )
    job_repository = StubAuthorizedRepository(
        None if failed_authorization == "job" else job
    )
    child_repositories = [SpyChildRepository() for _ in range(3)]
    loader = TargetedResumeSourceLoader(
        profile_repository=profile_repository,
        job_repository=job_repository,
        experience_repository=child_repositories[0],
        project_repository=child_repositories[1],
        technology_repository=child_repositories[2],
    )

    with pytest.raises(AuthorizedCompositionSourcesUnavailableError):
        loader.load(profile_id=11, job_id=21, authenticated_user_id=7)

    assert all(repository.calls == 0 for repository in child_repositories)
    assert profile_repository.calls == 1
    assert job_repository.calls == (0 if failed_authorization == "profile" else 1)
