"""Routes for performing actions on menu items."""
import json

from flask import Blueprint, jsonify, request

from app.controllers import MenuController
from app.models import MenuItem

__all__ = ('blueprint_menu',)

blueprint_menu = Blueprint('menu', __name__)


@blueprint_menu.route('/get_menu', methods=['GET'])
def get_menu():
    """
    Endpoint that retrieves the menu for the client.

    Gets all the menu items from a restaurant and complies
    it together to form the menu.
    """
    menu = MenuController.get_all_menu_items()
    return jsonify(menu), 200


@blueprint_menu.route('/menu_item/<string:item_id>', methods=['GET'])
def get_menu_item(item_id):
    """
    Endpoint for getting a specific menuy item.

    Returns `400` if the item is not found.
    """
    data = MenuController.get_menu_item_by_id(item_id)
    if not data:
        # FIXME: Should be 404 though, 400 means "the server could not understand the request"
        return jsonify({
            'status': 400,
            'message': f'Request could not be made. Check that an item with the id {item_id} actually exists.'
        }), 400

    return jsonify(data), 200


@blueprint_menu.route('/create_menu_item', methods=['POST'])
def create_menu_item():
    """
    Endpoint for creating a menu item.

    Returns 500 if the item cannot be created.
    """
    data = json.loads(request.data)

    menu_item = MenuItem(
        item_name=data['name'], item_desc=data['description'], item_price=data['price'],
        item_type=data['type'], img=data['img'], in_stock=data['in_stock']
    )

    new_item_id = MenuController.create_menu_item(menu_item)

    if not new_item_id:
        return jsonify({'status': 'Failed', 'message': 'Problem creating a new menu item.'}), 500

    return jsonify({'status': 'Success', 'message': f'Item added with id: {new_item_id}.'}), 201


@blueprint_menu.route('/update_menu_item/<string:item_id>', methods=['POST'])
def update_menu_item(item_id):
    """Endpoint for updating a menu item."""
    properties = json.loads(request.data)
    item_id = MenuController.update_menu_item(item_id, properties)
    return jsonify({"status": "Success", "message": f'Item with id {item_id} successfully updated.'}), 201


@blueprint_menu.route('/delete_menu_item/<string:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    """
    Endpoint for deleing a menu item.

    Returns 500 if the item cannot be deleted.
    """
    item_id = MenuController.delete_menu_item(item_id)

    if not item_id:
        return jsonify({
            'status': 'Failed',
            'message': f'There was a problem deleting the item with id {item_id}.'
        }), 500

    return jsonify({'status': 'Success', 'message': f'Item with id {item_id} has been deleted.'}), 200
