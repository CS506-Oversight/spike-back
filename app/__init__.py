from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from app.routes import root
from app.routes import auth_routes
from app.routes import db_routes
from app.routes import menu_routes
from app.routes import order_routes
from app.routes import staff_routes
