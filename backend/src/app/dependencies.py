from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from database.session import SessionLocal
from repositories.profile_repository import ProfileRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.profile_service import ProfileService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_profile_service(
    db: Session = Depends(get_db),
) -> ProfileService:
    profile_repository = ProfileRepository(db)
    return ProfileService(profile_repository)


def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    user_repository = UserRepository(db)
    return AuthService(user_repository)
