from flask import Blueprint, jsonify, request, current_app
from .services.snipeit_client import SnipeItClient
from .services.auth import verify_extension_request

api_bp = Blueprint("api", __name__)

def _get_client() -> SnipeItClient:
    return SnipeItClient(
        current_app.config["SNIPEIT_API_BASE_URL"],
        current_app.config["SNIPEIT_API_TOKEN"],
    )

@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "flask-middleware"}), 200

@api_bp.route("/snipeit/health", methods=["GET"])
def snipeit_health():
    verify_extension_request(request)
    client = _get_client()
    return jsonify(client.ping()), 200

@api_bp.route("/assets", methods=["GET"])
def list_assets():
    verify_extension_request(request)
    client = _get_client()
    search = request.args.get("search")
    return jsonify(client.list_assets(search)), 200

