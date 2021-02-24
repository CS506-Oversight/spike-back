"""Root routes."""
from flask import Blueprint

__all__ = ('blueprint_root',)

blueprint_root = Blueprint('root', __name__)


@blueprint_root.route('/', methods=['GET'])
def root():
    """Root endpoint that only checks if the server is running."""
    return 'Server is running...'  # FIXME: Change to json response
