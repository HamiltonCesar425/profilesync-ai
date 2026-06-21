from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


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
        examples=["strong-password"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "teste@example.com",
                "password": "strong-password",
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
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    token_type: str = Field(
        default="bearer",
        description="Tipo do token retornado.",
        examples=["bearer"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    )
