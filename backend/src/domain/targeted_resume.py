from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Literal


COMPOSITION_RULESET_VERSION = "targeted-resume-factual-v1"


class FactualSourceType(str, Enum):
    PROFILE = "profile"
    PROFESSIONAL_EXPERIENCE = "professional_experience"
    PROJECT = "project"
    TECHNOLOGY = "technology"


class ResumeSection(str, Enum):
    SUMMARY = "SUMMARY"
    EXPERIENCE = "EXPERIENCE"
    PROJECTS = "PROJECTS"
    TECHNOLOGIES = "TECHNOLOGIES"


class FactName(str, Enum):
    FULL_NAME = "full_name"
    PROFESSIONAL_TITLE = "professional_title"
    SUMMARY = "summary"
    LOCATION = "location"
    LINKEDIN_URL = "linkedin_url"
    GITHUB_URL = "github_url"
    COMPANY_NAME = "company_name"
    POSITION = "position"
    EMPLOYMENT_TYPE = "employment_type"
    WORK_MODEL = "work_model"
    DESCRIPTION = "description"
    START_DATE = "start_date"
    END_DATE = "end_date"
    IS_CURRENT = "is_current"
    PROJECT_NAME = "project_name"
    ROLE = "role"
    REPOSITORY_URL = "repository_url"
    DEMO_URL = "demo_url"
    TECHNOLOGY_NAME = "technology_name"
    CATEGORY = "category"
    PROFICIENCY_LEVEL = "proficiency_level"
    YEARS_EXPERIENCE = "years_experience"


FactValue = str | int | bool | date


@dataclass(frozen=True, order=True)
class SourceReference:
    source_type: FactualSourceType
    source_id: int


@dataclass(frozen=True)
class FactualValue:
    name: FactName
    value: FactValue


@dataclass(frozen=True)
class FactualBlock:
    section: ResumeSection
    facts: tuple[FactualValue, ...]
    provenance: tuple[SourceReference, ...]


@dataclass(frozen=True)
class TargetedResumeComposition:
    profile_id: int
    job_id: int
    ruleset_version: str
    blocks: tuple[FactualBlock, ...]
    source_manifest: tuple[SourceReference, ...]


@dataclass(frozen=True)
class TargetedResumePreview:
    preview_id: str
    composition: TargetedResumeComposition
    state: Literal["preview"] = "preview"


@dataclass(frozen=True)
class ProfileFacts:
    source_id: int
    user_id: int
    full_name: str
    professional_title: str
    summary: str
    location: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None


@dataclass(frozen=True)
class JobContext:
    source_id: int
    user_id: int
    title: str
    description: str


@dataclass(frozen=True)
class ProfessionalExperienceFacts:
    source_id: int
    profile_id: int
    company_name: str
    position: str
    start_date: date
    employment_type: str | None = None
    work_model: str | None = None
    location: str | None = None
    description: str | None = None
    end_date: date | None = None
    is_current: bool = False


@dataclass(frozen=True)
class ProjectFacts:
    source_id: int
    profile_id: int
    name: str
    description: str | None = None
    role: str | None = None
    repository_url: str | None = None
    demo_url: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False


@dataclass(frozen=True)
class TechnologyFacts:
    source_id: int
    profile_id: int
    name: str
    category: str
    proficiency_level: str
    years_experience: int | None = None


@dataclass(frozen=True)
class AuthorizedCompositionSources:
    authenticated_user_id: int
    profile: ProfileFacts
    job: JobContext
    professional_experiences: tuple[ProfessionalExperienceFacts, ...] = ()
    projects: tuple[ProjectFacts, ...] = ()
    technologies: tuple[TechnologyFacts, ...] = ()


class TargetedResumeCompositionError(Exception):
    """Base error for rejected deterministic compositions."""


class InvalidSourceIdentifierError(TargetedResumeCompositionError):
    """Raised when a source has no structurally valid identifier."""


class UnauthorizedCompositionSourceError(TargetedResumeCompositionError):
    """Raised when a source is outside the authorized user/profile context."""
