import uuid

import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from common.exceptions import register_exception_handlers
from common.logging_config import get_logger
from common.middelwares.operation_id import register_operation_id_middleware
from common.server_request_hooks import add_operation_id_to_span
from common.tracing_config import init_tracer

app = FastAPI()
logger = get_logger("microservice1")
tracer = init_tracer(service_name="microservice1")

FastAPIInstrumentor.instrument_app(app, server_request_hook=add_operation_id_to_span)
RequestsInstrumentor().instrument()

register_operation_id_middleware(app)
register_exception_handlers(app)


@app.get("/")
def index(request: Request):
    operation_id = getattr(request.state, "operation_id", str(uuid.uuid4()))
    logger.info(f"Calling microservice2 with operation_id={operation_id}")
    headers = {"X-Operation-Id": operation_id}
    try:
        r = requests.get("http://localhost:8002", headers=headers)
        return r.json()
    except Exception as e:
        logger.error(f"Error calling microservice2: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    uvicorn.run("microservice1.main:app", host="0.0.0.0", port=8001, reload=True)
