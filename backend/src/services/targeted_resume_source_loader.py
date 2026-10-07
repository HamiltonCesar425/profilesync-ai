from domain.targeted_resume import (
    AuthorizedCompositionSources,
    JobContext,
    ProfessionalExperienceFacts,
    ProfileFacts,
    ProjectFacts,
    TechnologyFacts,
)
from repositories.job_repository import JobRepository
from repositories.professional_experience_repository import (
    ProfessionalExperienceRepository,
)
from repositories.profile_repository import ProfileRepository
from repositories.project_repository import ProjectRepository
from repositories.technology_repository import TechnologyRepository


class AuthorizedCompositionSourcesUnavailableError(Exception):
    """Raised when the requested source context is unavailable to the user."""


class TargetedResumeSourceLoader:
    """Load authorized persisted state into immutable factual snapshots."""

    def __init__(
        self,
        profile_repository: ProfileRepository,
        job_repository: JobRepository,
        experience_repository: ProfessionalExperienceRepository,
        project_repository: ProjectRepository,
        technology_repository: TechnologyRepository,
    ) -> None:
        self.profile_repository = profile_repository
        self.job_repository = job_repository
        self.experience_repository = experience_repository
        self.project_repository = project_repository
        self.technology_repository = technology_repository

    def load(
        self,
        *,
        profile_id: int,
        job_id: int,
        authenticated_user_id: int,
    ) -> AuthorizedCompositionSources:
        profile = self.profile_repository.get_by_id_and_user_id(
            profile_id=profile_id,
            user_id=authenticated_user_id,
        )
        if profile is None:
            raise AuthorizedCompositionSourcesUnavailableError(
                "Authorized composition sources are unavailable."
            )

        job = self.job_repository.get_by_id_and_user_id(
            job_id=job_id,
            user_id=authenticated_user_id,
        )
        if job is None:
            raise AuthorizedCompositionSourcesUnavailableError(
                "Authorized composition sources are unavailable."
            )

        experiences = self.experience_repository.list_by_profile_id(profile_id)
        projects = self.project_repository.list_by_profile_id(profile_id)
        technologies = self.technology_repository.list_by_profile_id(profile_id)

        return AuthorizedCompositionSources(
            authenticated_user_id=authenticated_user_id,
            profile=ProfileFacts(
                source_id=profile.id,
                user_id=profile.user_id,
                full_name=profile.full_name,
                professional_title=profile.professional_title,
                summary=profile.summary,
                location=profile.location,
                linkedin_url=profile.linkedin_url,
                github_url=profile.github_url,
            ),
            job=JobContext(
                source_id=job.id,
                user_id=job.user_id,
                title=job.title,
                description=job.description,
            ),
            professional_experiences=tuple(
                ProfessionalExperienceFacts(
                    source_id=experience.id,
                    profile_id=experience.profile_id,
                    company_name=experience.company_name,
                    position=experience.position,
                    start_date=experience.start_date,
                    employment_type=experience.employment_type,
                    work_model=experience.work_model,
                    location=experience.location,
                    description=experience.description,
                    end_date=experience.end_date,
                    is_current=experience.is_current,
                )
                for experience in experiences
            ),
            projects=tuple(
                ProjectFacts(
                    source_id=project.id,
                    profile_id=project.profile_id,
                    name=project.name,
                    description=project.description,
                    role=project.role,
                    repository_url=project.repository_url,
                    demo_url=project.demo_url,
                    start_date=project.start_date,
                    end_date=project.end_date,
                    is_current=project.is_current,
                )
                for project in projects
            ),
            technologies=tuple(
                TechnologyFacts(
                    source_id=technology.id,
                    profile_id=technology.profile_id,
                    name=technology.name,
                    category=technology.category,
                    proficiency_level=technology.proficiency_level,
                    years_experience=technology.years_experience,
                )
                for technology in technologies
            ),
        )
