import uuid


def add_operation_id_to_span(span, scope):
    """
    Este hook se ejecuta cuando se crea el span para cada request.
    `scope` es el scope de Starlette que contiene detalles de la request,
    incluidas las cabeceras.
    """
    if span and scope:
        # scope["headers"] es una lista de tuples [(b'header-name', b'header-value'), ...]
        headers = dict(scope["headers"])
        # Los nombres de cabecera vienen en minúsculas y codificadas en bytes, ej. b'x-operation-id'
        operation_id = headers.get(b"x-operation-id", uuid.uuid4().bytes)
        # Conviértelo a string si es bytes:
        if isinstance(operation_id, bytes):
            operation_id = operation_id.decode("utf-8")
        span.set_attribute("operation_id", operation_id)
