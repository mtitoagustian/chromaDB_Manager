from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import ASGIApp
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
import traceback
import logging

logger = logging.getLogger("uvicorn.error")

class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
                return await call_next(request)
            
            response = await call_next(request)
            if response.status_code >= 400:
                return response  # biarkan error handler tangani
            # response.body() tidak bisa diakses langsung karena sudah dibaca,
            # maka cukup beri respons generik jika content-type JSON
            return JSONResponse(
                content={
                    "code": response.status_code,
                    "message": "Success",
                    "data": await response.json() if "application/json" in response.headers.get("content-type", "") else None
                },
                status_code=response.status_code
            )
        except Exception as e:
            logger.exception("Unhandled Exception")
            return JSONResponse(
                status_code=500,
                content={
                    "code": 500,
                    "message": "Internal Server Error",
                    "data": str(e)
                }
            )

# Optional: Global exception handler (untuk HTTPException dan ValidationError)
def register_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(f"HTTPException: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail,
                "data": None
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "code": 422,
                "message": "Validation error",
                "data": exc.errors()
            }
        )
