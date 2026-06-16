from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.settings import DATABASE_URL, DATABASE_FILE


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
print(f"USING DATABASE_URL: {DATABASE_URL}")
print(f"USING DATABASE_FILE: {DATABASE_FILE}")
print(f"DATABASE_FILE EXISTS: {DATABASE_FILE.exists()}")

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
