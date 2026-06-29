from models.profile_model import ProfileModel
from models.user_model import User
from schemas.project_schema import ProjectCreate, ProjectUpdate
from repositories.project_repository import ProjectRepository


def create_test_user(db):
    user = User(
        email="project-user@example.com",
        hashed_password="hashed-password",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_profile(db, user_id: int):
    profile = ProfileModel(
        user_id=user_id,
        full_name="Project User",
        professional_title="Backend Developer",
        summary="Developer profile for project repository tests.",
        location="Campinas, SP",
        linkedin_url="https://linkedin.com/in/project-user",
        github_url="https://github.com/project-user",
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def test_create_project(reset_database):
    db = reset_database
    user = create_test_user(db)
    test_profile = create_test_profile(db, user.id)
    repository = ProjectRepository(db)

    project_data = ProjectCreate(
        profile_id=test_profile.id,
        name="ProfileSync AI",
        description="API para gestão profissional assistida por IA.",
        role="Backend Developer",
        repository_url="https://github.com/example/profilesync-ai",
        demo_url="https://profilesync-ai.example.com",
        is_current=True,
    )

    project = repository.create(project_data)

    assert project.id is not None
    assert project.profile_id == test_profile.id
    assert project.name == "ProfileSync AI"
    assert project.is_current is True


def test_list_projects_by_profile_id(reset_database):
    db = reset_database
    user = create_test_user(db)
    test_profile = create_test_profile(db, user.id)
    repository = ProjectRepository(db)

    first_project = ProjectCreate(
        profile_id=test_profile.id,
        name="Project One",
        role="Developer",
    )
    second_project = ProjectCreate(
        profile_id=test_profile.id,
        name="Project Two",
        role="Developer",
    )

    repository.create(first_project)
    repository.create(second_project)

    projects = repository.list_by_profile_id(test_profile.id)

    assert len(projects) == 2
    assert projects[0].name == "Project One"
    assert projects[1].name == "Project Two"


def test_get_project_by_id(reset_database):
    db = reset_database
    user = create_test_user(db)
    test_profile = create_test_profile(db, user.id)
    repository = ProjectRepository(db)

    project = repository.create(
        ProjectCreate(
            profile_id=test_profile.id,
            name="Project Lookup",
            role="Developer",
        )
    )

    found_project = repository.get_by_id(project.id)

    assert found_project is not None
    assert found_project.id == project.id
    assert found_project.name == "Project Lookup"


def test_get_project_by_id_returns_none_when_not_found(reset_database):
    repository = ProjectRepository(reset_database)

    project = repository.get_by_id(999_999)

    assert project is None


def test_get_project_by_id_and_profile_id(reset_database):
    db = reset_database
    user = create_test_user(db)
    test_profile = create_test_profile(db, user.id)
    repository = ProjectRepository(db)

    project = repository.create(
        ProjectCreate(
            profile_id=test_profile.id,
            name="Scoped Project",
            role="Developer",
        )
    )

    found_project = repository.get_by_id_and_profile_id(
        project_id=project.id,
        profile_id=test_profile.id,
    )

    assert found_project is not None
    assert found_project.id == project.id
    assert found_project.profile_id == test_profile.id


def test_get_project_by_id_and_profile_id_returns_none_for_wrong_profile(
    reset_database,
):
    db = reset_database
    user = create_test_user(db)
    test_profile = create_test_profile(db, user.id)
    repository = ProjectRepository(db)

    project = repository.create(
        ProjectCreate(
            profile_id=test_profile.id,
            name="Private Project",
            role="Developer",
        )
    )

    found_project = repository.get_by_id_and_profile_id(
        project_id=project.id,
        profile_id=999_999,
    )

    assert found_project is None


def test_update_project(reset_database):
    db = reset_database
    user = create_test_user(db)
    test_profile = create_test_profile(db, user.id)
    repository = ProjectRepository(db)

    project = repository.create(
        ProjectCreate(
            profile_id=test_profile.id,
            name="Old Project Name",
            role="Old Role",
            is_current=False,
        )
    )

    updated_project = repository.update(
        project=project,
        project_data=ProjectUpdate(
            name="New Project Name",
            role="Tech Lead",
            is_current=True,
        ),
    )

    assert updated_project.id == project.id
    assert updated_project.name == "New Project Name"
    assert updated_project.role == "Tech Lead"
    assert updated_project.is_current is True


def test_delete_project(reset_database):
    db = reset_database
    user = create_test_user(db)
    test_profile = create_test_profile(db, user.id)
    repository = ProjectRepository(db)

    project = repository.create(
        ProjectCreate(
            profile_id=test_profile.id,
            name="Project To Delete",
            role="Developer",
        )
    )

    repository.delete(project)

    deleted_project = repository.get_by_id(project.id)

    assert deleted_project is None
