from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATABASE_FILE = DATA_DIR / "profilesync.db"

DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DATABASE_FILE.as_posix()}"
