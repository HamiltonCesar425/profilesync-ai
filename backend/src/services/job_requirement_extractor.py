import re


class JobRequirementExtractor:
    """Extrai requisistos técnicos a partir de descrição de uma vaga."""

    KNOWN_SKILLS = {
        "python",
        "fastapi",
        "django",
        "sql",
        "postgresql",
        "docker",
        "aws",
        "git",
        "tests",
        "pytest",
        "api rest",
    }

    def extract(self, description: str) -> list[str]:
        normalized_description = self._normalize(description)

        return sorted(
            skill
            for skill in self.KNOWN_SKILLS
            if self._contains_skill(normalized_description, skill)
        )

    def _normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"/s+", " ", text)

        return text.strip()

    def _contains_skill(self, text: str, skill: str) -> bool:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        return re.search(pattern, text) is not None
