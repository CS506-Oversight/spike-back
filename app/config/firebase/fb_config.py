"""Configuration for Firebase auth."""
import firebase_admin
from firebase_admin import auth, credentials, firestore

__all__ = ('fb_app', 'fb_auth', 'fb_db')

# Use a service account
cred = credentials.Certificate('app/serviceAccountKey.json')

fb_app = firebase_admin.initialize_app(cred)
fb_auth = auth
fb_db = firestore.client(fb_app)
