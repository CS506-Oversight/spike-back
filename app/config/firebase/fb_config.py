"""Configuration for Firebase auth."""
import json
import os

import firebase_admin
from firebase_admin import auth, credentials, firestore

__all__ = ('fb_app', 'fb_auth', 'fb_db')


def get_certificate(firebase_credential_path='app/serviceAccountKey.json'):
    """Get the firebase certificate."""
    certificate = None

    if os.path.exists(firebase_credential_path):
        certificate = credentials.Certificate('app/serviceAccountKey.json')
    elif 'FIREBASE_ACCOUNT_KEY' in os.environ:
        certificate = credentials.Certificate(json.loads(os.environ['FIREBASE_ACCOUNT_KEY']))

    if not certificate:
        print(
            'Firebase credential required. '
            'Either have a file named `serviceAccountKey.json` to be placed at `app` (`app/serviceAccountKey.json`) '
            'or define the content of that json file as `FIREBASE_ACCOUNT_KEY` in the environment variables.\n'
            'The file can be obtained via [Firebase Project Settings > Servide Accounts > Generate Private Key].'
        )

    return certificate


fb_app = firebase_admin.initialize_app(get_certificate())
fb_auth = auth
fb_db = firestore.client(fb_app)
