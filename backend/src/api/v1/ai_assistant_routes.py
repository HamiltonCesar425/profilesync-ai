from fastapi import APIRouter, Depends

from core.auth import get_current_user
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
    return AIAssistantService(
        provider=OpenAIClient(),
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
    return service.improve_professional_description(
        text=request.text,
    )
