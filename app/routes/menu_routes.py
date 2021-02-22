from app import app
from flask import request, jsonify
from app.models.menu_model import MenuItem
from app.controllers.menu_controller import MenuController
import json


MenuController = MenuController()



@app.route('/get_menu', methods=['GET'])
def get_menu():
    menu_list = MenuController.get_all_menu_items()
    return menu_list
    """Endpoint that retrieves the menu for the client.

    Gets all the menu items from a restaurant and complies
    it together to form the menu. Essentially is get_all_items
    """


@app.route('/menu_item/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    pass


@app.route('/create_menu_item', methods=['POST'])
def create_menu_item():
    pass


@app.route('/update_menu_item/<int:item_id>', methods=['PATCH'])
def update_menu_item(item_id):
    pass


@app.route('/delete_menu_item/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    pass

@app.route('/add_SKUS', methods=['POST'])
def add_skus():
    MenuController.add_skus()
    return "skus added"
