from app.config.firebase.fb_config import db
from app.config.stripe.stripe_config import Stripe
from app.models.menu_model import MenuItem
import json

class StaffController:

    def make_inStock(self, prod_id):
        SKU = Stripe.SKU.list(product=prod_id)
        updated = Stripe.SKU.modify(
            SKU["data"][0]["id"],
            active=True,
        )
        updated_product = Stripe.Product.modify(
            prod_id,
            active=True,
        )
        return updated_product


    def make_outStock(self, prod_id):
        SKU = Stripe.SKU.list(product=prod_id)
        updated = Stripe.SKU.modify(
            SKU["data"][0]["id"],
            active=False,
        )
        updated_product = Stripe.Product.modify(
            prod_id,
            active=False,
        )
        return updated_product