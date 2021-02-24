from app import app
from flask import request, jsonify
from app.models.menu_model import MenuItem
from app.controllers.menu_controller import MenuController
import json


MenuController = MenuController()


@app.route('/get_menu', methods=['GET'])
def get_menu():
    """Endpoint that retrieves the menu for the client.

    Gets all the menu items from a restaurant and complies
    it together to form the menu.
    """
    menu = MenuController.get_all_menu_items()
    return jsonify(menu), 200


@app.route('/menu_item/<string:item_id>', methods=['GET'])
def get_menu_item(item_id):
    data = MenuController.get_menu_item_by_id(item_id)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({
            "status": 400,
            "message": f"Request could not be made. Check that an item with the id {item_id} actually exists."}), 400


@app.route('/create_menu_item', methods=['POST'])
def create_menu_item():
    data = json.loads(request.data)

    menu_item = MenuItem(item_name=data["name"], item_desc=data["description"], item_price=data["price"],
                         item_type=data["type"], img=data["img"], in_stock=data["in_stock"])

    new_item_id = MenuController.create_menu_item(menu_item)

    if new_item_id:
        return jsonify({"status": "Success", "message": f'Item added with id: {new_item_id}.'}), 201

    return jsonify({"status": "Failed", "message": "Problem creating a new menu item."}), 500


@app.route('/update_menu_item/<string:item_id>', methods=['POST'])
def update_menu_item(item_id):
    properties = json.loads(request.data)
    item_id = MenuController.update_menu_item(item_id, properties)
    return jsonify({"status": "Success", "message": f'Item with id {item_id} successfully updated.'}), 201


@app.route('/delete_menu_item/<string:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    item_id = MenuController.delete_menu_item(item_id)

    if item_id:
        return jsonify({"status": "Success", "message": f'Item with id {item_id} has been deleted.'}), 200

    return jsonify({"status": "Failed", "message": f'There was a problem deleting the item with id {item_id}.'}), 500
