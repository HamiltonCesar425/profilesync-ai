from types import SimpleNamespace

import pytest

from schemas.user_schema import UserCreate
from services.auth_service import AuthService


class FakeUserRepository:
    def __init__(self) -> None:
        self.users: dict[str, SimpleNamespace] = {}

    def get_by_email(self, email: str) -> SimpleNamespace | None:
        return self.users.get(email)

    def create_user(
        self,
        email: str,
        hashed_password: str,
    ) -> SimpleNamespace:
        user = SimpleNamespace(
            id=1,
            email=email,
            hashed_password=hashed_password,
        )

        self.users[email] = user

        return user


def test_register_user() -> None:
    repository = FakeUserRepository()
    service = AuthService(repository)

    user_data = UserCreate(
        email="user@example.com",
        password="strong-password",
    )

    user = service.register_user(user_data)

    assert user.email == "user@example.com"
    assert user.hashed_password != "strong-password"


def test_register_existing_user_raises_error() -> None:
    repository = FakeUserRepository()
    service = AuthService(repository)

    user_data = UserCreate(
        email="user@example.com",
        password="strong-password",
    )

    service.register_user(user_data)

    with pytest.raises(ValueError, match="Email already registered"):
        service.register_user(user_data)


def test_authenticate_user_with_valid_credentials() -> None:
    repository = FakeUserRepository()
    service = AuthService(repository)

    user_data = UserCreate(
        email="user@example.com",
        password="strong-password",
    )

    service.register_user(user_data)

    user = service.authenticate_user(
        email="user@example.com",
        password="strong-password",
    )

    assert user is not None
    assert user.email == "user@example.com"


def test_authenticate_user_with_invalid_email() -> None:
    repository = FakeUserRepository()
    service = AuthService(repository)

    user = service.authenticate_user(
        email="missing@example.com",
        password="strong-password",
    )

    assert user is None


def test_authenticate_user_with_invalid_password() -> None:
    repository = FakeUserRepository()
    service = AuthService(repository)

    user_data = UserCreate(
        email="user@example.com",
        password="strong-password",
    )

    service.register_user(user_data)

    user = service.authenticate_user(
        email="user@example.com",
        password="wrong-password",
    )

    assert user is None


def test_create_user_access_token() -> None:
    repository = FakeUserRepository()
    service = AuthService(repository)

    user_data = UserCreate(
        email="user@example.com",
        password="strong-password",
    )

    user = service.register_user(user_data)

    token = service.create_user_access_token(user)

    assert isinstance(token, str)
    assert token
