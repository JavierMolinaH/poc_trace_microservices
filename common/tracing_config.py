from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def init_tracer(service_name: str = "poc-service"):
    """
    Inicializa el tracer de OpenTelemetry con exportador de Google Cloud.
    Aplica instrumentación a FastAPI y peticiones requests.
    """

    # Define el recurso (metadatos) de la aplicación
    resource = Resource(attributes={"service.name": service_name})

    # Creamos el TracerProvider con ese recurso
    provider = TracerProvider(resource=resource)

    # Exportador a Google Cloud Trace
    cloud_trace_exporter = CloudTraceSpanExporter(project_id="poctracemicroservices")

    # Procesador que envía spans en batch
    provider.add_span_processor(BatchSpanProcessor(cloud_trace_exporter))

    # Registrar el provider
    trace.set_tracer_provider(provider)

    # Instrumentaciones (FastAPI + Requests)
    # NOTA: la instrumentación de FastAPI configurará automáticamente
    # un middleware que crea spans para cada request HTTP entrante.
    RequestsInstrumentor().instrument()
    # Difiere la instrumentación de FastAPI hasta tener la app
    # en run-time (ver más abajo cómo aplicarlo en main.py).

    return trace.get_tracer(__name__)
