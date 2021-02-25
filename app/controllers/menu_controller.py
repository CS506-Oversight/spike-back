"""Controller implementations for item menu."""
from app.config import Stripe, fb_db

__all__ = ('MenuController',)


class MenuController:
    """Controller for menu items."""

    @staticmethod
    def get_all_menu_items():
        """
        Get all menu items.

        Returns ``None`` if any exceptions occur during the fetch.
        """
        final_menu = {'menu': []}
        col_ref = fb_db.collection('Menu')

        doc_ref = col_ref.get()
        for doc in doc_ref:
            final_menu['menu'].append(doc.to_dict())

        return final_menu

    @staticmethod
    def get_menu_item_by_id(item_id):
        """
        Get a menu item by its ``item_id``.

        Returns ``None`` if any exceptions occur during the fetch.
        """
        doc_ref = fb_db.collection('Menu').document(item_id)

        doc = doc_ref.get()
        if not doc.exists:
            raise Exception('Menu item does not exist!')

        return doc.to_dict()

    @staticmethod
    def create_menu_item(menu_item):
        """Create a new menu item."""
        # registers a new product
        new_product = Stripe.Product.create(
            name=menu_item.item_name,
            type='good',
            description=menu_item.item_desc,
            images=[menu_item.img],
            metadata={
                'Type': menu_item.item_type
            }
        )
        # registers a new price and binds it to the new product made above
        price_obj = Stripe.Price.create(
            unit_amount=int(menu_item.item_price * 100),
            currency='usd',
            product=new_product['id'])
        price_id = price_obj["id"]

        new_menu_item = {
            'name': menu_item.item_name,
            'description': menu_item.item_desc,
            'price': menu_item.item_price,
            'item_id': new_product['id'],
            'type': menu_item.item_type,
            'img': menu_item.img,
            'in_stock': menu_item.in_stock,
            "price_id": price_id
        }

        fb_db.collection('Menu').document(new_product['id']).set(new_menu_item)

        return new_product['id']

    @staticmethod
    def delete_menu_item(item_id):
        """Delete a menu item at ``item_id``."""
        fb_db.collection('Menu').document(item_id).delete()
        Stripe.Product.modify(item_id, active='false')
        return item_id

    @staticmethod
    def get_product_price_id(item_id):
        """Get the product price by ``item_id``."""
        price_data = Stripe.Price.list(product=item_id, active=True)
        price_id = price_data['data'][0]['id']
        return price_id

    @staticmethod
    def update_stripe_price(item_id, updated_price):
        """Update the price of ``item_id`` to ``updated_price`` on stripe."""
        target_price = int(updated_price * 100)
        price_list = Stripe.Price.list(product=item_id)
        data = price_list['data']

        price_exists = False

        # check if there is already a matching price
        for price_obj in data:
            if price_obj['unit_amount'] == target_price:
                price_exists = True
                if not price_obj['active']:
                    Stripe.Price.modify(price_obj['id'], active=True)
            else:
                if price_obj['active']:
                    Stripe.Price.modify(price_obj['id'], active=False)

        if not price_exists:
            Stripe.Price.create(
                unit_amount=int(updated_price * 100),
                currency='usd',
                product=item_id,
                active=True)  # new_price

    @classmethod
    def update_menu_item(cls, item_id, properties):
        """
        Updates a menu item based on what the user wants to change.

        A user is only permitted to change the following properties
        of a given menu item:
        - name
        - desc
        - price
        - in_stock
        - type
        - img
        """
        doc_ref = fb_db.collection('Menu')
        doc = doc_ref.document(item_id)

        for prop in properties:
            if prop == 'price':
                cls.update_stripe_price(item_id, properties[prop])
            if prop == 'description':
                Stripe.Product.modify(item_id, description=properties[prop])
            if prop == 'in_stock':
                Stripe.Product.modify(item_id, active=properties[prop])
            if prop == 'img':
                images = [properties[prop]]
                Stripe.Product.modify(item_id, images=images)
            if prop == 'type':
                Stripe.Product.modify(item_id, metadata={'Type': properties[prop]})
            if prop == 'name':
                Stripe.Product.modify(item_id, name=properties[prop])

        price_id = cls.get_product_price_id(item_id)
        properties["price_id"] = price_id

        doc.update(properties)
        return item_id
