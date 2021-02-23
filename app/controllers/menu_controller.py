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

    def update_menu_item(self, item_id, properties):
        pass
