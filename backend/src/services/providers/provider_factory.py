from core.settings import OPENAI_API_KEY, OPENAI_MODEL
from services.providers.base_provider import AIProvider
from services.providers.openai_provider import OpenAIProvider
from services.providers.unavailable_provider import (
    UnavailableAIProvider,
)


def create_ai_provider() -> AIProvider:
    if not OPENAI_API_KEY:
        return UnavailableAIProvider()

    return OpenAIProvider(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
    )
