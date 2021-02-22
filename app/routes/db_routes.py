from app import app
from app.config.firebase.fb_config import db
import flask
import json

menu_ref = db.collection(u'Menu')


@app.route('/allMenu', methods=['GET'])
def get_all():
    menu = menu_ref.get()
    print(menu)
    return menu[0].to_dict()


# @app.route("/users", methods=['GET'])
# def get_users():
#     return 'users'
#
#
# @app.route("/users/amount", methods=['GET'])
# def get_num_users():
#     return 'amount of users'
#
#
# @app.route("/user/create", methods=['POST'])
# def create_user():
#     return 'create a user'
