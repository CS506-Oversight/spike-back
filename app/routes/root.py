from app import app
from flask import request, jsonify
import json


@app.route("/", methods=['GET'])
def get_users():
    return 'Server is running...'
