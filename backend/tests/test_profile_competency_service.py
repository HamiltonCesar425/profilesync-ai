from datetime import date

import pytest

from domain.exceptions import DomainError
from models.professional_experience_model import ProfessionalExperienceModel
from models.profile_model import ProfileModel
from models.project_model import Project
from models.technology_model import TechnologyModel
from repositories.professional_experience_repository import (
    ProfessionalExperienceRepository,
)
from repositories.profile_repository import ProfileRepository
from repositories.project_repository import ProjectRepository
from repositories.technology_repository import TechnologyRepository
from services.profile_competency_service import ProfileCompetencyService


def create_service(db) -> ProfileCompetencyService:
    return ProfileCompetencyService(
        profile_repository=ProfileRepository(db),
        technology_repository=TechnologyRepository(db),
        experience_repository=ProfessionalExperienceRepository(db),
        project_repository=ProjectRepository(db),
    )


def test_aggregates_competencies_from_all_profile_sources(db_session, test_user):
    profile = ProfileModel(
        user_id=test_user.id,
        full_name="Competency User",
        professional_title="Backend Developer",
        summary="Profile used to test competency aggregation.",
        location=None,
        linkedin_url=None,
        github_url=None,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)

    db_session.add_all(
        [
            TechnologyModel(
                profile_id=profile.id,
                name="Python",
                category="Language",
                proficiency_level="Advanced",
            ),
            TechnologyModel(
                profile_id=profile.id,
                name=" python ",
                category="Language",
                proficiency_level="Advanced",
            ),
            ProfessionalExperienceModel(
                profile_id=profile.id,
                company_name="Example",
                position="FastAPI Developer",
                description="APIs with PostgreSQL and Docker.",
                start_date=date(2024, 1, 1),
                is_current=True,
            ),
            Project(
                profile_id=profile.id,
                name="Quality Pipeline",
                role="Developer",
                description="Automated tests with Pytest and Git.",
            ),
        ]
    )
    db_session.commit()

    competencies = create_service(db_session).get_profile_competencies(
        profile_id=profile.id,
        user_id=test_user.id,
    )

    assert competencies == [
        "Python",
        "docker",
        "fastapi",
        "postgresql",
        "git",
        "pytest",
        "tests",
    ]


def test_rejects_profile_owned_by_another_user(
    db_session, test_user, other_user
):
    profile = ProfileModel(
        user_id=other_user.id,
        full_name="Other User",
        professional_title="Developer",
        summary="Another profile.",
        location=None,
        linkedin_url=None,
        github_url=None,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)

    with pytest.raises(DomainError, match="Profile not found"):
        create_service(db_session).get_profile_competencies(
            profile_id=profile.id,
            user_id=test_user.id,
        )
