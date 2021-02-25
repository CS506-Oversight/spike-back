"""Controller implementations for orders."""
from app.config import Stripe, fb_db

from datetime import datetime

__all__ = ('OrderController',)


class OrderController:
    """Controller for orders."""

    @staticmethod
    def get_order(order_id):
        """Get the order at ``order_id``."""

    @staticmethod
    def get_orders(uid):
        """Get all orders."""
        doc_ref = fb_db.collection('Users').document(uid)
        doc = doc_ref.get().to_dict()

        user_type = doc['type']
        orders = {'orders': []}

        order_ref = fb_db.collection('Orders')

        # admin or staff has the right to see ALL orders
        if user_type == 'admin' or user_type == 'staff':
            orders_docs = order_ref.get()
            for order in orders_docs:
                orders['orders'].append(order.to_dict())

        # customers can ONLY see their orders
        elif user_type == 'customer':
            query = order_ref.where('customer_id', '==', uid).get()  # TODO: NEED TO FIND CORRECT QUERY ACTIONS

            # this does the check if the query is empty (i.e. returns empty array)
            for order in query:
                orders['orders'].append(order.to_dict())
        else:
            raise Exception('Unknown user type')

        return orders

    @staticmethod
    def create_order(session):
        """Create an ``order``."""

        # TODO: ADD SOME TESTING TO THIS!!!

        order_info = {
            'order_subtotal': session['amount_subtotal'] / 100,
            'order_total':  session['amount_total'] / 100,
            'order_tax': session['total_details']['amount_tax'] / 100,
            'order_id':  session['id'],
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

        doc_ref = fb_db.collection('Orders').document(order_id).set(order_info)

        return order_id

    @staticmethod
    def complete_order():
        """Allows orders to be marked as completed."""
