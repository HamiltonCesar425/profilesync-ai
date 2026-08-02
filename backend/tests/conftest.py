import os
import tempfile
from collections.abc import Generator
from pathlib import Path

os.environ.setdefault(
    "PROFILESYNC_SECRET_KEY",
    "test-only-secret-key-that-is-long-enough-for-automated-tests",
)

# Configure an isolated database before importing application modules. The
# temporary directory remains alive for the whole pytest process and is cleaned
# after the database engine is disposed.
TEST_DATABASE_DIRECTORY = tempfile.TemporaryDirectory(prefix="profilesync-tests-")
TEST_DATABASE_FILE = Path(TEST_DATABASE_DIRECTORY.name) / "profilesync-test.db"
os.environ["PROFILESYNC_DATABASE_URL"] = (
    f"sqlite:///{TEST_DATABASE_FILE.as_posix()}"
)

import pytest
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from core.login_rate_limiter import login_rate_limiter
from core.security import create_access_token
from models.user_model import User


def _assert_test_database_is_isolated() -> None:
    development_database_file = (
        Path(__file__).resolve().parents[1] / "data" / "profilesync.db"
    ).resolve()
    configured_database_file = Path(engine.url.database or "").resolve()

    if configured_database_file == development_database_file:
        raise RuntimeError(
            "Tests must not run against the development database: "
            f"{development_database_file}"
        )


def pytest_sessionfinish() -> None:
    engine.dispose()
    TEST_DATABASE_DIRECTORY.cleanup()


@pytest.fixture(autouse=True)
def reset_database() -> Generator[Session, None, None]:
    login_rate_limiter.reset()
    _assert_test_database_is_isolated()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    Base.metadata.drop_all(bind=engine)
    login_rate_limiter.reset()


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


@pytest.fixture
def auth_headers(test_user: User) -> dict[str, str]:
    token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}
