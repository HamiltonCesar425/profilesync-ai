from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)

from core.exceptions import (
    AIConfigurationError,
    AIProviderError,
    AIProviderUnavailableError,
    AIResponseError,
)
from core.settings import OPENAI_API_KEY, OPENAI_MODEL


class OpenAIClient:
    """Cliente responsável pela comunicação com a API da OpenAI."""

    def __init__(
        self,
        api_key: str | None = OPENAI_API_KEY,
        model: str = OPENAI_MODEL,
    ) -> None:
        if not api_key:
            raise AIConfigurationError("OPENAI_API_KEY is not configured.")

        if not model.strip():
            raise AIConfigurationError("OPENAI_MODEL must not be empty.")

        self._model = model.strip()
        self._client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:
        normalized_prompt = prompt.strip()

        if not normalized_prompt:
            raise AIConfigurationError("Prompt must not be empty.")

        try:
            response = self._client.responses.create(
                model=self._model,
                input=normalized_prompt,
            )
        except AuthenticationError as exc:
            raise AIConfigurationError("OpenAI authentication failed.") from exc
        except (
            APITimeoutError,
            APIConnectionError,
            RateLimitError,
        ) as exc:
            raise AIProviderUnavailableError(
                "OpenAI API is temporarily unavailable."
            ) from exc
        except APIStatusError as exc:
            if exc.status_code >= 500:
                raise AIProviderUnavailableError(
                    "OpenAI API is temporarily unavailable."
                ) from exc

            raise AIProviderError("OpenAI API rejected the request.") from exc
        except Exception as exc:
            raise AIProviderError(
                "Unexpected error while communicating with OpenAI."
            ) from exc

        output_text = response.output_text

        if not output_text or not output_text.strip():
            raise AIResponseError("OpenAI returned an empty response.")

        return output_text.strip()
