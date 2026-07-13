import pytest

from services.ai_assistant_service import (
    AIAssistantService,
    AIProviderError,
)


class FakeAIProvider:
    def __init__(self, response: str) -> None:
        self.response = response
        self.received_prompt: str | None = None

    def generate(self, prompt: str) -> str:
        self.received_prompt = prompt
        return self.response


def test_improve_professional_description() -> None:
    provider = FakeAIProvider("Desenvolveu APIs REST com Python e FastAPI.")
    service = AIAssistantService(provider)

    result = service.improve_professional_description("Desenvolvi APIs com Python.")

    assert result.original_text == "Desenvolvi APIs com Python."
    assert result.improved_text == "Desenvolveu APIs REST com Python e FastAPI."


def test_improve_professional_description_normalizes_whitespace() -> None:
    provider = FakeAIProvider("Desenvolveu APIs escaláveis com Python.")
    service = AIAssistantService(provider)

    result = service.improve_professional_description(" Desenvolvi APIs\ncom  Python. ")

    assert result.original_text == "Desenvolvi APIs com Python."


@pytest.mark.parametrize(
    "invalid_text",
    [
        "",
        "   ",
        "\n\t",
    ],
)
def test_improve_professional_description_rejects_empty_text(
    invalid_text: str,
) -> None:
    provider = FakeAIProvider("Descrição melhorada.")
    service = AIAssistantService(provider)

    with pytest.raises(
        ValueError,
        match="Professional description must not be empty.",
    ):
        service.improve_professional_description(invalid_text)


@pytest.mark.parametrize(
    "provider_response",
    [
        "",
        "   ",
        "\n\t",
    ],
)
def test_improve_professional_description_rejects_empty_provider_response(
    provider_response: str,
) -> None:
    provider = FakeAIProvider(provider_response)
    service = AIAssistantService(provider)

    with pytest.raises(
        AIProviderError,
        match="AI provider returned an empty professional description.",
    ):
        service.improve_professional_description("Desenvolvi APIs com Python.")


def test_improve_professional_description_strips_provider_response() -> None:
    provider = FakeAIProvider("  Desenvolveu APIs robustas com Python.  ")
    service = AIAssistantService(provider)

    result = service.improve_professional_description("Desenvolvi APIs com Python.")

    assert result.improved_text == "Desenvolveu APIs robustas com Python."


def test_prompt_contains_original_description() -> None:
    provider = FakeAIProvider("Descrição melhorada.")
    service = AIAssistantService(provider)

    service.improve_professional_description("Implementei integrações entre sistemas.")

    assert provider.received_prompt is not None
    assert "Implementei integrações entre sistemas." in provider.received_prompt


def test_prompt_contains_anti_hallucination_instructions() -> None:
    provider = FakeAIProvider("Descrição melhorada.")
    service = AIAssistantService(provider)

    service.improve_professional_description("Desenvolvi soluções internas.")

    assert provider.received_prompt is not None
    assert "Preserve all factual information." in provider.received_prompt
    assert "Do not invent technologies" in provider.received_prompt
    assert "achievements" in provider.received_prompt
    assert "qualifications" in provider.received_prompt


def test_prompt_requests_only_improved_description() -> None:
    provider = FakeAIProvider("Descrição melhorada.")
    service = AIAssistantService(provider)

    service.improve_professional_description("Criei automações em Python.")

    assert provider.received_prompt is not None
    assert "Return only the improved description." in provider.received_prompt
