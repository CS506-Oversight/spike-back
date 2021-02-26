"""Controller implementations for orders."""
from datetime import datetime
from app.config import Stripe, fb_db

__all__ = ('OrderController',)


class OrderController:
    """Controller for orders."""

    @staticmethod
    def get_order(user_id, user_role, order_id):
        """Get the order at ``order_id``."""
        order_ref = fb_db.collection('Orders')
        order = {'order': None}
        res = None

        if user_role in ('admin', 'staff'):
            res = order_ref.document(order_id).get()
            order['order'] = res.to_dict()
        elif user_role == 'customer':
            query = order_ref.where('customer_id', '==', user_id).where('order_id', '==', order_id)
            res = query.get()
            order['order'] = res[0].to_dict()

        return order

    @staticmethod
    def get_orders(uid):
        """Get all orders."""
        doc_ref = fb_db.collection('Users').document(uid)
        doc = doc_ref.get().to_dict()

        user_type = doc['type']
        orders = {'orders': []}

        order_ref = fb_db.collection('Orders')

        # admin or staff has the right to see ALL orders
        if user_type in ('admin', 'staff'):
            orders_docs = order_ref.get()
            for order in orders_docs:
                orders['orders'].append(order.to_dict())

        # customers can ONLY see their orders
        elif user_type == 'customer':
            query = order_ref.where('customer_id', '==', uid).get()

            # this does the check if the query is empty (i.e. returns empty array)
            for order in query:
                orders['orders'].append(order.to_dict())
        else:
            raise Exception('Unknown user type')

        return orders

    @staticmethod
    def create_order(session):
        """Create an ``order``."""
        order_info = {
            'order_subtotal': session['amount_subtotal'] / 100,
            'order_total': session['amount_total'] / 100,
            'order_tax': session['total_details']['amount_tax'] / 100,
            'order_id': session['id'],
            'customer_id': session['metadata']['customer_id'],
            'in_progress': True,
            'order_date': datetime.now()
        }

        order_id = order_info['order_id']
        order_line_items = Stripe.checkout.Session.list_line_items(order_id)
        item_data = order_line_items['data']

        item_list = []
        for item in item_data:
            list_item = f'{item["price"]["product"]} | {item["quantity"]}'
            item_list.append(list_item)

        order_info['items_ordered'] = item_list

        fb_db.collection('Orders').document(order_id).set(order_info)

        return order_id

    @staticmethod
    def complete_order(order_id):
        """Allows orders to be marked as completed."""
        order_ref = fb_db.collection('Orders')
        order = order_ref.document(order_id)

        order.update({'in_progress': False})

        return order_id

    @staticmethod
    def email_pdf(order_id):
        """Allows orders to be marked as completed."""
        order_ref = fb_db.collection('Orders')
        order = order_ref.document(order_id).get()
        print(order)
        order_dic = order.to_dict()
        user_id = order_dic["customer_id"]
        user = fb_db.collection('Users').document(user_id).get()
        user_dic = user.to_dict()
        email = user_dic["email"]

        print(email)
        #return email
