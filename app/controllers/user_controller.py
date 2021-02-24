from app.config.firebase.fb_config import db
from app.models.user_model import User
from flask import jsonify
import json

class UserController:
    def create_user(self, user):
        try:
            new_user = {
                "username": user.username,
                "password": user.password,
                "phone": user.phone,
                "address": user.address,
                "type": user.type,
                "email": user.email,
            }

            db.collection(u'Users').document(user.username).set(new_user)

            return user.username
        except Exception as e:
            return None

    def getUser(self, username):
        final_user = {}
        try:
            user = db.collection(u'Users').document(username).get()
            #print(user)
            user_dic = user.to_dict()
            del user_dic["password"]
            return user_dic
        except Exception as e:
            return None

    def update_user(self, username, properties):
        doc_ref = db.collection('Users')
        doc = doc_ref.document(username)
        print(properties)

        doc.update(properties)
        user = self.getUser(username)
        return user