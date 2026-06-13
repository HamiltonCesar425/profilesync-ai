from fastapi import Depends
from sqlalchemy.orm import Session

from database.session import get_db
from repositories.profile_repository import ProfileRepository
from services.profile_service import ProfileService


def get_profile_service(
    db: Session = Depends(get_db),
) -> ProfileService:
    repository = ProfileRepository(db=db)
    return ProfileService(repository=repository)
