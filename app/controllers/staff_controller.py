"""Controller implementations for the staff."""
# from app.config.firebase.fb_config import db
from app.config import Stripe

# from app.models.menu_model import MenuItem
# import json

# TODO: Commented some unused imports out, add it back if it's in-use

__all__ = ('StaffController',)


class StaffController:
    """Controller for staff."""

    @staticmethod
    def make_in_stock(prod_id):
        """Doc."""
        # FIXME: Add documentation
        SKU = Stripe.SKU.list(product=prod_id)
        Stripe.SKU.modify(
            SKU['data'][0]['id'],
            active=True,
        )  # FIXME: `updated` unused
        updated_product = Stripe.Product.modify(
            prod_id,
            active=True,
        )
        return updated_product

    @staticmethod
    def make_out_stock(prod_id):
        """Doc."""
        # FIXME: Add documentation
        SKU = Stripe.SKU.list(product=prod_id)
        Stripe.SKU.modify(
            SKU['data'][0]['id'],
            active=False,
        )  # FIXME: `updated` unused
        updated_product = Stripe.Product.modify(
            prod_id,
            active=False,
        )
        return updated_product
