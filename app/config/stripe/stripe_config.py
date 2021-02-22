import stripe
from os import environ
from dotenv import load_dotenv, find_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

stripe.api_key = environ.get('STRIPE_SECRET_KEY')
Stripe = stripe
