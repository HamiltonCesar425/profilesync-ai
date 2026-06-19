from jose import jwt

from core.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_password_hash,
    verify_password,
)


def test_get_password_hash_returns_different_value() -> None:
    password = "strong-password"

    hashed_password = get_password_hash(password)

    assert hashed_password != password


def test_verify_password_with_valid_password() -> None:
    password = "strong-password"
    hashed_password = get_password_hash(password)

    result = verify_password(password, hashed_password)

    assert result is True


def test_verify_password_with_invalid_password() -> None:
    password = "strong-password"
    hashed_password = get_password_hash(password)

    result = verify_password("wrong-password", hashed_password)

    assert result is False


def test_create_access_token() -> None:
    token = create_access_token({"sub": "user@example.com"})

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    assert payload["sub"] == "user@example.com"
    assert "exp" in payload
