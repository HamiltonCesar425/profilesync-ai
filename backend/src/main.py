from fastapi import FastAPI

from api.v1.profile_routes import router as profile_router
from api.v1.auth_routes import router as auth_router
from api.v1.resume_routes import router as resume_router
from api.v1.export_routes import router as export_router
from app.error_handlers import register_error_handlers
from core.logging_config import configure_logging
from database.session import Base, engine

configure_logging()


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ProfileSync AI API",
    version="0.1.0",
    description="API para gestão e geração assistida de perfis profissionais.",
)

register_error_handlers(app)


app.include_router(profile_router)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(export_router)


@app.get("/")
def read_root():
    return {
        "message": "ProfileSync AI API is running",
    }
