from app import app
from flask import request, jsonify, abort
from app.config.stripe.stripe_config import Stripe
import os
import datetime
from app.models.order_model import Order
from app.controllers.order_controller import OrderController
import json

OrderController = OrderController()
@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    pass


@app.route('/orders', methods=['GET'])
def get_orders():
    pass


@app.route('/create_order', methods=['POST'])
def create_order(order):
    pass

@app.route('/test_order', methods=['POST'])
def test_order():
    OrderController.test_order()
    return("tested")


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        if request.content_length > 1024**2:
            print('Request too large')
            abort(400)

        data = request.get_json()
        # print(json.dumps(data, indent=2))

        checkout_session = Stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=data['items'],
            mode='payment',
            success_url="http://localhost:8787/success",
            cancel_url="http://localhost:8787/cancel",
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 403


@app.route("/webhook", methods=['POST'])
def webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024**2:
        print('Request too large')
        abort(400)

    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = Stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_ENDPOINT_SECRET')
        )
    except ValueError as e:
        # invalid payload
        return "Invalid payload", 400
    except Stripe.error.SignatureVerificationError as e:
        # invalid signature
        return "Invalid signature", 400

    event_dict = event.to_dict()

    if event_dict['type'] == "checkout.session.completed":
        session = event['data']['object']

        print('SUCCESS!')

        # if store_donation(session) == 0:
        #     print('DB Success')
        # else:
        #     print('DB Failure')

    return "OK", 200

# def store_donation(session):
#     cur = None
#
#     try:
#         cur = db.connection.cursor()
#
#         payment_intent = Stripe.PaymentIntent.retrieve(session.payment_intent,)
#
#         if payment_intent.status == "succeeded":
#             tid = payment_intent.id
#             name = payment_intent.charges.data[0].billing_details.name
#             email = payment_intent.charges.data[0].billing_details.email
#             last_four = payment_intent.charges.data[0].payment_method_details.card.last4
#
#             timestamp = payment_intent.charges.data[0].created
#             date_of_purchase = datetime.fromtimestamp(
#                 int(timestamp)).strftime('%Y-%m-%d')
#
#             cur.execute('''INSERT INTO donation_transactions(full_name, email_address, tid, transaction_date, card_used)
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


@app.route("/success", methods=['GET'])
def success():
    return 'Purchase successful. Thank you!'


@app.route("/cancel", methods=['GET'])
def cancel():
    return 'Purchase cancelled.'
