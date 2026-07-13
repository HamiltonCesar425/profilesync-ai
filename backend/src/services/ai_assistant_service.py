from dataclasses import dataclass
from typing import Protocol

from core.exceptions import AIResponseError

class AIProvider(Protocol):
    def generate(self, prompt: str) -> str:
        """Generate text from the provided prompt."""


@dataclass(frozen=True)
class TextImprovementResult:
    original_text: str
    improved_text: str


class AIAssistantService:
    def __init__(self, provider: AIProvider) -> None:
        self._provider = provider

    def improve_professional_description(
        self,
        text: str,
    ) -> TextImprovementResult:
        normalized_text = self._normalize_text(text)

        if not normalized_text:
            raise ValueError("Professional description must not be empty.")

        prompt = self._build_improvement_prompt(normalized_text)
        improved_text = self._provider.generate(prompt).strip()

        if not improved_text:
            raise AIResponseError(
                "AI provider returned an empty professional description."
            )

        return TextImprovementResult(
            original_text=normalized_text,
            improved_text=improved_text,
        )

    @staticmethod
    def _normalize_text(text: str) -> str:
        return " ".join(text.split())

    @staticmethod
    def _build_improvement_prompt(text: str) -> str:
        return (
            "Improve the following professional description.\n"
            "Preserve all factual information.\n"
            "Do not invent technologies, responsibilities, achievements, "
            "metrics, companies, dates, or qualifications.\n"
            "Use clear, concise, professional language suitable for a resume.\n"
            "Return only the improved description.\n\n"
            f"Professional description:\n{text}"
        )
