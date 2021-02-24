"""Implementations for app construction."""
from flask import Flask
from flask_cors import CORS

from .routes import blueprint_menu, blueprint_order, blueprint_root, blueprint_user

__all__ = ('create_app',)


def create_app():
    """Create a Flask app and return it."""
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(blueprint_menu)
    app.register_blueprint(blueprint_order)
    app.register_blueprint(blueprint_user)
    app.register_blueprint(blueprint_root)

    return app
