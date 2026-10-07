from __future__ import annotations

from collections.abc import Iterable

from domain.targeted_resume import (
    COMPOSITION_RULESET_VERSION,
    AuthorizedCompositionSources,
    FactName,
    FactualBlock,
    FactualSourceType,
    FactualValue,
    FactValue,
    ProfessionalExperienceFacts,
    ProfileFacts,
    ProjectFacts,
    ResumeSection,
    SourceReference,
    TargetedResumeComposition,
    TechnologyFacts,
    UnauthorizedCompositionSourceError,
    InvalidSourceIdentifierError,
)


class TargetedResumeComposer:
    """Pure deterministic composer for already loaded factual sources."""

    def compose(
        self,
        sources: AuthorizedCompositionSources,
    ) -> TargetedResumeComposition:
        self._validate_sources(sources)

        blocks = self._compose_blocks(sources)
        manifest = tuple(
            sorted(
                {reference for block in blocks for reference in block.provenance},
                key=lambda reference: (
                    reference.source_type.value,
                    reference.source_id,
                ),
            )
        )

        return TargetedResumeComposition(
            profile_id=sources.profile.source_id,
            job_id=sources.job.source_id,
            ruleset_version=COMPOSITION_RULESET_VERSION,
            blocks=blocks,
            source_manifest=manifest,
        )

    def _compose_blocks(
        self,
        sources: AuthorizedCompositionSources,
    ) -> tuple[FactualBlock, ...]:
        blocks: list[FactualBlock] = []

        profile_block = self._profile_block(sources.profile)
        if profile_block is not None:
            blocks.append(profile_block)

        for experience in sources.professional_experiences:
            blocks.append(self._experience_block(experience))

        for project in sources.projects:
            blocks.append(self._project_block(project))

        for technology in sources.technologies:
            blocks.append(self._technology_block(technology))

        return tuple(blocks)

    @staticmethod
    def _profile_block(profile: ProfileFacts) -> FactualBlock | None:
        facts = TargetedResumeComposer._facts(
            (FactName.FULL_NAME, profile.full_name),
            (FactName.PROFESSIONAL_TITLE, profile.professional_title),
            (FactName.SUMMARY, profile.summary),
            (FactName.LOCATION, profile.location),
            (FactName.LINKEDIN_URL, profile.linkedin_url),
            (FactName.GITHUB_URL, profile.github_url),
        )
        if not facts:
            return None

        return FactualBlock(
            section=ResumeSection.SUMMARY,
            facts=facts,
            provenance=(SourceReference(FactualSourceType.PROFILE, profile.source_id),),
        )

    @staticmethod
    def _experience_block(source: ProfessionalExperienceFacts) -> FactualBlock:
        return FactualBlock(
            section=ResumeSection.EXPERIENCE,
            facts=TargetedResumeComposer._facts(
                (FactName.COMPANY_NAME, source.company_name),
                (FactName.POSITION, source.position),
                (FactName.EMPLOYMENT_TYPE, source.employment_type),
                (FactName.WORK_MODEL, source.work_model),
                (FactName.LOCATION, source.location),
                (FactName.DESCRIPTION, source.description),
                (FactName.START_DATE, source.start_date),
                (FactName.END_DATE, source.end_date),
                (FactName.IS_CURRENT, source.is_current),
            ),
            provenance=(
                SourceReference(
                    FactualSourceType.PROFESSIONAL_EXPERIENCE,
                    source.source_id,
                ),
            ),
        )

    @staticmethod
    def _project_block(source: ProjectFacts) -> FactualBlock:
        return FactualBlock(
            section=ResumeSection.PROJECTS,
            facts=TargetedResumeComposer._facts(
                (FactName.PROJECT_NAME, source.name),
                (FactName.ROLE, source.role),
                (FactName.DESCRIPTION, source.description),
                (FactName.REPOSITORY_URL, source.repository_url),
                (FactName.DEMO_URL, source.demo_url),
                (FactName.START_DATE, source.start_date),
                (FactName.END_DATE, source.end_date),
                (FactName.IS_CURRENT, source.is_current),
            ),
            provenance=(SourceReference(FactualSourceType.PROJECT, source.source_id),),
        )

    @staticmethod
    def _technology_block(source: TechnologyFacts) -> FactualBlock:
        return FactualBlock(
            section=ResumeSection.TECHNOLOGIES,
            facts=TargetedResumeComposer._facts(
                (FactName.TECHNOLOGY_NAME, source.name),
                (FactName.CATEGORY, source.category),
                (FactName.PROFICIENCY_LEVEL, source.proficiency_level),
                (FactName.YEARS_EXPERIENCE, source.years_experience),
            ),
            provenance=(
                SourceReference(FactualSourceType.TECHNOLOGY, source.source_id),
            ),
        )

    @staticmethod
    def _facts(
        *items: tuple[FactName, FactValue | None],
    ) -> tuple[FactualValue, ...]:
        return tuple(
            FactualValue(name=name, value=value)
            for name, value in items
            if value is not None and not (isinstance(value, str) and not value.strip())
        )

    @staticmethod
    def _validate_sources(sources: AuthorizedCompositionSources) -> None:
        TargetedResumeComposer._require_valid_source_identifiers(
            (sources.profile.source_id, sources.job.source_id),
        )

        if (
            sources.profile.user_id != sources.authenticated_user_id
            or sources.job.user_id != sources.authenticated_user_id
        ):
            raise UnauthorizedCompositionSourceError(
                "Profile and job must belong to the authenticated user."
            )

        factual_sources = (
            *sources.professional_experiences,
            *sources.projects,
            *sources.technologies,
        )
        TargetedResumeComposer._require_valid_source_identifiers(
            source.source_id for source in factual_sources
        )

        if any(
            source.profile_id != sources.profile.source_id for source in factual_sources
        ):
            raise UnauthorizedCompositionSourceError(
                "Every factual source must belong to the authorized profile."
            )

    @staticmethod
    def _require_valid_source_identifiers(source_ids: Iterable[int]) -> None:
        if any(source_id <= 0 for source_id in source_ids):
            raise InvalidSourceIdentifierError(
                "Every composition source must have a positive identifier."
            )
