"""Routes for performing actions on staff."""
from flask import Blueprint

from app.controllers import StaffController

__all__ = ('blueprint_staff',)

blueprint_staff = Blueprint('order', __name__)


@blueprint_staff.route('/in_stock/<product_id>', methods=['POST'])
def make_in_stock(product_id):
    """Doc."""
    # FIXME: Add documentation
    updated_product = StaffController.make_in_stock(product_id)
    return updated_product


@blueprint_staff.route('/out_stock/<product_id>', methods=['POST'])
def make_out_stock(product_id):
    """Doc."""
    # FIXME: Add documentation
    updated_product = StaffController.make_out_stock(product_id)
    return updated_product
