"""Routes for performing actions related to order."""
import os

from flask import Blueprint, abort, jsonify, request
from stripe.error import SignatureVerificationError

from app.config import Stripe

__all__ = ('blueprint_order',)

blueprint_order = Blueprint('order', __name__)


@blueprint_order.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get the order at ``order_id``."""
    # TODO: Define and document order not exists behavior
    print(order_id)  # Dummy print to check the argument


@blueprint_order.route('/orders', methods=['GET'])
def get_orders():
    """Get all available orders."""


@blueprint_order.route('/create_order', methods=['POST'])
def create_order(order):
    """Create an ``order``."""
    # TODO: Define and document the order-failed-to-create behavior
    print(order)  # Dummy call for checking the argument


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
        success_url='http://localhost:8787/success',
        cancel_url='http://localhost:8787/cancel',
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
    # event = None

    try:
        event = Stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_ENDPOINT_SECRET')
        )
    except ValueError as ex:
        # invalid payload
        print('Invalid webhook payload', ex)
        # FIXME: Consider return json for consistency
        return 'Invalid payload', 400
    except SignatureVerificationError as ex:
        # invalid signature
        print('Invalid webhook signature', ex)
        # FIXME: Consider return json for consistency
        return 'Invalid signature', 400

    event_dict = event.to_dict()

    if event_dict['type'] == 'checkout.session.completed':
        session = event['data']['object']

        print('SUCCESS!', session)

        # if store_donation(session) == 0:
        #     print('DB Success')
        # else:
        #     print('DB Failure')

    return 'OK', 200


# def store_donation(session):
#     cur = None
#
#     try:
#         cur = db.connection.cursor()
#
#         payment_intent = Stripe.PaymentIntent.retrieve(session.payment_intent,)
#
#         if payment_intent.status == 'succeeded':
#             tid = payment_intent.id
#             name = payment_intent.charges.data[0].billing_details.name
#             email = payment_intent.charges.data[0].billing_details.email
#             last_four = payment_intent.charges.data[0].payment_method_details.card.last4
#
#             timestamp = payment_intent.charges.data[0].created
#             date_of_purchase = datetime.fromtimestamp(
#                 int(timestamp)).strftime('%Y-%m-%d')
#
#             cur.execute('''INSERT INTO donation_transactions(full_name, email_address, tid, transaction_date,
#             card_used)
#                 VALUES('{}', '{}', '{}', '{}', '{}')
#             '''.format(name, email, tid, date_of_purchase, last_four)
#             )
#
#             # db.connection.commit()
#             cur.close()
#
#             return 0
#
#     except Exception as e:
#         if cur:
#             # TODO: add a rollback before closing
#             cur.close()
#
#         print(e)
#
#         return 1


@blueprint_order.route('/success', methods=['GET'])
def success():
    """Endpoint used by stripe for obtaining the response of order success."""
    return 'Purchase successful. Thank you!'


@blueprint_order.route('/cancel', methods=['GET'])
def cancel():
    """Endpoint used by stripe for obtaining the response of order cancellation."""
    return 'Purchase cancelled.'
