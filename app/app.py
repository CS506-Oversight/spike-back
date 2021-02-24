"""Implementations for app construction."""
from flask import Flask
from flask_cors import CORS

from .routes import blueprint_auth, blueprint_db, blueprint_menu, blueprint_order, blueprint_root, blueprint_staff

__all__ = ('create_app',)


def create_app():
    """Create a Flask app and return it."""
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(blueprint_auth)
    app.register_blueprint(blueprint_db)
    app.register_blueprint(blueprint_menu)
    app.register_blueprint(blueprint_order)
    app.register_blueprint(blueprint_root)
    app.register_blueprint(blueprint_staff)

    return app
