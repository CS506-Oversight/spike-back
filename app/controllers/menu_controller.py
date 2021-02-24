from app.config.firebase.fb_config import db
from app.config.stripe.stripe_config import Stripe
from app.models.menu_model import MenuItem
import json


class MenuController:
    def get_all_menu_items(self):
        final_menu = {"menu": []}
        col_ref = db.collection(u'Menu')

        try:
            doc_ref = col_ref.get()
            for doc in doc_ref:
                final_menu['menu'].append(doc.to_dict())

            return final_menu
        except Exception as e:
            return None

    def get_menu_item_by_id(self, item_id):
        try:
            doc_ref = db.collection(u'Menu').document(item_id)

            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                raise Exception('Menu item does not exist!')
        except Exception as e:
            return None

    def create_menu_item(self, menu_item):
        try:
            # registers a new product
            new_product = Stripe.Product.create(
                name=menu_item.item_name,
                type="good",
                description=menu_item.item_desc,
                images=[menu_item.img],
                metadata={
                    "Type": menu_item.item_type
                }
            )
            # registers a new price and binds it to the new product made above
            Stripe.Price.create(
                unit_amount=int(menu_item.item_price * 100),
                currency="usd",
                product=new_product["id"])

            new_menu_item = {
                "name": menu_item.item_name,
                "description": menu_item.item_desc,
                "price": menu_item.item_price,
                "item_id": new_product['id'],
                "type": menu_item.item_type,
                "img": menu_item.img,
                "in_stock": menu_item.in_stock
            }

            db.collection(u'Menu').document(new_product['id']).set(new_menu_item)

            return new_product["id"]

        except Exception as e:
            return None

    def delete_menu_item(self, item_id):
        try:
            db.collection(u'Menu').document(item_id).delete()
            Stripe.Product.modify(item_id, active="false")
            return item_id
        except Exception as e:
            return None

    def get_product_price_id(self, item_id):
        price_data = Stripe.Price.list(product=item_id)
        price_id = price_data["data"][0]["id"]
        print(price_id)
        return price_id

    def update_stripe_price(self, item_id, updated_price):
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
            new_price = Stripe.Price.create(
                unit_amount=int(updated_price * 100),
                currency="usd",
                product=item_id,
                active=True)

        return


    def update_menu_item(self, item_id, properties):
        """
        Updates a menu item based in what the user wants to change. A user should only
        be able to change the following properties if a given menu item:
            - name
            - desc
            - price
            - in_stock
            - type
            - img
        """

        doc_ref = db.collection('Menu')
        doc = doc_ref.document(item_id)

        doc.update(properties)

        for prop in properties:
            if prop == 'price':
                self.update_stripe_price(item_id, properties[prop])
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

        return item_id
