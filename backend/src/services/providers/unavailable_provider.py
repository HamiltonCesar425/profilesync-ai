from services.providers.base_provider import AIProvider


class UnavailableAIProvider(AIProvider):
    def generate(self, prompt: str) -> str:
        raise RuntimeError("AI assistant provider is not configured.")
