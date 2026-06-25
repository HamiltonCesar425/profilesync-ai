from types import SimpleNamespace

from exporters.docx_exporter import DOCXExporter


def test_docx_exporter_generates_docx_file():
    resume = SimpleNamespace(
        title="Currículo Desenvolvedor Full Stack",
        target_role="Desenvolvedor Full Stack",
        content=(
            "Desenvolvedor Full Stack com experiência em Python, "
            "FastAPI, SQLAlchemy, React e construção de produtos digitais."
        ),
        version=1,
    )
    content = DOCXExporter().export(resume)

    assert isinstance(content, bytes)
    assert content.startswith(b"PK")
    assert len(content) > 0

def test_docx_exporter_handles_empty_optional_fields():
    resume = SimpleNamespace(
        title="Currículo Básico",
        target_role=None,
        content=None,
        version=1,
    )
    content = DOCXExporter().export(resume)

    assert isinstance(content, bytes)
    assert content.startswith(b"PK")
    assert len(content) > 0
