import pytest

from services.providers.base_provider import AIProvider
from services.providers.unavailable_provider import (
    UnavailableAIProvider,
)


def test_ai_provider_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AIProvider()


def test_unavailable_ai_provider_raises_runtime_error():
    provider = UnavailableAIProvider()

    with pytest.raises(
        RuntimeError,
        match="AI assistant provider is not configured.",
    ):
        provider.generate("Improve this professional description.")
