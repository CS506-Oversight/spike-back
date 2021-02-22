from app import app
from flask import request, jsonify
from app.controllers.staff_controller import StaffController
import json

StaffController = StaffController()

@app.route('/inStock/<product_id>', methods=['POST'])
def make_inStock(product_id):
    StaffController.make_inStock(product_id)
    return "done"

@app.route('/outStock/<product_id>', methods=['POST'])
def make_outStock(product_id):
    StaffController.make_outStock(product_id)
    return "done"