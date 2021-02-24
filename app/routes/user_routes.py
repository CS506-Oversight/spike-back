from app import app
from flask import request, jsonify
from app.models.user_model import User
from app.controllers.user_controller import UserController
import json
import bcrypt

UserController = UserController()



@app.route('/create_user', methods=['POST'])
def create_user():
    data = json.loads(request.data)

    password = data["password"].encode('utf8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    user = User(username=data["username"], password=hashed, phone=data["phone"],
                address=data["address"], email=data["email"], type=data["type"])

    new_user_id = UserController.create_user(user)

    if new_user_id:
        return jsonify({"status": "Success", "message": f'User added with id: {new_user_id}.'}), 201

    return jsonify({"status": "Failed", "message": "Problem creating a new user."}), 500

@app.route('/check_pass', methods=['POST'])
def check_pass():
    data = json.loads(request.data)

    password = data["password"].encode('utf8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    if bcrypt.checkpw(password, hashed):
        user = UserController.getUser(data["username"])
        print(user)
        return jsonify(user), 200

    else:
        return jsonify({"status": "Failed", "message": "Password did not match"}), 401

@app.route('/get_user/<string:username>', methods=['GET'])
def get_user(username):
    data = UserController.getUser(username)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"status": "Failed", "message": "Password did not match"}), 401



@app.route('/update_user/<string:username>', methods=['POST'])
def update_user(username):
    properties = json.loads(request.data)
    user = UserController.update_user(username, properties)
    return user, 201

@app.route('/delete_user/<string:username>', methods=['DELETE'])
def delete_user(username):
    username = UserController.delete_user(username)
    if username:
        return jsonify({"status": "Success", "message": f'User with username {username} has been deleted.'}), 200

    return jsonify({"status": "Failed", "message": f'There was a problem deleting the user.'}), 500