"""Implementation for controlling the user data."""
import bcrypt

from app.config import fb_db

__all__ = ('UserController',)


class UserController:
    """User data controller."""

    @staticmethod
    def create_user(user):
        """Create a new user data."""
        new_user = {
            'user_id': user.user_id,
            'username': user.username,
            'password': user.password,
            'phone': user.phone,
            'address': user.address,
            'type': user.type,
            'email': user.email,
        }

        fb_db.collection('Users').document(user.user_id).set(new_user)

        return user.user_id

    @staticmethod
    def get_user(username):
        """Get the user data of ``user_name``."""
        user_ref = fb_db.collection('Users').where('username', '==', username).get()
        user_dic = user_ref[0].to_dict()
        del user_dic['password']
        return user_dic

    @staticmethod
    def get_hashed(username):
        """Get the hashed password of ``user_name``."""
        user = fb_db.collection('Users').where('username', '==', username).get()
        user_dic = user[0].to_dict()
        return user_dic['password']

    @staticmethod
    def check_username(username):
        """Check if``user_name``is in DB."""
        user_list = fb_db.collection('Users').where('username', '==', username).get()
        if len(user_list) > 0:
            return True
        return False

    @staticmethod
    def check_user_id(user_id):
        """Check if``user_name``is in DB."""
        user = fb_db.collection('Users').document(user_id).get()
        user_dic = user.to_dict()
        if user_dic:
            return True
        return False

    @classmethod
    def update_user(cls, username, properties):
        """Update the ``properties`` of the user data ``username``."""
        user = fb_db.collection('Users').where('username', '==', username).get()
        user_dic = user[0].to_dict()
        user_id = user_dic['user_id']
        doc_ref = fb_db.collection('Users')
        doc = doc_ref.document(user_id)

        if 'password' in properties:
            password = properties['password'].encode('utf8')
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            properties['password'] = hashed
        if 'username' in properties:
            del properties['username']

        doc.update(properties)
        user = cls.get_user(username)
        return user

    @staticmethod
    def delete_user(username):
        """Delete the user at ``username``."""
        user = fb_db.collection('Users').where('username', '==', username).get()
        user_dic = user[0].to_dict()
        user_id = user_dic['user_id']
        fb_db.collection('Users').document(user_id).delete()
        return username
