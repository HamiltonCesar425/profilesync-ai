from dataclasses import replace
from datetime import date

import pytest

from domain.targeted_resume import (
    AuthorizedCompositionSources,
    JobContext,
    ProfessionalExperienceFacts,
    ProfileFacts,
    ProjectFacts,
    SourceReference,
    TechnologyFacts,
)
from services.targeted_resume_composer import TargetedResumeComposer
from services.targeted_resume_preview_service import (
    TargetedResumePreviewService,
    TargetedResumePreviewStructuralError,
)


def make_sources() -> AuthorizedCompositionSources:
    return AuthorizedCompositionSources(
        authenticated_user_id=7,
        profile=ProfileFacts(
            source_id=11,
            user_id=7,
            full_name="Ada Lovelace",
            professional_title="Backend Engineer",
            summary="Desenvolve serviços Python.",
        ),
        job=JobContext(
            source_id=21,
            user_id=7,
            title="Backend Engineer",
            description="Python e APIs.",
        ),
        professional_experiences=(
            ProfessionalExperienceFacts(
                source_id=32,
                profile_id=11,
                company_name="New Engines",
                position="Engineer",
                start_date=date(2024, 1, 1),
            ),
            ProfessionalExperienceFacts(
                source_id=31,
                profile_id=11,
                company_name="Analytical Engines",
                position="Engineer",
                start_date=date(2024, 1, 1),
            ),
            ProfessionalExperienceFacts(
                source_id=33,
                profile_id=11,
                company_name="Early Engines",
                position="Engineer",
                start_date=date(2023, 1, 1),
            ),
        ),
        projects=(
            ProjectFacts(source_id=42, profile_id=11, name="Second"),
            ProjectFacts(source_id=41, profile_id=11, name="First"),
        ),
        technologies=(
            TechnologyFacts(
                source_id=52,
                profile_id=11,
                name="SQL",
                category="Database",
                proficiency_level="Intermediate",
            ),
            TechnologyFacts(
                source_id=51,
                profile_id=11,
                name="Python",
                category="Language",
                proficiency_level="Advanced",
            ),
        ),
    )


class FixedLoader:
    def __init__(self, sources: AuthorizedCompositionSources) -> None:
        self.sources = sources

    def load(self, **kwargs) -> AuthorizedCompositionSources:
        return self.sources


class RecordingComposer:
    def __init__(self, *, ruleset_version: str | None = None) -> None:
        self.received_sources: AuthorizedCompositionSources | None = None
        self.ruleset_version = ruleset_version

    def compose(self, sources: AuthorizedCompositionSources):
        self.received_sources = sources
        composition = TargetedResumeComposer().compose(sources)
        if self.ruleset_version is not None:
            return replace(composition, ruleset_version=self.ruleset_version)
        return composition


class InvalidManifestComposer:
    def compose(self, sources: AuthorizedCompositionSources):
        composition = TargetedResumeComposer().compose(sources)
        return replace(composition, source_manifest=())


class UnauthorizedProvenanceComposer:
    def compose(self, sources: AuthorizedCompositionSources):
        composition = TargetedResumeComposer().compose(sources)
        first_block = composition.blocks[0]
        unauthorized_reference = SourceReference(
            source_type=first_block.provenance[0].source_type,
            source_id=999_999,
        )
        invalid_block = replace(
            first_block,
            provenance=(unauthorized_reference,),
        )
        return replace(
            composition,
            blocks=(invalid_block, *composition.blocks[1:]),
            source_manifest=(unauthorized_reference,),
        )


def generate_preview(
    sources: AuthorizedCompositionSources,
    composer=None,
):
    service = TargetedResumePreviewService(
        source_loader=FixedLoader(sources),
        composer=composer or TargetedResumeComposer(),
    )
    return service.generate_preview(
        profile_id=sources.profile.source_id,
        job_id=sources.job.source_id,
        authenticated_user_id=sources.authenticated_user_id,
    )


def test_canonicalizes_source_collections_before_composition() -> None:
    composer = RecordingComposer()

    preview = generate_preview(make_sources(), composer)

    assert preview.state == "preview"
    assert composer.received_sources is not None
    assert [
        source.source_id
        for source in composer.received_sources.professional_experiences
    ] == [32, 31, 33]
    assert [source.source_id for source in composer.received_sources.projects] == [
        41,
        42,
    ]
    assert [
        source.source_id for source in composer.received_sources.technologies
    ] == [51, 52]


@pytest.mark.parametrize(
    "collection_name",
    ["professional_experiences", "projects", "technologies"],
)
def test_rejects_duplicate_identifiers_within_a_collection(
    collection_name: str,
) -> None:
    sources = make_sources()
    collection = getattr(sources, collection_name)
    duplicated_sources = replace(
        sources,
        **{collection_name: (collection[0], collection[0])},
    )

    with pytest.raises(TargetedResumePreviewStructuralError):
        generate_preview(duplicated_sources)


def test_equivalent_inputs_produce_stable_preview_identity() -> None:
    first = generate_preview(make_sources())
    reordered = replace(
        make_sources(),
        professional_experiences=tuple(
            reversed(make_sources().professional_experiences)
        ),
        projects=tuple(reversed(make_sources().projects)),
        technologies=tuple(reversed(make_sources().technologies)),
    )
    second = generate_preview(reordered)

    assert first.preview_id == second.preview_id
    assert first.preview_id.startswith("sha256:")
    assert len(first.preview_id) == len("sha256:") + 64
    assert first.composition == second.composition


def test_preview_identity_changes_when_a_fact_changes() -> None:
    sources = make_sources()
    changed_profile = replace(sources.profile, summary="Resumo alterado.")

    assert generate_preview(sources).preview_id != generate_preview(
        replace(sources, profile=changed_profile)
    ).preview_id


def test_preview_identity_changes_when_job_context_changes() -> None:
    sources = make_sources()
    changed_job = replace(sources.job, description="Outro contexto autorizado.")

    assert generate_preview(sources).preview_id != generate_preview(
        replace(sources, job=changed_job)
    ).preview_id


def test_preview_identity_changes_when_ruleset_version_changes() -> None:
    sources = make_sources()

    first = generate_preview(sources)
    second = generate_preview(
        sources,
        RecordingComposer(ruleset_version="targeted-resume-factual-v2"),
    )

    assert first.preview_id != second.preview_id


def test_rejects_manifest_inconsistent_with_factual_blocks() -> None:
    with pytest.raises(TargetedResumePreviewStructuralError):
        generate_preview(make_sources(), InvalidManifestComposer())


def test_rejects_provenance_outside_authorized_snapshot() -> None:
    with pytest.raises(TargetedResumePreviewStructuralError):
        generate_preview(make_sources(), UnauthorizedProvenanceComposer())
