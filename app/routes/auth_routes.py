from app import app
from flask import request, jsonify
from app.config.firebase.fb_config import auth
import json


@app.route('/login', methods=['POST'])
def index():
    # email = request.form['name']
    # password = request.form['password']
    data = json.loads(request.data)

    email = data['email']
    # password = data['password']

    try:
        user = auth.get_user_by_email(email=email)
        return jsonify({'success': True, 'user': user.uid}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        print(e)
        return jsonify({'success': False}), 400, {'ContentType': 'application/json'}


@app.route('/create_account', methods=['POST'])
def create_account():
    # email = request.form['name']
    # password = request.form['password']
    data = json.loads(request.data)

    email = data['email']
    password = data['password']

    new_user = auth.create_user(email=email, password=password)

    return jsonify({'user': new_user.uid}), 200, {'ContentType': 'application/json'}


@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    # email = request.form['name']
    data = json.loads(request.data)
    email = data['email']

    reset_link = auth.generate_password_reset_link(email=email)
    return reset_link
