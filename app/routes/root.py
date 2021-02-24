"""Root routes."""
from flask import Blueprint

__all__ = ('blueprint_root',)

blueprint_root = Blueprint('order', __name__)


@blueprint_root.route('/', methods=['GET'])
def get_users():
    """Endpoint to get the users (?)."""
    # TODO: Finish implementing or remove
    return 'Server is running...'
