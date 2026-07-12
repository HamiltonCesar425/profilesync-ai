from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_auth_service
from core.login_rate_limiter import login_rate_limiter
from schemas.user_schema import TokenResponse, UserCreate, UserResponse
from services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuário",
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
    summary="Login OAuth2 com email e senha",
    description=(
        "Autentica o usuário pelo fluxo OAuth2 Password Flow usado pelo Swagger. "
        "No campo username, informe o email cadastrado. "
        "No campo password, informe a senha. "
        "Após autorizar, o Swagger enviará automaticamente o token Bearer "
        "para os endpoints protegidos."
    ),
)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    client_host = request.client.host if request.client else "unknown"
    attempt_key = f"{client_host}:{form_data.username.strip().casefold()}"
    login_rate_limiter.check(attempt_key)

    try:
        response = auth_service.login(
            email=form_data.username,
            password=form_data.password,
        )
    except HTTPException as exc:
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            login_rate_limiter.record_failure(attempt_key)
        raise

    login_rate_limiter.reset(attempt_key)
    return response
