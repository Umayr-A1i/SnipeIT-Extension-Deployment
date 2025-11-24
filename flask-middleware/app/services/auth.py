from flask import current_app, Request
from werkzeug.exceptions import Unauthorized

def verify_extension_request(request: Request) -> None:
    expected = current_app.config.get("EXTENSION_API_KEY")
    provided = request.headers.get("X-Extension-Api-Key")

    if not provided or provided != expected:
        raise Unauthorized("Invalid or missing extension API key")

