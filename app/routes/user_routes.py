"""Routes for user data control."""
import json
import random
import string
import bcrypt
from flask import Blueprint, jsonify, request

from app.controllers.user_controller import UserController
from app.models.user_model import User

__all__ = ('blueprint_user',)

blueprint_user = Blueprint('user', __name__)


@blueprint_user.route('/create_user', methods=['POST'])
def create_user():
    """Endpoint to create a user data."""
    data = json.loads(request.data)
    uid = 'user_' + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)])
    password = data['password'].encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if not UserController.check_username(data['username']):
        user = User(user_id=uid, username=data['username'], password=hashed.decode('utf-8'), phone=data['phone'],
                    address=data['address'], email=data['email'], type=data['type'])
        new_user_id = UserController.create_user(user)

        if not new_user_id:
            return jsonify({'status': 'Failed', 'message': 'Problem creating a new user.'}), 500

        return jsonify({'status': 'Success', 'message': f'User added with id: {new_user_id}.'}), 201
    else:
        return jsonify({'status': 'Failed', 'message': 'Username already taken'}), 401


@blueprint_user.route('/check_pass', methods=['POST'])
def check_pass():
    """Check if the user passes the auth check."""
    data = json.loads(request.data)
    password = data['password'].encode('utf-8')

    if UserController.check_username(data["username"]):
        hashed = UserController.get_hashed(data["username"]).encode('utf-8')
        if bcrypt.checkpw(password, hashed):
            user = UserController.get_user(data['username'])
            return jsonify(user), 200

        return jsonify({'status': 'Failed', 'message': 'Password is Incorrect'}), 401

    return jsonify({'status': 'Failed', 'message': 'Not a valid username'}), 401


@blueprint_user.route('/get_user/<string:username>', methods=['GET'])
def get_user(username):
    """Get the user data of username."""
    data = UserController.get_user(username)
    if UserController.check_username(data["username"]):
        if data:
            return jsonify(data), 200
        else:
            return jsonify({'status': 'Failed', 'message': 'Not a valid Username'}), 401
    else:
        return jsonify({'status': 'Failed', 'message': 'Not a valid Username'}), 401


@blueprint_user.route('/update_user/<string:username>', methods=['POST'])
def update_user(username):
    """Update the user data of ``username``."""
    properties = json.loads(request.data)
    if UserController.check_username(username):
        user = UserController.update_user(username, properties)
        return jsonify(user), 201
    else:
        return jsonify({'status': 'Failed', 'message': 'Not a valid Username'}), 401


@blueprint_user.route('/delete_user/<string:username>', methods=['DELETE'])
def delete_user(username):
    """Endpoint to delete the user at ``username``."""
    if UserController.check_username(username):
        username = UserController.delete_user(username)
        if username:
            return jsonify({'status': 'Success', 'message': f'User with user_id {username} has been deleted.'}), 200

        return jsonify({'status': 'Failed', 'message': 'There was a problem deleting the user.'}), 500
    else:
        return jsonify({'status': 'Failed', 'message': 'Not a valid Username'}), 401
