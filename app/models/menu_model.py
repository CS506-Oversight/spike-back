class MenuItem:
    def __init__(self, item_name, item_desc, item_price, in_stock, img, item_type, item_id=None):
        self.item_name = item_name
        self.item_desc = item_desc
        self.item_price = item_price
        self.item_id = item_id
        self.img = img
        self.item_type = item_type
        self.in_stock = in_stock
