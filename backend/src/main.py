from fastapi import FastAPI

from api.v1.career_intelligence_routes import router as career_intelligence_router
from api.v1.job_routes import router as job_router
from api.v1.profile_intelligence_routes import router as profile_intelligence_router
from api.v1 import professional_experience_routes
from api.v1.project_routes import router as project_router
from api.v1 import technology_routes
from api.v1.ats_routes import router as ats_router
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

app.include_router(career_intelligence_router)
app.include_router(job_router)
app.include_router(profile_intelligence_router)
app.include_router(professional_experience_routes.router)
app.include_router(project_router)
app.include_router(technology_routes.router)
app.include_router(ats_router)
app.include_router(profile_router)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(export_router)


@app.get("/")
def read_root():
    return {
        "message": "ProfileSync AI API is running",
    }
