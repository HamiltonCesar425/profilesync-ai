from database import Base, engine, SessionLocal
from repositories.profile_repository import ProfileRepository


def setup_function() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_profile() -> None:
    db = SessionLocal()
    repository = ProfileRepository(db)

    profile = repository.create(
        full_name="Hamilton Cesar",
        professional_title="Desenvolvedor Python",
        summary="Perfil profissional em evolução.",
        location="Campinas, SP",
        linkedin_url="https://linkedin.com/in/hamilton",
        github_url="https://github.com/HamiltonCesar425",
    )

    assert profile.id is not None
    assert profile.full_name == "Hamilton Cesar"
    assert profile.professional_title == "Desenvolvedor Python"
    assert profile.summary == "Perfil profissional em evolução."
    assert profile.location == "Campinas, SP"
    assert profile.linkedin_url == "https://linkedin.com/in/hamilton"
    assert profile.github_url == "https://github.com/HamiltonCesar425"

    db.close()


def test_list_all_profiles() -> None:
    db = SessionLocal()
    repository = ProfileRepository(db)

    repository.create(
        full_name="Hamilton Cesar",
        professional_title="Desenvolvedor Python",
        summary="Primeiro perfil.",
    )

    repository.create(
        full_name="Ana Silva",
        professional_title="Cientista de Dados",
        summary="Segundo perfil.",
    )

    profiles = repository.list_all()

    assert len(profiles) == 2
    assert profiles[0].full_name == "Hamilton Cesar"
    assert profiles[1].full_name == "Ana Silva"

    db.close()


def test_get_by_id_existing_profile() -> None:
    db = SessionLocal()
    repository = ProfileRepository(db)

    created_profile = repository.create(
        full_name="Hamilton Cesar",
        professional_title="Desenvolvedor Python",
        summary="Perfil existente.",
    )

    found_profile = repository.get_by_id(created_profile.id)

    assert found_profile is not None
    assert found_profile.id == created_profile.id
    assert found_profile.full_name == "Hamilton Cesar"

    db.close()


def test_get_by_id_non_existing_profile() -> None:
    db = SessionLocal()
    repository = ProfileRepository(db)

    profile = repository.get_by_id(999)

    assert profile is None

    db.close()
