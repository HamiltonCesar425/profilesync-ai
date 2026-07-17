import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

PROFILESYNC_SECRET_KEY = os.getenv("PROFILESYNC_SECRET_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5-mini",
)

DEFAULT_CORS_ALLOWED_ORIGINS = "http://localhost:5173"

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        DEFAULT_CORS_ALLOWED_ORIGINS,
    ).split(",")
    if origin.strip()
]

DATA_DIR = BASE_DIR / "data"
DATABASE_FILE = DATA_DIR / "profilesync.db"

DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DATABASE_FILE.as_posix()}"
