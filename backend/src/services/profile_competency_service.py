from domain.exceptions import DomainError
from repositories.professional_experience_repository import (
    ProfessionalExperienceRepository,
)
from repositories.profile_repository import ProfileRepository
from repositories.project_repository import ProjectRepository
from repositories.technology_repository import TechnologyRepository
from services.job_requirement_extractor import JobRequirementExtractor


class ProfileCompetencyService:
    """Agrega competências estruturadas e detectadas nos dados de um perfil."""

    def __init__(
        self,
        profile_repository: ProfileRepository,
        technology_repository: TechnologyRepository,
        experience_repository: ProfessionalExperienceRepository,
        project_repository: ProjectRepository,
        requirement_extractor: JobRequirementExtractor | None = None,
    ) -> None:
        self.profile_repository = profile_repository
        self.technology_repository = technology_repository
        self.experience_repository = experience_repository
        self.project_repository = project_repository
        self.requirement_extractor = requirement_extractor or JobRequirementExtractor()

    def get_profile_competencies(
        self,
        profile_id: int,
        user_id: int,
    ) -> list[str]:
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=profile_id,
            user_id=user_id,
        )

        if profile is None:
            raise DomainError("Profile not found")

        competencies: list[str] = []
        seen: set[str] = set()

        def add_competency(value: str) -> None:
            competency = value.strip()
            normalized = competency.casefold()

            if not competency or normalized in seen:
                return

            seen.add(normalized)
            competencies.append(competency)

        technologies = self.technology_repository.list_by_profile_id(profile_id)
        for technology in technologies:
            add_competency(technology.name)

        experiences = self.experience_repository.list_by_profile_id(profile_id)
        experience_text = " ".join(
            part
            for experience in experiences
            for part in (experience.position, experience.description)
            if part
        )
        for competency in self.requirement_extractor.extract(experience_text):
            add_competency(competency)

        projects = self.project_repository.list_by_profile_id(profile_id)
        project_text = " ".join(
            part
            for project in projects
            for part in (project.name, project.role, project.description)
            if part
        )
        for competency in self.requirement_extractor.extract(project_text):
            add_competency(competency)

        return competencies
