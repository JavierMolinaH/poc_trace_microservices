import uuid


def add_operation_id_to_span(span, scope):
    if span and scope:
        headers = dict(scope["headers"])
        operation_id = headers.get(b"x-operation-id", uuid.uuid4().bytes)
        if isinstance(operation_id, bytes):
            operation_id = operation_id.decode("utf-8")
        span.set_attribute("operation_id", operation_id)
