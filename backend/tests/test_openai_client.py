from types import SimpleNamespace
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import httpx
import pytest
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
)

from core.exceptions import (
    AIConfigurationError,
    AIProviderError,
    AIProviderUnavailableError,
    AIResponseError,
)
from integrations.openai_client import OpenAIClient


@pytest.fixture
def openai_sdk_client() -> Generator[MagicMock, None, None]:
    with patch("integrations.openai_client.OpenAI") as openai_class:
        sdk_client = MagicMock()
        openai_class.return_value = sdk_client
        yield sdk_client


def create_http_response(status_code: int) -> httpx.Response:
    request = httpx.Request(
        method="POST",
        url="https://api.openai.com/v1/responses",
    )
    return httpx.Response(
        status_code=status_code,
        request=request,
    )


def test_initializes_openai_sdk_with_api_key() -> None:
    with patch("integrations.openai_client.OpenAI") as openai_class:
        OpenAIClient(
            api_key="test-api-key",
            model="gpt-5-mini",
        )

    openai_class.assert_called_once_with(
        api_key="test-api-key",
    )


@pytest.mark.parametrize(
    "api_key",
    [
        None,
        "",
    ],
)
def test_rejects_missing_api_key(
    api_key: str | None,
) -> None:
    with pytest.raises(
        AIConfigurationError,
        match="OPENAI_API_KEY is not configured",
    ):
        OpenAIClient(
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
def test_rejects_empty_model(model: str) -> None:
    with pytest.raises(
        AIConfigurationError,
        match="OPENAI_MODEL must not be empty",
    ):
        OpenAIClient(
            api_key="test-api-key",
            model=model,
        )


def test_generate_returns_stripped_output_text(
    openai_sdk_client: MagicMock,
) -> None:
    openai_sdk_client.responses.create.return_value = SimpleNamespace(
        output_text="  Improved professional description.  "
    )

    client = OpenAIClient(
        api_key="test-api-key",
        model="gpt-5-mini",
    )

    result = client.generate(
        "Improve this professional description."
    )

    assert result == "Improved professional description."


def test_generate_normalizes_prompt(
    openai_sdk_client: MagicMock,
) -> None:
    openai_sdk_client.responses.create.return_value = SimpleNamespace(
        output_text="Improved description."
    )

    client = OpenAIClient(
        api_key="test-api-key",
        model="gpt-5-mini",
    )

    client.generate(
        "  Improve this description.  "
    )

    openai_sdk_client.responses.create.assert_called_once_with(
        model="gpt-5-mini",
        input="Improve this description.",
    )


@pytest.mark.parametrize(
    "prompt",
    [
        "",
        "   ",
        "\n\t",
    ],
)
def test_generate_rejects_empty_prompt(
    openai_sdk_client: MagicMock,
    prompt: str,
) -> None:
    client = OpenAIClient(
        api_key="test-api-key",
        model="gpt-5-mini",
    )

    with pytest.raises(
        AIConfigurationError,
        match="Prompt must not be empty",
    ):
        client.generate(prompt)

    openai_sdk_client.responses.create.assert_not_called()


@pytest.mark.parametrize(
    "output_text",
    [
        None,
        "",
        "   ",
        "\n\t",
    ],
)
def test_generate_rejects_empty_response(
    openai_sdk_client: MagicMock,
    output_text: str | None,
) -> None:
    openai_sdk_client.responses.create.return_value = SimpleNamespace(
        output_text=output_text
    )

    client = OpenAIClient(
        api_key="test-api-key",
        model="gpt-5-mini",
    )

    with pytest.raises(
        AIResponseError,
        match="OpenAI returned an empty response",
    ):
        client.generate("Valid prompt.")


def test_generate_translates_authentication_error(
    openai_sdk_client: MagicMock,
) -> None:
    response = create_http_response(status_code=401)

    openai_sdk_client.responses.create.side_effect = AuthenticationError(
        "Invalid API key.",
        response=response,
        body=None,
    )

    client = OpenAIClient(
        api_key="invalid-api-key",
        model="gpt-5-mini",
    )

    with pytest.raises(
        AIConfigurationError,
        match="OpenAI authentication failed",
    ):
        client.generate("Valid prompt.")


def test_generate_translates_timeout_error(
    openai_sdk_client: MagicMock,
) -> None:
    request = httpx.Request(
        method="POST",
        url="https://api.openai.com/v1/responses",
    )

    openai_sdk_client.responses.create.side_effect = APITimeoutError(
        request=request
    )

    client = OpenAIClient(
        api_key="test-api-key",
        model="gpt-5-mini",
    )

    with pytest.raises(
        AIProviderUnavailableError,
        match="OpenAI API is temporarily unavailable",
    ):
        client.generate("Valid prompt.")


def test_generate_translates_connection_error(
    openai_sdk_client: MagicMock,
) -> None:
    request = httpx.Request(
        method="POST",
        url="https://api.openai.com/v1/responses",
    )

    openai_sdk_client.responses.create.side_effect = APIConnectionError(
        message="Connection failed.",
        request=request,
    )

    client = OpenAIClient(
        api_key="test-api-key",
        model="gpt-5-mini",
    )

    with pytest.raises(
        AIProviderUnavailableError,
        match="OpenAI API is temporarily unavailable",
    ):
        client.generate("Valid prompt.")


def test_generate_translates_rate_limit_error(
    openai_sdk_client: MagicMock,
) -> None:
    response = create_http_response(status_code=429)

    openai_sdk_client.responses.create.side_effect = RateLimitError(
        "Rate limit exceeded.",
        response=response,
        body=None,
    )

    client = OpenAIClient(
        api_key="test-api-key",
        model="gpt-5-mini",
    )

    with pytest.raises(
        AIProviderUnavailableError,
        match="OpenAI API is temporarily unavailable",
    ):
        client.generate("Valid prompt.")


def test_generate_translates_server_error(
    openai_sdk_client: MagicMock,
) -> None:
    response = create_http_response(status_code=500)

    openai_sdk_client.responses.create.side_effect = APIStatusError(
        "Internal server error.",
        response=response,
        body=None,
    )

    client = OpenAIClient(
        api_key="test-api-key",
        model="gpt-5-mini",
    )

    with pytest.raises(
        AIProviderUnavailableError,
        match="OpenAI API is temporarily unavailable",
    ):
        client.generate("Valid prompt.")


def test_generate_translates_client_status_error(
    openai_sdk_client: MagicMock,
) -> None:
    response = create_http_response(status_code=400)

    openai_sdk_client.responses.create.side_effect = APIStatusError(
        "Invalid request.",
        response=response,
        body=None,
    )

    client = OpenAIClient(
        api_key="test-api-key",
        model="gpt-5-mini",
    )

    with pytest.raises(
        AIProviderError,
        match="OpenAI API rejected the request",
    ):
        client.generate("Valid prompt.")


def test_generate_translates_unexpected_error(
    openai_sdk_client: MagicMock,
) -> None:
    openai_sdk_client.responses.create.side_effect = RuntimeError(
        "Unexpected internal failure."
    )

    client = OpenAIClient(
        api_key="test-api-key",
        model="gpt-5-mini",
    )

    with pytest.raises(
        AIProviderError,
        match="Unexpected error while communicating with OpenAI",
    ):
        client.generate("Valid prompt.")
