"""Configuration for FB auth via Firebase."""
import firebase_admin
from firebase_admin import auth, credentials, firestore

# Use a service account
cred = credentials.Certificate('app/serviceAccountKey.json')

try:
    fb_app = firebase_admin.initialize_app(cred)
    db = firestore.client(fb_app)
    auth = auth
except Exception as e:
    print('something went wrong with firebase initialization', e)


