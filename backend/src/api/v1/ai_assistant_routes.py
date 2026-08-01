from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import get_current_user
from core.exceptions import (
    AIConfigurationError,
    AIProviderUnavailableError,
)
from integrations.openai_client import OpenAIClient
from models.user_model import User
from schemas.ai_assistant_schema import (
    ImproveProfessionalDescriptionRequest,
    ImproveProfessionalDescriptionResponse,
)
from services.ai_assistant_service import AIAssistantService

router = APIRouter(
    prefix="/ai-assistant",
    tags=["AI Assistant"],
)


def get_ai_assistant_service() -> AIAssistantService:
    try:
        provider = OpenAIClient()
    except AIConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "O recurso de IA está temporariamente indisponível. "
                "Você pode continuar editando sua descrição manualmente."
            ),
        ) from exc

    return AIAssistantService(
        provider=provider,
    )


@router.post(
    "/improve-professional-description",
    response_model=ImproveProfessionalDescriptionResponse,
)
def improve_professional_description(
    request: ImproveProfessionalDescriptionRequest,
    current_user: User = Depends(get_current_user),
    service: AIAssistantService = Depends(get_ai_assistant_service),
) -> ImproveProfessionalDescriptionResponse:
    del current_user

    try:
        return service.improve_professional_description(
            text=request.text,
        )
    except AIProviderUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "O serviço de IA está temporariamente indisponível. "
                "Tente novamente mais tarde."
            ),
        ) from exc
