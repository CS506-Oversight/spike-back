class MenuItem:
    def __init__(self, item_name, item_desc, item_price, item_id=None, quantity=None, img=None, item_type=None):
        self.item_name = item_name
        self.item_desc = item_desc
        self.item_price = item_price
        self.item_id = item_id
        self.quantity = quantity
        self.img = img
        self.item_type = item_type
        #self.in_stock = in_stock
        #sekf.SKU = SKU