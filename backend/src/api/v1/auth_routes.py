from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_auth_service
from schemas.user_schema import Token, UserCreate, UserResponse
from services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
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
    response_model=Token,
)
def login_user(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    user = auth_service.authenticate_user(
        email=user_data.email,
        password=user_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = auth_service.create_user_access_token(user)

    return Token(
        access_token=access_token,
        token_type="bearer",
    )
