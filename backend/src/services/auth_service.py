from models.user_model import User
from repositories.user_repository import UserRepository
from schemas.user_schema import UserCreate
from core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register_user(self, user_data: UserCreate) -> User:
        existing_user = self.user_repository.get_by_email(user_data.email)

        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = get_password_hash(user_data.password)

        return self.user_repository.create_user(
            email=user_data.email,
            hashed_password=hashed_password,
        )

    def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> User | None:
        user = self.user_repository.get_by_email(email)

        if not user:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        return user

    def create_user_access_token(self, user: User) -> str:
        return create_access_token(
            data={"sub": user.email},
        )
