import uvicorn
from fastapi import FastAPI, Request
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from common.exceptions import register_exception_handlers
from common.logging_config import get_logger
from common.middelwares.operation_id import register_operation_id_middleware
from common.server_request_hooks import add_operation_id_to_span
from common.tracing_config import init_tracer

app = FastAPI()
logger = get_logger("microservice3")
tracer = init_tracer(service_name="microservice3")

FastAPIInstrumentor.instrument_app(app, server_request_hook=add_operation_id_to_span)
RequestsInstrumentor().instrument()

register_operation_id_middleware(app)
register_exception_handlers(app)


@app.get("/")
def index(request: Request):
    logger.info("Hello from microservice3 - root endpoint")
    operation_id = getattr(request.state, "operation_id", None)
    raise ValueError(
        f"This is a test error for microservice3 with operation_id={operation_id}"
    )


if __name__ == "__main__":
    uvicorn.run("microservice3.main:app", host="0.0.0.0", port=8003, reload=True)
