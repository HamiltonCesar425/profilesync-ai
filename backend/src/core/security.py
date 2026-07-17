from core.settings import PROFILESYNC_SECRET_KEY

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext


if not PROFILESYNC_SECRET_KEY:
    raise RuntimeError(
        "PROFILESYNC_SECRET_KEY must be configured with a persistent random secret."
    )
SECRET_KEY = PROFILESYNC_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

