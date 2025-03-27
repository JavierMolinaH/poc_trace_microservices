from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def init_tracer(service_name: str = "poc-service"):
    resource = Resource(attributes={"service.name": service_name})
    provider = TracerProvider(resource=resource)
    cloud_trace_exporter = CloudTraceSpanExporter(project_id="poctracemicroservices")
    provider.add_span_processor(BatchSpanProcessor(cloud_trace_exporter))
    trace.set_tracer_provider(provider)
    RequestsInstrumentor().instrument()
    return trace.get_tracer(__name__)
