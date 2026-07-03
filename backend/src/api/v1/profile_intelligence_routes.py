from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from core.auth import get_current_user
from models.user_model import User
from schemas.profile_intelligence_schema import ProfessionalDiagnosis
from services.profile_intelligence_service import ProfileIntelligenceService

router = APIRouter(
    prefix="/profile-intelligence",
    tags=["Profile Intelligence"],
)


@router.post(
    "/analyze",
    response_model=ProfessionalDiagnosis,
    status_code=status.HTTP_200_OK,
)
def analyze_profile(
    target_role: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfessionalDiagnosis:
    """Gera diagnóstico profissional inicial para o usuário autenticado."""

    service = ProfileIntelligenceService()

    return service.generate_diagnosis(
        target_role=target_role,
        technologies=[],
        projects_count=0,
        experiences_count=0,
    )
