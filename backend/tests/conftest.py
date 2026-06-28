from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine


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
