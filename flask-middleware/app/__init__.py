from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config["SNIPEIT_API_BASE_URL"] = os.getenv("SNIPEIT_API_BASE_URL")
    app.config["SNIPEIT_API_TOKEN"] = os.getenv("SNIPEIT_API_TOKEN")
    app.config["EXTENSION_API_KEY"] = os.getenv("EXTENSION_API_KEY")

    missing = [k for k in ["SNIPEIT_API_BASE_URL", "SNIPEIT_API_TOKEN", "EXTENSION_API_KEY"]
               if not app.config.get(k)]
    if missing:
        raise RuntimeError(f"Missing config values: {', '.join(missing)}")

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
