# common/exceptions.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from common.logging_config import get_logger

logger = get_logger("exceptions")


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, HTTPException):
        logger.error(f"HTTPException: {exc.detail}", exc_info=True)
    else:
        logger.error(f"Unhandled exception: {repr(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "operation_id": request.state.operation_id,
        },
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(RuntimeError, global_exception_handler)
    app.add_exception_handler(ValueError, global_exception_handler)
    app.add_exception_handler(KeyError, global_exception_handler)
    app.add_exception_handler(HTTPException, global_exception_handler)
    app.add_exception_handler(RequestValidationError, global_exception_handler)
