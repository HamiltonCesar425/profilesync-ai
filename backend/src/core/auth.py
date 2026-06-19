from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.security import ALGORITHM, SECRET_KEY
from database.session import get_db
from models.user_model import User
from repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError as exc:
        raise credentials_exception from exc

    user_repository = UserRepository(db)
    user = user_repository.get_by_email(email)

    if user is None:
        raise credentials_exception

    return user
