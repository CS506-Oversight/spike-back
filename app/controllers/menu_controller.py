from app.config.firebase.fb_config import db
from app.config.stripe.stripe_config import Stripe
from app.models.menu_model import MenuItem
import json


class MenuController:
    #TODO : add current inventory amount
    def get_all_menu_items(self):
        menu_list = (Stripe.Product.list(limit=30))
        print(menu_list)
        final_menu = {}
        for item in menu_list:
            price_data = Stripe.Price.list(product=item["id"])
            price = price_data["data"][0]["unit_amount"]/float(100)
            new_item = MenuItem(item["name"], item["description"], price, item["id"])
            final_menu[item["name"]] = json.dumps(new_item.__dict__)
        return final_menu


#Unused for now but could be used later
    def get_all_prices(self):
        data_list = Stripe.Price.list()
        #print(data_list)
        price_list = {}
        for item in data_list:
            price_list[item["product"]] = item["unit_amount"]
        return price_list


    def get_menu_item(self, item_id):
        pass

    def create_menu_item(self, menu_item):
        pass

    def delete_menu_item(self, item_id):
        pass

    def update_menu_item(self, item_id):
        pass

    def add_skus(self):
        menu_list = (Stripe.Product.list(limit=30))
        for item in menu_list:
            price_data = Stripe.Price.list(product=item["id"])
            price = price_data["data"][0]["unit_amount"]
            currency = price_data["data"][0]["currency"]
            Stripe.SKU.create(
                price = price,
                inventory={"type": "finite", "quantity": 50},
                product=item["id"],
                currency=currency,
            )