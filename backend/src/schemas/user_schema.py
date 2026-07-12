from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

AUTH_SCHEME = "bearer"
OPENAPI_CREDENTIAL_SAMPLE = "strong-password"
OPENAPI_JWT_SAMPLE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ..., description="E-mail cadastrado do usuário.", examples=["teste@example.com"]
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Senha do usuário.",
        examples=[OPENAPI_CREDENTIAL_SAMPLE],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "teste@example.com",
                "password": OPENAPI_CREDENTIAL_SAMPLE,
            }
        }
    )


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="Token JWT de acesso.",
        examples=[OPENAPI_JWT_SAMPLE],
    )
    token_type: str = Field(
        default=AUTH_SCHEME,
        description="Tipo do token retornado.",
        examples=[AUTH_SCHEME],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": OPENAPI_JWT_SAMPLE,
                "token_type": AUTH_SCHEME,
            }
        }
    )
