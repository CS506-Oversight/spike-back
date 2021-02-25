"""Routes for user data control."""
import json

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

    password = data['password'].encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    user = User(username=data['username'], password=hashed.decode('utf-8'), phone=data['phone'],
                address=data['address'], email=data['email'], type=data['type'])

    new_user_id = UserController.create_user(user)

    if not new_user_id:
        return jsonify({'status': 'Failed', 'message': 'Problem creating a new user.'}), 500

    return jsonify({'status': 'Success', 'message': f'User added with id: {new_user_id}.'}), 201


@blueprint_user.route('/check_pass', methods=['POST'])
def check_pass():
    """Check if the user passes the auth check."""
    data = json.loads(request.data)
    password = data['password'].encode('utf-8')
    print(data)
    #hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if (UserController.check_username(data["username"])):
        hashed = UserController.get_hashed(data["username"])
        if bcrypt.checkpw(password, hashed):
            user = UserController.get_user(data['username'])
            return jsonify(user), 200
        else:
            return jsonify({'status': 'Failed', 'message': 'wPassword did not match'}), 401
    else:
        return jsonify({'status': 'Failed', 'message': 'Not a valid username'}), 401




@blueprint_user.route('/get_user/<string:username>', methods=['GET'])
def get_user(username):
    """Get the user data of ``username``."""
    data = UserController.get_user(username)
    if not data:
        return jsonify({'status': 'Failed', 'message': 'Password did not match'}), 401

    return jsonify(data), 200


@blueprint_user.route('/update_user/<string:username>', methods=['POST'])
def update_user(username):
    """Update the user data of ``username``."""
    properties = json.loads(request.data)
    user = UserController.update_user(username, properties)
    return user, 201


@blueprint_user.route('/delete_user/<string:username>', methods=['DELETE'])
def delete_user(username):
    """Endpoint to delete the user at ``username``."""
    username = UserController.delete_user(username)
    if username:
        return jsonify({'status': 'Success', 'message': f'User with username {username} has been deleted.'}), 200

    return jsonify({'status': 'Failed', 'message': 'There was a problem deleting the user.'}), 500


