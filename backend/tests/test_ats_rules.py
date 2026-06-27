from types import SimpleNamespace

from services.ats_validation_rules import (
    ContentLengthRule,
    RequiredSectionsRule,
    ResumeTitleRule,
    TargetRoleRule,
)


def make_resume(**overrides):
    data = {
        "title": "Currículo Desenvolvedor Full Stack",
        "target_role": "Desenvolvedor Full Stack Python",
        "summary": "Profissional com experiência em Python, FastAPI e APIs REST.",
        "experience": "Atuação em desenvolvimento backend, testes automatizados e APIs.",
        "education": "Formação em tecnologia e ciência de dados.",
        "skills": "Python, FastAPI, SQLAlchemy, Pytest, Docker.",
        "projects": "ProfileSync AI, Financial IA.",
        "certifications": "Certificações em Python e segurança.",
    }
    data.update(overrides)

    sections = (
        ("Resumo", data["summary"]),
        ("Experiência", data["experience"]),
        ("Formação", data["education"]),
        ("Competências", data["skills"]),
        ("Projetos", data["projects"]),
        ("Certificações", data["certifications"]),
    )
    content = "\n\n".join(
        f"{heading}\n{value.strip()}"
        for heading, value in sections
        if value.strip()
    )

    return SimpleNamespace(
        title=data["title"],
        target_role=data["target_role"],
        content=content,
    )


def test_resume_title_rule_passes_when_title_exists():
    resume = make_resume()

    result = ResumeTitleRule().validate(resume)

    assert result.passed is True


def test_resume_title_rule_fails_when_title_is_empty():
    resume = make_resume(title="")

    result = ResumeTitleRule().validate(resume)

    assert result.passed is False


def test_target_role_rule_passes_when_target_role_exists():
    resume = make_resume()

    result = TargetRoleRule().validate(resume)

    assert result.passed is True


def test_target_role_rule_fails_when_target_role_is_empty():
    resume = make_resume(target_role="")

    result = TargetRoleRule().validate(resume)

    assert result.passed is False


def test_content_length_rule_passes_when_resume_has_enough_content():
    resume = make_resume(
        summary="Profissional com sólida experiência em Python e FastAPI. " * 5,
        experience="Desenvolvimento de APIs, testes automatizados e integração. " * 5,
        skills="Python, FastAPI, SQLAlchemy, Pytest, Docker, GitHub Actions. " * 5,
    )

    result = ContentLengthRule().validate(resume)

    assert result.passed is True


def test_content_length_rule_fails_when_resume_has_insufficient_content():
    resume = make_resume(
        summary="Pouco conteúdo.",
        experience="",
        education="",
        skills="",
        projects="",
        certifications="",
    )

    result = ContentLengthRule().validate(resume)

    assert result.passed is False


def test_required_sections_rule_passes_when_required_sections_exist():
    resume = make_resume()

    result = RequiredSectionsRule().validate(resume)

    assert result.passed is True


def test_required_sections_rule_fails_when_required_sections_are_missing():
    resume = make_resume(
        summary="",
        experience="",
        education="",
        skills="",
    )

    result = RequiredSectionsRule().validate(resume)

    assert result.passed is False
