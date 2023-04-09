
from typing import (
    TYPE_CHECKING, Iterable,
)

if TYPE_CHECKING:
    from _typeshed.wsgi import StartResponse, WSGIEnvironment


def application(
    environ: "WSGIEnvironment",
    start_response: "StartResponse",
) -> Iterable[bytes]:
    response_body = 'Dabadee dabadoo\n'

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/plain',),
        ('Content-Length', str(len(response_body)),),
    ]

    start_response(status, response_headers)

    return [response_body.encode()]
