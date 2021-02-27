"""Controller implementations for orders."""
import pytz
from datetime import datetime, timedelta
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
    def get_pickup_time(date_time_obj, total_time):
        # TODO: Calculate total time
        cst = pytz.timezone('US/Central')
        fmt = '%H:%M %p'

        print(date_time_obj)

        pickup_time_utc = date_time_obj + timedelta(minutes=total_time)

        times = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        time_to_str = pickup_time_utc.strftime(fmt)
        time_split = time_to_str.split(' ')

        pm_or_am = time_split[1]
        hour_min_split = time_split[0].split(':')

        hour = hour_min_split[0]
        hour_to_tweleve_clock = times[int(hour)]

        pickup_time = f'{hour_to_tweleve_clock}:{hour_min_split[1]} {pm_or_am}'

        return pickup_time

    @staticmethod
    def create_order(session, payment_type, receipt_url):
        """Create an ``order``."""
        order_info = {
            'order_subtotal': session['amount_subtotal'] / 100,
            'order_total': session['amount_total'] / 100,
            'order_tax': session['total_details']['amount_tax'] / 100,
            'order_id': session['id'],
            'customer_id': session['metadata']['customer_id'],
            'in_progress': True,
            'order_date': datetime.now(),
            'type': payment_type,
            'receipt': receipt_url
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
        menu_ref = fb_db.collection('Menu')
        menu = menu_ref.document(order_id)

        menu.update({'in_progress': False})

        return order_id

    @staticmethod
    def get_successful_order(session_id):
        """Allows orders to be marked as completed."""
        order_ref = fb_db.collection('Orders')
        order = order_ref.document(session_id).get()

        order_info = order.to_dict()
        order_info['pickup_time'] = OrderController.get_pickup_time(order_info['order_date'], 45)

        return order_info
