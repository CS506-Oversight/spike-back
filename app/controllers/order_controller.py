from app.config.firebase.fb_config import db
from app.config.stripe.stripe_config import Stripe


class OrderController:
    def get_order(self, order_id):
        pass

    def get_orders(self):
        pass

    def create_order(self, order):
        pass

    def test_order(self):
        # Test for Inventory with sunrise mimosa
        self.removeFromInventory("prod_IzhmfPUg6tM3zH", 1)

#removes amoujnt of item of given product ID from the inventory
#negative amounts will add to inventory
    def removeFromInventory(self, prod_id, amount):
        SKU = Stripe.SKU.list(product=prod_id)
        inventory = SKU["data"][0]["inventory"]["quantity"]-amount
        #Precursor for out of stock warning
        if (inventory > 0):
            updated = Stripe.SKU.modify(
                SKU["data"][0]["id"],
                inventory={
                    "quantity": inventory,
                    "type": "finite",
                },
                active=True,
            )
            updated_product = Stripe.Product.modify(
                prod_id,
                active=True,
            )
        else:
            updated = Stripe.SKU.modify(
                SKU["data"][0]["id"],
                inventory={
                "quantity": inventory,
                "type": "finite",
                },
                active=False,
            )
            updated_product = Stripe.Product.modify(
                prod_id,
                active=False,
            )
        print(SKU)
        print(updated)