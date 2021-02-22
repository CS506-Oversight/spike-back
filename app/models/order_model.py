class Order:
    def __init__(self, order_id, order_subtotal, order_tax, customer_name, customer_email, items_ordered, order_date):
        self.order_id = order_id
        self.order_subtotal = order_subtotal
        self.order_tax = order_tax
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.items_ordered = items_ordered  # should be a list of menu item ids
        self.order_date = order_date
