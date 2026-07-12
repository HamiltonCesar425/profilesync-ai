import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.settings import DATABASE_URL, DATABASE_FILE

logger = logging.getLogger(__name__)


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
logger.info(
    "Database configured (driver=%s, file_exists=%s)",
    engine.url.drivername,
    DATABASE_FILE.exists(),
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
