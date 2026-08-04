import re


class JobRequirementExtractor:
    """Extrai requisistos técnicos a partir de descrição de uma vaga."""

    KNOWN_SKILLS = {
        "python",
        "fastapi",
        "django",
        "flask",
        "javascript",
        "typescript",
        "react",
        "node.js",
        "java",
        "c#",
        ".net",
        "sql",
        "postgresql",
        "mongodb",
        "redis",
        "sqlalchemy",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "git",
        "ci/cd",
        "tests",
        "pytest",
        "api rest",
    }

    SKILL_ALIASES = {
        "dotnet": ".net",
        "nodejs": "node.js",
        "rest api": "api rest",
        "testes": "tests",
        "testes automatizados": "tests",
    }

    def extract(self, description: str) -> list[str]:
        if not description.strip():
            return []

        normalized_description = self._normalize(description)

        detected_skills = {
            skill
            for skill in self.KNOWN_SKILLS
            if self._contains_skill(normalized_description, skill)
        }

        detected_skills.update(
            skill
            for alias, skill in self.SKILL_ALIASES.items()
            if self._contains_skill(normalized_description, alias)
        )

        return sorted(detected_skills)

    def _normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _contains_skill(self, text: str, skill: str) -> bool:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        return re.search(pattern, text) is not None
