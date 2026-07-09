from services.job_requirement_extractor import (
    JobRequirementExtractor as JobRequirementExtractor,
)


def test_extract_job_requirements():
    extractor = JobRequirementExtractor()

    description = """
    Buscamos desenvolver Python com experiência
    em FastAPI, Docker, PostgreSQL, Git e tests
    automatizados.
    """

    result = extractor.extract(description)

    assert result == [
        "docker",
        "fastapi",
        "git",
        "postgresql",
        "python",
        "tests",
    ]


def test_extract_empty_job_requirements():
    extractor = JobRequirementExtractor()

    result = extractor.extract("Buscamos profissional comunicativo e organizado.")

    assert result == []


def test_extract_ignore_case():
    extractor = JobRequirementExtractor()

    result = extractor.extract("Conhecimento em PYTHON e Docker.")

    assert result == [
        "docker",
        "python",
    ]
