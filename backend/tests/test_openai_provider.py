from types import SimpleNamespace

import pytest

from services.providers.openai_provider import OpenAIProvider


class FakeResponses:
    def __init__(self) -> None:
        self.received_model = None
        self.received_input = None

    def create(
        self,
        *,
        model: str,
        input: str,
    ):
        self.received_model = model
        self.received_input = input

        return SimpleNamespace(
            output_text="Descrição profissional aprimorada.",
        )


class FakeOpenAIClient:
    def __init__(self) -> None:
        self.responses = FakeResponses()


def test_openai_provider_generates_text(monkeypatch):
    fake_client = FakeOpenAIClient()

    def fake_openai(*, api_key: str):
        assert api_key == "test-api-key"
        return fake_client

    monkeypatch.setattr(
        "services.providers.openai_provider.OpenAI",
        fake_openai,
    )

    provider = OpenAIProvider(
        api_key="test-api-key",
        model="gpt-5-mini",
    )

    result = provider.generate(
        "Improve this professional description.",
    )

    assert result == "Descrição profissional aprimorada."
    assert fake_client.responses.received_model == "gpt-5-mini"
    assert fake_client.responses.received_input == (
        "Improve this professional description."
    )


@pytest.mark.parametrize(
    "api_key",
    [
        "",
        "   ",
        "\n\t",
    ],
)
def test_openai_provider_rejects_empty_api_key(api_key):
    with pytest.raises(
        ValueError,
        match="OpenAI API key must not be empty.",
    ):
        OpenAIProvider(
            api_key=api_key,
            model="gpt-5-mini",
        )


@pytest.mark.parametrize(
    "model",
    [
        "",
        "   ",
        "\n\t",
    ],
)
def test_openai_provider_rejects_empty_model(model):
    with pytest.raises(
        ValueError,
        match="OpenAI model must not be empty.",
    ):
        OpenAIProvider(
            api_key="test-api-key",
            model=model,
        )


def test_openai_provider_strips_configuration(monkeypatch):
    captured_api_key = None

    def fake_openai(*, api_key: str):
        nonlocal captured_api_key
        captured_api_key = api_key

        return FakeOpenAIClient()

    monkeypatch.setattr(
        "services.providers.openai_provider.OpenAI",
        fake_openai,
    )

    provider = OpenAIProvider(
        api_key="  test-api-key  ",
        model="  gpt-5-mini  ",
    )

    provider.generate("Prompt")

    assert captured_api_key == "test-api-key"
