from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_auth_service
from schemas.user_schema import UserCreate, UserResponse, LoginRequest, TokenResponse
from services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    try:
        return auth_service.register_user(user_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login com email e senha",
    description=(
        "Autentica o usuário usando JSON no corpo da requissição. "
        "Após o login, copie o campo access_token retornado e use-o no "
        "botão Authorize do Swagger para acessar endpoints protegidos."
    ),
)
def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return auth_service.login(
        email=payload.email,
        password=payload.password,
    )
