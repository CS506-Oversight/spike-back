"""Controller implementations for orders."""
from app.config import Stripe

__all__ = ('OrderController',)


class OrderController:
    """Controller for orders."""

    @staticmethod
    def get_order(order_id):
        """Get the order at ``order_id``."""

    @staticmethod
    def get_orders():
        """Get all orders."""

    @staticmethod
    def create_order(order):
        """Create an ``order``."""

    @classmethod
    def test_order(cls):
        """Dummy method for testing the order data."""
        # Test for Inventory with sunrise mimosa
        cls.remove_from_inventory('prod_IzhmfPUg6tM3zH', 1)

    @staticmethod
    def remove_from_inventory(prod_id, amount):
        """Doc."""
        # FIXME: Seems like a testing method, either convert to a working code and document it or delete it after test
        #   Also some unused variables were commented to pass CI
        # removes amount of item of given product ID from the inventory
        # negative amounts will add to inventory
        SKU = Stripe.SKU.list(product=prod_id)
        inventory = SKU['data'][0]['inventory']['quantity'] - amount
        # Precursor for out of stock warning
        if inventory > 0:
            updated = Stripe.SKU.modify(
                SKU['data'][0]['id'],
                inventory={
                    'quantity': inventory,
                    'type': 'finite',
                },
                active=True,
            )
            Stripe.Product.modify(
                prod_id,
                active=True,
            )  # updated_product
        else:
            updated = Stripe.SKU.modify(
                SKU['data'][0]['id'],
                inventory={
                    'quantity': inventory,
                    'type': 'finite',
                },
                active=False,
            )
            Stripe.Product.modify(
                prod_id,
                active=False,
            )  # updated_product
        print(SKU)
        print(updated)
