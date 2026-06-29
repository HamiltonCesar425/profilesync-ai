from sqlalchemy.orm import Session

from models.project_model import Project
from schemas.project_schema import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, project_data: ProjectCreate) -> Project:
        project = Project(**self._dump_project_data(project_data))
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def list_by_profile_id(self, profile_id: int) -> list[Project]:
        return (
            self.db.query(Project)
            .filter(Project.profile_id == profile_id)
            .order_by(Project.id)
            .all()
        )

    def get_by_id(self, project_id: int) -> Project | None:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_by_id_and_profile_id(
        self,
        project_id: int,
        profile_id: int,
    ) -> Project | None:
        return (
            self.db.query(Project)
            .filter(
                Project.id == project_id,
                Project.profile_id == profile_id,
            )
            .first()
        )

    def update(
        self,
        project: Project,
        project_data: ProjectUpdate,
    ) -> Project:
        update_data = self._dump_project_data(project_data, exclude_unset=True)

        for field, value in update_data.items():
            setattr(project, field, value)

        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: Project) -> None:
        self.db.delete(project)
        self.db.commit()

    @staticmethod
    def _dump_project_data(
        project_data: ProjectCreate | ProjectUpdate,
        exclude_unset: bool = False,
    ) -> dict:
        data = project_data.model_dump(exclude_unset=exclude_unset)

        for url_field in ("repository_url", "demo_url"):
            if data.get(url_field) is not None:
                data[url_field] = str(data[url_field])

        return data
