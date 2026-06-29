from datetime import date

import pytest

from models.profile_model import ProfileModel
from models.project_model import Project
from models.user_model import User
from repositories.profile_repository import ProfileRepository
from repositories.project_repository import ProjectRepository
from schemas.project_schema import ProjectCreate, ProjectUpdate
from services.project_service import ProjectService


def create_user(db_session, email="user@example.com"):
    user = User(
        email=email,
        hashed_password="hashed-password",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def create_profile(db_session, user_id: int):
    profile = ProfileModel(
        user_id=user_id,
        full_name="Maria Aparecida",
        professional_title="Desenvolvedor Backend",
        summary="Perfil profissional de teste.",
        location="CityTest, SP",
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)
    return profile


def create_service(db_session):
    return ProjectService(
        project_repository=ProjectRepository(db_session),
        profile_repository=ProfileRepository(db_session),
    )


def create_project(db_session, profile_id: int):
    project = Project(
        profile_id=profile_id,
        name="ProfileSync AI",
        description="Sistema de gestão de perfil profissional.",
        repository_url="https://github.com/example/profilesync-ai",
        demo_url="https://profilesync.example.com",
        start_date=date(2026, 6, 1),
        end_date=None,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project


def test_create_project_success(reset_database):
    db_session = reset_database
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    service = create_service(db_session)

    payload = ProjectCreate(
        profile_id=profile.id,
        name="ProfileSync AI",
        description="Sistema de gestão de perfil profissional.",
        repository_url="https://github.com/example/profilesync-ai",
        demo_url="https://profilesync.example.com",
        start_date="2026-06-01",
        end_date=None,
    )

    project = service.create_project(payload, user.id)

    assert project.id is not None
    assert project.profile_id == profile.id
    assert project.name == payload.name
    assert project.description == payload.description
    assert project.repository_url == str(payload.repository_url)
    assert project.demo_url == str(payload.demo_url)
    assert project.start_date == payload.start_date


def test_create_project_rejects_profile_from_another_user(reset_database):
    db_session = reset_database
    owner = create_user(db_session, "owner@example.com")
    intruder = create_user(db_session, "intruder@example.com")
    profile = create_profile(db_session, owner.id)
    service = create_service(db_session)

    payload = ProjectCreate(
        profile_id=profile.id,
        name="Projeto Indevido",
        description="Tentativa de usar perfil de outro usuário.",
        repository_url=None,
        demo_url=None,
        start_date=None,
        end_date=None,
    )

    with pytest.raises(ValueError, match="Profile not found"):
        service.create_project(payload, intruder.id)


def test_list_projects_by_profile_success(reset_database):
    db_session = reset_database
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    project = create_project(db_session, profile.id)
    service = create_service(db_session)

    projects = service.list_projects_by_profile(profile.id, user.id)

    assert len(projects) == 1
    assert projects[0].id == project.id
    assert projects[0].profile_id == profile.id


def test_get_project_success(reset_database):
    db_session = reset_database
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    project = create_project(db_session, profile.id)
    service = create_service(db_session)

    result = service.get_project(
        project_id=project.id,
        profile_id=profile.id,
        user_id=user.id,
    )

    assert result.id == project.id
    assert result.name == project.name


def test_get_project_rejects_other_user(reset_database):
    db_session = reset_database
    owner = create_user(db_session, "owner@example.com")
    intruder = create_user(db_session, "intruder@example.com")
    profile = create_profile(db_session, owner.id)
    project = create_project(db_session, profile.id)
    service = create_service(db_session)

    with pytest.raises(ValueError, match="Profile not found"):
        service.get_project(
            project_id=project.id,
            profile_id=profile.id,
            user_id=intruder.id,
        )


def test_update_project_success(reset_database):
    db_session = reset_database
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    project = create_project(db_session, profile.id)
    service = create_service(db_session)

    payload = ProjectUpdate(
        name="ProfileSync AI Atualizado",
        description="Descrição atualizada.",
        repository_url="https://github.com/example/updated",
        demo_url=None,
        start_date="2026-06-10",
        end_date=None,
    )

    updated = service.update_project(
        project_id=project.id,
        profile_id=profile.id,
        project_data=payload,
        user_id=user.id,
    )

    assert updated.id == project.id
    assert updated.name == payload.name
    assert updated.description == payload.description
    assert updated.repository_url == str(payload.repository_url)
    assert updated.demo_url is None
    assert updated.start_date == payload.start_date


def test_update_project_rejects_other_user(reset_database):
    db_session = reset_database
    owner = create_user(db_session, "owner@example.com")
    intruder = create_user(db_session, "intruder@example.com")
    profile = create_profile(db_session, owner.id)
    project = create_project(db_session, profile.id)
    service = create_service(db_session)

    payload = ProjectUpdate(name="Alteração indevida")

    with pytest.raises(ValueError, match="Profile not found"):
        service.update_project(
            project_id=project.id,
            profile_id=profile.id,
            project_data=payload,
            user_id=intruder.id,
        )


def test_delete_project_success(reset_database):
    db_session = reset_database
    user = create_user(db_session)
    profile = create_profile(db_session, user.id)
    project = create_project(db_session, profile.id)
    service = create_service(db_session)

    service.delete_project(
        project_id=project.id,
        profile_id=profile.id,
        user_id=user.id,
    )

    deleted_project = db_session.query(Project).filter(Project.id == project.id).first()

    assert deleted_project is None


def test_delete_project_rejects_other_user(reset_database):
    db_session = reset_database
    owner = create_user(db_session, "owner@example.com")
    intruder = create_user(db_session, "intruder@example.com")
    profile = create_profile(db_session, owner.id)
    project = create_project(db_session, profile.id)
    service = create_service(db_session)

    with pytest.raises(ValueError, match="Profile not found"):
        service.delete_project(
            project_id=project.id,
            profile_id=profile.id,
            user_id=intruder.id,
        )
