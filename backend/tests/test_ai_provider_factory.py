from services.providers.openai_provider import OpenAIProvider
from services.providers.provider_factory import create_ai_provider
from services.providers.unavailable_provider import (
    UnavailableAIProvider,
)


def test_create_ai_provider_returns_unavailable_without_api_key(
    monkeypatch,
):
    monkeypatch.setattr(
        "services.providers.provider_factory.OPENAI_API_KEY",
        None,
    )

    provider = create_ai_provider()

    assert isinstance(provider, UnavailableAIProvider)


def test_create_ai_provider_returns_openai_provider_with_api_key(
    monkeypatch,
):
    monkeypatch.setattr(
        "services.providers.provider_factory.OPENAI_API_KEY",
        "test-api-key",
    )
    monkeypatch.setattr(
        "services.providers.provider_factory.OPENAI_MODEL",
        "gpt-5-mini",
    )

    class FakeOpenAI:
        def __init__(self, *, api_key: str) -> None:
            self.api_key = api_key

    monkeypatch.setattr(
        "services.providers.openai_provider.OpenAI",
        FakeOpenAI,
    )

    provider = create_ai_provider()

    assert isinstance(provider, OpenAIProvider)
