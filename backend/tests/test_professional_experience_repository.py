from datetime import date

import pytest

from models.profile_model import ProfileModel
from models.user_model import User
from repositories.professional_experience_repository import (
    ProfessionalExperienceRepository,
)
from schemas.professional_experience_schema import (
    ProfessionalExperienceCreate,
    ProfessionalExperienceUpdate,
)


@pytest.fixture
def db_session(reset_database):
    return reset_database


def create_user(db_session, email: str = "user@example.com") -> User:
    user = User(email=email, hashed_password="hashed-password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def create_profile(db_session, user_id: int) -> ProfileModel:
    profile = ProfileModel(
        full_name="TestUser",
        professional_title="Desenvolvedor Full Stack",
        summary="Resumo profissional.",
        location="Citytest, SP",
        linkedin_url=None,
        github_url=None,
        user_id=user_id,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)
    return profile


def make_experience_create() -> ProfessionalExperienceCreate:
    return ProfessionalExperienceCreate(
        company_name="Empresa Teste",
        position="Desenvolvedor Python",
        employment_type="PJ",
        work_model="Remoto",
        location="Campinas, SP",
        description="Desenvolvimento de APIs e pipelines de dados.",
        start_date=date(2024, 1, 1),
        end_date=None,
        is_current=True,
    )


def test_create_professional_experience(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    repository = ProfessionalExperienceRepository(db_session)

    experience = repository.create(
        profile_id=profile.id,
        experience_data=make_experience_create(),
    )

    assert experience.id is not None
    assert experience.profile_id == profile.id
    assert experience.company_name == "Empresa Teste"
    assert experience.position == "Desenvolvedor Python"
    assert experience.is_current is True


def test_list_by_profile_id_returns_only_profile_experiences(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    other_profile = create_profile(db_session, user.id)

    repository = ProfessionalExperienceRepository(db_session)

    first_experience = repository.create(
        profile_id=profile.id,
        experience_data=make_experience_create(),
    )
    repository.create(
        profile_id=other_profile.id,
        experience_data=ProfessionalExperienceCreate(
            company_name="Outra Empresa",
            position="Analista de Dados",
            employment_type="CLT",
            work_model="Híbrido",
            location="São Paulo, SP",
            description="Análise de dados.",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
            is_current=False,
        ),
    )

    experiences = repository.list_by_profile_id(profile.id)

    assert len(experiences) == 1
    assert experiences[0].id == first_experience.id


def test_get_by_id_returns_professional_experience(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    repository = ProfessionalExperienceRepository(db_session)

    created_experience = repository.create(
        profile_id=profile.id,
        experience_data=make_experience_create(),
    )

    experience = repository.get_by_id(created_experience.id)

    assert experience is not None
    assert experience.id == created_experience.id


def test_get_by_id_returns_none_when_not_found(db_session):
    repository = ProfessionalExperienceRepository(db_session)

    experience = repository.get_by_id(999)

    assert experience is None


def test_get_by_id_and_profile_id_returns_professional_experience(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    repository = ProfessionalExperienceRepository(db_session)

    created_experience = repository.create(
        profile_id=profile.id,
        experience_data=make_experience_create(),
    )

    experience = repository.get_by_id_and_profile_id(
        experience_id=created_experience.id,
        profile_id=profile.id,
    )

    assert experience is not None
    assert experience.id == created_experience.id


def test_get_by_id_and_profile_id_returns_none_for_wrong_profile(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    other_profile = create_profile(db_session, user.id)
    repository = ProfessionalExperienceRepository(db_session)

    created_experience = repository.create(
        profile_id=profile.id,
        experience_data=make_experience_create(),
    )

    experience = repository.get_by_id_and_profile_id(
        experience_id=created_experience.id,
        profile_id=other_profile.id,
    )

    assert experience is None


def test_update_professional_experience(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    repository = ProfessionalExperienceRepository(db_session)

    experience = repository.create(
        profile_id=profile.id,
        experience_data=make_experience_create(),
    )

    updated_experience = repository.update(
        experience=experience,
        experience_data=ProfessionalExperienceUpdate(
            company_name="Empresa Atualizada",
            position="Engenheiro de Software",
            employment_type="CLT",
            work_model="Híbrido",
            location="São Paulo, SP",
            description="Atuação em backend e dados.",
            start_date=date(2024, 2, 1),
            end_date=date(2025, 2, 1),
            is_current=False,
        ),
    )

    assert updated_experience.company_name == "Empresa Atualizada"
    assert updated_experience.position == "Engenheiro de Software"
    assert updated_experience.is_current is False
    assert updated_experience.end_date == date(2025, 2, 1)


def test_delete_professional_experience(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    repository = ProfessionalExperienceRepository(db_session)

    experience = repository.create(
        profile_id=profile.id,
        experience_data=make_experience_create(),
    )

    repository.delete(experience)

    deleted_experience = repository.get_by_id(experience.id)

    assert deleted_experience is None
