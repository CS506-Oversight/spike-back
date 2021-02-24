"""Routes for user authentications."""
import json

from flask import Blueprint, jsonify, request

from app.config import fb_auth

__all__ = ('blueprint_auth',)

blueprint_auth = Blueprint('auth', __name__)


@blueprint_auth.route('/login', methods=['POST'])
def index():
    """User login endpoint."""
    # email = request.form['name']
    # password = request.form['password']
    data = json.loads(request.data)

    email = data['email']
    # password = data['password']

    # FIXME: For all exceptions occurred during request handling,
    #  re-route it to the error handler,
    #  unless some exception raising is expected
    # return jsonify({'success': False}), 400, {'ContentType': 'application/json'}

    user = fb_auth.get_user_by_email(email=email)
    return jsonify({'success': True, 'user': user.uid}), 200, {'ContentType': 'application/json'}


@blueprint_auth.route('/create_account', methods=['POST'])
def create_account():
    """User account creation endpoint."""
    # email = request.form['name']
    # password = request.form['password']
    data = json.loads(request.data)

    email = data['email']
    password = data['password']

    new_user = fb_auth.create_user(email=email, password=password)

    return jsonify({'user': new_user.uid}), 200, {'ContentType': 'application/json'}


@blueprint_auth.route('/forgot_password', methods=['POST'])
def forgot_password():
    """User password reset endpoint."""
    # email = request.form['name']
    data = json.loads(request.data)
    email = data['email']

    reset_link = fb_auth.generate_password_reset_link(email=email)
    return reset_link
