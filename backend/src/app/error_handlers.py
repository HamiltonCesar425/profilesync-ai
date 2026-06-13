from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.exceptions import (
    DomainError,
    InvalidProfileDataError,
    ProfileNotFoundError,
)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ProfileNotFoundError)
    async def profile_not_found_handler(
        request: Request,
        exc: ProfileNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "error": "profile_not_found",
                "message": str(exc),
            },
        )

    @app.exception_handler(InvalidProfileDataError)
    async def invalid_profile_data_handler(
        request: Request,
        exc: InvalidProfileDataError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "error": "invalid_profile_data",
                "message": str(exc),
            },
        )

    @app.exception_handler(DomainError)
    async def domain_error_handler(
        request: Request,
        exc: DomainError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "error": "domain_error",
                "message": str(exc),
            },
        )
