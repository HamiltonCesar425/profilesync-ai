from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
import jwt
import pytest

import core.auth as auth_module
from core.security import ALGORITHM, SECRET_KEY, create_access_token


class FixedUserRepository:
    def __init__(self, _db, user: object) -> None:
        self.user = user

    def get_by_email(self, email: str) -> object | None:
        if email == "user@example.com":
            return self.user
        return None


def assert_unauthorized(token: str) -> None:
    with pytest.raises(HTTPException) as exc_info:
        auth_module.get_current_user(token=token, db=object())

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


def test_accepts_valid_unexpired_token(monkeypatch: pytest.MonkeyPatch) -> None:
    expected_user = object()
    monkeypatch.setattr(
        auth_module,
        "UserRepository",
        lambda db: FixedUserRepository(db, expected_user),
    )
    token = create_access_token({"sub": "user@example.com"})

    current_user = auth_module.get_current_user(token=token, db=object())

    assert current_user is expected_user


def test_rejects_expired_token() -> None:
    token = jwt.encode(
        {
            "sub": "user@example.com",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    assert_unauthorized(token)


def test_rejects_signed_token_without_expiration() -> None:
    token = jwt.encode(
        {"sub": "user@example.com"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    assert_unauthorized(token)


def test_rejects_signed_token_without_subject() -> None:
    token = jwt.encode(
        {"exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    assert_unauthorized(token)


def test_rejects_token_with_invalid_signature() -> None:
    token = jwt.encode(
        {
            "sub": "user@example.com",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        "different-test-signing-key-with-safe-length",
        algorithm=ALGORITHM,
    )

    assert_unauthorized(token)
