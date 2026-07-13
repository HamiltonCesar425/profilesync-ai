from openai import OpenAI

from services.providers.base_provider import AIProvider


class OpenAIProvider(AIProvider):
    def __init__(
        self,
        api_key: str,
        model: str,
    ) -> None:
        if not api_key.strip():
            raise ValueError("OpenAI API key must not be empty.")

        if not model.strip():
            raise ValueError("OpenAI model must not be empty.")

        self._model = model.strip()
        self._client = OpenAI(
            api_key=api_key.strip(),
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        response = self._client.responses.create(
            model=self._model,
            input=prompt,
        )

        return response.output_text
