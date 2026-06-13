from fastapi import FastAPI

from api.v1.profile_routes import router as profile_router
from app.error_handlers import register_error_handlers
from database.session import Base, engine
from models import profile_model

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ProfileSync AI API",
    version="0.1.0",
    description="API para gestão e geração assistida de perfis profissionais.",
)

register_error_handlers(app)


app.include_router(profile_router)


@app.get("/")
def read_root():
    return {
        "message": "ProfileSync AI API is running",
    }
