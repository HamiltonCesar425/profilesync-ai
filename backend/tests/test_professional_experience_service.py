from datetime import date, timedelta

import pytest

from models.profile_model import ProfileModel
from models.user_model import User
from repositories.professional_experience_repository import (
    ProfessionalExperienceRepository,
)
from repositories.profile_repository import ProfileRepository
from schemas.professional_experience_schema import (
    ProfessionalExperienceCreate,
    ProfessionalExperienceUpdate,
)
from services.professional_experience_service import (
    ProfessionalExperienceService,
)


@pytest.fixture
def db_session(reset_database):
    return reset_database


def create_service(db_session) -> ProfessionalExperienceService:
    return ProfessionalExperienceService(
        repository=ProfessionalExperienceRepository(db_session),
        profile_repository=ProfileRepository(db_session),
    )


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


def make_experience_create(
    **overrides,
) -> ProfessionalExperienceCreate:
    data = {
        "company_name": "Empresa Teste",
        "position": "Desenvolvedor Python",
        "employment_type": "PJ",
        "work_model": "Remoto",
        "location": "Campinas, SP",
        "description": "Desenvolvimento de APIs e pipelines de dados.",
        "start_date": date(2024, 1, 1),
        "end_date": None,
        "is_current": True,
    }

    data.update(overrides)

    return ProfessionalExperienceCreate(**data)


def test_create_experience(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    experience = service.create_experience(
        profile_id=profile.id,
        user_id=user.id,
        experience_data=make_experience_create(),
    )

    assert experience.id is not None
    assert experience.profile_id == profile.id
    assert experience.company_name == "Empresa Teste"
    assert experience.position == "Desenvolvedor Python"


def test_create_experience_raises_error_when_profile_not_found(db_session):
    user = create_user(db_session)
    service = create_service(db_session)

    with pytest.raises(ValueError, match="Perfil não encontrado."):
        service.create_experience(
            profile_id=999,
            user_id=user.id,
            experience_data=make_experience_create(),
        )


def test_create_experience_rejects_future_start_date(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    future_date = date.today() + timedelta(days=1)

    with pytest.raises(
        ValueError,
        match="A data de início não pode ser posterior à data atual.",
    ):
        service.create_experience(
            profile_id=profile.id,
            user_id=user.id,
            experience_data=make_experience_create(
                start_date=future_date,
            ),
        )


def test_create_experience_rejects_future_end_date(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    future_date = date.today() + timedelta(days=1)

    with pytest.raises(
        ValueError,
        match="A data de término não pode ser posterior à data atual.",
    ):
        service.create_experience(
            profile_id=profile.id,
            user_id=user.id,
            experience_data=make_experience_create(
                end_date=future_date,
                is_current=False,
            ),
        )


def test_create_experience_rejects_end_date_before_start_date(
    db_session,
):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    with pytest.raises(
        ValueError,
        match=("A data de término não pode ser anterior à data de início."),
    ):
        service.create_experience(
            profile_id=profile.id,
            user_id=user.id,
            experience_data=make_experience_create(
                start_date=date(2024, 2, 1),
                end_date=date(2024, 1, 1),
                is_current=False,
            ),
        )


def test_create_experience_rejects_current_with_end_date(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    with pytest.raises(
        ValueError,
        match=("Uma experiência atual não pode possuir data de término."),
    ):
        service.create_experience(
            profile_id=profile.id,
            user_id=user.id,
            experience_data=make_experience_create(
                end_date=date(2025, 1, 1),
                is_current=True,
            ),
        )


def test_create_experience_requires_end_date_when_not_current(
    db_session,
):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    with pytest.raises(
        ValueError,
        match=("Uma experiência encerrada deve possuir data de término."),
    ):
        service.create_experience(
            profile_id=profile.id,
            user_id=user.id,
            experience_data=make_experience_create(
                end_date=None,
                is_current=False,
            ),
        )


def test_list_experiences(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    service.create_experience(
        profile_id=profile.id,
        user_id=user.id,
        experience_data=make_experience_create(),
    )

    experiences = service.list_experiences(
        profile_id=profile.id,
        user_id=user.id,
    )

    assert len(experiences) == 1
    assert experiences[0].company_name == "Empresa Teste"


def test_list_experiences_raises_error_when_profile_not_found(db_session):
    user = create_user(db_session)
    service = create_service(db_session)

    with pytest.raises(ValueError, match="Perfil não encontrado."):
        service.list_experiences(
            profile_id=999,
            user_id=user.id,
        )


def test_get_experience(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    created_experience = service.create_experience(
        profile_id=profile.id,
        user_id=user.id,
        experience_data=make_experience_create(),
    )

    experience = service.get_experience(
        experience_id=created_experience.id,
        profile_id=profile.id,
        user_id=user.id,
    )

    assert experience.id == created_experience.id
    assert experience.profile_id == profile.id


def test_get_experience_raises_error_when_profile_not_found(
    db_session,
):
    user = create_user(db_session)
    service = create_service(db_session)

    with pytest.raises(
        ValueError,
        match="Perfil não encontrado.",
    ):
        service.get_experience(
            experience_id=999,
            profile_id=999,
            user_id=user.id,
        )


def test_get_experience_raises_error_when_experience_not_found(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    with pytest.raises(
        ValueError,
        match="Experiência profissional não encontrada.",
    ):
        service.get_experience(
            experience_id=999,
            profile_id=profile.id,
            user_id=user.id,
        )


def test_update_experience(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    experience = service.create_experience(
        profile_id=profile.id,
        user_id=user.id,
        experience_data=make_experience_create(),
    )

    updated_experience = service.update_experience(
        experience_id=experience.id,
        profile_id=profile.id,
        user_id=user.id,
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


def test_update_experience_rejects_future_start_date(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    experience = service.create_experience(
        profile_id=profile.id,
        user_id=user.id,
        experience_data=make_experience_create(),
    )

    future_date = date.today() + timedelta(days=1)

    with pytest.raises(
        ValueError,
        match="A data de início não pode ser posterior à data atual.",
    ):
        service.update_experience(
            experience_id=experience.id,
            profile_id=profile.id,
            user_id=user.id,
            experience_data=ProfessionalExperienceUpdate(
                start_date=future_date,
            ),
        )


def test_update_experience_rejects_finished_without_end_date(
    db_session,
):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    experience = service.create_experience(
        profile_id=profile.id,
        user_id=user.id,
        experience_data=make_experience_create(),
    )

    with pytest.raises(
        ValueError,
        match=("Uma experiência encerrada deve possuir data de término."),
    ):
        service.update_experience(
            experience_id=experience.id,
            profile_id=profile.id,
            user_id=user.id,
            experience_data=ProfessionalExperienceUpdate(
                is_current=False,
            ),
        )


def test_delete_experience(db_session):
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    experience = service.create_experience(
        profile_id=profile.id,
        user_id=user.id,
        experience_data=make_experience_create(),
    )

    service.delete_experience(
        experience_id=experience.id,
        profile_id=profile.id,
        user_id=user.id,
    )

    with pytest.raises(
        ValueError,
        match="Experiência profissional não encontrada.",
    ):
        service.get_experience(
            experience_id=experience.id,
            profile_id=profile.id,
            user_id=user.id,
        )
