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


_global_operation_id = None


def set_operation_id(operation_id: str):
    global _global_operation_id
    _global_operation_id = operation_id


def get_operation_id() -> str:
    return _global_operation_id or "NO-OPERATION-ID"


class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["operation_id"] = get_operation_id()
        log_record["environment"] = os.getenv("ENVIRONMENT", "local")


def get_logger(name: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    use_gcp_logging = os.getenv("USE_GCP_LOGGING", "").lower() in ["true", "1"] or False

    if use_gcp_logging and GCP_AVAILABLE:
        client = cloud_logging.Client()
        gcp_handler = CloudLoggingHandler(client, name=name or "poc-logger")
        gcp_handler.setFormatter(CustomJsonFormatter())
        logger.addHandler(gcp_handler)
    else:
        handler = logging.StreamHandler()
        formatter = CustomJsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
