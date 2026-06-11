from fastapi import FastAPI

from api.v1.profile_routes import router as profile_router

app = FastAPI(
    title="ProfileSync AI API",
    version="0.1.0",
    description="API para gestão e geração assistida de perfis profissionais.",
)

app.include_router(profile_router)


@app.get("/")
def read_root():
    return {
        "message": "ProfileSync AI API ia running",
    }
