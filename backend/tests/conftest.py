from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models.user_model import User


@pytest.fixture(autouse=True)
def reset_database() -> Generator[Session, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(reset_database: Session) -> Session:
    return reset_database

def create_test_user(db_session: Session, email: str) -> User:
    user = User(
        email=email,
        hashed_password="hashed-password",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user(db_session: Session) -> User:
    return create_test_user(db_session, "user@example.com")


@pytest.fixture
def other_user(db_session: Session) -> User:
    return create_test_user(db_session, "other@example.com")
