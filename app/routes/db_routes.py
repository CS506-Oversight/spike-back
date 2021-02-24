"""Routes for fetching the data from the database."""
from flask import Blueprint

from app.config import fb_db

__all__ = ('blueprint_db',)

blueprint_db = Blueprint('db', __name__)

menu_ref = fb_db.collection('Menu')


@blueprint_db.route('/allMenu', methods=['GET'])
def get_all():
    """Endpoint to get all menu items."""
    menu = menu_ref.get()
    print(menu)
    return menu[0].to_dict()

# @blueprint_db.route('/users', methods=['GET'])
# def get_users():
#     return 'users'
#
#
# @blueprint_db.route('/users/amount', methods=['GET'])
# def get_num_users():
#     return 'amount of users'
#
#
# @blueprint_db.route('/user/create', methods=['POST'])
# def create_user():
#     return 'create a user'
