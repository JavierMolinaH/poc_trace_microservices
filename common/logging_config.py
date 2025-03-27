# common/logging_config.py

import logging
import os

from pythonjsonlogger.json import JsonFormatter

try:
    from google.cloud import logging as cloud_logging
    from google.cloud.logging_v2.handlers import CloudLoggingHandler

    GCP_AVAILABLE = True
except ImportError:
    GCP_AVAILABLE = False


# Variable global para almacenar un operation_id (ej: vía contextvars, request.state, etc.)
# Para la demo, usaremos una variable global simple, pero en un proyecto real
# podrías usar contextvars o el state de FastAPI.
_global_operation_id = None


def set_operation_id(operation_id: str):
    """Asignar operation_id para los logs (en un request entrante, por ejemplo)."""
    global _global_operation_id
    _global_operation_id = operation_id


def get_operation_id() -> str:
    """Obtener el operation_id actual."""
    return _global_operation_id or "NO-OPERATION-ID"


class CustomJsonFormatter(JsonFormatter):
    """
    Formateador JSON que añade el operation_id a cada log.
    """

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        # Añadimos el operation_id
        log_record["operation_id"] = get_operation_id()
        # Puedes incluir más campos personalizados si quieres:
        log_record["environment"] = os.getenv("ENVIRONMENT", "local")


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Retorna un logger configurado.
    Si detecta que estamos en GCP (o se forzó su uso), utiliza CloudLoggingHandler.
    Si no, usa un StreamHandler local con JSON.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        # Evitar configurar dos veces el logger.
        return logger

    logger.setLevel(logging.INFO)

    # ¿Estamos en GCP o en local?
    use_gcp_logging = os.getenv("USE_GCP_LOGGING", "").lower() in ["true", "1"] or False

    if use_gcp_logging and GCP_AVAILABLE:
        # En GCP - Usa Cloud Logging
        client = cloud_logging.Client()
        gcp_handler = CloudLoggingHandler(client, name=name or "poc-logger")
        gcp_handler.setFormatter(CustomJsonFormatter())
        logger.addHandler(gcp_handler)
    else:
        # Local - Usa un StreamHandler con JSON
        handler = logging.StreamHandler()
        formatter = CustomJsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
