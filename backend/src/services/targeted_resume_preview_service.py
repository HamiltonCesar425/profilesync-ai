from __future__ import annotations

from dataclasses import replace
from datetime import date
import hashlib
import json
from collections.abc import Iterable
from typing import Any

from domain.targeted_resume import (
    AuthorizedCompositionSources,
    FactualBlock,
    FactualSourceType,
    SourceReference,
    TargetedResumeComposition,
    TargetedResumePreview,
)
from services.targeted_resume_composer import TargetedResumeComposer
from services.targeted_resume_source_loader import TargetedResumeSourceLoader


PREVIEW_IDENTITY_SCHEMA_VERSION = "targeted-resume-preview-identity-v1"


class TargetedResumePreviewStructuralError(Exception):
    """Raised when a preview cannot satisfy required structural invariants."""


class TargetedResumePreviewService:
    """Generate an authenticated, non-persisted factual preview."""

    def __init__(
        self,
        source_loader: TargetedResumeSourceLoader,
        composer: TargetedResumeComposer,
    ) -> None:
        self.source_loader = source_loader
        self.composer = composer

    def generate_preview(
        self,
        *,
        profile_id: int,
        job_id: int,
        authenticated_user_id: int,
    ) -> TargetedResumePreview:
        sources = self.source_loader.load(
            profile_id=profile_id,
            job_id=job_id,
            authenticated_user_id=authenticated_user_id,
        )
        ordered_sources = self._canonicalize_sources(sources)
        composition = self.composer.compose(ordered_sources)
        self._validate_postconditions(ordered_sources, composition)

        preview_id = self._build_preview_id(ordered_sources, composition)
        return TargetedResumePreview(
            preview_id=preview_id,
            composition=composition,
        )

    @classmethod
    def _canonicalize_sources(
        cls,
        sources: AuthorizedCompositionSources,
    ) -> AuthorizedCompositionSources:
        cls._require_unique_ids(
            source.source_id for source in sources.professional_experiences
        )
        cls._require_unique_ids(source.source_id for source in sources.projects)
        cls._require_unique_ids(source.source_id for source in sources.technologies)

        return replace(
            sources,
            professional_experiences=tuple(
                sorted(
                    sources.professional_experiences,
                    key=lambda source: (source.start_date, source.source_id),
                    reverse=True,
                )
            ),
            projects=tuple(
                sorted(sources.projects, key=lambda source: source.source_id)
            ),
            technologies=tuple(
                sorted(sources.technologies, key=lambda source: source.source_id)
            ),
        )

    @staticmethod
    def _require_unique_ids(source_ids: Iterable[int]) -> None:
        identifiers = tuple(source_ids)
        if len(identifiers) != len(set(identifiers)):
            raise TargetedResumePreviewStructuralError(
                "A factual source collection contains duplicate identifiers."
            )

    @classmethod
    def _validate_postconditions(
        cls,
        sources: AuthorizedCompositionSources,
        composition: TargetedResumeComposition,
    ) -> None:
        if (
            composition.profile_id != sources.profile.source_id
            or composition.job_id != sources.job.source_id
            or not composition.ruleset_version
        ):
            raise TargetedResumePreviewStructuralError(
                "The composition context is inconsistent with its authorized sources."
            )

        authorized_references = cls._authorized_references(sources)
        block_references: set[SourceReference] = set()

        for block in composition.blocks:
            if not block.provenance or len(block.provenance) != len(
                set(block.provenance)
            ):
                raise TargetedResumePreviewStructuralError(
                    "Every factual block requires unique provenance."
                )
            if any(reference.source_id <= 0 for reference in block.provenance):
                raise TargetedResumePreviewStructuralError(
                    "Every provenance reference requires a positive identifier."
                )
            if not set(block.provenance).issubset(authorized_references):
                raise TargetedResumePreviewStructuralError(
                    "A factual block references an unauthorized source."
                )
            block_references.update(block.provenance)

        expected_manifest = tuple(
            sorted(
                block_references,
                key=lambda reference: (
                    reference.source_type.value,
                    reference.source_id,
                ),
            )
        )
        if composition.source_manifest != expected_manifest:
            raise TargetedResumePreviewStructuralError(
                "The source manifest is inconsistent with factual blocks."
            )

    @staticmethod
    def _authorized_references(
        sources: AuthorizedCompositionSources,
    ) -> set[SourceReference]:
        references = {
            SourceReference(
                source_type=FactualSourceType.PROFILE,
                source_id=sources.profile.source_id,
            )
        }
        references.update(
            SourceReference(
                source_type=FactualSourceType.PROFESSIONAL_EXPERIENCE,
                source_id=source.source_id,
            )
            for source in sources.professional_experiences
        )
        references.update(
            SourceReference(
                source_type=FactualSourceType.PROJECT,
                source_id=source.source_id,
            )
            for source in sources.projects
        )
        references.update(
            SourceReference(
                source_type=FactualSourceType.TECHNOLOGY,
                source_id=source.source_id,
            )
            for source in sources.technologies
        )
        return references

    @classmethod
    def _build_preview_id(
        cls,
        sources: AuthorizedCompositionSources,
        composition: TargetedResumeComposition,
    ) -> str:
        payload = {
            "identity_schema_version": PREVIEW_IDENTITY_SCHEMA_VERSION,
            "authenticated_user_id": sources.authenticated_user_id,
            "sources": cls._sources_payload(sources),
            "composition": cls._composition_payload(composition),
        }
        canonical_payload = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        digest = hashlib.sha256(canonical_payload).hexdigest()
        return f"sha256:{digest}"

    @classmethod
    def _sources_payload(cls, sources: AuthorizedCompositionSources) -> dict[str, Any]:
        return {
            "profile": {
                "source_id": sources.profile.source_id,
                "user_id": sources.profile.user_id,
                "full_name": sources.profile.full_name,
                "professional_title": sources.profile.professional_title,
                "summary": sources.profile.summary,
                "location": sources.profile.location,
                "linkedin_url": sources.profile.linkedin_url,
                "github_url": sources.profile.github_url,
            },
            "job": {
                "source_id": sources.job.source_id,
                "user_id": sources.job.user_id,
                "title": sources.job.title,
                "description": sources.job.description,
            },
            "professional_experiences": [
                {
                    "source_id": source.source_id,
                    "profile_id": source.profile_id,
                    "company_name": source.company_name,
                    "position": source.position,
                    "start_date": source.start_date.isoformat(),
                    "employment_type": source.employment_type,
                    "work_model": source.work_model,
                    "location": source.location,
                    "description": source.description,
                    "end_date": cls._date_value(source.end_date),
                    "is_current": source.is_current,
                }
                for source in sources.professional_experiences
            ],
            "projects": [
                {
                    "source_id": source.source_id,
                    "profile_id": source.profile_id,
                    "name": source.name,
                    "description": source.description,
                    "role": source.role,
                    "repository_url": source.repository_url,
                    "demo_url": source.demo_url,
                    "start_date": cls._date_value(source.start_date),
                    "end_date": cls._date_value(source.end_date),
                    "is_current": source.is_current,
                }
                for source in sources.projects
            ],
            "technologies": [
                {
                    "source_id": source.source_id,
                    "profile_id": source.profile_id,
                    "name": source.name,
                    "category": source.category,
                    "proficiency_level": source.proficiency_level,
                    "years_experience": source.years_experience,
                }
                for source in sources.technologies
            ],
        }

    @classmethod
    def _composition_payload(
        cls,
        composition: TargetedResumeComposition,
    ) -> dict[str, Any]:
        return {
            "profile_id": composition.profile_id,
            "job_id": composition.job_id,
            "ruleset_version": composition.ruleset_version,
            "blocks": [cls._block_payload(block) for block in composition.blocks],
            "source_manifest": [
                cls._reference_payload(reference)
                for reference in composition.source_manifest
            ],
        }

    @classmethod
    def _block_payload(cls, block: FactualBlock) -> dict[str, Any]:
        return {
            "section": block.section.value,
            "facts": [
                {
                    "name": fact.name.value,
                    "value": cls._fact_value(fact.value),
                }
                for fact in block.facts
            ],
            "provenance": [
                cls._reference_payload(reference)
                for reference in sorted(
                    block.provenance,
                    key=lambda reference: (
                        reference.source_type.value,
                        reference.source_id,
                    ),
                )
            ],
        }

    @staticmethod
    def _reference_payload(reference: SourceReference) -> dict[str, Any]:
        return {
            "source_type": reference.source_type.value,
            "source_id": reference.source_id,
        }

    @staticmethod
    def _date_value(value: date | None) -> str | None:
        return value.isoformat() if value is not None else None

    @staticmethod
    def _fact_value(value: Any) -> Any:
        return value.isoformat() if isinstance(value, date) else value
