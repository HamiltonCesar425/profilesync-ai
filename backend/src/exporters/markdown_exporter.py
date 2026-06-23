class MarkdownExporter:
    @staticmethod
    def export(resume) -> str:
        """Export a resume to Markdown, supporting both resume representations.

        Older callers provide individual ATS sections, while the current model
        stores the generated resume in ``content`` alongside metadata.
        """
        def value(field: str) -> str:
            field_value = getattr(resume, field, None)
            return field_value.strip() if isinstance(field_value, str) and field_value.strip() else "Não informado."

        if hasattr(resume, "content"):
            sections = [
                f"# {value('title')}",
                "",
                "## Cargo Alvo",
                "",
                value("target_role"),
                "",
                "## Conteúdo do Currículo",
                "",
                value("content"),
                "",
                "## Versão",
                "",
                str(getattr(resume, "version", 1)),
                "",
            ]
            return "\n".join(sections)

        sections = [
            f"# {value('title')}",
            "",
            "## Resumo Profissional",
            "",
            value("summary"),
            "",
            "## Experiência Profissional",
            "",
            value("experience"),
            "",
            "## Competências",
            "",
            value("skills"),
            "",
            "## Formação",
            "",
            value("education"),
            "",
            "## Certificações",
            "",
            value("certifications"),
            "",
            "## Projetos",
            "",
            value("projects"),
            "",
        ]

        return "\n".join(sections)
