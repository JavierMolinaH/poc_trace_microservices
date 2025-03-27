import uuid

from fastapi import FastAPI, Request
from starlette.responses import Response

from common.logging_config import set_operation_id


async def operation_id_middleware(request: Request, call_next):
    operation_id = request.headers.get("X-Operation-Id", str(uuid.uuid4()))
    request.state.operation_id = operation_id
    set_operation_id(operation_id)
    response: Response = await call_next(request)
    return response


def register_operation_id_middleware(app: FastAPI):
    app.middleware("http")(operation_id_middleware)
