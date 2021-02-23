from app.config.firebase.fb_config import db
from app.config.stripe.stripe_config import Stripe
from app.models.menu_model import MenuItem
import json


class MenuController:
    def get_all_menu_items(self):  # TODO : add current inventory amount
        menu_list = (Stripe.Product.list(limit=30))
        print(menu_list)
        final_menu = {}
        for item in menu_list:
            price = self.get_product_price(item["id"])
            new_item = MenuItem(item["name"], item["description"], price, item["id"])
            final_menu[item["name"]] = json.dumps(new_item.__dict__)
        return final_menu

    def get_all_prices(self):  # Unused for now but could be used later
        data_list = Stripe.Price.list()
        #print(data_list)
        price_list = {}
        for item in data_list:
            price_list[item["product"]] = item["unit_amount"]
        return price_list

    def get_product_price(self, product_id):
        price_data = Stripe.Price.list(product=product_id)
        price = price_data["data"][0]["unit_amount"] / float(100)
        return price

    def get_menu_item_by_id(self, item_id):
        try:
            product = Stripe.Product.retrieve(item_id)
            # print(product)
            if product:
                menu_item = {
                    "name": product["name"],
                    "description": product["description"],
                    "price": self.get_product_price(item_id),
                    "item_id": item_id,
                    "type": product["metadata"]["Type"],
                }
                return menu_item
        except Exception as e:
            print('Something went wrong with: get_menu_item', e)
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

            # registers a new SKU using the new product made above
            Stripe.SKU.create(
                price=int(menu_item.item_price * 100),
                currency="usd",
                product=new_product["id"],
                inventory={"type": "finite", "quantity": menu_item.quantity},
                image=menu_item.img)
        except Exception as e:
            #  print('Problem adding new menu item', e)
            return None

        return new_product["id"]

    def delete_menu_item(self, item_id):
        pass

    def update_menu_item(self, item_id):
        pass
