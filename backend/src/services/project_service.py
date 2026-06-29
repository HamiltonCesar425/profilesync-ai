from models.project_model import Project
from repositories.profile_repository import ProfileRepository
from repositories.project_repository import ProjectRepository
from schemas.project_schema import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(
        self,
        project_repository: ProjectRepository,
        profile_repository: ProfileRepository,
    ) -> None:
        self.project_repository = project_repository
        self.profile_repository = profile_repository

    def create_project(
        self,
        project_data: ProjectCreate,
        user_id: int,
    ) -> Project:
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=project_data.profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise ValueError("Profile not found or access denied")

        return self.project_repository.create(project_data)

    def list_projects_by_profile(
        self,
        profile_id: int,
        user_id: int,
    ) -> list[Project]:
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise ValueError("Profile not found or access denied")

        return self.project_repository.list_by_profile_id(profile_id)

    def get_project(
        self,
        project_id: int,
        profile_id: int,
        user_id: int,
    ) -> Project:
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise ValueError("Profile not found or access denied")

        project = self.project_repository.get_by_id_and_profile_id(
            project_id=project_id,
            profile_id=profile_id,
        )

        if project is None:
            raise ValueError("Project not found")

        return project

    def update_project(
        self,
        project_id: int,
        profile_id: int,
        project_data: ProjectUpdate,
        user_id: int,
    ) -> Project:
        project = self.get_project(
            project_id=project_id,
            profile_id=profile_id,
            user_id=user_id,
        )

        return self.project_repository.update(project, project_data)

    def delete_project(
        self,
        project_id: int,
        profile_id: int,
        user_id: int,
    ) -> None:
        project = self.get_project(
            project_id=project_id,
            profile_id=profile_id,
            user_id=user_id,
        )

        self.project_repository.delete(project)
