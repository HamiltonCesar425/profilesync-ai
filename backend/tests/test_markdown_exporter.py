from types import SimpleNamespace

from exporters.markdown_exporter import MarkdownExporter


def test_markdown_exporter_generates_ats_friendly_content():
    resume = SimpleNamespace(
        title="Currículo Desenvolvedor Full Stack",
        summary="Resumo profissional objetivo.",
        experience="Experiência com FastAPI e React.",
        skills="Python, FastAPI, SQLAlchemy, React",
        education="Formação em Ciência de Dados.",
        certifications="Certificação Python.",
        projects="ProfileSync AI.",
    )

    content = MarkdownExporter.export(resume)

    assert "# Currículo Desenvolvedor Full Stack" in content
    assert "## Resumo Profissional" in content
    assert "## Experiência Profissional" in content
    assert "## Competências" in content
    assert "## Formação" in content
    assert "## Certificações" in content
    assert "## Projetos" in content
    assert "FastAPI" in content


def test_markdown_exporter_uses_default_text_for_empty_fields():
    resume = SimpleNamespace(
        title="Currículo Básico",
        summary=None,
        experience=None,
        skills=None,
        education=None,
        certifications=None,
        projects=None,
    )

    content = MarkdownExporter.export(resume)

    assert "# Currículo Básico" in content
    assert content.count("Não informado.") == 6
