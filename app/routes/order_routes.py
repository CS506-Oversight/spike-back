"""Routes for performing actions related to order."""
import os

import json

from flask import Blueprint, abort, jsonify, request
from stripe.error import SignatureVerificationError
from app.controllers import OrderController

from app.config import Stripe

__all__ = ('blueprint_order',)

blueprint_order = Blueprint('order', __name__)


@blueprint_order.route('/order/<string:order_id>', methods=['GET'])
def get_order(order_id):
    """Get the order at ``order_id``."""
    # TODO: Define and document order not exists behavior
    data = json.loads(request.data)

    user_id = data['user_id']
    user_role = data['type']

    order = OrderController.get_order(user_id, user_role, order_id)

    return jsonify(order)


@blueprint_order.route('/orders', methods=['GET'])
def get_orders():
    """Get all available orders.

    Information of the user should be passed in. Specifically,
    their UID. Certain data will be returned based on who the user is.
    """

    data = json.loads(request.data)
    uid = data['uid']

    orders = OrderController.get_orders(uid)

    return jsonify(orders), 200


@blueprint_order.route('/complete_order', methods=['POST'])
def complete_order():
    """Allows orders to be marked as completed."""
    data = json.loads(request.data)
    order_id = OrderController.complete_order(data['order_id'])

    return jsonify({'status': 'Success', 'message': f'Order {order_id} successfully marked as completed.'}), 201


@blueprint_order.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Endpoint to create a checkout session."""
    if request.content_length > 1024 ** 2:
        abort(400)

    data = request.get_json()

    checkout_session = Stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=data['items'],
        mode='payment',
        success_url='http://localhost:8787/success',  # change to frontend page
        cancel_url='http://localhost:8787/cancel',  # change to frontend page
        metadata=data['metadata']
    )

    # FIXME: Catch the specific error for auth only
    #   return jsonify(error=str(e)), 403

    return jsonify({'id': checkout_session.id})


@blueprint_order.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint for the system webhook."""
    if request.content_length > 1024 ** 2:
        abort(400)

    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = Stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_ENDPOINT_SECRET')
        )
    except ValueError as ex:
        # invalid payload
        return jsonify({'message': 'Invalid payload.'}), 400
    except SignatureVerificationError as ex:
        # invalid signature
        return jsonify({'message': 'Invalid signature.'}), 400

    event_dict = event.to_dict()

    if event_dict['type'] == 'checkout.session.completed':
        session = event['data']['object']

        order_id = OrderController.create_order(session)

        if order_id:
            return {'order_id': order_id, 'message': 'Order was successfully placed.'}, 201

    return 'OK', 200


@blueprint_order.route('/success', methods=['GET'])
def success():
    """Endpoint used by stripe for obtaining the response of order success."""
    return 'Purchase successful. Thank you!'


@blueprint_order.route('/cancel', methods=['GET'])
def cancel():
    """Endpoint used by stripe for obtaining the response of order cancellation."""
    return 'Purchase cancelled.'
