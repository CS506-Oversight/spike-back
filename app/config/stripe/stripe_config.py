"""Configuration for Stripe."""
from os import environ

import stripe
from dotenv import find_dotenv, load_dotenv

__all__ = ('Stripe',)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

stripe.api_key = environ.get('STRIPE_SECRET_KEY')
Stripe = stripe
