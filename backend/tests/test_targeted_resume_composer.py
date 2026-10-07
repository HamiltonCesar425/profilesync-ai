from dataclasses import replace
from datetime import date

import pytest

from domain.targeted_resume import (
    COMPOSITION_RULESET_VERSION,
    AuthorizedCompositionSources,
    FactName,
    FactualSourceType,
    JobContext,
    ProfessionalExperienceFacts,
    ProfileFacts,
    ProjectFacts,
    ResumeSection,
    SourceReference,
    TechnologyFacts,
    UnauthorizedCompositionSourceError,
    InvalidSourceIdentifierError,
)
from services.targeted_resume_composer import TargetedResumeComposer


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
            description=(
                "Python, Kubernetes, liderança técnica e aumento de 40% de desempenho."
            ),
        ),
        professional_experiences=(
            ProfessionalExperienceFacts(
                source_id=31,
                profile_id=11,
                company_name="Analytical Engines",
                position="Backend Engineer",
                start_date=date(2023, 1, 1),
                description="Desenvolveu serviços Python.",
                is_current=True,
            ),
        ),
        projects=(
            ProjectFacts(
                source_id=41,
                profile_id=11,
                name="API Platform",
                role="Developer",
                description="Implementou uma API com FastAPI.",
            ),
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
                years_experience=4,
            ),
        ),
    )


def factual_values(composition) -> list[object]:
    return [fact.value for block in composition.blocks for fact in block.facts]


def test_existing_facts_can_be_selected_and_composed() -> None:
    composition = TargetedResumeComposer().compose(make_sources())

    assert composition.profile_id == 11
    assert composition.job_id == 21
    assert composition.ruleset_version == COMPOSITION_RULESET_VERSION
    assert [block.section for block in composition.blocks] == [
        ResumeSection.SUMMARY,
        ResumeSection.EXPERIENCE,
        ResumeSection.PROJECTS,
        ResumeSection.TECHNOLOGIES,
        ResumeSection.TECHNOLOGIES,
    ]
    assert "Analytical Engines" in factual_values(composition)
    assert "API Platform" in factual_values(composition)
    assert "Python" in factual_values(composition)


def test_composer_does_not_include_unpersisted_fact() -> None:
    composition = TargetedResumeComposer().compose(make_sources())

    values = factual_values(composition)
    assert "Kubernetes" not in values
    assert "liderança técnica" not in values
    assert all("40%" not in value for value in values if isinstance(value, str))


def test_composer_rejects_source_without_positive_identifier() -> None:
    sources = make_sources()
    invalid_technology = TechnologyFacts(
        source_id=0,
        profile_id=sources.profile.source_id,
        name="Kubernetes",
        category="Infrastructure",
        proficiency_level="Advanced",
    )

    with pytest.raises(InvalidSourceIdentifierError):
        TargetedResumeComposer().compose(
            AuthorizedCompositionSources(
                authenticated_user_id=sources.authenticated_user_id,
                profile=sources.profile,
                job=sources.job,
                technologies=(invalid_technology,),
            )
        )


def test_composer_does_not_infer_missing_information() -> None:
    composition = TargetedResumeComposer().compose(make_sources())
    experience = next(
        block
        for block in composition.blocks
        if block.section is ResumeSection.EXPERIENCE
    )

    fact_names = {fact.name for fact in experience.facts}
    assert FactName.END_DATE not in fact_names
    assert FactName.EMPLOYMENT_TYPE not in fact_names
    assert FactName.WORK_MODEL not in fact_names
    assert FactName.LOCATION not in fact_names


def test_job_requirement_does_not_become_candidate_skill() -> None:
    composition = TargetedResumeComposer().compose(make_sources())
    technology_values = {
        fact.value
        for block in composition.blocks
        if block.section is ResumeSection.TECHNOLOGIES
        for fact in block.facts
        if fact.name is FactName.TECHNOLOGY_NAME
    }

    assert technology_values == {"Python", "SQL"}
    assert "Kubernetes" not in technology_values


def test_composer_preserves_loaded_source_order() -> None:
    sources = make_sources()
    experience = sources.professional_experiences[0]
    project = sources.projects[0]
    ordered_sources = replace(
        sources,
        professional_experiences=(
            experience,
            replace(experience, source_id=30, company_name="Difference Engines"),
        ),
        projects=(
            project,
            replace(project, source_id=40, name="Compiler Platform"),
        ),
    )

    composition = TargetedResumeComposer().compose(ordered_sources)
    source_ids_by_section = {
        section: [
            block.provenance[0].source_id
            for block in composition.blocks
            if block.section is section
        ]
        for section in (
            ResumeSection.EXPERIENCE,
            ResumeSection.PROJECTS,
            ResumeSection.TECHNOLOGIES,
        )
    }

    assert source_ids_by_section == {
        ResumeSection.EXPERIENCE: [31, 30],
        ResumeSection.PROJECTS: [41, 40],
        ResumeSection.TECHNOLOGIES: [52, 51],
    }


def test_factual_blocks_preserve_valid_provenance() -> None:
    composition = TargetedResumeComposer().compose(make_sources())

    assert all(block.provenance for block in composition.blocks)
    assert composition.source_manifest == (
        SourceReference(FactualSourceType.PROFESSIONAL_EXPERIENCE, 31),
        SourceReference(FactualSourceType.PROFILE, 11),
        SourceReference(FactualSourceType.PROJECT, 41),
        SourceReference(FactualSourceType.TECHNOLOGY, 51),
        SourceReference(FactualSourceType.TECHNOLOGY, 52),
    )
    assert {
        reference for block in composition.blocks for reference in block.provenance
    } == set(composition.source_manifest)


def test_equivalent_inputs_produce_deterministic_result() -> None:
    composer = TargetedResumeComposer()

    assert composer.compose(make_sources()) == composer.compose(make_sources())


def test_composer_preserves_factual_identity() -> None:
    composition = TargetedResumeComposer().compose(make_sources())
    experience = next(
        block
        for block in composition.blocks
        if block.section is ResumeSection.EXPERIENCE
    )

    facts = {fact.name: fact.value for fact in experience.facts}
    assert facts[FactName.COMPANY_NAME] == "Analytical Engines"
    assert facts[FactName.POSITION] == "Backend Engineer"
    assert facts[FactName.DESCRIPTION] == "Desenvolveu serviços Python."
    assert facts[FactName.START_DATE] == date(2023, 1, 1)
    assert facts[FactName.IS_CURRENT] is True


def test_composer_rejects_cross_user_context_before_composition() -> None:
    sources = make_sources()

    with pytest.raises(UnauthorizedCompositionSourceError):
        TargetedResumeComposer().compose(
            AuthorizedCompositionSources(
                authenticated_user_id=999,
                profile=sources.profile,
                job=sources.job,
                professional_experiences=sources.professional_experiences,
                projects=sources.projects,
                technologies=sources.technologies,
            )
        )


def test_composer_rejects_source_from_another_profile() -> None:
    sources = make_sources()
    foreign_source = TechnologyFacts(
        source_id=99,
        profile_id=999,
        name="Python",
        category="Language",
        proficiency_level="Advanced",
    )

    with pytest.raises(UnauthorizedCompositionSourceError):
        TargetedResumeComposer().compose(
            AuthorizedCompositionSources(
                authenticated_user_id=sources.authenticated_user_id,
                profile=sources.profile,
                job=sources.job,
                technologies=(foreign_source,),
            )
        )


def test_targeted_resume_generation_does_not_require_ai() -> None:
    composer = TargetedResumeComposer()

    composition = composer.compose(make_sources())

    assert composition.blocks


def test_factual_integrity_precedes_resume_completeness() -> None:
    sources = make_sources()
    sparse_profile = ProfileFacts(
        source_id=sources.profile.source_id,
        user_id=sources.profile.user_id,
        full_name=sources.profile.full_name,
        professional_title=sources.profile.professional_title,
        summary="",
    )

    composition = TargetedResumeComposer().compose(
        AuthorizedCompositionSources(
            authenticated_user_id=sources.authenticated_user_id,
            profile=sparse_profile,
            job=sources.job,
        )
    )

    assert len(composition.blocks) == 1
    values = factual_values(composition)
    assert values == ["Ada Lovelace", "Backend Engineer"]
    assert "Kubernetes" not in values
