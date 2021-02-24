"""Flask app routes."""
from .auth_routes import blueprint_auth
from .db_routes import blueprint_db
from .menu_routes import blueprint_menu
from .order_routes import blueprint_order
from .root import blueprint_root
from .staff_routes import blueprint_staff
